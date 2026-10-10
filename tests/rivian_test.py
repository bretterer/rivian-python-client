"""Tests for `rivian.rivian`."""

# pylint: disable=protected-access
from __future__ import annotations

import asyncio
import base64
import json
from typing import Any
from unittest.mock import AsyncMock, Mock

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from rivian import Rivian
from rivian.const import (
    VEHICLE_STATE_PROPERTIES,
    VEHICLE_STATES_SUBSCRIPTION_ONLY_PROPERTIES,
)
from rivian.exceptions import (
    RivianApiException,
    RivianApiRateLimitError,
    RivianBadRequestError,
    RivianDataError,
    RivianInvalidOTP,
    RivianTemporarilyLockedError,
    RivianUnauthenticated,
)
from rivian.parallax import _decode_protobuf_fields

from .responses import (
    AUTHENTICATION_OTP_RESPONSE,
    AUTHENTICATION_RESPONSE,
    CREATE_DEPARTURE_SCHEDULE_RESPONSE,
    CSRF_TOKEN_RESPONSE,
    DELETE_DEPARTURE_SCHEDULE_RESPONSE,
    LIVE_CHARGING_SESSION_RESPONSE,
    OTP_TOKEN_RESPONSE,
    SEND_VEHICLE_OPERATION_RESPONSE,
    SET_CHARGING_SCHEDULES_RESPONSE,
    UPDATE_DEPARTURE_SCHEDULE_RESPONSE,
    USER_INFORMATION_RESPONSE,
    VEHICLE_CHARGING_SCHEDULES_RESPONSE,
    VEHICLE_STATE_RESPONSE,
    WALLBOXES_RESPONSE,
    error_response,
    load_response,
)


async def test_csrf_token_request(aresponses: ResponsesMockServer) -> None:
    """Test CSRF token request."""
    aresponses.add(
        "rivian.com", "/api/gql/gateway/graphql", "POST", response=CSRF_TOKEN_RESPONSE
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()
        await rivian.create_csrf_token()
        assert rivian._csrf_token == "valid_csrf_token"
        assert rivian._app_session_token == "valid_app_session_token"
        await rivian.close()


async def test_authentication(aresponses: ResponsesMockServer) -> None:
    """Test authentication."""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response=AUTHENTICATION_RESPONSE,
    )
    async with (
        aiohttp.ClientSession(),
        Rivian(csrf_token="token", app_session_token="token") as rivian,
    ):
        await rivian.authenticate("username", "password")
        assert rivian._access_token == "valid_access_token"
        assert rivian._refresh_token == "valid_refresh_token"
        assert rivian._user_session_token == "valid_user_session_token"


async def test_invalid_authentication(aresponses: ResponsesMockServer) -> None:
    """Test invalid authentication."""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response=error_response("UNAUTHENTICATED", "UNAUTHENTICATED"),
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(csrf_token="token", app_session_token="token")
        with pytest.raises(RivianUnauthenticated):
            await rivian.authenticate("username", "bad_password")
        await rivian.close()


async def test_authentication_with_otp(aresponses: ResponsesMockServer) -> None:
    """Test authentication with OTP enabled."""
    aresponses.add(
        "rivian.com", "/api/gql/gateway/graphql", "POST", response=OTP_TOKEN_RESPONSE
    )
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response=AUTHENTICATION_OTP_RESPONSE,
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(csrf_token="token", app_session_token="token")
        await rivian.authenticate("username", "password")
        assert rivian._otp_needed
        assert rivian._otp_token == "token"

        await rivian.validate_otp("username", "code")
        assert rivian._access_token == "token"
        assert rivian._refresh_token == "token"
        assert rivian._user_session_token == "token"
        await rivian.close()


async def test_authentication_with_expired_otp(aresponses: ResponsesMockServer) -> None:
    """Test authentication with expired OTP token."""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response=error_response("UNAUTHENTICATED", "OTP_TOKEN_EXPIRED"),
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(csrf_token="token", app_session_token="token")
        rivian._otp_needed = True
        rivian._otp_token = "token"

        with pytest.raises(RivianInvalidOTP):
            await rivian.validate_otp("username", "expired_code")
        await rivian.close()


