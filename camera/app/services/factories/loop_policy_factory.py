"""Factory for selecting the type of loop policy."""

from enum import StrEnum, auto

from app.policies.api_loop_policy import APILoopPolicy
from app.policies.loop_policy import LoopPolicy
from app.policies.offline_loop_policy import OfflineLoopPolicy
from app.services.api.api_service import APIService
from app.surveillance_system import SurveillanceSystem


class LoopPolicyType(StrEnum):
    """Enum for selecting the type of loop policy."""

    API = auto()
    OFFLINE = auto()


def create_loop_policy(
    loop_type: LoopPolicyType,
    camera_system: SurveillanceSystem,
    api_service: APIService | None = None,
) -> LoopPolicy:
    """Factory for selecting the type of loop policy.

    Args:
        loop_type: The type of loop policy to create.
        camera_system: The camera state machine wrapper.
        api_service: The API service.

    Returns:
        The loop policy.
    """
    match loop_type:
        case LoopPolicyType.API:
            if api_service is None:
                raise ValueError("API service is not provided")
            return APILoopPolicy(camera_system, api_service)
        case LoopPolicyType.OFFLINE:
            return OfflineLoopPolicy(camera_system)
