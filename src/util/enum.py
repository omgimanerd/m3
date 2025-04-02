"""Enums used by this codebase."""

from enum import Enum

from dataclasses_json import config


class Platform(Enum):
    """CurseForge or Modrinth, we only support exporting packs to these two
    platforms."""
    CURSEFORGE = 'curseforge'
    MODRINTH = 'modrinth'


# pylint: disable-next=invalid-name
def PlatformField() -> dict:
    """Returns a dict containing the arguments to dataclasses.field for
    declaring a JSON-serializable Platform enum field in a dataclass.
    """
    return {
        'metadata': config(
            encoder=Platform,
            decoder=Platform.__getitem__
        )
    }
