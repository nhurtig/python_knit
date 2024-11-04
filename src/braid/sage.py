"""For interacting with sagemath"""

from typing import List, Tuple

# pylint: disable=no-name-in-module
from sage.all import BraidGroup  # type: ignore


def canonicalize_braid(n: int, braid: List[int]) -> List[Tuple[str, int]]:
    """Calls sagemath to canonicalize a braid word

    Args:
        n (int): Number of strands
        braid (List[int]): List of generators, 1-indexed, negative to represent inverses

    Returns:
        List[Tuple[str, int]]: List of syllables in the braid word
    """
    if n < 2:
        return []
    normal_form = BraidGroup(n)(braid).left_normal_form()
    return sum(
        [[(str(g), int(p)) for (g, p) in s.syllables()] for s in normal_form],
        [],
    )
