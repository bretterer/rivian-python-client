"""Asynchronous Python client for the Rivian API."""

from __future__ import annotations

import asyncio
import logging
import socket
import sys
import time
import uuid
from collections.abc import Callable
from typing import Any, Type
from warnings import warn

import aiohttp
from aiohttp import ClientResponse, ClientWebSocketResponse

from .const import LIVE_SESSION_PROPERTIES, VEHICLE_STATE_PROPERTIES, VehicleCommand
from .exceptions import (
    RivianApiException,
    RivianApiRateLimitError,
    RivianBadRequestError,
    RivianDataError,
    RivianInvalidCredentials,
    RivianInvalidOTP,
    RivianPhoneLimitReachedError,
    RivianTemporarilyLockedError,
    RivianUnauthenticated,
)
from .utils import generate_vehicle_command_hmac
from .ws_monitor import WebSocketMonitor

if sys.version_info >= (3, 11):
    import asyncio as async_timeout
else:
    import async_timeout

_LOGGER = logging.getLogger(__name__)

GRAPHQL_BASEPATH = "https://rivian.com/api/gql"
GRAPHQL_GATEWAY = GRAPHQL_BASEPATH + "/gateway/graphql"
GRAPHQL_CHARGING = GRAPHQL_BASEPATH + "/chrg/user/graphql"
GRAPHQL_WEBSOCKET = "wss://api.rivian.com/gql-consumer-subscriptions/graphql"

APOLLO_CLIENT_NAME = "com.rivian.ios.consumer-apollo-ios"

BASE_HEADERS = {
    "User-Agent": "RivianApp/707 CFNetwork/1237 Darwin/20.4.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Apollographql-Client-Name": APOLLO_CLIENT_NAME,
}

CLOUD_CONNECTION_TEMPLATE = "{ lastSync }"
LOCATION_TEMPLATE = "{ latitude longitude timeStamp }"
VALUE_TEMPLATE = "{ timeStamp value }"
TEMPLATE_MAP = {
    "cloudConnection": CLOUD_CONNECTION_TEMPLATE,
    "gnssLocation": LOCATION_TEMPLATE,
}

LIVE_SESSION_VALUE_RECORD_KEYS = {
    "current",
    "currentMiles",
    "kilometersChargedPerHour",
    "power",
    "rangeAddedThisSession",
    "soc",
    "timeRemaining",
    "totalChargedEnergy",
    "vehicleChargerState",
}
VALUE_RECORD_TEMPLATE = "{ __typename value updatedAt }"

ERROR_CODE_CLASS_MAP: dict[str, Type[RivianApiException]] = {
    "BAD_CURRENT_PASSWORD": RivianInvalidCredentials,
    "BAD_REQUEST_ERROR": RivianBadRequestError,
    "DATA_ERROR": RivianDataError,
    "INTERNAL_SERVER_ERROR": RivianApiException,
    "RATE_LIMIT": RivianApiRateLimitError,
    "SESSION_MANAGER_ERROR": RivianTemporarilyLockedError,
    "UNAUTHENTICATED": RivianUnauthenticated,
}


def send_deprecation_warning(old_name: str, new_name: str) -> None:  # pragma: no cover
    """Send a deprecation warning."""
    message = f"{old_name} has been deprecated in favor of {new_name}, the alias will be removed in the future"
    warn(
        message,
        DeprecationWarning,
        stacklevel=2,
    )
    _LOGGER.warning(message)


