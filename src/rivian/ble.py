"""Rivian BLE handler."""

from __future__ import annotations

import asyncio
import logging
import platform
import secrets

from .utils import generate_ble_command_hmac

_LOGGER = logging.getLogger(__name__)

try:
    from bleak import BleakClient, BleakScanner, BLEDevice  # type: ignore
except ImportError:
    _LOGGER.error("Please install 'rivian-python-client[ble]' to use BLE features.")
    raise


DEVICE_LOCAL_NAME = "Rivian Phone Key"

ACTIVE_ENTRY_CHARACTERISTIC_UUID = "5249565F-4D4F-424B-4559-5F5752495445"
PHONE_ID_VEHICLE_ID_UUID = "AA49565A-4D4F-424B-4559-5F5752495445"
PHONE_NONCE_VEHICLE_NONCE_UUID = "E020A15D-E730-4B2C-908B-51DAF9D41E19"

CONNECT_TIMEOUT = 10.0
NOTIFICATION_TIMEOUT = 3.0


class BleNotificationResponse:
    """BLE notification response helper."""

    def __init__(self) -> None:
        """Initialize the BLE notification response helper."""
        self.data: bytes | None = None
        self.event = asyncio.Event()

    def notification_handler(self, _, notification_data: bytearray) -> None:
        """Notification handler."""
        self.data = notification_data
        self.event.set()

    async def wait(self, timeout: float | None = NOTIFICATION_TIMEOUT) -> bool:
        """Wait for the notification response."""
        return await asyncio.wait_for(self.event.wait(), timeout)


async def create_notification_handler(
    client: BleakClient, char_specifier: str
) -> BleNotificationResponse:
    """Create a notification handler."""
    response = BleNotificationResponse()
    await client.start_notify(char_specifier, response.notification_handler)
    return response


async def pair_phone(
    device: BLEDevice,
    phone_id: str,
    vas_vehicle_id: str,
    vehicle_key: str,
    private_key: str,
) -> bool:
    """Pair a phone locally via BLE.

    The phone must first be enrolled via `rivian.enroll_phone`.
    This finishes the process to enable cloud and local vehicle control.
    """
    _LOGGER.debug("Connecting to %s", device)
    try:
        async with BleakClient(device, timeout=CONNECT_TIMEOUT) as client:
            _LOGGER.debug("Connected to %s", device)
            vehicle_id_handler = await create_notification_handler(
                client, PHONE_ID_VEHICLE_ID_UUID
            )
            nonce_handler = await create_notification_handler(
                client, PHONE_NONCE_VEHICLE_NONCE_UUID
            )

            _LOGGER.debug("Validating id")
            await client.write_gatt_char(
                PHONE_ID_VEHICLE_ID_UUID, bytes.fromhex(phone_id.replace("-", ""))
            )
            await vehicle_id_handler.wait()

            assert vehicle_id_handler.data
            vehicle_id_response = vehicle_id_handler.data.hex()
            if vehicle_id_response != vas_vehicle_id.replace("-", ""):
                _LOGGER.debug(
                    "Incorrect vehicle id: received %s, expected %s",
                    vehicle_id_response,
                    vas_vehicle_id,
                )
                return False

            _LOGGER.debug("Exchanging nonce")
            phone_nonce = secrets.token_bytes(16)
            hmac = generate_ble_command_hmac(phone_nonce, vehicle_key, private_key)
            await client.write_gatt_char(
                PHONE_NONCE_VEHICLE_NONCE_UUID, phone_nonce + hmac
            )
            await nonce_handler.wait()

            # Vehicle is authenticated, trigger bonding
            _LOGGER.debug("Attempting to pair")
            if platform.system() == "Darwin":
                # Mac BLE API doesn't have an explicit way to trigger bonding
                # Instead, enable notification on protected characteristic to trigger bonding manually
                await client.start_notify(
                    ACTIVE_ENTRY_CHARACTERISTIC_UUID, lambda _, __: None
                )
            else:
                await client.pair()

            _LOGGER.debug("Successfully paired with %s", device)
            return True
    except Exception as ex:  # pylint: disable=broad-except
        _LOGGER.debug(
            "Couldn't connect to %s. "
            'Make sure you are in the correct vehicle and have selected "Set Up" for the appropriate key and try again'
            "%s",
            device,
            ("" if isinstance(ex, asyncio.TimeoutError) else f": {ex}"),
        )
    return False


async def find_phone_key() -> BLEDevice | None:
    """Find phone key."""
    async with BleakScanner() as scanner:
        return await scanner.find_device_by_name(DEVICE_LOCAL_NAME)


async def set_bluez_pairable(device: BLEDevice) -> bool:
    """Set bluez to pairable on Linux systems."""
    if (_os := platform.system()) != "Linux":
        raise OSError(f"BlueZ is not available on {_os}-based systems")

    # pylint: disable=import-error, import-outside-toplevel
    from dbus_fast import BusType  # type: ignore
    from dbus_fast.aio import MessageBus  # type: ignore

    try:
        path = device.details["props"]["Adapter"]
    except Exception:  # pylint: disable=broad-except
        path = "/org/bluez/hci0"
        _LOGGER.warning(
            "Couldn't determine BT controller path, defaulting to %s: %s",
            path,
            device.details,
            exc_info=True,
        )

    try:
        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
        introspection = await bus.introspect("org.bluez", path)
        pobject = bus.get_proxy_object("org.bluez", path, introspection)
        iface = pobject.get_interface("org.bluez.Adapter1")
        if not await iface.get_pairable():
            await iface.set_pairable(True)
        bus.disconnect()
    except Exception as ex:  # pylint: disable=broad-except
        _LOGGER.error(ex)
        return False

    return True
