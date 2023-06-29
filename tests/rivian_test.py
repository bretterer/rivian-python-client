"""Tests for `rivian.rivian`."""
from __future__ import annotations

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from rivian import Rivian
from rivian.exceptions import (
    RivianApiException,
    RivianApiRateLimitError,
    RivianDataError,
    RivianInvalidOTP,
    RivianTemporarilyLockedError,
)

# pylint: disable=protected-access


async def test_graphql_csrf_token_request(aresponses: ResponsesMockServer) -> None:
    """Test GraphQL Response for a CSRF token request"""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json:"},
            text="""{
                "data": {
                    "createCsrfToken": {
                        "__typename": "CreateCsrfTokenResponse",
                        "csrfToken": "valid_csrf_token",
                        "appSessionToken": "valid_app_session_token"
                    }
                }
            }""",
        ),
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()
        await rivian.create_csrf_token()
        assert rivian._csrf_token == "valid_csrf_token"
        assert rivian._app_session_token == "valid_app_session_token"
        await rivian.close()


async def test_graphql_authenticate_request(aresponses: ResponsesMockServer) -> None:
    """Test GraphQL Response for a Authentication request"""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json:"},
            text="""{
                "data": {
                    "login": {
                        "__typename": "MobileLoginResponse",
                        "accessToken": "valid_access_token",
                        "refreshToken": "valid_refresh_token",
                        "userSessionToken": "valid_user_session_token"
                    }
                }
            }""",
        ),
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()
        rivian._csrf_token = "token"
        rivian._app_session_token = "token"
        await rivian.authenticate_graphql("username", "password")
        assert rivian._access_token == "valid_access_token"
        assert rivian._refresh_token == "valid_refresh_token"
        assert rivian._user_session_token == "valid_user_session_token"
        await rivian.close()


