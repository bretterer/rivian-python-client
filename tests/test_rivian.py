"""Tests for `rivian.rivian`."""

# pylint: disable=protected-access
from __future__ import annotations

import asyncio
import base64
import gc
import json
import uuid
from datetime import UTC, date, datetime
from typing import Any
from unittest.mock import AsyncMock, Mock

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from rivian import Rivian
from rivian.const import (
    VEHICLE_STATE_PROPERTIES,
    VEHICLE_STATES_SUBSCRIPTION_ONLY_PROPERTIES,
    VehicleCommand,
)
from rivian.exceptions import (
    RivianApiException,
    RivianApiRateLimitError,
    RivianBadRequestError,
    RivianDataError,
    RivianInvalidOTP,
    RivianPhoneLimitReachedError,
    RivianTemporarilyLockedError,
    RivianUnauthenticated,
)
from rivian.parallax import UNLOCK_RVM, encode_unlock
from rivian.parallax.proto import command_pb2, operation_pb2
from rivian.rivian import _CHARGING_NETWORK_IDS
from rivian.utils import generate_key_pair

from .responses import (
    AUTHENTICATION_OTP_RESPONSE,
    AUTHENTICATION_RESPONSE,
    CREATE_DEPARTURE_SCHEDULE_RESPONSE,
    CSRF_TOKEN_RESPONSE,
    DELETE_DEPARTURE_SCHEDULE_RESPONSE,
    DEPART_NOW_RESPONSE,
    OTP_TOKEN_RESPONSE,
    PLACES_RESPONSE,
    SEND_LOCATION_TO_VEHICLE_RESPONSE,
    SEND_PARALLAX_COMMAND_RESPONSE,
    SEND_VEHICLE_OPERATION_RESPONSE,
    SET_CHARGING_SCHEDULES_RESPONSE,
    SKIP_NEXT_SCHEDULED_DEPARTURE_RESPONSE,
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


async def test_skip_and_depart_now(aresponses: ResponsesMockServer) -> None:
    """Test skipping a scheduled departure and departing now."""
    requests = capture_requests(
        aresponses,
        SKIP_NEXT_SCHEDULED_DEPARTURE_RESPONSE,
        SKIP_NEXT_SCHEDULED_DEPARTURE_RESPONSE,
        DEPART_NOW_RESPONSE,
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="csrf",
            app_session_token="token",
            user_session_token="token",
        )

        response = await rivian.skip_next_scheduled_departure(
            "vehicle_id", "schedule_id", date(2026, 10, 14)
        )
        response_json = await response.json()
        assert response_json["data"]["skipNextScheduledDeparture"]["success"] is True
        assert requests[0]["variables"] == {
            "vehicleId": "vehicle_id",
            "scheduleId": "schedule_id",
            "skipDate": "2026-10-14",
        }

        # A datetime sends only its date; a string is sent as is
        await rivian.skip_next_scheduled_departure(
            "vehicle_id", "schedule_id", datetime(2026, 10, 14, 7, 30, tzinfo=UTC)
        )
        assert requests[1]["variables"]["skipDate"] == "2026-10-14"

        response = await rivian.depart_now("vehicle_id", "schedule_id", "2026-10-14")
        response_json = await response.json()
        assert response_json["data"]["departNow"]["success"] is True
        assert requests[2]["variables"] == {
            "vehicleId": "vehicle_id",
            "scheduleId": "schedule_id",
            "skipDate": "2026-10-14",
        }
        await rivian.close()


async def test_send_location_to_vehicle(aresponses: ResponsesMockServer) -> None:
    """Test sending a destination to a vehicle."""
    requests = capture_requests(aresponses, SEND_LOCATION_TO_VEHICLE_RESPONSE)
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="csrf",
            app_session_token="token",
            user_session_token="token",
        )

        response = await rivian.send_location_to_vehicle(
            "vehicle_id", "123 Main St, Springfield, IL"
        )
        response_json = await response.json()
        result = response_json["data"]["parseAndShareLocationToVehicle"]
        assert result["publishResponse"]["result"] == 0
        assert requests[0]["variables"] == {
            "str": "123 Main St, Springfield, IL",
            "vehicleId": "vehicle_id",
            "requiresWakeup": True,
        }
        await rivian.close()


