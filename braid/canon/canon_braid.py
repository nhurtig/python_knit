"""
This module sets up the CanonBraid class, which
is separate from the Braid class. They're represented
in a more mathematical form -- count of
Delta braids and permutations
"""

from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from braid.canon.permutation import Permutation


class CanonBraid:
    """Mathematical representation of a
    greedy normal form braid
    """

    def __init__(self, b: Braid):
        intermediate = ProgressiveCanonBraid(b)
        self.__m = intermediate.m()
        self.__n = intermediate.n()
        self.__perms: list[Permutation] = []
        for simple_braid in intermediate:
            self.__perms.append(Permutation(simple_braid))

class ProgressiveCanonBraid:
    """Less mathematical representation;
    keeps simple braids as ordered indices
    """

    def __init__(self, b: Braid) -> None:
        self.__m = 0
        self.__n = b.n()
        self.__ss: list[Braid] = []
        self.__iter_index = -1
        for gen in b:
            self.__push_gen(gen)

    def m(self) -> int:
        """Getter

        Returns:
            int: Leading Delta braid count
            (possibly negative)
        """
        return self.__m

    def n(self) -> int:
        """Getter

        Returns:
            int: Number of strands
        """
        return self.__n

    def __push_gen(self, g: BraidGenerator) -> None:
        #TODO
        raise NotImplementedError()

    def __iter__(self) -> ProgressiveCanonBraid:
        return self

    def __next__(self) -> Braid:
        if self.__iter_index  >= len(self.__ss):
            raise StopIteration
        s = self.__ss[self.__iter_index]
        self.__iter_index += 1
        return s
