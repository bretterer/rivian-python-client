import platform
import asyncio
import secrets
from asyncio import TimeoutError
from bleak import BleakScanner, BleakClient, BleakError
from rivian import utils

RIVIAN_PHONE_ID_VEHICLE_ID_UUID = "AA49565A-4D4F-424B-4559-5F5752495445"
RIVIAN_PNONCE_VNONCE_UUID = "E020A15D-E730-4B2C-908B-51DAF9D41E19"
RIVIAN_BLE_ACTIVE_ENTRY_UUID = "5249565F-4D4F-424B-4559-5F5752495445"
RIVIAN_PHONE_KEY_LOCAL_NAME = "Rivian Phone Key"

# Create an asyncio.Event object to signal the arrival of a new notification.
notification_event = asyncio.Event()
notification_data = None

def notification_handler(sender, data):
    global notification_data
    notification_data = data
    notification_event.set()
    
async def scan_for_device(target_device_name): 
    while True:
        # Sleep before the next scan
        await asyncio.sleep(1)  

        devices = await BleakScanner.discover()
        for device in devices:
            if device.name is not None and target_device_name in device.name:
                print(f"Found Device: {device.name}, Address: {device.address}")
                return device.address

async def connect_to_device(address):
    global client
    print(f"Connecting to {address}")

    try:
        client = BleakClient(address, timeout=10.0)
        await client.connect()
        print(f"Connected: {client.is_connected}")

        return client.is_connected 
    except (BleakError, TimeoutError, OSError):
        print(f"Failed to connect to {address}. Retrying...")
        return False 

async def pair_phone(vehicle_id, phone_id, vehicle_key, private_key):
    while True:
        address = await scan_for_device(RIVIAN_PHONE_KEY_LOCAL_NAME)
        success = await connect_to_device(address)

        if success:
            await client.start_notify(RIVIAN_PHONE_ID_VEHICLE_ID_UUID, notification_handler)
            await client.start_notify(RIVIAN_PNONCE_VNONCE_UUID, notification_handler)
            # wait to enable notifications for RIVIAN_BLE_ACTIVE_ENTRY_UUID

            # write the phone ID (16-bytes) response will be vehicle ID
            await client.write_gatt_char(RIVIAN_PHONE_ID_VEHICLE_ID_UUID, bytes.fromhex(phone_id.replace("-", "")))
            await notification_event.wait()
            notification_event.clear()

            # todo check vehicle id

            # generate pnonce (16-bytes random)
            pnonce = secrets.token_bytes(16)  
            hmac = utils.generate_ble_command_hmac(pnonce, vehicle_key, private_key)
    
            # write pnonce (48-bytes) response will be vnonce
            await client.write_gatt_char(RIVIAN_PNONCE_VNONCE_UUID,  pnonce + hmac )
            await notification_event.wait()

            # vehicle is authenticated, trigger bonding 
            if platform.system() == "Darwin":
                # Mac BLE API doesn't have an explicit way to trigger bonding
                # enable notification on RIVIAN_BLE_ACTIVE_ENTRY_UUID to trigger bonding
                await client.start_notify(RIVIAN_BLE_ACTIVE_ENTRY_UUID, notification_handler)
            else:
                await client.pair()

        if success:
            # todo check other steps above
            print("Successfully connected and paired")
            break
        else:
            print("Retrying...")
