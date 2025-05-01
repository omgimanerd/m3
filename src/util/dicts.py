"""Utility file with dict manipulation functions."""
from collections.abc import Callable


def reindex(dict_of_dataclasses, f: Callable):
    """Reindexes a given dict of objects on a new key in the objects.

    To work as intended, note that the new key to reindex on must:
        - Exist as a field on all dataclass objects in the dict
        - Be unique across all dataclass objects in the dict
        - Be hashable

    Args:
        dict_of_dataclasses: a dict of dataclass objects
        f: a function that returns the dataclass field to reindex on
    """
    return {
        f(obj): obj for _, obj in dict_of_dataclasses.items()
    }
