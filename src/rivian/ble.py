"""Rivian BLE handler."""
from __future__ import annotations
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

NOTIFICATION_TIMEOUT = 3.0
CONNECT_TIMEOUT = 10.0

async def pair_phone(
    device: BLEDevice, vehicle_id: str, phone_id: str, vehicle_key: str, private_key: str
) -> bool:
    success = False

    # Create an asyncio.Event object to signal the arrival of a new notification.
    vid_event = asyncio.Event()
    nonce_event = asyncio.Event()
    notification_data: bytearray | None = None

    # Callback for notifications from vehicle characteristics 
    def id_notification_handler(_, data: bytearray) -> None:
        nonlocal notification_data
        notification_data = data
        vid_event.set()

    def nonce_notification_handler(_, data: bytearray) -> None:
        nonlocal notification_data
        notification_data = data
        nonce_event.set()

    # this is a dummy callback (unused)
    def active_entry_notification_handler(_, data: bytearray) -> None:
        pass

    try:
        _LOGGER.debug(f"Connecting to {BLEDevice.name} [{BLEDevice.address}]")
        async with BleakClient(device, timeout=CONNECT_TIMEOUT) as client:
            _LOGGER.debug(f"Connected to {BLEDevice.name} [{BLEDevice.address}]")
            await client.start_notify(PHONE_ID_VEHICLE_ID_UUID, id_notification_handler)
            await client.start_notify(PNONCE_VNONCE_UUID, nonce_notification_handler)
            # wait to enable notifications for BLE_ACTIVE_ENTRY_UUID

            # write the phone ID (16-bytes) response will be vehicle ID
            await client.write_gatt_char(PHONE_ID_VEHICLE_ID_UUID, bytes.fromhex(phone_id.replace("-", "")))
            await asyncio.wait_for(vid_event.wait(), NOTIFICATION_TIMEOUT)

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
            await asyncio.wait_for(nonce_event.wait(), NOTIFICATION_TIMEOUT)

            # vehicle is authenticated, trigger bonding 
            if platform.system() == "Darwin":
                # Mac BLE API doesn't have an explicit way to trigger bonding
                # enable notification on BLE_ACTIVE_ENTRY_UUID to trigger bonding
                await client.start_notify(BLE_ACTIVE_ENTRY_UUID, active_entry_notification_handler)
            else:
                await client.pair()
            
            success = True

    except Exception as e:
        _LOGGER.debug(f"An exception occurred while pairing: {str(e)}")

    return success
