"""Asynchronous Python client for the Rivian API."""
from __future__ import annotations
import asyncio
import json

from typing import Any, Mapping

from .vehicleInfo import RivianVehicleInfo

class Rivian:
    """Main class for handling connections with the Rivian API."""
    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> None:
        """Initialize connection with the Rivian API.
        Class constructor for setting up an Rivian object to
        communicate with the Rivian API instance.
        Args:
            username: Username for your Rivian Account.
            password: Password for your Rivian Account.
            client_id: The Client ID for the Rivian API.
            client_secret: The Client secret for the Rivian API.
        """
        self._auth_url = "https://auth.rivianservices.com"
        self._base_url = "https://rivian.com"

        self.vehicle_info = RivianVehicleInfo(self)

    async def request(
        self,
        uri: str,
        method: str = "GET",
        data: Any | None = None,
        json_data: dict | None = None,
        params: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        """Handle a request to the Rivian API."""
