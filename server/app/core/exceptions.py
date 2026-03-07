"""Custom exceptions for the server."""


class RecordNotFoundError(Exception):
    """Exception raised when a record is not found."""

    pass


class RecordAlreadyExistsError(Exception):
    """Exception raised when a record already exists."""

    pass


class InvalidDataError(Exception):
    """Exception raised when invalid data is provided."""

    pass
