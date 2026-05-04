"""Model for a user's data."""

from pydantic import BaseModel, EmailStr, Field

# Regex pattern to match the email address format (doesn't check if it's real)
email_regex: str = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}$"


class User(BaseModel):
    """Model for a user's data gained from the server API.

    Attributes:
        id: A user's ID
        email: Email of the user
        is_admin: A flag for whether the user is an admin
    """

    id: int = Field(ge=1)
    email: EmailStr = Field(pattern=email_regex)
    is_admin: bool = Field(default=False)

    class Config:
        """Config subclass of UserResponse."""

        from_attributes: bool = True
