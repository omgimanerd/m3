"""Class for multikey dicts."""

from typing import Hashable, Union


class MultiKeyDict:
    """Utility class that handles mapping multiple keys to the same value.

    Values are keyed by a tuple of keys (a multikey), of which any can be used to 
    look up the value. The size of the tuple is user-specified, fixed, and must 
    be known at instantiation time. Adding values to the dict requires a 
    complete tuple of keys, but lookups can be done with any key in the tuple.

    Note that when removing a value, the associated multikey will also be removed.
    Removal or modification of individual keys after a value is added is not 
    supported.

    It may be useful to stick to consistent ordering of these keys for all data 
    entries when adding values, but the ordering must be enforced by the caller 
    of this class.
    """

    def __init__(self, num_of_keys: int):
        """Initializes multikey dict to expect specified number of keys."""
        self.num_of_keys = num_of_keys
        self.keys = {}
        self.data = {}

    def _is_existing_key(self, key: Hashable) -> bool:
        """Returns True if a given key is a valid individual key for the dict, 
        else returns False."""
        return key in self.keys

    def _validate_multikey(self, keys: tuple) -> bool:
        """Validates that a given multikey contains the right number of keys, 
        each key is a valid key for the dict, and the multikey is linked to data.

        Returns true if the multikey is valid, raises error otherwise.
        """
        if len(keys) != self.num_of_keys:
            raise ValueError(
                f'Expected {self.num_of_keys} keys, got {len(keys)}')
        for key_ in keys:
            if not self._is_existing_key(key_):
                raise ValueError(f'Given key {key_} was not found')
        if self.data.get(keys) is None:
            raise ValueError(f'Given multikey {keys} not associated with data')
        return True

    def add(self, keys: tuple, data: any):
        """Given a multikey and data, adds the entry to the dict. The multikey 
        must contain the number of expected keys.

        Args:
            keys: the multikey to use to index the data
            data: the data to add to dict
        """
        if len(keys) != self.num_of_keys:
            raise ValueError(
                f'Expected {self.num_of_keys} keys, got {len(keys)}')
        for key_ in keys:
            if self._is_existing_key(key_):
                raise ValueError(f'Given key {key_} already exists')
        for key_ in keys:
            self.keys[key_] = keys
        self.data[keys] = data

    def remove(self, keys: tuple) -> tuple:
        """Removes a given multikey from the multikey dict if it is valid.

        Args:
            keys: the multikey to remove from dict

        Returns:
            The removed multikey as a tuple, else raise an error.
        """
        self._validate_multikey(keys)
        for key_ in keys:
            self.keys.pop(key_)
        return self.data.pop(keys)

    def get(self, key: Union[tuple, Hashable]) -> any:
        """Given a key or multikey, gets the associated data.

        Args:
            key: the key or multikey to look up the data with

        Returns:
            The data associated with the given key or None.
        """
        if isinstance(key, tuple):
            self._validate_multikey(key)
            return self.data[key]
        if isinstance(key, Hashable):
            if self._is_existing_key(key):
                return self.data[self.keys[key]]
        return None

    def len(self) -> int:
        """Returns the number of multikeys mapped to data.

        Note that each multikey is counted as one despite potentially containing 
        multiple keys.
        """
        return len(self.data)

    def get_multikeys(self):
        """Returns all multikeys in the dict."""
        return self.keys.values()

    def get_keys(self):
        """Returns all individual keys."""
        return self.keys.keys()
