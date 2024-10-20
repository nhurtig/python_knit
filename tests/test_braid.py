"""
Tests for braid word
canonicalization
"""

from braid.braid import Braid
from braid.canon.canon_braid import CanonBraid

EXAMPLE_2008_STRING = "aBabacABABAbbCB"


def test_early_canon() -> None:
    """Ensures the canonicalization of prefixes
    of the 2008 example are correct
    """
    assert str(CanonBraid(Braid.str_to_braid(4, ""))) == ""
    assert str(CanonBraid(Braid.str_to_braid(4, "a"))) == "a"
    assert str(CanonBraid(Braid.str_to_braid(4, "aB"))) == "ABACBAabcbba"
    assert str(CanonBraid(Braid.str_to_braid(4, "aBa"))) == "ABACBAabcbbaa"
    assert str(CanonBraid(Braid.str_to_braid(4, "aBab"))) == "ABACBAabcbbaab"
    assert str(CanonBraid(Braid.str_to_braid(4, "aBaba"))) == "aab"
    assert str(CanonBraid(Braid.str_to_braid(4, "aBabac"))) == "aabc"


def test_2008_example() -> None:
    """Ensures the example from the 2008
    paper has the expected result
    """
    orig_braid = Braid.str_to_braid(4, EXAMPLE_2008_STRING)
    cb = CanonBraid(orig_braid)
    assert str(cb) == "ABACBAABACBAcaabcbbcbaa"
