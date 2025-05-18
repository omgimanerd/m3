"""Utility methods for working with dataclasses"""

from dataclasses import Field, field, fields, is_dataclass
from pathlib import Path, PurePath
from typing import Any

import orjson


def dataclass_json(cls):
    """Custom decorator for dataclasses that defines a json() method to
    serialize the class to JSON using orjson and a custom serialization function
    for data types without default serialization behavior.

    Note that we are NOT using the dataclass_json package, this just uses the
    same namespace.
    """

    def json(self) -> str:
        """Class method that will be added to the decorated class that defers
        serialization logic to orjson.dumps."""
        return orjson.dumps(self, default=_serializer,
                            option=orjson.OPT_INDENT_2).decode('utf-8')
    cls.json = json
    return cls


def _serializer(obj: Any) -> str:
    """Serializer utility to pass as an argument into orjson."""
    if isinstance(obj,  PurePath):
        return str(obj)
    raise TypeError


# pylint: disable-next=invalid-name
def PathField(path: str | Path) -> Field:
    """Returns the dataclasses.Field object to assign the default value of
    a dataclass member of type pathlib.Path

    Args:
        path: The default path to hold in the field.

    Returns:
        the field object
    """
    # pylint: disable-next=invalid-field-call
    return field(
        default_factory=lambda: path if isinstance(
            path, PurePath) else Path(path)
    )


def get_field_names(dataclass_) -> list[str]:
    """Returns the top-level field names for a given dataclass as a list of
    strings.

    Args:
        dataclass: The dataclass class object to get the field names for.

    Returns:
        list of field names as strings
    """
    if not is_dataclass(dataclass_):
        raise ValueError(f"{dataclass_.__class__.__name__} is not a dataclass")
    return [field.name for field in fields(dataclass_)]
