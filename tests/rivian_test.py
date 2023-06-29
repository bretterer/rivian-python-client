"""Tests for `rivian.rivian`."""
import asyncio
from unittest.mock import patch

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from rivian import Rivian
from rivian.exceptions import (
    RivianApiException,
    RivianApiRateLimitError,
    RivianDataError,
    RivianExpiredTokenError,
    RivianInvalidCredentials,
    RivianInvalidOTP,
    RivianTemporarilyLockedError,
    RivianUnauthenticated,
)


@pytest.mark.asyncio
async def test_authentication_request_with_otp(aresponses):
    """Test JSON Response for an authentication request requiring OTP"""
    aresponses.add(
        "auth.rivianservices.com",
        "/auth/api/v1/token/auth",
        "POST",
        aresponses.Response(
            status=401,
            headers={"Content-Type": "application/json:"},
            text="""{
                "api": "/auth/api/v1/token/auth",
                "error": "otp_entry_required",
                "error_description": "User is registered for MFA",
                "result": -901,
                "session_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMwOTQ3NzQsIm5iZiI6MTY1MzA5Mzg3MywiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJzZXNzaW9uX2lkIjoic2Vzc2lvbl9pZCJ9.bC84P5DBu517gjARQhR9FRIsI_Hv1mWYBy_OD52QVgI"
            }""",
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        response = await rivian.authenticate("username", "password")
        response_json = await response.json()
        assert response.status == 401
        assert response_json["error_description"] == "User is registered for MFA"
        assert (
            response_json["session_token"]
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMwOTQ3NzQsIm5iZiI6MTY1MzA5Mzg3MywiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJzZXNzaW9uX2lkIjoic2Vzc2lvbl9pZCJ9.bC84P5DBu517gjARQhR9FRIsI_Hv1mWYBy_OD52QVgI"
        )
        await rivian.close()


@pytest.mark.asyncio
async def test_otp_validation(aresponses):
    """Test JSON Response for an otp validation"""
    aresponses.add(
        "auth.rivianservices.com",
        "/auth/api/v1/token/auth",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json:"},
            text="""{
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4",
                "api": "/auth/api/v1/token/auth",
                "expires_in": 7200,
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Njg2NDU5MDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsInVzZXJfaWQiOiJ1c2VyX2lkIn0.Gu3SQt1la_SJwvU4hKccojygfTqFL1nWrxsEDv-ewks",
                "result": 0,
                "rights": {},
                "token_type": "bearer"
            }""",
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        response = await rivian.validate_otp(
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMwOTQ3NzQsIm5iZiI6MTY1MzA5Mzg3MywiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJzZXNzaW9uX2lkIjoic2Vzc2lvbl9pZCJ9.bC84P5DBu517gjARQhR9FRIsI_Hv1mWYBy_OD52QVgI",
            "123456",
        )
        assert response.status == 200
        response_json = await response.json()
        assert response_json["expires_in"] == 7200
        assert (
            response_json["access_token"]
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4"
        )
        assert (
            response_json["refresh_token"]
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Njg2NDU5MDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsInVzZXJfaWQiOiJ1c2VyX2lkIn0.Gu3SQt1la_SJwvU4hKccojygfTqFL1nWrxsEDv-ewks"
        )
        await rivian.close()


@pytest.mark.asyncio
async def test_authentication_request_without_otp(aresponses):
    """Test JSON Response for an authentication request without OTP"""
    aresponses.add(
        "auth.rivianservices.com",
        "/auth/api/v1/token/auth",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json:"},
            text="""{
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4",
                "api": "/auth/api/v1/token/auth",
                "expires_in": 7200,
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Njg2NDU5MDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsInVzZXJfaWQiOiJ1c2VyX2lkIn0.Gu3SQt1la_SJwvU4hKccojygfTqFL1nWrxsEDv-ewks",
                "result": 0,
                "rights": {},
                "token_type": "bearer"
            }""",
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        response = await rivian.authenticate("username", "password")
        assert response.status == 200
        response_json = await response.json()
        assert response_json["expires_in"] == 7200
        assert (
            response_json["access_token"]
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4"
        )
        assert (
            response_json["refresh_token"]
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Njg2NDU5MDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsInVzZXJfaWQiOiJ1c2VyX2lkIn0.Gu3SQt1la_SJwvU4hKccojygfTqFL1nWrxsEDv-ewks"
        )
        await rivian.close()


@pytest.mark.asyncio
async def test_refresh_access_token(aresponses):
    """Test JSON Response for refreshing access_token"""
    aresponses.add(
        "auth.rivianservices.com",
        "/auth/api/v1/token/refresh",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json:"},
            text="""{
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4",
                "api": "/auth/api/v1/token/refresh",
                "app_id": "RIVIAN_MOBILE",
                "expires_in": 7200,
                "result": 0,
                "token_type": "bearer"
            }""",
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        response = await rivian.refresh_access_token(
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMwOTQ3NzQsIm5iZiI6MTY1MzA5Mzg3MywiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJzZXNzaW9uX2lkIjoic2Vzc2lvbl9pZCJ9.bC84P5DBu517gjARQhR9FRIsI_Hv1mWYBy_OD52QVgI",
            "abcd1234",
            "wxyz9876",
        )
        assert response.status == 200
        response_json = await response.json()
        assert response_json["expires_in"] == 7200
        assert (
            response_json["access_token"]
            == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4"
        )
        await rivian.close()


@pytest.mark.asyncio
async def test_expired_access_token_throws_exception(aresponses):
    """Test JSON Response for refreshing access_token"""
    aresponses.add(
        "cesium.rivianservices.com",
        "/v2/vehicle/latest",
        "POST",
        aresponses.Response(
            status=401,
            headers={"Content-Type": "application/json:"},
            text="""{
                "error_code": -40,
                "error_desc": "Authentication Error <class 'rcore.rexceptions.RPermissionErrorTokenExpired'>",
                "error_name": "AuthError"
            }""",
        ),
    )
    with pytest.raises(RivianExpiredTokenError):
        async with aiohttp.ClientSession() as session:
            rivian = Rivian("abcd1234", "wxyz9876")

            response = await rivian.get_vehicle_info("vin123", "accessToken", [])
            assert response.status == 401

            await rivian.close()


@pytest.mark.asyncio
async def test_graphql_csrf_token_request(aresponses):
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
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        response = await rivian.create_csrf_token()
        response_json = await response.json()
        assert response.status == 200
        assert rivian._csrf_token == "valid_csrf_token"
        assert rivian._app_session_token == "valid_app_session_token"
        await rivian.close()


@pytest.mark.asyncio
async def test_graphql_authenticate_request(aresponses):
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
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        rivian._csrf_token = "token"
        rivian._app_session_token = "token"
        response = await rivian.authenticate_graphql("username", "password")
        response_json = await response.json()
        assert response.status == 200
        assert rivian._access_token == "valid_access_token"
        assert rivian._refresh_token == "valid_refresh_token"
        assert rivian._user_session_token == "valid_user_session_token"
        await rivian.close()


@pytest.mark.asyncio
async def test_get_registered_wallboxes(aresponses):
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
        rivian = Rivian("abcd1234", "wxyz9876")
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


@pytest.mark.asyncio
async def test_get_vehicle_state(aresponses):
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
        rivian = Rivian("abcd1234", "wxyz9876")
        rivian._app_session_token = "token"
        rivian._user_session_token = "token"
        properties = dict()
        response = await rivian.get_vehicle_state("vin", properties)
        response_json = await response.json()
        assert response.status == 200
        assert len(response_json["data"]["vehicleState"]) == 72
        await rivian.close()


@pytest.mark.asyncio
async def test_get_live_charging_session(aresponses):
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
        rivian = Rivian("abcd1234", "wxyz9876")
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
        rivian = Rivian("", "")
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
        rivian = Rivian("", "")
        with pytest.raises(RivianDataError):
            await rivian.get_vehicle_state("vin", {})
        await rivian.close()

    aresponses.add(
        "rivian.com",
        "/api/gql/gateway/graphql",
        "POST",
        response={"errors": [{}]},
    )
    async with aiohttp.ClientSession():
        rivian = Rivian("", "")
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
        rivian = Rivian("", "")
        with pytest.raises(RivianInvalidOTP):
            await rivian.authenticate_graphql("", "")
        await rivian.close()