async def test_trips(aresponses: ResponsesMockServer) -> None:
    """Test sending and ending a trip."""
    requests = capture_requests(
        aresponses,
        {"data": {"sendTripToVehicle": True}},
        {"data": {"sendTripToVehicle": False}},
        {"data": {"sendParallaxPayload": {"success": True}}},
        {"data": {"sendParallaxPayload": None}},
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="csrf",
            app_session_token="token",
            user_session_token="token",
        )

        stops = [("Stadium", 39.05, -94.48)]
        assert await rivian.send_trip_to_vehicle("vehicle_id", (40.1, -92.5), stops, 30)
        attrs = requests[0]["variables"]["attrs"]
        waypoints = attrs["waypoints"]
        assert [w["address"]["name"] for w in waypoints] == [
            "Vehicle location",
            "Stadium",
        ]
        assert waypoints[-1]["minArrivalSoC"] == 30
        assert "minArrivalSoC" not in waypoints[0]
        assert [n["networkId"] for n in attrs["preferences"]["networks"]] == list(
            _CHARGING_NETWORK_IDS
        )
        assert not await rivian.send_trip_to_vehicle("vehicle_id", (40.1, -92.5), stops)
        for bad in ({"stops": []}, {"min_arrival_soc": 101}):
            with pytest.raises(RivianBadRequestError):
                await rivian.send_trip_to_vehicle(
                    "vehicle_id", (0, 0), **({"stops": stops} | bad)
                )

        assert await rivian.end_trip("vehicle_id", "user")
        assert requests[2]["variables"]["meta"] == {
            "isVehicleModelOp": False,
            "model": "c2v_navigation.trip_copilot.updated_trip",
            "requiresWakeup": True,
            "vehicleId": "vehicle_id",
        }
        assert not await rivian.end_trip("vehicle_id", "user")


async def test_start_gear_guard_live_stream(aresponses: ResponsesMockServer) -> None:
    """Test starting a Gear Guard live stream."""
    requests = capture_requests(
        aresponses,
        SEND_PARALLAX_COMMAND_RESPONSE,
        {"data": {"sendParallaxPayload": None}},
        SEND_PARALLAX_COMMAND_RESPONSE,
        SEND_PARALLAX_COMMAND_RESPONSE,
        {"data": {"sendParallaxPayload": None}},
    )
    vehicle_key, private_key = generate_key_pair()
    keys = {
        "identity_id": "identity_id",
        "vehicle_key": vehicle_key,
        "private_key": private_key,
    }
    live = {"endpoint": "wss://kinesis", "role": "VIEWER", "iceServers": []}
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="csrf",
            app_session_token="token",
            user_session_token="token",
        )
        subscriptions: list[dict[str, Any]] = []
        unsubscribe = AsyncMock()

        async def subscribe(
            payload: dict[str, Any], callback: Any, _: str, on_error: Any
        ) -> Any:
            subscriptions.append(payload)
            callback({"payload": {"data": {"gearGuardLiveConfig": live}}})
            return unsubscribe

        rivian._start_subscription = subscribe  # type: ignore[method-assign]
        config = await rivian.start_gear_guard_live_stream("vehicle_id", "rear", **keys)
        assert config == live
        _, operation = decode_parallax_command(requests[0])
        assert operation.rvm == "security.video_monitoring.start_live_streaming"
        # The config is routed by the start command's id
        assert subscriptions[0]["variables"]["commandId"] == operation.command_id.hex()

        # A rejected start returns None and still ends the subscription
        assert not await rivian.start_gear_guard_live_stream("vehicle_id", **keys)
        assert unsubscribe.await_count == 2
        with pytest.raises(RivianBadRequestError):
            await rivian.start_gear_guard_live_stream("vehicle_id", "roof", **keys)

        # A refused start fails straight away instead of timing out
        async def refuse(
            payload: dict[str, Any], callback: Any, _: str, on_error: Any
        ) -> Any:
            on_error(
                {"payload": [{"extensions": {"reason": "VEHICLE_COMMAND_FORBIDDEN"}}]}
            )
            return unsubscribe

        rivian._start_subscription = refuse  # type: ignore[method-assign]
        with pytest.raises(RivianApiException, match="VEHICLE_COMMAND_FORBIDDEN"):
            await rivian.start_gear_guard_live_stream("vehicle_id", timeout=30, **keys)

        # An error payload sent as an object instead of a list still fails the start
        async def refuse_object(
            payload: dict[str, Any], callback: Any, _: str, on_error: Any
        ) -> Any:
            on_error({"payload": {"extensions": {"reason": "VEHICLE_ASLEEP"}}})
            return unsubscribe

        rivian._start_subscription = refuse_object  # type: ignore[method-assign]
        with pytest.raises(RivianApiException, match="VEHICLE_ASLEEP"):
            await rivian.start_gear_guard_live_stream("vehicle_id", timeout=30, **keys)

        # A refusal before a rejected start is read, so asyncio doesn't log it
        loop = asyncio.get_running_loop()
        unread: list[dict[str, Any]] = []
        loop.set_exception_handler(lambda _, context: unread.append(context))
        try:
            rivian._start_subscription = refuse  # type: ignore[method-assign]
            assert not await rivian.start_gear_guard_live_stream("vehicle_id", **keys)
            gc.collect()
        finally:
            loop.set_exception_handler(None)
        assert not unread


