"""Tests for `rivian.rivian`."""

# pylint: disable=protected-access
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
    RivianUnauthenticated,
)

from .responses import (
    AUTHENTICATION_OTP_RESPONSE,
    AUTHENTICATION_RESPONSE,
    CSRF_TOKEN_RESPONSE,
    LIVE_CHARGING_SESSION_RESPONSE,
    OTP_TOKEN_RESPONSE,
    USER_INFORMATION_RESPONSE,
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
    async with aiohttp.ClientSession():
        async with Rivian(csrf_token="token", app_session_token="token") as rivian:
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
