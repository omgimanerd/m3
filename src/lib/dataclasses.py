"""Utility methods for working with dataclasses"""

from dataclasses import Field, field
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