async def test_search_places(aresponses: ResponsesMockServer) -> None:
    """Test searching for places."""
    requests = capture_requests(aresponses, PLACES_RESPONSE, {"data": {"places": None}})
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="csrf",
            app_session_token="token",
            user_session_token="token",
        )

        results = await rivian.search_places("REI", 40.175, -92.591)
        assert results == PLACES_RESPONSE["data"]["places"]["results"]
        assert requests[0]["variables"]["params"] == {
            "query": "REI",
            "userLocation": {"latitude": 40.175, "longitude": -92.591},
            "autocomplete": "None",
        }
        assert await rivian.search_places("REI", 40.175, -92.591) == []


async def test_suggest_places(aresponses: ResponsesMockServer) -> None:
    """Test suggesting search texts for partial text."""
    predictions = [{"query": "restaurants"}, {"query": "Red Lobster"}]
    requests = capture_requests(
        aresponses,
        {"data": {"places": {"queryPredictions": predictions}}},
        {"data": {"places": None}},
    )
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="csrf",
            app_session_token="token",
            user_session_token="token",
        )

        assert await rivian.suggest_places("RE", 40.175, -92.591) == [
            "restaurants",
            "Red Lobster",
        ]
        assert requests[0]["variables"]["params"]["autocomplete"] == "Place"
        assert await rivian.suggest_places("RE", 40.175, -92.591) == []


async def test_subscribe_for_departure_schedules() -> None:
    """Test subscribing to departure schedules."""
    rivian = Rivian(user_session_token="token")
    unsubscribe = AsyncMock()
    monitor = Mock(wait_for_ack=AsyncMock(return_value=True))
    monitor.start_subscription = AsyncMock(return_value=unsubscribe)
    rivian._ws_monitor = monitor
    rivian._ws_connect = AsyncMock(return_value=monitor)  # type: ignore[method-assign]
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


SEND_REMOTE_COMMAND_MUTATION = (
    "mutation SendRemoteCommand($vehicleId: String!, $model: String!, "
    "$parallaxPayloadB64: String!) { sendParallaxPayload("
    "payload: $parallaxPayloadB64, meta: { vehicleId: $vehicleId model: $model "
    "isVehicleModelOp: true requiresWakeup: true } ) { success sequenceNumber } }"
)
COMMAND_ID = "00010203-0405-0607-0809-0a0b0c0d0e0f"


def decode_parallax_command(
    request: dict[str, Any],
) -> tuple[command_pb2.Envelope, command_pb2.Operation]:
    """Decode the envelope and operation of a sendParallaxPayload request."""
    payload = base64.b64decode(request["variables"]["parallaxPayloadB64"])
    envelope = command_pb2.Envelope.FromString(payload)
    return envelope, command_pb2.Operation.FromString(envelope.composite.bytes_val)


