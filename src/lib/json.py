"""Contains helpers to serialize dataclass fields to JSON"""

from pathlib import PurePath
from typing import Any

import orjson


def dataclass_json(cls):
    """Custom decorator for dataclasses that defines a json() method to
    serialize the class to JSON using orjson and a custom serialization function
    for data types without default serialization behavior."""

    def json(self) -> str:
        """Class method that will be added to the decorated class that defers
        serialization logic to orjson.dumps."""
        return orjson.dumps(self, default=serializer,
                            option=orjson.OPT_INDENT_2).decode('utf-8')
    cls.json = json
    return cls


def serializer(obj: Any) -> str:
    """Serializer utility to pass as an argument into orjson."""
    if isinstance(obj,  PurePath):
        return str(obj)
    raise TypeError