async def test_get_registered_wallboxes(aresponses: ResponsesMockServer) -> None:
    """Test GraphQL Response for a getRegisteredWallboxes request"""
    aresponses.add(
        "rivian.com",
        "/api/gql/chrg/user/graphql",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json:"},
            text="""{
                "data": {
                    "getRegisteredWallboxes": [{
                        "__typename": "WallboxRecord",
                        "wallboxId": "W1-1113-3RV7-1-1234-00012",
                        "userId": "01-2a3259ba-0be3-42a7-bf82-69adea27dcdd-2b4532cd",
                        "wifiId": "Network",
                        "name": "Wall Charger",
                        "linked": true,
                        "latitude": "42.3601866",
                        "longitude": "-71.0589682",
                        "chargingStatus": "AVAILABLE",
                        "power": null,
                        "currentVoltage": null,
                        "currentAmps": null,
                        "softwareVersion": "V03.01.47",
                        "model": "W1-1113-3RV7",
                        "serialNumber": "W1-1113-3RV7-1-1234-00012",
                        "maxAmps": null,
                        "maxVoltage": "224.0",
                        "maxPower": "11000"
                    }]
                }
            }""",
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian()
        rivian._csrf_token = "token"
        rivian._app_session_token = "token"
        rivian._user_session_token = "token"
        response = await rivian.get_registered_wallboxes()
        response_json = await response.json()
        assert response.status == 200
        assert len(response_json["data"]["getRegisteredWallboxes"]) == 1
        assert (
            response_json["data"]["getRegisteredWallboxes"][0]["wallboxId"]
            == "W1-1113-3RV7-1-1234-00012"
        )
        await rivian.close()


async def test_get_vehicle_state(aresponses: ResponsesMockServer) -> None:
    """Test GraphQL Response for a vehicleState request"""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json:"},
            text="""{
                "data": {
                    "vehicleState": {
                        "__typename": "VehicleState",
                        "gnssLocation": {
                            "__typename": "VehicleLocation",
                            "latitude": 42.3601866,
                            "longitude": -71.0589682,
                            "timeStamp": "2022-10-26T20:07:01.081Z"
                        },
                        "alarmSoundStatus": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-07T04:42:39.880Z",
                            "value": "false"
                        },
                        "timeToEndOfCharge": {
                            "__typename": "TimeStampedFloat",
                            "timeStamp": "2022-10-26T20:04:38.716Z",
                            "value": 0
                        },
                        "doorFrontLeftLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "doorFrontLeftClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "doorFrontRightLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "doorFrontRightClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "doorRearLeftLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "doorRearLeftClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "doorRearRightLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "doorRearRightClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "windowFrontLeftClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "windowFrontRightClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "windowFrontLeftCalibrated": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "Calibrated"
                        },
                        "windowFrontRightCalibrated": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "Calibrated"
                        },
                        "windowRearLeftCalibrated": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "Calibrated"
                        },
                        "windowRearRightCalibrated": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "Calibrated"
                        },
                        "closureFrunkLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "closureFrunkClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "gearGuardLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "unlocked"
                        },
                        "closureLiftgateLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "closureLiftgateClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "signal_not_available"
                        },
                        "windowRearLeftClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "windowRearRightClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "closureSideBinLeftLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "closureSideBinLeftClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "closureSideBinRightLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "closureSideBinRightClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "closureTailgateLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "closureTailgateClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "closureTonneauLocked": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "locked"
                        },
                        "closureTonneauClosed": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.179Z",
                            "value": "closed"
                        },
                        "wiperFluidState": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-14T01:01:22.260Z",
                            "value": "normal"
                        },
                        "powerState": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:46:39.763Z",
                            "value": "ready"
                        },
                        "batteryHvThermalEventPropagation": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T16:58:03.936Z",
                            "value": "off"
                        },
                        "vehicleMileage": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-26T19:43:13.847Z",
                            "value": 8928840
                        },
                        "brakeFluidLow": null,
                        "gearStatus": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:43:18.344Z",
                            "value": "park"
                        },
                        "tirePressureStatusFrontLeft": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:39:27.589Z",
                            "value": "OK"
                        },
                        "tirePressureStatusValidFrontLeft": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:39:27.589Z",
                            "value": "valid"
                        },
                        "tirePressureStatusFrontRight": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:39:27.589Z",
                            "value": "OK"
                        },
                        "tirePressureStatusValidFrontRight": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:39:27.589Z",
                            "value": "valid"
                        },
                        "tirePressureStatusRearLeft": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:39:27.589Z",
                            "value": "OK"
                        },
                        "tirePressureStatusValidRearLeft": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:39:27.589Z",
                            "value": "valid"
                        },
                        "tirePressureStatusRearRight": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:39:27.589Z",
                            "value": "OK"
                        },
                        "tirePressureStatusValidRearRight": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:39:27.589Z",
                            "value": "valid"
                        },
                        "batteryLevel": {
                            "__typename": "TimeStampedFloat",
                            "timeStamp": "2022-10-26T19:46:30.360Z",
                            "value": 53.400002
                        },
                        "chargerState": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T18:00:45.533Z",
                            "value": "charging_ready"
                        },
                        "batteryHvThermalEvent": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:40:08.035Z",
                            "value": "nominal"
                        },
                        "rangeThreshold": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:40:08.035Z",
                            "value": "vehicle_range_normal"
                        },
                        "distanceToEmpty": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-26T19:38:56.266Z",
                            "value": 266
                        },
                        "otaAvailableVersionNumber": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 0
                        },
                        "otaAvailableVersionWeek": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 0
                        },
                        "otaAvailableVersionYear": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 0
                        },
                        "otaCurrentVersionNumber": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 3
                        },
                        "otaCurrentVersionWeek": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 35
                        },
                        "otaCurrentVersionYear": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 2022
                        },
                        "otaDownloadProgress": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 0
                        },
                        "otaInstallDuration": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 0
                        },
                        "otaInstallProgress": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 0
                        },
                        "otaInstallReady": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:43:18.428Z",
                            "value": "ota_available"
                        },
                        "otaInstallTime": {
                            "__typename": "TimeStampedInt",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": 0
                        },
                        "otaInstallType": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": "Convenience"
                        },
                        "otaStatus": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": "Idle"
                        },
                        "otaCurrentStatus": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-07T09:07:17.231Z",
                            "value": "Install_Success"
                        },
                        "cabinClimateInteriorTemperature": {
                            "__typename": "TimeStampedFloat",
                            "timeStamp": "2022-10-26T20:07:04.559Z",
                            "value": 21
                        },
                        "cabinClimateDriverTemperature": {
                            "__typename": "TimeStampedFloat",
                            "timeStamp": "2022-10-26T20:07:04.559Z",
                            "value": 20
                        },
                        "cabinPreconditioningStatus": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.808Z",
                            "value": "undefined"
                        },
                        "cabinPreconditioningType": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:45:39.808Z",
                            "value": "NONE"
                        },
                        "petModeStatus": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:43:18.485Z",
                            "value": "Off"
                        },
                        "petModeTemperatureStatus": {
                            "__typename": "TimeStampedString",
                            "timeStamp": "2022-10-26T19:43:18.485Z",
                            "value": "Default"
                        }
                    }
                }
            }""",
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian()
        rivian._app_session_token = "token"
        rivian._user_session_token = "token"
        properties = dict()
        response = await rivian.get_vehicle_state("vin", properties)
        response_json = await response.json()
        assert response.status == 200
        assert len(response_json["data"]["vehicleState"]) == 72
        await rivian.close()


async def test_get_live_charging_session(aresponses: ResponsesMockServer) -> None:
    """Test GraphQL Response for a getLiveSessionData request"""
    aresponses.add(
        "rivian.com",
        "/api/gql/chrg/user/graphql",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json:"},
            text="""{
                "data": {
                    "getLiveSessionData": {
                        "isRivianCharger": null,
                        "isFreeSession": null,
                        "vehicleChargerState": {
                            "__typename": "StringValueRecord",
                            "value": "charging_active",
                            "updatedAt": "2022-10-27T21:25:16.226Z"
                        },
                        "chargerId": null,
                        "startTime": "2022-10-27T20:48:27.222Z",
                        "timeElapsed": "2229",
                        "timeRemaining": {
                            "__typename": "StringValueRecord",
                            "value": "9651",
                            "updatedAt": "2022-10-27T21:25:27.222Z"
                        },
                        "kilometersChargedPerHour": {
                            "__typename": "FloatValueRecord",
                            "value": 32,
                            "updatedAt": "2022-10-27T21:25:25.149Z"
                        },
                        "power": {
                            "__typename": "FloatValueRecord",
                            "value": 9,
                            "updatedAt": "2022-10-27T21:25:16.226Z"
                        },
                        "rangeAddedThisSession": {
                            "__typename": "FloatValueRecord",
                            "value": 20,
                            "updatedAt": "2022-10-27T21:25:25.149Z"
                        },
                        "totalChargedEnergy": {
                            "__typename": "FloatValueRecord",
                            "value": 6,
                            "updatedAt": "2022-10-27T21:25:16.226Z"
                        },
                        "currentPrice": null
                    }
                }
            }""",
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian()
        rivian._app_session_token = "token"
        rivian._user_session_token = "token"
        properties = dict()
        response = await rivian.get_live_charging_session("vin", properties)
        response_json = await response.json()
        assert response.status == 200
        assert (
            response_json["data"]["getLiveSessionData"]["vehicleChargerState"]["value"]
            == "charging_active"
        )
        await rivian.close()


async def test_graphql_errors(aresponses: ResponsesMockServer) -> None:
    """Test GraphQL error responses."""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response={"errors": [{"extensions": {"code": "RATE_LIMIT"}}]},
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianApiRateLimitError):
            await rivian.get_vehicle_state("vin", {})
        await rivian.close()

    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response={"errors": [{"extensions": {"code": "DATA_ERROR"}}]},
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianDataError):
            await rivian.get_vehicle_state("vin", {})
        await rivian.close()

    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response={"errors": [{"extensions": {"code": "SESSION_MANAGER_ERROR"}}]},
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianTemporarilyLockedError):
            await rivian.get_vehicle_state("vin", {})
        await rivian.close()

    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response={"errors": [{}]},
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianApiException):
            await rivian.get_vehicle_state("vin", {})
        await rivian.close()

    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response={
            "errors": [
                {"extensions": {"code": "BAD_USER_INPUT", "reason": "INVALID_OTP"}}
            ]
        },
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianInvalidOTP):
            await rivian.authenticate("", "")
        await rivian.close()