async def test_get_user_information(aresponses: ResponsesMockServer) -> None:
    """Test get user information request."""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response=USER_INFORMATION_RESPONSE,
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="token", app_session_token="token", user_session_token="token"
        )
        response = await rivian.get_user_information()
        response_json = await response.json()
        assert response.status == 200
        assert (current_user := response_json["data"]["currentUser"])
        assert current_user["id"] == "id"
        assert len(current_user["vehicles"]) == 1
        await rivian.close()


async def test_get_registered_wallboxes(aresponses: ResponsesMockServer) -> None:
    """Test GraphQL Response for a getRegisteredWallboxes request"""
    aresponses.add(
        "rivian.com", "/api/gql/chrg/user/graphql", "POST", response=WALLBOXES_RESPONSE
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="token", app_session_token="token", user_session_token="token"
        )
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
        response=VEHICLE_STATE_RESPONSE,
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(app_session_token="token", user_session_token="token")
        response = await rivian.get_vehicle_state("vin", {})
        response_json = await response.json()
        assert response.status == 200
        assert len(response_json["data"]["vehicleState"]) == 72
        await rivian.close()


async def test_get_vehicle_state_default_query(aresponses: ResponsesMockServer) -> None:
    """Test the default vehicleState query only requests queryable fields"""
    queries: list[str] = []

    async def handler(request: aiohttp.web.Request) -> aiohttp.web.Response:
        queries.append((await request.json())["query"])
        return aresponses.Response(
            text=json.dumps(VEHICLE_STATE_RESPONSE), content_type="application/json"
        )

    aresponses.add("rivian.com", "/api/gql/gateway/graphql", "POST", response=handler)
    async with aiohttp.ClientSession():
        rivian = Rivian(app_session_token="token", user_session_token="token")
        await rivian.get_vehicle_state("vin")
        await rivian.close()

    assert not VEHICLE_STATE_PROPERTIES & VEHICLE_STATES_SUBSCRIPTION_ONLY_PROPERTIES
    assert "gnssLocation { latitude longitude timeStamp }" in queries[0]
    assert "isAuthorized" not in queries[0]
    for subscription_only in VEHICLE_STATES_SUBSCRIPTION_ONLY_PROPERTIES:
        assert f"{subscription_only} " not in queries[0]


def test_vehicle_state_subscription_fragment() -> None:
    """Test the vehicleState subscription fragment keeps `isAuthorized`"""
    fragment = Rivian()._build_vehicle_state_fragment({"gnssLocation"})
    assert fragment == "{ gnssLocation { latitude longitude timeStamp isAuthorized } }"


