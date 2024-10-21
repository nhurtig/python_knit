"""Tests braid word
canonicalization using an example
from the 2008 paper"""

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


def test_identity_identity() -> None:
    """This catches a real bug that occured when
    an identity ended up being pushed to the root of
    a progressive canon braid, and it recorded the
    identity instead of throwing it away"""
    b = Braid.str_to_braid(2, "aaAA")
    cb = CanonBraid(b)
    assert cb == CanonBraid(Braid(2))


def test_big_reversal() -> None:
    """Tests that a huge reversal doesn't proc
    RecursionError; a previous implementation
    did"""
    lst = (
        "A, b, c, d, e, f, g, h, i, j, k, b, c, d, e, f, g, h, i, j, b, c, "
        "d, e, f, g, h, i, b, c, d, e, f, g, h, b, c, d, e, f, g, b, c, d, "
        "e, f, a, b, c, d, e, a, b, c, d, a, b, c, a, b, a, a, b, a, c, b, "
        "a, d, c, b, a, e, d, c, b, a, f, e, d, c, b, g, f, e, d, c, b, a, "
        "h, g, f, e, d, c, b, a, i, h, g, f, e, d, c, b, a, j, i, h, g, f, "
        "e, d, c, b, a, k, j, i, h, g, f, e, d, c, b, a"
    )
    big_braid = Braid.str_to_braid(12, "".join(lst.split(", ")))
    big_braid.reverse()
