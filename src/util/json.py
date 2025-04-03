"""Contains helpers to serialize dataclass fields to JSON"""

from pathlib import PurePath
from typing import Any


def serializer(obj: Any) -> str:
    """Serializer utility to pass as an argument into orjson."""
    if isinstance(obj,  PurePath):
        return str(obj)
    raise TypeError
