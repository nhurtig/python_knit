"""
Permutations are used in
braid canonicalization to represent
simple (aka positive permutation)
braids
"""

from braid.braid import Braid


class Permutation:
    """
    A permutation is a bijective
    map [n] -> [n]
    """

    def __init__(self, simple: Braid) -> None:
        self.__perm = Permutation.make_perm(simple)

    @staticmethod
    def make_perm(b: Braid) -> list[int]:
        """Raises NotAPermutationError if
        this list doesn't represent a permutation

        Args:
            perm (Braid): Braid, hopefully simple,
            to be converted

        Raises:
            NotSimpleError: Raised if
            the braid isn't simple
        """

        # Keep track of
        # who has crossed who; raise
        # exception if there's a double
        # cross. Raise exception if
        # a gen is negative

        perm: list[int] = list(range(b.n()))
        crossings: set[int] = set()
        for g in b:
            if not g.sign.is_pos():
                raise NotSimpleError()
            over = perm.index(g.i())
            under = perm.index(g.i() + 1)

            key = over * b.n() + under
            if key in crossings:
                raise NotSimpleError()
            crossings.add(key)

            perm[over] = g.i() + 1
            perm[under] = g.i()

        return perm

class NotSimpleError(Exception):
    """
    Raised whenever you tried to make a permutation
    out of a list that didn't represent a
    bijection
    """
