"""
Tests for braid word
canonicalization
"""

from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from braid.canon.canon_braid import CanonBraid

EXAMPLE_2008_STRING = "aBabacABABAbbCB"

def str_to_braid(n: int, s: str) -> Braid:
    """Constructs a braid word
    from the string

    Args:
        n (int): Number of strands
        s (str): Alphabetical string representing
        characters

    Returns:
        Braid: braid word on
        n strands described
        by the string
    """
    b = Braid(n)
    gens = [BraidGenerator.from_char(c) for c in s]
    for g in gens:
        b.append(g)
    return b

def test_empty_canon():
    """Ensures the canonicalization of
    the empty word is the empty word
    """
    assert CanonBraid(str_to_braid(4, "")) == None

def test_early_canon():
    """Ensures the canonicalization of prefixes
    of the 2008 example are correct
    """
    # assert CanonBraid(str_to_braid(4, "a")) is None
    assert CanonBraid(str_to_braid(4, "aB")) is None
    # assert CanonBraid(str_to_braid(4, "aBa")) is None
    # assert CanonBraid(str_to_braid(4, "aBab")) is None
    # assert CanonBraid(str_to_braid(4, "aBaba")) is None
    # assert CanonBraid(str_to_braid(4, "aBabac")) is None

def test_2008_example():
    """Ensures the example from the 2008
    paper has the expected result
    """
    assert CanonBraid(str_to_braid(4, EXAMPLE_2008_STRING)) == None
