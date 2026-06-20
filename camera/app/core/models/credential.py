"""Model for a camera credential."""

from pydantic import BaseModel, Field, field_validator


class Credential(BaseModel):
    """Model for a camera's credential.

    Used to authenticate with the server's API.

    Attributes:
        client_id: The client ID
        user_id: The user/owner's ID
        client_secret: The client secret
    """

    client_id: str
    user_id: int = Field(ge=1)
    camera_id: int | None = None
    client_secret: str

    @classmethod
    def _split_client_id(cls, client_id: str) -> list[str]:
        return list(filter(lambda x: x != "", client_id.split(":")))

    @field_validator("client_id", mode="after")
    @classmethod
    def _verify_client_id(cls, value: str) -> str:
        """Client ID should follow format <user_name>:<bunch-of-chars>.

        Args:
            value: The client ID

        Returns:
            The client ID if the format is correct

        Raises:
            ValueError: If the client ID is not in the correct format
        """
        if len(Credential._split_client_id(value)) != 2:
            raise ValueError("Client ID is not in the correct format")
        return value

    def get_user_name_quick(self) -> str:
        """Returns a name linked to this credential.

        The client ID contains a user name in it, so this is a quick way to get
        some form of name. This is not guaranteed to be unique, so it is
        preferred to call the server's API instead for a more accurate username.

        Returns:
            The user name
        """
        return Credential._split_client_id(self.client_id)[0]
