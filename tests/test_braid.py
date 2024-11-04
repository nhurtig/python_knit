"""Tests braid word
canonicalization using an example
from the 2008 paper"""

from braid.braid import Braid

EXAMPLE_2008_STRING = "aBabacABABAbbCB"


def test_early_canon() -> None:
    """Ensures the canonicalization of prefixes
    of the 2008 example are correct
    """
    assert str(Braid.str_to_braid(4, "").canon()) == ""
    assert str(Braid.str_to_braid(4, "a").canon()) == "a"
    assert str(Braid.str_to_braid(4, "aB").canon()) == "ABACBAabcbba"
    assert str(Braid.str_to_braid(4, "aBa").canon()) == "ABACBAabcbbaa"
    assert str(Braid.str_to_braid(4, "aBab").canon()) == "ABACBAabcbbaab"
    assert str(Braid.str_to_braid(4, "aBaba").canon()) == "aab"
    assert str(Braid.str_to_braid(4, "aBabac").canon()) == "aabc"


def test_2008_example() -> None:
    """Ensures the example from the 2008
    paper has the expected result
    """
    orig_braid = Braid.str_to_braid(4, EXAMPLE_2008_STRING)
    cb = orig_braid.canon()
    # assert str(cb) == "ABACBAABACBAcaabcbbcbaa" # original
    assert str(cb) == "ABACBAABACBAacabcbbcbaa"  # sagemath is slightly different?


def test_identity_identity() -> None:
    """This catches a real bug that occured when
    an identity ended up being pushed to the root of
    a progressive canon braid, and it recorded the
    identity instead of throwing it away"""
    b = Braid.str_to_braid(2, "aaAA")
    cb = b.canon()
    assert cb == Braid(2).canon()
