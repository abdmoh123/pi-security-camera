"""Service for setting up details for the camera system."""

import re

from pisec_cam.core.models.camera import BaseCamera, camera_name_regex
from pisec_cam.core.models.credential import Credential
from pisec_cam.services.app_data_handler import app_data_handler


def create_credentials_file(
    client_id: str | None = None,
    user_id: int | None = None,
    client_secret: str | None = None,
) -> None:
    """Create the credentials file.

    Args:
        client_id: The client ID, defaults to None
        user_id: The user ID, defaults to None
        client_secret: The client secret, defaults to None
    """
    while user_id is None:
        try:
            user_id = int(input("Enter the user ID: "))
            if user_id < 1:
                user_id = None
        except ValueError:
            print("Entered user ID is not an integer. Try again...")

    while client_id is None:
        try:
            client_id = Credential.verify_client_id(
                input("Paste in the client ID: ")
            )
        except ValueError:
            print("Entered client ID format is incorrect. Try again...")

    while client_secret is None:
        try:
            client_secret = input("Paste in the client secret: ")
        except ValueError:
            print("Entered client secret format is incorrect. Try again...")

    app_data_handler.update_credentials_file(
        Credential(
            client_id=client_id, user_id=user_id, client_secret=client_secret
        )
    )


def create_server_address_file(server_address: str | None = None) -> None:
    """Create the server address file.

    Args:
        server_address: The server address, defaults to None
    """
    pattern = r"^https?://.*"

    while server_address is None:
        server_address = input("Enter the server address: ")
        if "\n" in server_address or re.match(pattern, server_address) is None:
            print("Entered server address format is incorrect. Try again...")
            server_address = None

    app_data_handler.update_server_address_file(server_address)


def create_camera_details_file(camera_name: str | None = None) -> None:
    """Create the camera details file.

    Args:
        camera_name: The camera name, defaults to None
    """
    while camera_name is None:
        camera_name = input("Enter a name for the camera: ")
        if re.match(camera_name_regex, camera_name) is None:
            print("Entered camera name format is incorrect. Try again...")
            camera_name = None

    app_data_handler.update_camera_details_file(BaseCamera(name=camera_name))


def setup_system() -> bool:
    """Set up the system."""
    server_address: str | None = None
    credentials: Credential | None = None
    camera_details: BaseCamera | None = None
    try:
        server_address = app_data_handler.read_server_address()
        credentials = app_data_handler.read_credentials()
        camera_details = app_data_handler.read_camera_details()
    except (FileNotFoundError, ValueError) as e:
        print(e)

    changed: bool = False

    if server_address is None:
        print("Server address file not found. Creating a new one...")
        create_server_address_file(server_address)
        changed = True
    if credentials is None:
        print("Credentials file is missing. Creating a new one...")
        create_credentials_file()
        changed = True
    if camera_details is None:
        print("Camera details file is missing. Creating a new one...")
        create_camera_details_file()
        changed = True

    return changed
