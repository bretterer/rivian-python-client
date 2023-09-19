import platform
import asyncio
import secrets
import logging

from bleak import BleakClient, BLEDevice
from rivian import utils

_LOGGER = logging.getLogger(__name__)

PHONE_ID_VEHICLE_ID_UUID = "AA49565A-4D4F-424B-4559-5F5752495445"
PNONCE_VNONCE_UUID = "E020A15D-E730-4B2C-908B-51DAF9D41E19"
BLE_ACTIVE_ENTRY_UUID = "5249565F-4D4F-424B-4559-5F5752495445"

async def pair_phone(
    device: BLEDevice, vehicle_id, phone_id, vehicle_key, private_key
) -> bool:
    success = True

    # Create an asyncio.Event object to signal the arrival of a new notification.
    notification_event = asyncio.Event()
    notification_data = None

    # Callback for notifications from vehicle characteristics 
    def notification_handler(_, data: bytearray):
        nonlocal notification_data
        notification_data = data
        notification_event.set()

    try:
        async with BleakClient(device, timeout=10) as client:
            _LOGGER.debug(f"Connecting to {BLEDevice.name} [{BLEDevice.address}]")
            await client.start_notify(PHONE_ID_VEHICLE_ID_UUID, notification_handler)
            await client.start_notify(PNONCE_VNONCE_UUID, notification_handler)
            # wait to enable notifications for BLE_ACTIVE_ENTRY_UUID

            # write the phone ID (16-bytes) response will be vehicle ID
            await client.write_gatt_char(PHONE_ID_VEHICLE_ID_UUID, bytes.fromhex(phone_id.replace("-", "")))
            await notification_event.wait()
            notification_event.clear()

            vas_vehicle_id = notification_data.hex()
            if vas_vehicle_id != vehicle_id:
                _LOGGER.debug(
                    "Incorrect vas vehicle id: received %s, expected %s",
                    vas_vehicle_id,
                    vehicle_id)
                return False

            # generate pnonce (16-bytes random)
            pnonce = secrets.token_bytes(16)  
            hmac = utils.generate_ble_command_hmac(pnonce, vehicle_key, private_key)
    
            # write pnonce (48-bytes) response will be vnonce
            await client.write_gatt_char(PNONCE_VNONCE_UUID,  pnonce + hmac )
            await notification_event.wait()

            # vehicle is authenticated, trigger bonding 
            if platform.system() == "Darwin":
                # Mac BLE API doesn't have an explicit way to trigger bonding
                # enable notification on BLE_ACTIVE_ENTRY_UUID to trigger bonding
                await client.start_notify(BLE_ACTIVE_ENTRY_UUID, notification_handler)
            else:
                await client.pair()
    except:
        success = False

    return success
