"""Asynchronous Python client for the Rivian API."""

import asyncio
from unittest.mock import patch

import aiohttp
import pytest

from rivian import Rivian

@pytest.mark.asyncio
async def test_json_request(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        "auth.rivianservices.com",
        "/auth/api/v1/token/auth",
        "POST",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "ok"}',
        ),
    )
    async with aiohttp.ClientSession() as session:
        rivian = Rivian("client_id", "client_secret")
        response = await rivian.authenticate("username", "password")
        assert response["status"] == "ok"
        await rivian.close()