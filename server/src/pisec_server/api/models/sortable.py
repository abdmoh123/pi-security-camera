"""Sortable class used in request param pydantic models."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, TypeVar, cast, get_args

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema

T = TypeVar("T", bound=Enum)


@dataclass(frozen=True)
class Sortable[T]:
    """Sortable class used in request param pydantic models.

    Attributes:
        field: The field to sort by.
        ascending: Whether to sort in ascending or descending order.
    """

    field: T
    ascending: bool = True

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source: Any,  # pyright: ignore[reportExplicitAny, reportAny]
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Get the core schema for the Sortable class.

        This is used by pydantic when converting the string in a request to a
        Sortable object.

        The format must follow <field_name>:<asc|desc>.

        Args:
            source: The Sortable class.
            handler: The get core schema handler.

        Returns:
            The core schema for the Sortable class to be used by pydantic.

        Raises:
            TypeError: If the Sortable class is not parametrised with an enum
                type, or if the input to be parsed is not a string.
            ValueError: If the Sortable class is not in the correct format.
        """
        args = get_args(source)
        if not args and len(args) != 1 and not isinstance(args[0], type):
            raise TypeError("Sortable must have one parametrised enum type")
        enum_type: type[Enum] = args[0]

        def parse(value: Any) -> "Sortable[T]":  # pyright: ignore[reportAny, reportExplicitAny]
            if isinstance(value, cls):
                return value

            if not isinstance(value, str):
                raise TypeError("Parsed value must be a string")

            split_value = value.strip().split(":")
            if len(split_value) != 2:
                raise ValueError(f"Invalid format: {value}")

            field_name, direction = split_value

            try:
                # Cast was required to get rid of the errors and warnings
                # The type will always be correct though due to the T Enum bound
                field: T = cast(T, enum_type(field_name))
                match direction:
                    case "asc":
                        ascending = True
                    case "desc":
                        ascending = False
                    case _:
                        raise ValueError(f"Invalid direction: {direction}, must be asc or desc")
            except ValueError:
                allowed_types = ", ".join(str(m) for m in enum_type)
                raise ValueError(f"Invalid sortable: {field_name}. Allowed values: {allowed_types}")

            return cls(field, ascending=ascending)

        # Use str schema first so OpenAPI documents it as a string
        return core_schema.chain_schema([core_schema.str_schema(), core_schema.no_info_plain_validator_function(parse)])
