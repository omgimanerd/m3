"""Utility methods for working with dataclasses"""

from dataclasses import Field, field, fields, is_dataclass
from pathlib import Path, PurePath


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


def get_field_names(dataclass) -> list[str]:
    """Returns the top-level field names for a given dataclass as a list of 
    strings.

    Args:
        dataclass: The dataclass class object to get the field names for.

    Returns:
        list of field names as strings
    """
    if not is_dataclass(dataclass):
        raise ValueError(f'{dataclass.__class__.__name__} is not a dataclass')
    return [field.name for field in fields(dataclass)]