class Rivian:
    """Main class for the Rivian API Client"""

    def __init__(
        self,
        request_timeout: int = 10,
        session: aiohttp.client.ClientSession | None = None,
        *,
        access_token: str = "",
        refresh_token: str = "",
        csrf_token: str = "",
        app_session_token: str = "",
        user_session_token: str = "",
    ) -> None:
        self._session = session
        self._close_session = False

        self._access_token = access_token
        self._refresh_token = refresh_token
        self._csrf_token = csrf_token
        self._app_session_token = app_session_token
        self._user_session_token = user_session_token

        self.request_timeout = request_timeout

        self._otp_needed = False
        self._otp_token = ""

        self._ws_monitor: WebSocketMonitor | None = None
        self._subscriptions: dict[str, str] = {}

    async def create_csrf_token(self) -> None:
        """Create cross-site-request-forgery (csrf) token."""
        url = GRAPHQL_GATEWAY

        headers = {**BASE_HEADERS}

        graphql_json = {
            "operationName": "CreateCSRFToken",
            "query": "mutation CreateCSRFToken {\n  createCsrfToken {\n    __typename\n    csrfToken\n    appSessionToken\n  }\n}",
            "variables": None,
        }

        response = await self.__graphql_query(headers, url, graphql_json)

        response_json = await response.json()

        csrf_data = response_json["data"]["createCsrfToken"]
        self._csrf_token = csrf_data["csrfToken"]
        self._app_session_token = csrf_data["appSessionToken"]

    async def authenticate(self, username: str, password: str) -> None:
        """Authenticate against the Rivian GraphQL API with Username and Password"""
        url = GRAPHQL_GATEWAY

        headers = BASE_HEADERS | {
            "Csrf-Token": self._csrf_token,
            "A-Sess": self._app_session_token,
            "Apollographql-Client-Name": APOLLO_CLIENT_NAME,
        }

        graphql_json = {
            "operationName": "Login",
            "query": "mutation Login($email: String!, $password: String!) {\n  login(email: $email, password: $password) {\n    __typename\n    ... on MobileLoginResponse {\n      __typename\n      accessToken\n      refreshToken\n      userSessionToken\n    }\n    ... on MobileMFALoginResponse {\n      __typename\n      otpToken\n    }\n  }\n}",
            "variables": {"email": username, "password": password},
        }

        response = await self.__graphql_query(headers, url, graphql_json)

        response_json = await response.json()

        login_data = response_json["data"]["login"]

        if "otpToken" in login_data:
            self._otp_needed = True
            self._otp_token = login_data["otpToken"]
        else:
            self._access_token = login_data["accessToken"]
            self._refresh_token = login_data["refreshToken"]
            self._user_session_token = login_data["userSessionToken"]

    async def authenticate_graphql(
        self, username: str, password: str
    ) -> None:  # pragma: no cover
        """### DEPRECATED (use `authenticate` instead)

        Authenticate against the Rivian GraphQL API with Username and Password.
        """
        send_deprecation_warning("authenticate_graphql", "authenticate")
        return await self.authenticate(username=username, password=password)

    async def validate_otp(self, username: str, otp_code: str) -> None:
        """Validates OTP against the Rivian GraphQL API with Username, OTP Code, and OTP Token"""
        url = GRAPHQL_GATEWAY

        headers = BASE_HEADERS | {
            "Csrf-Token": self._csrf_token,
            "A-Sess": self._app_session_token,
            "Apollographql-Client-Name": APOLLO_CLIENT_NAME,
        }

        graphql_json = {
            "operationName": "LoginWithOTP",
            "query": "mutation LoginWithOTP($email: String!, $otpCode: String!, $otpToken: String!) {\n  loginWithOTP(email: $email, otpCode: $otpCode, otpToken: $otpToken) {\n    __typename\n    ... on MobileLoginResponse {\n      __typename\n      accessToken\n      refreshToken\n      userSessionToken\n    }\n  }\n}",
            "variables": {
                "email": username,
                "otpCode": otp_code,
                "otpToken": self._otp_token,
            },
        }

        response = await self.__graphql_query(headers, url, graphql_json)

        response_json = await response.json()

        login_data = response_json["data"]["loginWithOTP"]

        self._access_token = login_data["accessToken"]
        self._refresh_token = login_data["refreshToken"]
        self._user_session_token = login_data["userSessionToken"]

    async def validate_otp_graphql(
        self, username: str, otpCode: str
    ) -> None:  # pragma: no cover
        """### DEPRECATED (use `validate_otp` instead)

        Validates OTP against the Rivian GraphQL API with Username, OTP Code, and OTP Token.
        """
        send_deprecation_warning("validate_otp_graphql", "validate_otp")
        return await self.validate_otp(username=username, otp_code=otpCode)

    async def disenroll_phone(self, identity_id: str) -> bool:
        """Disenroll a phone."""
        url = GRAPHQL_GATEWAY
        headers = BASE_HEADERS | {
            "Csrf-Token": self._csrf_token,
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }
        graphql_json = {
            "operationName": "DisenrollPhone",
            "variables": {"attrs": {"enrollmentId": identity_id}},
            "query": "mutation DisenrollPhone($attrs: DisenrollPhoneAttributes!) { disenrollPhone(attrs: $attrs) { __typename success } }",
        }

        response = await self.__graphql_query(headers, url, graphql_json)
        if response.status == 200:
            data = await response.json()
            return data.get("data", {}).get("disenrollPhone", {}).get("success")
        return False

    async def enroll_phone(
        self,
        user_id: str,
        vehicle_id: str,
        device_type: str,
        device_name: str,
        public_key: str,
    ) -> bool:
        """Enroll a phone.

        To generate a public/private key for enrollment, use the `utils.generate_key_pair` function.
        The private key will need to be retained to sign commands sent via the `send_vehicle_command` method.
        To enable vehicle control, the phone will then also need to be paired locally via BLE,
        which can be done via `ble.pair_phone`.
        """
        url = GRAPHQL_GATEWAY
        headers = BASE_HEADERS | {
            "Csrf-Token": self._csrf_token,
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }
        graphql_json = {
            "operationName": "EnrollPhone",
            "variables": {
                "attrs": {
                    "userId": user_id,
                    "vehicleId": vehicle_id,
                    "publicKey": public_key,
                    "type": device_type,
                    "name": device_name,
                }
            },
            "query": "mutation EnrollPhone($attrs: EnrollPhoneAttributes!) { enrollPhone(attrs: $attrs) { __typename success } }",
        }
        response = await self.__graphql_query(headers, url, graphql_json)
        if response.status == 200:
            data = await response.json()
            if data.get("data", {}).get("enrollPhone", {}).get("success"):
                return True
        return False

    async def get_drivers_and_keys(self, vehicle_id: str) -> ClientResponse:
        """Get drivers and keys."""
        url = GRAPHQL_GATEWAY
        headers = BASE_HEADERS | {
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }

        graphql_json = {
            "operationName": "DriversAndKeys",
            "query": "query DriversAndKeys($vehicleId:String){getVehicle(id:$vehicleId){__typename id vin invitedUsers{__typename...on ProvisionedUser{firstName lastName email roles userId devices{type mappedIdentityId id hrid deviceName isPaired isEnabled}}...on UnprovisionedUser{email inviteId status}}}}",
            "variables": {"vehicleId": vehicle_id},
        }

        return await self.__graphql_query(headers, url, graphql_json)

    async def get_user_information(
        self, include_phones: bool = False
    ) -> ClientResponse:
        """Get user information."""
        url = GRAPHQL_GATEWAY

        headers = BASE_HEADERS | {
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }

        vehicles_fragment = "vehicles { id vin name vas { __typename vasVehicleId vehiclePublicKey } roles state createdAt updatedAt vehicle { __typename id vin modelYear make model expectedBuildDate plannedBuildDate expectedGeneralAssemblyStartDate actualGeneralAssemblyDate vehicleState { supportedFeatures { __typename name status } } } }"
        phones_fragment = "enrolledPhones { __typename vas { __typename vasPhoneId publicKey } enrolled { __typename deviceType deviceName vehicleId identityId shortName } }"
        _2fa_fragment = "registrationChannels { type }"

        graphql_json = {
            "operationName": "getUserInfo",
            "query": f"query getUserInfo {{ currentUser {{ __typename id {vehicles_fragment} {_2fa_fragment} {phones_fragment if include_phones else ''} }} }}",
            "variables": None,
        }

        return await self.__graphql_query(headers, url, graphql_json)

    async def get_registered_wallboxes(self) -> ClientResponse:
        """Get registered wallboxes."""
        url = GRAPHQL_CHARGING

        headers = BASE_HEADERS | {
            "Csrf-Token": self._csrf_token,
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }

        graphql_json = {
            "operationName": "getRegisteredWallboxes",
            "query": "query getRegisteredWallboxes {\n  getRegisteredWallboxes {\n    __typename\n    wallboxId\n    userId\n    wifiId\n    name\n    linked\n    latitude\n    longitude\n    chargingStatus\n    power\n    currentVoltage\n    currentAmps\n    softwareVersion\n    model\n    serialNumber\n    maxAmps\n    maxVoltage\n    maxPower\n  }\n}",
            "variables": None,
        }

        return await self.__graphql_query(headers, url, graphql_json)

    async def get_vehicle_command_state(self, command_id: str) -> ClientResponse:
        """Get vehicle command state."""
        url = GRAPHQL_GATEWAY

        headers = BASE_HEADERS | {
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }

        graphql_query = "query getVehicleCommand($id: String!) { getVehicleCommand(id: $id) { __typename id command createdAt state responseCode statusCode } }"

        graphql_json = {
            "operationName": "getVehicleCommand",
            "query": graphql_query,
            "variables": {"id": command_id},
        }

        return await self.__graphql_query(headers, url, graphql_json)

    async def get_vehicle_images(
        self,
        *,
        extension: str | None = None,
        resolution: str | None = None,
        vehicle_version: str | None = None,
        preorder_version: str | None = None,
    ) -> ClientResponse:
        """Get vehicle images.

        Known parameter values:
          - extension: `png`, `webp`
          - resolution: `@1x`, `@2x`, `@3x` (for png); `hdpi`, `xhdpi`, `xxhdpi`, `xxxhdpi` (for webp)
          - vehicle_version/preorder_version: `1`, `2` (all other values return v1 images)
        """
        url = GRAPHQL_GATEWAY

        headers = BASE_HEADERS | {
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }

        graphql_query = "query getVehicleImages( $extension: String $resolution: String $versionForVehicle: String $versionForPreOrder: String ) { getVehicleOrderMobileImages( resolution: $resolution extension: $extension version: $versionForPreOrder ) { ...image } getVehicleMobileImages( resolution: $resolution extension: $extension version: $versionForVehicle ) { ...image } } fragment image on VehicleMobileImage { orderId vehicleId url extension resolution size design placement overlays { url overlay zIndex } }"

        graphql_json = {
            "operationName": "getVehicleImages",
            "query": graphql_query,
            "variables": {
                "extension": extension,
                "resolution": resolution,
                "versionForVehicle": vehicle_version,
                "versionForPreOrder": preorder_version,
            },
        }

        return await self.__graphql_query(headers, url, graphql_json)

    async def get_vehicle_state(
        self, vin: str, properties: set[str] | None = None
    ) -> ClientResponse:
        """Get vehicle state."""
        if not properties:
            properties = VEHICLE_STATE_PROPERTIES

        url = GRAPHQL_GATEWAY

        headers = BASE_HEADERS | {
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }

        graphql_query = "query GetVehicleState($vehicleID: String!) {\n  vehicleState(id: $vehicleID) "
        graphql_query += self._build_vehicle_state_fragment(properties)
        graphql_query += "}"

        graphql_json = {
            "operationName": "GetVehicleState",
            "query": graphql_query,
            "variables": {"vehicleID": vin},
        }

        return await self.__graphql_query(headers, url, graphql_json)

    async def get_vehicle_ota_update_details(self, vehicle_id: str) -> ClientResponse:
        """Get vehicle OTA update details."""
        url = GRAPHQL_GATEWAY
        headers = BASE_HEADERS | {
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }

        graphql_query = "query getOTAUpdateDetails($vehicleId:String!){getVehicle(id:$vehicleId){availableOTAUpdateDetails{url version locale}currentOTAUpdateDetails{url version locale}}}"

        graphql_json = {
            "operationName": "getOTAUpdateDetails",
            "query": graphql_query,
            "variables": {"vehicleId": vehicle_id},
        }

        return await self.__graphql_query(headers, url, graphql_json)

    async def get_live_charging_session(
        self, vin: str, properties: set[str] | None = None
    ) -> ClientResponse:
        """Get live charging session data."""
        if not properties:
            properties = LIVE_SESSION_PROPERTIES

        url = GRAPHQL_CHARGING
        headers = BASE_HEADERS | {"U-Sess": self._user_session_token}

        fragment = " ".join(
            f"{p} {VALUE_RECORD_TEMPLATE if p in LIVE_SESSION_VALUE_RECORD_KEYS else ''}"
            for p in properties
        )
        graphql_query = f"""
            query getLiveSessionData($vehicleId: ID!) {{
                getLiveSessionData(vehicleId: $vehicleId) {{
                    __typename
                    {fragment}
                }}
            }}"""

        graphql_json = {
            "operationName": "getLiveSessionData",
            "query": graphql_query,
            "variables": {"vehicleId": vin},
        }

        return await self.__graphql_query(headers, url, graphql_json)

    def _validate_vehicle_command(
        self, command: VehicleCommand | str, params: dict[str, Any] | None = None
    ) -> None:
        """Validate certian vehicle command/param combos."""
        if command == VehicleCommand.CHARGING_LIMITS:
            if not (
                params
                and isinstance((limit := params.get("SOC_limit")), int)
                and 50 <= limit <= 100
            ):
                raise RivianBadRequestError(
                    "Charging limit must include parameter `SOC_limit` with a valid value between 50 and 100"
                )
        if command in (
            VehicleCommand.CABIN_HVAC_DEFROST_DEFOG,
            VehicleCommand.CABIN_HVAC_LEFT_SEAT_HEAT,
            VehicleCommand.CABIN_HVAC_LEFT_SEAT_VENT,
            VehicleCommand.CABIN_HVAC_REAR_LEFT_SEAT_HEAT,
            VehicleCommand.CABIN_HVAC_REAR_RIGHT_SEAT_HEAT,
            VehicleCommand.CABIN_HVAC_RIGHT_SEAT_HEAT,
            VehicleCommand.CABIN_HVAC_RIGHT_SEAT_VENT,
            VehicleCommand.CABIN_HVAC_STEERING_HEAT,
        ):
            if not (
                params
                and isinstance((level := params.get("level")), int)
                and 0 <= level <= 4
            ):
                raise RivianBadRequestError(
                    "HVAC setting must include parameter `level` with a valid value between 0 and 4"
                )
        if command == VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP:
            if not (
                params
                and isinstance((temp := params.get("HVAC_set_temp")), (float, int))
                and (16 <= temp <= 29 or temp in (0, 63.5))
            ):
                raise RivianBadRequestError(
                    "HVAC setting must include parameter `HVAC_set_temp` with a valid value between 16 and 29 or 0/63.5 for LO/HI, respectively"
                )
            params["HVAC_set_temp"] = str(params["HVAC_set_temp"])

    async def send_vehicle_command(
        self,
        command: VehicleCommand | str,
        vehicle_id: str,
        phone_id: str,
        identity_id: str,
        vehicle_key: str,
        private_key: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> str | None:
        """Send a command to the vehicle.

        To generate a public/private key for commands, use the `utils.generate_key_pair` function.
        The public key will first need to be enrolled via the `enroll_phone` method, otherwise commands will fail.

        Certain commands may require additional details via the `params` mapping.
        Some known examples include:
          - `CABIN_HVAC_*`: params = {"level": 0..4} where 0 is off, 1 is on, 2 is low/level_1, 3 is medium/level_2 and 4 is high/level_3
          - `CABIN_PRECONDITIONING_SET_TEMP`: params = {"HVAC_set_temp": "deg_C"} where `deg_C` is a string value between 16 and 29 or 0/63.5 for LO/HI, respectively
          - `CHARGING_LIMITS`: params = {"SOC_limit": 50..100}
        """
        self._validate_vehicle_command(command, params)

        command = str(command)
        timestamp = str(int(time.time()))
        hmac = generate_vehicle_command_hmac(
            command, timestamp, vehicle_key, private_key
        )

        url = GRAPHQL_GATEWAY
        headers = BASE_HEADERS | {
            "Csrf-Token": self._csrf_token,
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }
        graphql_json = {
            "operationName": "sendVehicleCommand",
            "variables": {
                "attrs": {
                    "command": command,
                    "hmac": hmac,
                    "timestamp": str(timestamp),
                    "vasPhoneId": phone_id,
                    "deviceId": identity_id,
                    "vehicleId": vehicle_id,
                }
                | ({"params": params} if params else {})
            },
            "query": "mutation sendVehicleCommand($attrs: VehicleCommandAttributes!) { sendVehicleCommand(attrs: $attrs) { __typename id command state } }",
        }

        response = await self.__graphql_query(headers, url, graphql_json)
        if response.status == 200:
            data = await response.json()
            if status := data.get("data", {}).get("sendVehicleCommand", {}):
                return status.get("id")
        return None

    async def subscribe_for_vehicle_updates(
        self,
        vehicle_id: str,
        callback: Callable[[dict[str, Any]], None],
        properties: set[str] | None = None,
    ) -> Callable | None:
        """Open a web socket connection to receive updates."""
        if not properties:
            properties = VEHICLE_STATE_PROPERTIES

        try:
            await self._ws_connect()
            assert self._ws_monitor
            async with async_timeout.timeout(self.request_timeout):
                await self._ws_monitor.connection_ack.wait()
            payload = {
                "operationName": "VehicleState",
                "query": f"subscription VehicleState($vehicleID: String!) {{ vehicleState(id: $vehicleID) {self._build_vehicle_state_fragment(properties)} }}",
                "variables": {"vehicleID": vehicle_id},
            }
            unsubscribe = await self._ws_monitor.start_subscription(payload, callback)
            _LOGGER.debug("%s subscribed to updates", vehicle_id)
            return unsubscribe
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.error(ex)
            return None

    async def _ws_connect(self) -> ClientWebSocketResponse:
        """Initiate a websocket connection."""

        async def connection_init(websocket: ClientWebSocketResponse) -> None:
            await websocket.send_json(
                {
                    "payload": {
                        "client-name": APOLLO_CLIENT_NAME,
                        "client-version": "1.13.0-1494",
                        "dc-cid": f"m-ios-{uuid.uuid4()}",
                        "u-sess": self._user_session_token,
                    },
                    "type": "connection_init",
                }
            )

        if not self._ws_monitor:
            self._ws_monitor = WebSocketMonitor(
                self, GRAPHQL_WEBSOCKET, connection_init
            )
        ws_monitor = self._ws_monitor
        if ws_monitor.websocket is None or ws_monitor.websocket.closed:
            await ws_monitor.new_connection(True)
            assert ws_monitor.websocket
        if ws_monitor.monitor is None or ws_monitor.monitor.done():
            await ws_monitor.start_monitor()
        return ws_monitor.websocket

    async def __graphql_query(
        self, headers: dict[str, str], url: str, body: dict[str, Any]
    ) -> ClientResponse:
        """Execute and return arbitrary graphql query."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        if "dc-cid" not in headers:
            headers["dc-cid"] = f"m-ios-{uuid.uuid4()}"

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    "POST",
                    url,
                    json=body,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            raise RivianApiException(
                "Timeout occurred while connecting to Rivian API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise RivianApiException(
                "Error occurred while communicating with Rivian."
            ) from exception

        try:
            response_json = await response.json()
            if errors := response_json.get("errors"):
                for error in errors:
                    if extensions := error.get("extensions"):
                        code = extensions["code"]
                        if (code, extensions.get("reason")) in (
                            ("BAD_USER_INPUT", "INVALID_OTP"),
                            ("UNAUTHENTICATED", "OTP_TOKEN_EXPIRED"),
                        ):
                            raise RivianInvalidOTP(
                                response.status, response_json, headers, body
                            )
                        if (code, extensions.get("reason")) == (
                            "CONFLICT",
                            "ENROLL_PHONE_LIMIT_REACHED",
                        ):
                            raise RivianPhoneLimitReachedError(
                                response.status, response_json, headers, body
                            )
                        if err_cls := ERROR_CODE_CLASS_MAP.get(code):
                            raise err_cls(response.status, response_json, headers, body)
                raise RivianApiException(
                    "Error occurred while reading the graphql response from Rivian.",
                    response.status,
                    response_json,
                    headers,
                    body,
                )
        except Exception as exception:
            raise exception

        return response

    async def close(self) -> None:
        """Close open client session."""
        if self._ws_monitor:
            await self._ws_monitor.close()
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> Rivian:
        """Async enter.
        Returns:
            The Rivian object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.
        Args:
            _exc_info: Exec type.
        """
        await self.close()

    def _build_vehicle_state_fragment(self, properties: set[str]) -> str:
        """Build GraphQL vehicle state fragment from properties."""
        frag = " ".join(f"{p} {TEMPLATE_MAP.get(p,VALUE_TEMPLATE)}" for p in properties)
        return f"{{ {frag} }}"
