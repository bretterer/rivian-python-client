"""Asynchronous Python client for the Rivian API."""
from __future__ import annotations

from typing import Any

import asyncio
import json
import socket
import random

import logging

import aiohttp
import async_timeout
from yarl import URL

from rivian.exceptions import RivianExpiredTokenError

_LOGGER = logging.getLogger(__name__)

CESIUM_BASEPATH = "https://cesium.rivianservices.com/v2"
AUTH_BASEPATH = "https://auth.rivianservices.com/auth/api/v1"
GRAPHQL_BASEPATH = "https://rivian.com/api/gql"
GRAPHQL_GATEWAY = GRAPHQL_BASEPATH + "/gateway/graphql"
GRAPHQL_CHARGING = GRAPHQL_BASEPATH + "/chrg/user/graphql"

BASE_HEADERS = {
    "User-Agent": "RivianApp/707 CFNetwork/1237 Darwin/20.4.0",
    "Accept": "application/json",
    "Content-Type": "application/json",
}

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

        self.client_id = client_id
        self.client_secret = client_secret
        self.request_timeout = request_timeout

        self._otp_needed = False

    async def authenticate(
        self,
        username: str,
        password: str,
    ) -> ClientRequest:
        """Authenticate against the Rivian API with Username and Password"""
        url = url = AUTH_BASEPATH + "/token/auth"

        headers = dict()
        headers.update(BASE_HEADERS)

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
        url = url = AUTH_BASEPATH + "/token/auth"

        headers = dict()
        headers.update(BASE_HEADERS)
        headers.update({
            "Authorization": "Bearer " + self._session_token,
        })

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
        url = url = AUTH_BASEPATH + "/token/refresh"

        headers = dict()
        headers.update(BASE_HEADERS)

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

        headers = dict()
        headers.update(BASE_HEADERS)
        headers.update({
            "Authorization": "Bearer " + access_token,
        })

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

    async def create_csrf_token(
        self
    ) -> dict[str, Any]:
        """create cross-site-request-forgery (csrf) token"""
        
        url = GRAPHQL_GATEWAY

        headers = dict()
        headers.update(BASE_HEADERS)

        graphql_json = {
            "operationName": "CreateCSRFToken",
            "query": "mutation CreateCSRFToken {\n  createCsrfToken {\n    __typename\n    csrfToken\n    appSessionToken\n  }\n}",
            "variables": None
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

        headers = dict()
        headers.update(BASE_HEADERS)
        headers.update({
            "Csrf-Token": self._csrf_token,
            "A-Sess": self._app_session_token,
            "Apollographql-Client-Name": "com.rivian.ios.consumer-apollo-ios"
        })

        graphql_json = {
            "operationName": "Login",
            "query": "mutation Login($email: String!, $password: String!) {\n  login(email: $email, password: $password) {\n    __typename\n    ... on MobileLoginResponse {\n      __typename\n      accessToken\n      refreshToken\n      userSessionToken\n    }\n    ... on MobileMFALoginResponse {\n      __typename\n      otpToken\n    }\n  }\n}",
            "variables": {
                "email": username,
                "password": password
            }
        }

        response = await self.__graphql_query(headers, url, graphql_json)
        
        response_json = await response.json()
        self._access_token = response_json["data"]["login"]["accessToken"]
        self._refresh_token = response_json["data"]["login"]["refreshToken"]
        self._user_session_token = response_json["data"]["login"]["userSessionToken"]
        
        return response


    async def get_user_information(
        self
    ) -> ClientResponse:
        """get user information (user.id, vehicle vins)"""
        url = GRAPHQL_GATEWAY
        
        headers = dict()
        headers.update(BASE_HEADERS)
        headers.update({
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token
        })
        
        graphql_json = {
            "operationName": "getUserInfo",
            "query": "query getUserInfo {\n    currentUser {\n        __typename\n        id\n        vehicles {\n        id\n        vin\n        vas {\n            __typename\n            vasVehicleId\n            vehiclePublicKey\n        }\n        roles\n        state\n        createdAt\n        updatedAt\n        vehicle {\n            __typename\n            id\n            vin\n            modelYear\n            make\n            model\n            expectedBuildDate\n            plannedBuildDate\n            expectedGeneralAssemblyStartDate\n            actualGeneralAssemblyDate\n        }\n        }\n    }\n}",
            "variables": None
        }

        return await self.__graphql_query(headers, url, graphql_json)


    async def get_registered_wallboxes(
        self
    ) -> ClientResponse:
        """get wallboxes (graphql)"""
        url = GRAPHQL_CHARGING
        
        headers = dict()
        headers.update(BASE_HEADERS)
        headers.update({
            "Csrf-Token": self._csrf_token,
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token
        })
        
        graphql_json = {
            "operationName": "getRegisteredWallboxes",
            "query": "query getRegisteredWallboxes {\n  getRegisteredWallboxes {\n    __typename\n    wallboxId\n    userId\n    wifiId\n    name\n    linked\n    latitude\n    longitude\n    chargingStatus\n    power\n    currentVoltage\n    currentAmps\n    softwareVersion\n    model\n    serialNumber\n    maxAmps\n    maxVoltage\n    maxPower\n  }\n}",
            "variables": None
        }

        return await self.__graphql_query(headers, url, graphql_json)
    

    async def get_vehicle_state(
        self, vin: str, properties: dict[str]
    ) -> ClientResponse:
        """get vehicle state (graphql)"""
        url = GRAPHQL_GATEWAY
        
        headers = dict()
        headers.update(BASE_HEADERS)
        headers.update({
            "A-Sess": self._app_session_token,
            "U-Sess": self._user_session_token
        })

        graphql_query = "query GetVehicleState($vehicleID: String!) {\n  vehicleState(id: $vehicleID) {\n    __typename\n:   "
        gnss_attribute_template = "{\n      __typename\n      latitude\n      longitude\n      timeStamp\n    }\n"
        generic_sensor_template = "{\n      __typename\n      timeStamp\n      value\n    }\n"

        for key in properties:
            template = generic_sensor_template
            if key == 'gnssLocation':
                template = gnss_attribute_template
        
            graphql_query += f'{key} {template}'
        graphql_query += '}'
        
        graphql_json = {
            "operationName":"GetVehicleState",
            "query":graphql_query,
            "variables": { 
                "vehicleID": vin
            }
        }

        return await self.__graphql_query(headers, url, graphql_json)


    async def get_live_charging_session(
        self, user_id: str, vin: str, properties: dict[str]
    ) -> ClientResponse:
        """get live charging session data (graphql)"""
        url = GRAPHQL_CHARGING
        
        headers = dict()
        headers.update(BASE_HEADERS)
        headers.update({
            "U-Sess": self._user_session_token
        })

        graphql_query = "query getLiveSessionData($vehicleId: ID!) {\n  getLiveSessionData(vehicleId: $vehicleId) {\n    __typename\n:   "
        detail_sensors = ['vehicleChargerState', 'timeRemaining', 'kilometersChargedPerHour', 'power', 'rangeAddedThisSession', 'totalChargedEnergy']
        detail_sensor_template = "{\n      __typename\n      value\n      updatedAt\n    }\n"

        for key in properties:
            template = ''
            if key in detail_sensors:
                template = detail_sensor_template
            graphql_query += f'{key} {template}'
        graphql_query += '}'
        
        graphql_json = {
            "operationName":"getLiveSessionData",
            "query":graphql_query,
            "variables": { 
                "userId": user_id,
                "vehicleId": vin
            }
        }

        return await self.__graphql_query(headers, url, graphql_json)


    async def __graphql_query(
        self, headers: dict(str, str), url: str, body: str
    ):
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
            raise Exception(
                "Timeout occurred while connecting to Rivian API."
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise Exception(
                "Error occurred while communicating with Rivian."
            ) from exception

        if response.status != 200:
            raise Exception("Error occurred while reading the graphql response from Rivian.")
            
        response_json = await response.json()
        if 'errors' in response_json:
            raise Exception("Error occurred while reading the graphql response from Rivian.")
        
        return response


    async def close(self) -> None:
        """Close open client session."""
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
