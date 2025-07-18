"""Class for multikey dicts."""

from collections.abc import Hashable
from typing import Self, Tuple


class MultiKeyDict:
    """Utility class that handles mapping multiple keys to the same value.

    Values are keyed by a tuple of keys (a multikey), of which any can be used
    to look up the value. The size of the tuple is user-specified, fixed, and
    must be known at instantiation time. Adding values to the dict requires a
    complete tuple of keys, but lookups can be done with any key in the tuple.

    Note that when removing a value, the associated multikey will also be
    removed. Removal or modification of individual keys after a value is added
    is not supported.

    It may be useful to stick to consistent ordering of these keys for all data
    entries when adding values, but the ordering must be enforced by the caller
    of this class.
    """

    def __init__(self, num_of_keys: int):
        """Initializes multikey dict to expect specified number of keys."""
        self.num_of_keys = num_of_keys
        self.keys_to_multikeys = {}
        self.data = {}

    def __eq__(self, value):
        """If the given value is a MultiKeyDict instance, compare it to self and
        return True if the keys and data stored in the dicts are equal. Return
        False otherwise."""
        if not isinstance(value, MultiKeyDict):
            return False
        if len(self) != len(value):
            return False
        if self.num_of_keys != value.num_of_keys:
            return False
        if self.keys_to_multikeys != value.keys_to_multikeys:
            return False
        return True

    def _validate_multikey(self, multikey: tuple):
        """Validates that a given multikey contains the right number of keys.

        Returns true if the multikey is valid, raises error otherwise.
        """
        if len(multikey) != self.num_of_keys:
            raise ValueError(
                f'Expected {self.num_of_keys} keys, got {len(multikey)}')

    def is_existing_key(self, key: Hashable) -> bool:
        """Returns True if the given key is an existing key in the
        keys_to_multikey map."""
        return key in self.keys_to_multikeys

    def is_existing_multikey(self, key: tuple) -> bool:
        """Returns True if a given multikey is an existing multikey for the
        dict."""
        return key in self.data

    def add(self, multikey: tuple, data: any):
        """Given a multikey and data, adds the data to the dict. The multikey
        must contain the number of expected keys.

        Args:
            multikey: the multikey to use to index the data
            data: the data to add to dict
        """
        self._validate_multikey(multikey)
        for key_ in multikey:
            if self.is_existing_key(key_):
                raise ValueError(f'Given key {key_} already exists')
            self.keys_to_multikeys[key_] = multikey
        self.data[multikey] = data

    def remove(self, multikey: tuple) -> tuple:
        """Removes a given multikey from the multikey dict if it is valid.

        Args:
            multikey: the multikey to remove from dict

        Returns:
            The removed data entry, else raise an error.
        """
        self._validate_multikey(multikey)
        if not self.is_existing_multikey(multikey):
            raise KeyError(f'Given multikey {multikey} does not exist')
        for key_ in multikey:
            self.keys_to_multikeys.pop(key_)
        return self.data.pop(multikey)

    def get(self, key: Hashable) -> any:
        """Given a key that is part of an existing multikey, gets the associated
         data.

        Args:
            key: the key to look up the data with

        Returns:
            The data associated with the given key or None.
        """
        return self.data.get(self.keys_to_multikeys.get(key, None), None)

    def get_by_multikey(self, key: Tuple) -> any:
        """Given a valid multikey, gets the associated data.

        Args:
            key: the multikey to look up the data with

        Returns:
            The data associated with the given multikey or None.
        """
        return self.data.get(key, None)

    def __len__(self):
        """Returns the number of data entries."""
        return len(self.data)

    def get_multikeys(self):
        """Returns all multikeys in the dict."""
        return self.data.keys()

    def get_keys(self):
        """Returns all individual keys."""
        return self.keys_to_multikeys.keys()

    def get_values(self):
        """Returns all values in the multikey dict."""
        return self.data.values()

    def get_multikey_difference(self, multikey_dict: Self):
        """Returns the set difference of self's multikeys and the given multikey
        dict's multikeys.
        """
        base_dict_set = set(self.get_multikeys())
        comparison_dict_set = set(multikey_dict.get_multikeys())
        return base_dict_set.difference(comparison_dict_set)
