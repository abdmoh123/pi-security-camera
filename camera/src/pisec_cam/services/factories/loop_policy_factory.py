"""Factory for selecting the type of loop policy."""

from httpx import HTTPStatusError

from pisec_cam.core.api.api_service_context import APIServiceContext
from pisec_cam.core.models.camera import CameraCreate
from pisec_cam.core.models.credential import Credential
from pisec_cam.core.types.loop_policy_type import LoopPolicyType
from pisec_cam.policies.api_loop_policy import APILoopPolicy
from pisec_cam.policies.loop_policy import LoopPolicy
from pisec_cam.policies.offline_loop_policy import OfflineLoopPolicy
from pisec_cam.services.api.api_service import APIService
from pisec_cam.services.api.auth import OAuth2Authenticator
from pisec_cam.services.app_data_handler import app_data_handler
from pisec_cam.surveillance_system import SurveillanceSystem
from pisec_cam.utils import get_mac_address


def create_loop_policy(
    loop_type: LoopPolicyType,
    camera_system: SurveillanceSystem,
) -> LoopPolicy:
    """Factory for selecting the type of loop policy.

    Args:
        loop_type: The type of loop policy to create.
        camera_system: The camera state machine wrapper.

    Returns:
        The loop policy.
    """
    match loop_type:
        case LoopPolicyType.API:
            api_routes_root: str | None = None
            credential: Credential | None = None
            authenticator: OAuth2Authenticator | None = None
            try:
                api_server_host = app_data_handler.read_server_address()
                api_routes_root = f"{api_server_host}/api/v0"
                credential = app_data_handler.read_credentials()
                authenticator = OAuth2Authenticator(
                    f"{api_routes_root}/auth/camera_token", credential
                )
            except FileNotFoundError as e:
                print("Warning: Videos won't be uploaded to a remote server.")
                print(e)

            if (
                api_routes_root is None
                or credential is None
                or authenticator is None
            ):
                return OfflineLoopPolicy(camera_system)

            api_context = APIServiceContext(api_routes_root, authenticator)
            with APIService(api_context) as api_service:
                is_reachable = api_service.can_connect()
                is_registered = credential.camera_id is not None
                if is_reachable and not is_registered:
                    try:
                        camera_input_data = (
                            app_data_handler.read_camera_details()
                        )
                        camera_details = CameraCreate(
                            name=camera_input_data.name,
                            mac_address=get_mac_address(),
                        )
                        api_service.register_camera(camera_details)
                        app_data_handler.update_credentials_file(
                            api_service.context.authenticator.credential
                        )
                        is_registered = True
                    except FileNotFoundError as e:
                        # TODO: If file failed to update after registering,
                        #       unregister the camera
                        print(f"Failed to read/write data: {e}")
                    except HTTPStatusError as e:
                        print(f"Failed to register camera: {e}")

                return (
                    APILoopPolicy(camera_system, api_context)
                    if is_reachable and is_registered
                    else OfflineLoopPolicy(camera_system)
                )
        case LoopPolicyType.OFFLINE:
            return OfflineLoopPolicy(camera_system)