async def send_unlock(rivian: Rivian, **overrides: Any) -> str | None:
    """Send an unlock with a phone key and a vehicle key, or what overrides them."""
    vehicle_key, _ = generate_key_pair()
    _, private_key = generate_key_pair()
    args: dict[str, Any] = {
        "vehicle_id": "vehicle_id",
        "rvm": UNLOCK_RVM,
        "payload": encode_unlock(),
        "identity_id": "identity_id",
        "vehicle_key": vehicle_key,
        "private_key": private_key,
    }
    return await rivian.send_parallax_command(**(args | overrides))


def parallax_rivian() -> Rivian:
    """A client that can send commands."""
    return Rivian(csrf_token="csrf", app_session_token="app", user_session_token="user")


async def test_send_parallax_command(aresponses: ResponsesMockServer) -> None:
    """Test sending a signed Parallax command."""
    requests = capture_requests(
        aresponses,
        SEND_PARALLAX_COMMAND_RESPONSE,
        SEND_PARALLAX_COMMAND_RESPONSE,
        {"data": {"sendParallaxPayload": {"success": False, "sequenceNumber": 0}}},
        {"data": {"sendParallaxPayload": None}},
        {"data": None},
    )
    async with aiohttp.ClientSession():
        rivian = parallax_rivian()

        # Any form of a UUID is accepted, and returned in its canonical form
        assert await send_unlock(rivian, command_id=COMMAND_ID.upper()) == COMMAND_ID
        assert requests[0]["operationName"] == "SendRemoteCommand"
        assert requests[0]["query"] == SEND_REMOTE_COMMAND_MUTATION
        assert requests[0]["variables"]["vehicleId"] == "vehicle_id"
        assert requests[0]["variables"]["model"] == UNLOCK_RVM
        envelope, operation = decode_parallax_command(requests[0])
        assert operation.rvm == UNLOCK_RVM
        assert operation.payload == encode_unlock()
        assert operation.vehicle_id == "vehicle_id"
        assert uuid.UUID(bytes=operation.command_id) == uuid.UUID(COMMAND_ID)
        assert envelope.security_info.mapped_identity == "identity_id"

        # Without an id, a new one is made and returned
        new_id = await send_unlock(rivian)
        assert new_id is not None
        assert uuid.UUID(new_id).version == 4
        envelope, _ = decode_parallax_command(requests[1])
        assert uuid.UUID(bytes=envelope.correlation_id) == uuid.UUID(new_id)

        # Not accepted, or no answer
        for _ in range(3):
            assert await send_unlock(rivian) is None
        assert len(requests) == 5
        await rivian.close()


async def test_send_parallax_command_request_headers(
    aresponses: ResponsesMockServer,
) -> None:
    """Test that a Parallax command is sent with the session's headers."""
    headers: dict[str, str] = {}

    async def handler(request: aiohttp.web.Request) -> aiohttp.web.Response:
        headers.update(request.headers)
        return aresponses.Response(
            text=json.dumps(SEND_PARALLAX_COMMAND_RESPONSE),
            content_type="application/json",
        )

    aresponses.add("rivian.com", "/api/gql/gateway/graphql", "POST", response=handler)
    async with aiohttp.ClientSession():
        rivian = parallax_rivian()
        assert await send_unlock(rivian)
        assert headers["Csrf-Token"] == "csrf"
        assert headers["A-Sess"] == "app"
        assert headers["U-Sess"] == "user"
        await rivian.close()


async def test_send_parallax_command_error_response(
    aresponses: ResponsesMockServer,
) -> None:
    """Test that only an accepted command, in a successful response, is returned."""
    for status in (202, 500):
        aresponses.add(
            "rivian.com",
            "/api/gql/gateway/graphql",
            "POST",
            response=aresponses.Response(
                status=status,
                text=json.dumps(SEND_PARALLAX_COMMAND_RESPONSE),
                content_type="application/json",
            ),
        )
    async with aiohttp.ClientSession():
        rivian = parallax_rivian()
        for _ in range(2):
            assert await send_unlock(rivian) is None
        await rivian.close()


