"""
This module sets up the CanonBraid class, which
is separate from the Braid class. They're represented
in a more mathematical form -- count of
Delta braids and permutations
"""

from __future__ import annotations
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
            self.__perms.append(Permutation(simple_braid.simple_perm()))

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
        s_primes: list[Braid] = []
        u: Braid = Braid(self.n())
        u.append(BraidGenerator(g.i(), True))

        while len(self.__ss) > 0:
            s: Braid = self.__ss.pop()

            if g.pos():
                s.invert_gens()
                s.concat(u)
                (u_prime, s_prime) = s.reverse()
                s_prime.invert_gens()
            else:
                u.invert_gens()
                s.reverse_gens()
                u.concat(s)
                (s_prime, u_prime) = u.reverse()
                s_prime.reverse_gens()
                u_prime.invert_gens()

            u = u_prime
            s_primes = [s_prime] + s_primes

        p = Permutation(u.simple_perm())
        if g.pos():
            if p.is_delta():
                self.__m += 1
                self.__ss = s_primes
            else:
                self.__ss = [u] + s_primes
        else:
            if p.is_identity():
                self.__ss = s_primes
            else:
                self.__m -= 1
                self.__ss = [p.left_divisor().to_simple()] + s_primes

    def __iter__(self) -> ProgressiveCanonBraid:
        return self

    def __next__(self) -> Braid:
        if self.__iter_index  >= len(self.__ss):
            raise StopIteration
        s = self.__ss[self.__iter_index]
        self.__iter_index += 1
        return s
