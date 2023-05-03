"""Asynchronous Python client for the Rivian API."""
from __future__ import annotations

import asyncio
import json
import logging
import socket
import uuid
from collections.abc import Callable
from typing import Any

import aiohttp
import async_timeout
from aiohttp import ClientRequest, ClientResponse, ClientWebSocketResponse

from .const import VEHICLE_STATE_PROPERTIES
from .exceptions import (
    RivianApiException,
    RivianApiRateLimitError,
    RivianDataError,
    RivianExpiredTokenError,
    RivianInvalidCredentials,
    RivianInvalidOTP,
    RivianTemporarilyLockedError,
    RivianUnauthenticated,
)
from .ws_monitor import WebSocketMonitor

_LOGGER = logging.getLogger(__name__)

CESIUM_BASEPATH = "https://cesium.rivianservices.com/v2"
AUTH_BASEPATH = "https://auth.rivianservices.com/auth/api/v1"
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

LOCATION_TEMPLATE = "{ latitude longitude timeStamp }"
VALUE_TEMPLATE = "{ timeStamp value }"
TEMPLATE_MAP = {"gnssLocation": LOCATION_TEMPLATE}


class Rivian:
    """Main class for the Rivian API Client"""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        request_timeout: int = 10,
        session: aiohttp.client.ClientSession | None = None,
    ) -> None:
        self._session = session
        self._close_session = False
        self._session_token = ""
        self._access_token = ""
        self._refresh_token = ""
        self._csrf_token = ""
        self._app_session_token = ""
        self._user_session_token = ""

        self.client_id = client_id
        self.client_secret = client_secret
        self.request_timeout = request_timeout

        self._otp_needed = False
        self._otp_token = ""

        self._ws_monitor: WebSocketMonitor | None = None
        self._subscriptions: dict[str, str] = {}

    async def authenticate(
        self,
        username: str,
        password: str,
    ) -> ClientResponse | dict[str, str]:
        """Authenticate against the Rivian API with Username and Password"""
        url = AUTH_BASEPATH + "/token/auth"

        headers = {**BASE_HEADERS}

        json_data = {
            "grant_type": "password",
            "username": username,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "pwd": password,
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    "POST",
                    url,
                    json=json_data,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            raise Exception(
                "Timeout occurred while connecting to Rivian API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise Exception(
                "Error occurred while communicating with Rivian."
            ) from exception

        content_type = response.headers.get("Content-Type", "")

        if response.status == 401:
            self._otp_needed = True
            response_json = await response.json()
            self._session_token = response_json["session_token"]
            return response

        if response.status // 100 in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise Exception(response.status, json.loads(contents.decode("utf8")))
            raise Exception(response.status, {"message": contents.decode("utf8")})

        if "application/json" in content_type:
            response_json = await response.json()
            self._access_token = response_json["access_token"]
            self._refresh_token = response_json["refresh_token"]
            return response

        text = await response.text()
        return {"message": text}

    async def validate_otp(
        self,
        username: str,
        otp: str,
    ) -> dict[str, Any]:
        """Validate the OTP"""
        url = AUTH_BASEPATH + "/token/auth"

        headers = BASE_HEADERS | {"Authorization": "Bearer " + self._session_token}

        json_data = {
            "grant_type": "password",
            "username": username,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "otp_token": otp,
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    "POST",
                    url,
                    json=json_data,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            raise Exception(
                "Timeout occurred while connecting to Rivian API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise Exception(
                "Error occurred while communicating with Rivian."
            ) from exception

        content_type = response.headers.get("Content-Type", "")

        if response.status // 100 in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise Exception(response.status, json.loads(contents.decode("utf8")))
            raise Exception(response.status, {"message": contents.decode("utf8")})

        if "application/json" in content_type:
            response_json = await response.json()
            self._access_token = response_json["access_token"]
            self._refresh_token = response_json["refresh_token"]
            return response

        text = await response.text()
        return {"message": text}

    async def refresh_access_token(
        self,
        refresh_token: str,
        client_id: str,
        client_secret: str,
    ) -> ClientRequest:
        """Validate the OTP"""
        url = AUTH_BASEPATH + "/token/refresh"

        headers = {**BASE_HEADERS}

        json_data = {
            "token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    "POST",
                    url,
                    json=json_data,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            raise Exception(
                "Timeout occurred while connecting to Rivian API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise Exception(
                "Error occurred while communicating with Rivian."
            ) from exception

        content_type = response.headers.get("Content-Type", "")

        if response.status // 100 in [4, 5]:
            contents = await response.read()
            response.close()

            if content_type == "application/json":
                raise Exception(
                    response.status, json.loads(contents.decode("utf8")), json_data
                )
            raise Exception(response.status, {"message": contents.decode("utf8")})

        if "application/json" in content_type:
            response_json = await response.json()
            self._access_token = response_json["access_token"]
            return response

        return response

    async def get_vehicle_info(
        self, vin: str, access_token: str, properties: dict[str]
    ) -> dict[str, Any]:
        """get the vehicle info"""
        url = CESIUM_BASEPATH + "/vehicle/latest"

        headers = BASE_HEADERS | {"Authorization": "Bearer " + access_token}

        json_data = {
            "car": vin,
            "properties": properties,
        }

        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self._session.request(
                    "POST",
                    url,
                    json=json_data,
                    headers=headers,
                )
        except asyncio.TimeoutError as exception:
            raise Exception(
                "Timeout occurred while connecting to Rivian API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise Exception(
                "Error occurred while communicating with Rivian."
            ) from exception

        if response.status // 100 in [4, 5]:
            contents = await response.read()
            response.close()

            response_json = await response.json()
            if response.status == 401 and response_json["error_code"] == -40:
                raise RivianExpiredTokenError(
                    response.status,
                    response_json,
                    headers,
                    json_data,
                )

            raise Exception(
                response.status,
                json.loads(contents.decode("utf8")),
                headers,
                json_data,
            )

        return response

    async def create_csrf_token(self) -> dict[str, Any]:
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

        return response

    async def authenticate_graphql(
        self,
        username: str,
        password: str,
    ) -> dict[str, Any]:
        """Authenticate against the Rivian GraphQL API with Username and Password"""
        url = GRAPHQL_GATEWAY

        headers = BASE_HEADERS | {
            "Csrf-Token": self._csrf_token,
            "A-Sess": self._app_session_token,
            "Apollographql-Client-Name": APOLLO_CLIENT_NAME,
            "Dc-Cid": f"m-ios-{uuid.uuid4()}",
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

        return response

    async def validate_otp_graphql(self, username: str, otpCode: str) -> dict[str, Any]:
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
                "otpCode": otpCode,
                "otpToken": self._otp_token,
            },
        }

        response = await self.__graphql_query(headers, url, graphql_json)

        response_json = await response.json()

        login_data = response_json["data"]["loginWithOTP"]

        self._access_token = login_data["accessToken"]
        self._refresh_token = login_data["refreshToken"]
        self._user_session_token = login_data["userSessionToken"]

        return response

    async def get_user_information(self) -> ClientResponse:
        """get user information (user.id, vehicle vins)"""
        url = GRAPHQL_GATEWAY

        headers = BASE_HEADERS | {
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token,
        }

        graphql_json = {
            "operationName": "getUserInfo",
            "query": "query getUserInfo {\n    currentUser {\n        __typename\n        id\n        vehicles {\n        id\n        vin\n        name\n        vas {\n            __typename\n            vasVehicleId\n            vehiclePublicKey\n        }\n        roles\n        state\n        createdAt\n        updatedAt\n        vehicle {\n            __typename\n            id\n            vin\n            modelYear\n            make\n            model\n            expectedBuildDate\n            plannedBuildDate\n            expectedGeneralAssemblyStartDate\n            actualGeneralAssemblyDate\n        }\n        }\n    }\n}",
            "variables": None,
        }

        return await self.__graphql_query(headers, url, graphql_json)

    async def get_registered_wallboxes(self) -> ClientResponse:
        """get wallboxes (graphql)"""
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

    async def get_vehicle_state(self, vin: str, properties: set[str]) -> ClientResponse:
        """get vehicle state (graphql)"""
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

    async def get_live_charging_session(
        self, user_id: str, vin: str, properties: dict[str]
    ) -> ClientResponse:
        """get live charging session data (graphql)"""
        url = GRAPHQL_CHARGING

        headers = BASE_HEADERS | {"U-Sess": self._user_session_token}

        graphql_query = "query getLiveSessionData($vehicleId: ID!) {\n  getLiveSessionData(vehicleId: $vehicleId) {\n    __typename\n   "
        detail_sensors = [
            "vehicleChargerState",
            "timeRemaining",
            "kilometersChargedPerHour",
            "power",
            "rangeAddedThisSession",
            "totalChargedEnergy",
        ]
        detail_sensor_template = (
            "{\n      __typename\n      value\n      updatedAt\n    }\n"
        )

        for key in properties:
            template = ""
            if key in detail_sensors:
                template = detail_sensor_template
            graphql_query += f"{key} {template}"
        graphql_query += "}"
        graphql_query += "}"

        graphql_json = {
            "operationName": "getLiveSessionData",
            "query": graphql_query,
            "variables": {"userId": user_id, "vehicleId": vin},
        }

        return await self.__graphql_query(headers, url, graphql_json)

    async def subscribe_for_vehicle_updates(
        self,
        vin: str,
        properties: set[str] | None = None,
        callback: Callable = None,
    ) -> Callable | None:
        """Open a web socket connection to receive updates."""
        if not properties:
            properties = VEHICLE_STATE_PROPERTIES

        try:
            await self._ws_connect()
            async with async_timeout.timeout(self.request_timeout):
                await self._ws_monitor.connection_ack.wait()
            payload = {
                "operationName": "VehicleState",
                "query": f"subscription VehicleState($vehicleID: String!) {{ vehicleState(id: $vehicleID) {self._build_vehicle_state_fragment(properties)} }}",
                "variables": {"vehicleID": vin},
            }
            unsubscribe = await self._ws_monitor.start_subscription(payload, callback)
            _LOGGER.debug("%s subscribed to updates", vin)
            return unsubscribe
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGER.error(ex)

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
        if ws_monitor.monitor is None or ws_monitor.monitor.done():
            await ws_monitor.start_monitor()
        return ws_monitor.websocket

    async def __graphql_query(self, headers: dict(str, str), url: str, body: str):
        """execute and return arbitrary graphql query"""
        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._close_session = True

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
                    extensions = error["extensions"]
                    if (code := extensions["code"]) == "UNAUTHENTICATED":
                        raise RivianUnauthenticated(
                            response.status, response_json, headers, body
                        )
                    if code == "DATA_ERROR":
                        raise RivianDataError(
                            response.status, response_json, headers, body
                        )
                    if code == "BAD_CURRENT_PASSWORD":
                        raise RivianInvalidCredentials(
                            response.status, response_json, headers, body
                        )
                    if (
                        code == "BAD_USER_INPUT"
                        and extensions["reason"] == "INVALID_OTP"
                    ):
                        raise RivianInvalidOTP(
                            response.status, response_json, headers, body
                        )
                    if code == "SESSION_MANAGER_ERROR":
                        raise RivianTemporarilyLockedError(
                            response.status, response_json, headers, body
                        )
                    if code == "RATE_LIMIT":
                        raise RivianApiRateLimitError(
                            response.status, response_json, headers, body
                        )
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