@pytest.mark.parametrize(
    "overrides",
    [
        {"command_id": ""},
        {"command_id": "not-a-uuid"},
        {"command_id": b"0" * 16},
        {"command_id": 5},
        {"vehicle_id": ""},
        {"rvm": ""},
        {"identity_id": ""},
    ],
)
async def test_send_parallax_command_refuses_bad_arguments(
    aresponses: ResponsesMockServer, overrides: dict[str, Any]
) -> None:
    """Test that a bad command id, or a missing id, is refused before sending."""
    requests = capture_requests(aresponses, SEND_PARALLAX_COMMAND_RESPONSE)
    async with aiohttp.ClientSession():
        rivian = parallax_rivian()
        with pytest.raises(RivianBadRequestError):
            await send_unlock(rivian, **overrides)
        assert not requests


async def test_send_parallax_command_with_bad_keys(
    aresponses: ResponsesMockServer,
) -> None:
    """Test that keys that can't sign fail before anything is sent."""
    requests = capture_requests(aresponses, SEND_PARALLAX_COMMAND_RESPONSE)
    async with aiohttp.ClientSession():
        rivian = parallax_rivian()
        with pytest.raises(ValueError):
            await send_unlock(rivian, private_key="not a key")
        assert not requests


async def test_subscribe_for_parallax_command_state() -> None:
    """Test following a Parallax command."""
    rivian = Rivian(user_session_token="token")
    unsubscribe = AsyncMock()
    monitor = Mock(wait_for_ack=AsyncMock(return_value=True))
    monitor.start_subscription = AsyncMock(return_value=unsubscribe)
    rivian._ws_monitor = monitor
    rivian._ws_connect = AsyncMock(return_value=monitor)  # type: ignore[method-assign]
    callback = Mock()

    # The id is subscribed to in the form it was signed in
    assert (
        await rivian.subscribe_for_parallax_command_state(
            "vehicle_id", COMMAND_ID.upper(), callback
        )
        is unsubscribe
    )
    payload, subscribed_callback = monitor.start_subscription.call_args.args
    assert payload["operationName"] == "vehicleCommandStatePx"
    assert payload["query"] == (
        "subscription vehicleCommandStatePx($vehicleId: String!, "
        "$commandId: String!) { vehicleCommandStatePx(vehicleId: $vehicleId, "
        "commandId: $commandId) { payload } }"
    )
    assert payload["variables"] == {"vehicleId": "vehicle_id", "commandId": COMMAND_ID}
    assert subscribed_callback is callback

    with pytest.raises(RivianBadRequestError):
        await rivian.subscribe_for_parallax_command_state(
            "vehicle_id", "not-a-uuid", callback
        )

    rivian._ws_connect.side_effect = aiohttp.ClientError
    assert (
        await rivian.subscribe_for_parallax_command_state(
            "vehicle_id", COMMAND_ID, callback
        )
        is None
    )


def test_ws_backoff_without_a_web_socket() -> None:
    """Test the web socket backoff properties before anything has connected."""
    rivian = Rivian()
    assert rivian.ws_backoff_remaining == 0
    assert not rivian.ws_rate_limited
    assert not rivian.ws_unauthenticated


def decode_vehicle_operation(
    request: dict[str, Any],
) -> operation_pb2.VehicleOperationRequest.Operation:
    """Decode the operation of a sendVehicleOperation request."""
    payload = base64.b64decode(request["variables"]["payload"])
    return operation_pb2.VehicleOperationRequest.FromString(payload).operation


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
        operation = decode_vehicle_operation(requests[0])
        assert operation.rvm == "comfort.cabin.climate_hold_setting"
        assert operation.type == operation_pb2.OPERATION_WRITE
        assert operation.payload == b"\x08\xa0\x38"

        assert await rivian.request_climate_hold_status("vehicle_id") is True
        operation = decode_vehicle_operation(requests[1])
        assert operation.rvm == "comfort.cabin.climate_hold_status"
        assert operation.type == operation_pb2.OPERATION_READ
        assert operation.payload == b""

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

        # Only the 15 minute steps from 2 to 8 hours are sent
        for minutes in (0, 60, 105, 130, 495):
            with pytest.raises(RivianBadRequestError):
                await rivian.set_climate_hold_duration("vehicle_id", minutes)
        assert len(requests) == 3
        await rivian.close()


