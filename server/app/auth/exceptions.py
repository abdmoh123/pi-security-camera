"""Custom exceptions for authentication and authorization."""


class TokenEncodingError(Exception):
    """Exception raised when there is an error encoding the access token."""

    pass


class TokenDecodingError(Exception):
    """Exception raised when there is an error decoding the access token."""

    pass


class TokenExpiredError(Exception):
    """Exception raised when the access token has expired."""

    pass


class PermissionDeniedError(Exception):
    """Exception raised when the user does not have the required permissions."""

    pass
