"""Asynchronous Python client for the Rivian API."""
from __future__ import annotations

from typing import Any

import asyncio
import json
import socket

import logging

import aiohttp
import async_timeout
from yarl import URL

_LOGGER = logging.getLogger(__name__)


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
        url = "https://auth.rivianservices.com/auth/api/v1/token/auth"

        headers = {
            "User-Agent": "RivianApp/707 CFNetwork/1237 Darwin/20.4.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

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
        url = "https://auth.rivianservices.com/auth/api/v1/token/auth"

        headers = {
            "User-Agent": "RivianApp/707 CFNetwork/1237 Darwin/20.4.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._session_token,
        }

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
    ) -> dict[str, Any]:
        """Validate the OTP"""
        url = "https://auth.rivianservices.com/auth/api/v1/token/refresh"

        headers = {
            "User-Agent": "RivianApp/707 CFNetwork/1237 Darwin/20.4.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

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

        text = await response.text()
        return {"message": text}

    async def get_vehicle_info(
        self, vin: str, access_token: str, properties: dict[str]
    ) -> dict[str, Any]:
        """get the vehicle info"""
        url = "https://cesium.rivianservices.com/v2/vehicle/latest"

        headers = {
            "User-Agent": "RivianApp/707 CFNetwork/1237 Darwin/20.4.0",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + access_token,
        }

        json_data = {
            "car": vin,
            "properties": [
                "body/closures/door_FL_state",
                "body/closures/door_FL_locked_state",
                "body/closures/door_FR_state",
                "body/closures/door_FR_locked_state",
                "body/closures/door_RL_state",
                "body/closures/door_RL_locked_state",
                "body/closures/door_RR_state",
                "body/closures/door_RR_locked_state",
                "body/closures/frunk_state",
                "body/closures/frunk_locked_state",
                "body/closures/tailgate_state",
                "body/closures/tailgate_locked_state",
                "body/closures/liftgate_state",
                "body/closures/liftgate_locked_state",
                "body/closures/tonneau_state",
                "body/closures/tonneau_locked_state",
                "body/closures/sidebin_L_state",
                "body/closures/sidebin_L_locked_state",
                "body/closures/sidebin_R_state",
                "body/closures/sidebin_R_locked_state",
                "body/closures/front_left_window_state",
                "body/closures/front_right_window_state",
                "body/closures/rear_left_window_state",
                "body/closures/rear_right_window_state",
                "body/closures/gear_guard_locked_state",
                "$gnss",
                "energy_storage/charger/adjusted_soc",
                "energy_storage/charger/vehicle_charger_state",
                "energy_storage/charger/EMS_charger_remainingtime_min_1",
                "energy_storage/vehicle_energy/vehicle_range",
                "energy_storage/icd_cid_notifications/range_threshold",
                "dynamics/propulsion_status/PRNDL",
                "thermal/tmm_status/cabin_precondition_state",
                "thermal/hvac_cabin_control/cabin_temperature",
                "body/alarm/sound_alarm",
                "telematics/ota_status/current_version_year",
                "telematics/ota_status/current_version_week",
                "telematics/ota_status/current_version_number",
                "telematics/ota_status/available_version_year",
                "telematics/ota_status/available_version_week",
                "telematics/ota_status/available_version_number",
                "telematics/ota_status/status",
                "telematics/ota_status/install_duration",
                "telematics/ota_status/install_progress",
                "telematics/ota_status/pending_reason_active_mode",
                "core/ota_status/cgm_ota_install_fast_charging",
                "core/ota_status/cgm_ota_install_hv_batt_low",
                "telematics/ota_status/pending_reason_lv_batt",
                "core/ota_status/cgm_ota_install_not_parked",
                "telematics/ota_status/pending_reason_other",
                "telematics/ota_status/status_current",
                "dynamics/odometer/value",
                "dynamics/tires/tire_FL_pressure_status",
                "dynamics/tires/tire_FR_pressure_status",
                "dynamics/tires/tire_RL_pressure_status",
                "dynamics/tires/tire_RR_pressure_status",
                "dynamics/tires/tire_FL_pressure_status_valid",
                "dynamics/tires/tire_FR_pressure_status_valid",
                "dynamics/tires/tire_RL_pressure_status_valid",
                "dynamics/tires/tire_RR_pressure_status_valid",
                "dynamics/powertrain_status/brake_fluid_level_low",
                "body/wipers/fluid_state",
                "core/power_modes/power_state",
            ],
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
                    response.status,
                    json.loads(contents.decode("utf8")),
                    headers,
                    json_data,
                )
            raise Exception(response.status, {"message": contents.decode("utf8")})

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
