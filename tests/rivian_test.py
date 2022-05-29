"""Tests for `rivian.rivian`."""
import asyncio
from unittest.mock import patch

import aiohttp
import pytest

from rivian import Rivian
from rivian.exceptions import RivianExpiredTokenError

@pytest.mark.asyncio
async def test_authentication_request_with_otp(aresponses):
    """Test JSON Response for an authentication request requiring OTP"""
    aresponses.add(
        "auth.rivianservices.com",
        "/auth/api/v1/token/auth",
        "POST",
        aresponses.Response(
            status=401,
            headers={
                "Content-Type": "application/json:"
            },
            text='''{
                "api": "/auth/api/v1/token/auth",
                "error": "otp_entry_required",
                "error_description": "User is registered for MFA",
                "result": -901,
                "session_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMwOTQ3NzQsIm5iZiI6MTY1MzA5Mzg3MywiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJzZXNzaW9uX2lkIjoic2Vzc2lvbl9pZCJ9.bC84P5DBu517gjARQhR9FRIsI_Hv1mWYBy_OD52QVgI"
            }'''
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        response = await rivian.authenticate("username", "password")
        response_json = await response.json()
        assert response.status == 401
        assert response_json["error_description"] == "User is registered for MFA"
        assert response_json["session_token"] == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMwOTQ3NzQsIm5iZiI6MTY1MzA5Mzg3MywiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJzZXNzaW9uX2lkIjoic2Vzc2lvbl9pZCJ9.bC84P5DBu517gjARQhR9FRIsI_Hv1mWYBy_OD52QVgI"
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
            headers={
                "Content-Type": "application/json:"
            },
            text='''{
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4",
                "api": "/auth/api/v1/token/auth",
                "expires_in": 7200,
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Njg2NDU5MDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsInVzZXJfaWQiOiJ1c2VyX2lkIn0.Gu3SQt1la_SJwvU4hKccojygfTqFL1nWrxsEDv-ewks",
                "result": 0,
                "rights": {},
                "token_type": "bearer"
            }'''
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        response = await rivian.validate_otp("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMwOTQ3NzQsIm5iZiI6MTY1MzA5Mzg3MywiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJzZXNzaW9uX2lkIjoic2Vzc2lvbl9pZCJ9.bC84P5DBu517gjARQhR9FRIsI_Hv1mWYBy_OD52QVgI", "123456")
        assert response.status == 200
        response_json = await response.json()
        assert response_json["expires_in"] == 7200
        assert response_json["access_token"] == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4"
        assert response_json["refresh_token"] == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Njg2NDU5MDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsInVzZXJfaWQiOiJ1c2VyX2lkIn0.Gu3SQt1la_SJwvU4hKccojygfTqFL1nWrxsEDv-ewks"
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
            headers={
                "Content-Type": "application/json:"
            },
            text='''{
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4",
                "api": "/auth/api/v1/token/auth",
                "expires_in": 7200,
                "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Njg2NDU5MDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsInVzZXJfaWQiOiJ1c2VyX2lkIn0.Gu3SQt1la_SJwvU4hKccojygfTqFL1nWrxsEDv-ewks",
                "result": 0,
                "rights": {},
                "token_type": "bearer"
            }'''
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        response = await rivian.authenticate("username", "password")
        assert response.status == 200
        response_json = await response.json()
        assert response_json["expires_in"] == 7200
        assert response_json["access_token"] == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4"
        assert response_json["refresh_token"] == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2Njg2NDU5MDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsInVzZXJfaWQiOiJ1c2VyX2lkIn0.Gu3SQt1la_SJwvU4hKccojygfTqFL1nWrxsEDv-ewks"
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
            headers={
                "Content-Type": "application/json:"
            },
            text='''{
                "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4",
                "api": "/auth/api/v1/token/refresh",
                "app_id": "RIVIAN_MOBILE",
                "expires_in": 7200,
                "result": 0,
                "token_type": "bearer"
            }'''
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("abcd1234", "wxyz9876")
        response = await rivian.refresh_access_token("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMwOTQ3NzQsIm5iZiI6MTY1MzA5Mzg3MywiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJzZXNzaW9uX2lkIjoic2Vzc2lvbl9pZCJ9.bC84P5DBu517gjARQhR9FRIsI_Hv1mWYBy_OD52QVgI", "abcd1234", "wxyz9876")
        assert response.status == 200
        response_json = await response.json()
        assert response_json["expires_in"] == 7200
        assert response_json["access_token"] == "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NTMxMDExMDIsIm5iZiI6MTY1MzA5MzkwMSwiaXNzIjoicml2aWFuLmNvbSIsImF1ZCI6WyJodHRwczovL2Nsb3VkLnJpdmlhbnNlcnZpY2VzLmNvbS8iLCJodHRwczovL2F1dGgucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vKi1zZXJ2aWNlLWNocmctKi5wcm9kIiwiaHR0cHM6Ly9kdC1ncWwtYWNjb3VudC1tYW5hZ2VyLnByb2QuKi5kYy5nb3Jpdi5jbyIsImh0dHBzOi8vdHJpcC1wcm9kLnJpdmlhbnNlcnZpY2VzLmNvbSIsImh0dHBzOi8vaWQucml2aWFuc2VydmljZXMuY29tLyIsImh0dHBzOi8vZGF0YS5yaXZpYW5zZXJ2aWNlcy5jb20vIiwiaHR0cHM6Ly9hcHBzLmdvcml2LmNvL2FwaS92cy9ncWwtZ2F0ZXdheSJdLCJzY29wZSI6IioiLCJ1c2VyX2lkIjoidXNlcl9pZCJ9.WsQIlNYTVxupCNJd3ohRbzReeoeqEdwjM9bYJkyTnu4"
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
            headers={
                "Content-Type": "application/json:"
            },
            text='''{
                "error_code": -40,
                "error_desc": "Authentication Error <class 'rcore.rexceptions.RPermissionErrorTokenExpired'>",
                "error_name": "AuthError"
            }'''
        ),
    )
    with pytest.raises(RivianExpiredTokenError):
        async with aiohttp.ClientSession() as session:
            rivian = Rivian("abcd1234", "wxyz9876")

            response = await rivian.get_vehicle_info("vin123", "accessToken", [])
            assert response.status == 401

            await rivian.close()

