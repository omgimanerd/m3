"""Class for multikey dicts."""

from typing import Hashable, Union


class MultiKeyDict:
    """Utility class for supporting data with multiple lookup keys.

    The key set is defined as a tuple, but data can be looked up with any 
    individual key in the key set or the complete key set.

    Requires prior knowledge of total number of keys and each data entry must 
    be added to the multikey dict with all the keys present. The total number of 
    keys present when inserting data is enforced by the class. 
    It may be useful to stick to consistent ordering of these keys for all data 
    entries, but the ordering must be enforced by the caller of this class.
    """

    def __init__(self, num_of_keys: int):
        """Initializes multikey dict to expect specified number of keys."""
        self.num_of_keys = num_of_keys
        self.keys = {}
        self.data = {}

    def _is_existing_key(self, key: Hashable) -> bool:
        """Returns if a given key is a valid individual key for the dict."""
        return key in self.keys

    def _validate_key_set(self, keys: tuple) -> bool:
        """Validates that a given key set contains the right number of keys, 
        each key is a valid key for the dict, and the key set is linked to data.

        Returns true if the key set is valid, raises error otherwise.
        """
        if len(keys) != self.num_of_keys:
            raise ValueError(
                f'Expected {self.num_of_keys} keys, got {len(keys)}')
        for key_ in keys:
            if not self._is_existing_key(key_):
                raise ValueError(f'Given key {key_} was not found')
        if self.data.get(keys) is None:
            raise ValueError(f'Given key set {keys} not associated with data')
        return True

    def add(self, keys: tuple, data: any):
        """Given a key set and data, adds the entry to the dict. The key set 
        must contain the number of expected keys.

        Args:
            keys: the key set to use to index the data
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
        """Removes a given key set from the multikey dict if it is valid.

        Args:
            keys: the key set to remove from dict

        Returns:
            The removed key set as a tuple, else raise an error.
        """
        self._validate_key_set(keys)
        for key_ in keys:
            self.keys.pop(key_)
        return self.data.pop(keys)

    def get(self, key: Union[tuple, Hashable]) -> any:
        """Given a key or key set, gets the associated data.

        Args:
            key: the key or key set to look up the data with

        Returns:
            The data associated with the given key or an error.
        """
        if isinstance(key, tuple):
            self._validate_key_set(key)
            return self.data[key]
        if isinstance(key, Hashable):
            if self._is_existing_key(key):
                return self.data[self.keys[key]]
        raise ValueError(
            f'Expected tuple or Hashable, unexpected key type: {type(key)}')

    def len(self) -> int:
        """Returns the number of key sets mapped to data.

        Note that each key set is counted as one despite potentially containing 
        multiple keys.
        """
        return len(self.data)

    def get_keysets(self):
        """Returns all key sets in the dict."""
        return self.keys.values()

    def get_keys(self):
        """Returns all individual keys."""
        return self.keys.keys()
