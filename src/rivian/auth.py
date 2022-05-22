"""Asynchronous Python client for the Rivian API."""
from __future__ import annotations

class RivianAuth:
    """Provides authentication services for the Rivian API."""


    def __init__(
        self,
    ) -> None:
        """Initalize Object"""

    async def authenticate(
        self,
        username: str | None = None,
        password: str | None = None,
        client_id: str | None = None,
        client_secret: str | None = None,
    ) -> str:
        """Authenticate against the Rivian API"""

    async def validateOTP(
        self,
        otp: str | None = None,
    ) -> str:
        """Validate a OTP for 2FA"""

