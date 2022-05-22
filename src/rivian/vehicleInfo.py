"""Asynchronous Python client for the Rivian API."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import Rivian

class RivianVehicleInfo:
    """Provides vehicle info of Rivian."""

    def __init__(
        self,
        rivian: Rivian
    ) -> None:
        """Initialize object.
        Args:
            rivian: Rivian instance
        """
        self._rivian = rivian

    async def getVehicleInfo(
        self,
    ) -> None: #TODO: Update return type to correct object
        """Get the vehicle information stats"""

