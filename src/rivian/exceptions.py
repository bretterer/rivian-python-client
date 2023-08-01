"""Rivian exceptions."""


class RivianApiException(Exception):
    """Base Rivian API exception."""


class RivianExpiredTokenError(RivianApiException):
    """Access Token Expired Error"""


class RivianUnauthenticated(RivianApiException):
    """User Token Invalid Error"""


class RivianInvalidCredentials(RivianApiException):
    """Invalid User Credentials - Check Username and Password"""


class RivianInvalidOTP(RivianApiException):
    """User's One Time Password Invalid - Try Again"""


class RivianDataError(RivianApiException):
    """Rivian Server Data Error"""


class RivianTemporarilyLockedError(RivianApiException):
    """Rivian User Temporarily Locked Error"""


class RivianApiRateLimitError(RivianApiException):
    """Rivian API is being rate limited."""


class RivianPhoneLimitReachedError(RivianApiException):
    """Rivian phone limit has been reached."""


class RivianBadRequestError(RivianApiException):
    """Rivian API bad request."""
