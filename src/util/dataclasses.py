"""Utility methods for working with dataclasses"""

from pathlib import Path

from dataclasses_json import config


# pylint: disable-next=invalid-name
def PathField(path: str) -> dict:
    """Returns a dict containing the arguments to dataclasses.field for
    declaring a JSON-serializable pathlib.Path field in a dataclass.

    Args:
        path: The default path to hold in the field.

    Returns:
        A dict containing the arguments to dataclasses.field, to be used as
        field(**PathField(...))
    """
    return {
        'default_factory': Path(path),
        'metadata': config(
            encoder=Path,
            decoder=str
        )
    }
