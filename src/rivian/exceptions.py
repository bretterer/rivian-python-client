class RivianExpiredTokenError(Exception):
    """Access Token Expired Error"""

class RivianUnauthenticated(Exception):
    """User Token Invalid Error"""

class RivianInvalidCredentials(Exception):
    """Invalid User Credentials - Check Username and Password"""

class RivianInvalidOTP(Exception):
    """User's One Time Password Invalid - Try Again"""

class RivianDataError(Exception):
    """Rivian Server Data Error"""

class RivianTemporarilyLockedError(Exception):
    """Rivian User Temporarily Locked Error"""