@pytest.mark.parametrize(
    "command",
    [
        VehicleCommand.CABIN_HVAC_3RD_ROW_REAR_LEFT_SEAT_HEAT,
        VehicleCommand.CABIN_HVAC_3RD_ROW_REAR_RIGHT_SEAT_HEAT,
    ],
)
async def test_send_vehicle_command_requires_level(command: VehicleCommand) -> None:
    """Test third row seat heat commands require a `level` parameter."""
    rivian = Rivian()
    with pytest.raises(RivianBadRequestError):
        await rivian.send_vehicle_command(
            command, "vehicle_id", "phone_id", "identity_id", "vehicle_key", ""
        )
    await rivian.close()


@pytest.mark.parametrize(
    ("command", "params"),
    [
        (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": 30}),
        (VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, {"HVAC_set_temp": "warm"}),
        (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": 40}),
        (VehicleCommand.CHARGING_LIMITS, {"SOC_limit": 80.5}),
        (VehicleCommand.CHARGING_LIMITS, None),
        (VehicleCommand.CABIN_HVAC_STEERING_HEAT, {"level": 5}),
    ],
)
def test_validate_vehicle_command(
    command: VehicleCommand, params: dict[str, Any] | None
) -> None:
    """Invalid params are rejected the same way for either way of sending."""
    with pytest.raises(RivianBadRequestError):
        Rivian.validate_vehicle_command(command, params)


def test_validate_vehicle_command_keeps_params() -> None:
    """Validation leaves the params alone; `send_vehicle_command` converts the temperature."""
    params = {"HVAC_set_temp": 21}
    Rivian.validate_vehicle_command(
        VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP, params
    )
    assert params == {"HVAC_set_temp": 21}


async def test_send_vehicle_command_keeps_params(
    aresponses: ResponsesMockServer,
) -> None:
    """The temperature is sent as a string, and the caller's params can be sent again."""
    response = {"data": {"sendVehicleCommand": {"id": "command_id"}}}
    requests = capture_requests(aresponses, response, response)
    vehicle_key, private_key = generate_key_pair()
    params = {"HVAC_set_temp": 21}
    async with aiohttp.ClientSession():
        rivian = parallax_rivian()
        for _ in range(2):
            assert (
                await rivian.send_vehicle_command(
                    VehicleCommand.CABIN_PRECONDITIONING_SET_TEMP,
                    "vehicle_id",
                    "phone_id",
                    "identity_id",
                    vehicle_key,
                    private_key,
                    params=params,
                )
                == "command_id"
            )
        await rivian.close()
    assert params == {"HVAC_set_temp": 21}
    assert [r["variables"]["attrs"]["params"] for r in requests] == [
        {"HVAC_set_temp": "21"}
    ] * 2


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


@pytest.mark.parametrize(
    ("code", "reason", "exception"),
    [
        ("UNAUTHENTICATED", None, RivianUnauthenticated),
        ("BAD_USER_INPUT", "INVALID_OTP", RivianInvalidOTP),
        ("CONFLICT", "ENROLL_PHONE_LIMIT_REACHED", RivianPhoneLimitReachedError),
        (None, None, RivianApiException),
    ],
)
async def test_graphql_errors_do_not_include_secrets(
    aresponses: ResponsesMockServer,
    code: str | None,
    reason: str | None,
    exception: type[RivianApiException],
) -> None:
    """Test GraphQL error exceptions leave out request headers and body."""
    response = error_response(code, reason)
    aresponses.add("rivian.com", "/api/gql/gateway/graphql", "POST", response=response)
    async with aiohttp.ClientSession():
        rivian = Rivian(
            csrf_token="secret-csrf",
            app_session_token="secret-app-session",
            user_session_token="secret-user-session",
        )
        with pytest.raises(exception) as exc_info:
            await rivian.authenticate("user@example.com", "secret-password")
        await rivian.close()

    for text in (str(exc_info.value), repr(exc_info.value)):
        assert "secret" not in text
        assert "user@example.com" not in text
    # Status and response stay available to callers
    assert exc_info.value.args[-2:] == (200, response)


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