async def test_get_live_charging_session(aresponses: ResponsesMockServer) -> None:
    """Test GraphQL Response for a getLiveSessionData request"""
    aresponses.add(
        "rivian.com",
        "/api/gql/chrg/user/graphql",
        "POST",
        response=LIVE_CHARGING_SESSION_RESPONSE,
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(app_session_token="token", user_session_token="token")
        response = await rivian.get_live_charging_session("vin", {})
        response_json = await response.json()
        assert response.status == 200
        assert (
            response_json["data"]["getLiveSessionData"]["vehicleChargerState"]["value"]
            == "charging_active"
        )
        await rivian.close()


async def test_get_charging_schedules(aresponses: ResponsesMockServer) -> None:
    """Test getting vehicle charging schedules."""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response=VEHICLE_CHARGING_SCHEDULES_RESPONSE,
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(app_session_token="token", user_session_token="token")
        response = await rivian.get_charging_schedules("vehicle_id")
        response_json = await response.json()
        assert response.status == 200
        schedules = response_json["data"]["getVehicle"]["chargingSchedules"]
        assert len(schedules) == 1
        assert schedules[0]["amperage"] == 32
        assert schedules[0]["enabled"] is True
        assert len(schedules[0]["weekDays"]) == 7
        await rivian.close()


async def test_set_charging_schedules(aresponses: ResponsesMockServer) -> None:
    """Test setting vehicle charging schedules."""
    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response=SET_CHARGING_SCHEDULES_RESPONSE,
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="csrf",
            app_session_token="token",
            user_session_token="token",
        )
        schedules = [
            {
                "weekDays": [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                "startTime": 0,
                "duration": 1440,
                "location": {"latitude": 37.7749, "longitude": -122.4194},
                "amperage": 16,
                "enabled": True,
            }
        ]
        response = await rivian.set_charging_schedules("vehicle_id", schedules)
        response_json = await response.json()
        assert response.status == 200
        assert response_json["data"]["setChargingSchedules"]["success"] is True
        await rivian.close()


DEPARTURE_SCHEDULE = {
    "name": "Weekdays",
    "isEnabled": True,
    "repeatsWeekly": {"days": ["Monday"], "startsAtMin": 450, "skippedOn": []},
    "departureSettings": {
        "shouldOverrideChargeSchedule": False,
        "comfortSettings": {
            "cabinTempCelsius": 21,
            "frontDefogDefrost": "Off",
            "surfaceHeatVentLevels": {
                "frontLeftSeat": "Off",
                "frontRightSeat": "Off",
                "rearLeftSeat": "Off",
                "rearRightSeat": "Off",
                "steeringWheel": "Off",
            },
        },
    },
}


def capture_requests(
    aresponses: ResponsesMockServer, *responses: dict[str, Any]
) -> list[dict[str, Any]]:
    """Queue gateway responses and return a list that collects the request bodies."""
    requests: list[dict[str, Any]] = []

    def add(response: dict[str, Any]) -> None:
        async def handler(request: aiohttp.web.Request) -> aiohttp.web.Response:
            requests.append(await request.json())
            return aresponses.Response(
                text=json.dumps(response), content_type="application/json"
            )

        aresponses.add(
            "rivian.com", "/api/gql/gateway/graphql", "POST", response=handler
        )

    for response in responses:
        add(response)
    return requests


async def test_departure_schedules(aresponses: ResponsesMockServer) -> None:
    """Test creating, updating and deleting a departure schedule."""
    requests = capture_requests(
        aresponses,
        CREATE_DEPARTURE_SCHEDULE_RESPONSE,
        UPDATE_DEPARTURE_SCHEDULE_RESPONSE,
        DELETE_DEPARTURE_SCHEDULE_RESPONSE,
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="csrf",
            app_session_token="token",
            user_session_token="token",
        )

        response = await rivian.create_departure_schedule(
            "vehicle_id", DEPARTURE_SCHEDULE
        )
        response_json = await response.json()
        assert response_json["data"]["createDepartureSchedule"]["success"] is True
        assert requests[0]["variables"] == {
            "vehicleId": "vehicle_id",
            "schedule": DEPARTURE_SCHEDULE,
        }

        response = await rivian.update_departure_schedule(
            "vehicle_id", "schedule_id", DEPARTURE_SCHEDULE
        )
        response_json = await response.json()
        assert response_json["data"]["updateDepartureSchedule"]["success"] is True
        assert requests[1]["variables"] == {
            "vehicleId": "vehicle_id",
            "scheduleId": "schedule_id",
            "schedule": DEPARTURE_SCHEDULE,
        }

        response = await rivian.delete_departure_schedule("vehicle_id", "schedule_id")
        response_json = await response.json()
        assert response_json["data"]["deleteDepartureSchedule"]["success"] is True
        assert requests[2]["variables"] == {
            "vehicleId": "vehicle_id",
            "scheduleId": "schedule_id",
        }
        await rivian.close()


async def test_subscribe_for_departure_schedules() -> None:
    """Test subscribing to departure schedules."""
    rivian = Rivian(user_session_token="token")
    unsubscribe = AsyncMock()
    monitor = Mock(connection_ack=asyncio.Event())
    monitor.connection_ack.set()
    monitor.start_subscription = AsyncMock(return_value=unsubscribe)
    rivian._ws_monitor = monitor
    rivian._ws_connect = AsyncMock()  # type: ignore[method-assign]
    callback = Mock()

    assert (
        await rivian.subscribe_for_departure_schedules("vehicle_id", callback)
        is unsubscribe
    )
    payload, subscribed_callback = monitor.start_subscription.call_args.args
    assert "vehicleDepartureSchedules(vehicleId: $vehicleId)" in payload["query"]
    assert payload["variables"] == {"vehicleId": "vehicle_id"}
    assert subscribed_callback is callback

    rivian._ws_connect.side_effect = aiohttp.ClientError
    assert (
        await rivian.subscribe_for_departure_schedules("vehicle_id", callback) is None
    )


def decode_vehicle_operation(request: dict[str, Any]) -> list[tuple[int, int, Any]]:
    """Decode the operation of a sendVehicleOperation request."""
    payload = base64.b64decode(request["variables"]["payload"])
    _, (_, _, operation) = _decode_protobuf_fields(payload)
    return _decode_protobuf_fields(operation)


async def test_send_vehicle_operation(aresponses: ResponsesMockServer) -> None:
    """Test sending vehicle operations."""
    requests = capture_requests(
        aresponses,
        SEND_VEHICLE_OPERATION_RESPONSE,
        SEND_VEHICLE_OPERATION_RESPONSE,
        {"data": {"sendVehicleOperation": None}},
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="csrf",
            app_session_token="token",
            user_session_token="token",
        )

        assert await rivian.set_climate_hold_duration("vehicle_id", 120) is True
        assert requests[0]["variables"]["vehicleId"] == "vehicle_id"
        assert decode_vehicle_operation(requests[0]) == [
            (1, 2, b"comfort.cabin.climate_hold_setting"),
            (2, 0, 1),
            (4, 2, b"\x08\xa0\x38"),
        ]

        assert await rivian.request_climate_hold_status("vehicle_id") is True
        assert decode_vehicle_operation(requests[1]) == [
            (1, 2, b"comfort.cabin.climate_hold_status"),
            (2, 0, 0),
        ]

        assert await rivian.send_vehicle_operation("vehicle_id", "some.rvm") is False

        aresponses.add(
            "rivian.com",
            "/api/gql/gateway/graphql",
            "POST",
            response=aresponses.Response(
                status=500, text="{}", content_type="application/json"
            ),
        )
        assert await rivian.send_vehicle_operation("vehicle_id", "some.rvm") is False

        with pytest.raises(RivianBadRequestError):
            await rivian.set_climate_hold_duration("vehicle_id", 0)
        assert len(requests) == 3
        await rivian.close()


async def test_graphql_errors(aresponses: ResponsesMockServer) -> None:
    """Test GraphQL error responses."""
    host = "rivian.com"
    path = "/api/gql/gateway/graphql"

    aresponses.add(host, path, "POST", response=error_response("RATE_LIMIT"))
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianApiRateLimitError):
            await rivian.get_vehicle_state("vin", {})
        await rivian.close()

    aresponses.add(host, path, "POST", response=error_response("DATA_ERROR"))
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianDataError):
            await rivian.get_vehicle_state("vin", {})
        await rivian.close()

    aresponses.add(host, path, "POST", response=error_response("SESSION_MANAGER_ERROR"))
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianTemporarilyLockedError):
            await rivian.get_vehicle_state("vin", {})
        await rivian.close()

    aresponses.add(host, path, "POST", response=error_response())
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianApiException):
            await rivian.get_vehicle_state("vin", {})
        await rivian.close()

    aresponses.add(
        host, path, "POST", response=error_response("BAD_USER_INPUT", "INVALID_OTP")
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()
        with pytest.raises(RivianInvalidOTP):
            await rivian.authenticate("", "")
        await rivian.close()


async def test_get_drivers_and_keys(aresponses: ResponsesMockServer) -> None:
    """Test get drivers and keys."""
    host = "rivian.com"
    path = "/api/gql/gateway/graphql"

    aresponses.add(
        host, path, "POST", response=load_response("drivers_and_keys_success")
    )
    async with aiohttp.ClientSession():
        rivian = Rivian()

        response = await rivian.get_drivers_and_keys(vehicle_id="vehicleId")
        response_json = await response.json()
        assert response.status == 200
        assert (drivers_and_keys := response_json["data"]["getVehicle"])
        assert drivers_and_keys["id"] == "id"
        assert len(drivers_and_keys["invitedUsers"]) == 4
        await rivian.close()
