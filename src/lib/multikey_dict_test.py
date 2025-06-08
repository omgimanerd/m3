"""Unit testing for multikey dict"""

import pytest

from src.lib.multikey_dict import MultiKeyDict


def test_multikey_dict_basic():
    """Basic add, remove, lookup functionality for multikey dict."""
    m = MultiKeyDict(3)
    assert len(m) == 0

    # Adding entries
    m.add((1, 2, 3), 'a')
    m.add((4, 5, 6), 'b')
    assert len(m) == 2
    assert m.get_multikeys() == {(1, 2, 3), (4, 5, 6)}
    assert m.get_keys() == {1, 2, 3, 4, 5, 6}
    assert list(m.get_values()) == ['a', 'b']

    # Key existence
    for k in [1, 2, 3, 4, 5, 6]:
        assert m.is_existing_key(k)
    assert not m.is_existing_key(10)
    assert m.is_existing_multikey((1, 2, 3))
    assert m.is_existing_multikey((4, 5, 6))
    assert not m.is_existing_multikey((7, 8, 9))
    assert not m.is_existing_multikey((1, 8, 9))

    # Preexisting key
    with pytest.raises(ValueError):
        m.add((1, 6, 8), 'a')
    with pytest.raises(ValueError):
        m.add((3, 4, 5), 'a')

    # Lookups
    assert m.get(1) == 'a'
    assert m.get(2) == 'a'
    assert m.get(3) == 'a'
    assert m.get(4) == 'b'
    assert m.get(5) == 'b'
    assert m.get(6) == 'b'

    # Removal
    assert m.remove((1, 2, 3)) == 'a'
    assert len(m) == 1
    assert m.get_multikeys() == {(4, 5, 6)}
    assert m.get_keys() == {4, 5, 6}
    assert list(m.get_values()) == ['b']
