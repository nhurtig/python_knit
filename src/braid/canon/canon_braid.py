"""
This module sets up the CanonBraid class, which
is separate from the Braid class. They're represented
in a more mathematical form -- count of
Delta braids and permutations
"""

from __future__ import annotations
from typing import Sequence
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from braid.canon.permutation import Permutation
from category.object import PrimitiveObject
from fig_gen.latex import Latex


class CanonBraid(Latex):
    """Mathematical representation of a
    greedy normal form braid
    """

    def __init__(self, b: Braid):
        intermediate = ProgressiveCanonBraid(b)
        self.__m = intermediate.m()
        self.__n = intermediate.n()
        self.__iter_index = -1
        self.__perms: list[Permutation] = []
        for simple_braid in intermediate:
            self.__perms.append(Permutation(simple_braid.simple_perm()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CanonBraid):
            return False
        return (
            self.n() == other.n()
            and self.m() == other.m()
            and list(self) == list(other)
        )

    def __repr__(self) -> str:
        return f"CanonBraid(n={self.__n}, Delta^({self.__m}, {self.__perms})"

    def __str__(self) -> str:
        out = ""
        delta = Permutation.delta(self.__n)
        for _ in range(abs(self.__m)):
            if self.__m < 0:
                out += str(delta)[::-1].upper()
            else:
                out += str(delta)

        for p in self.__perms:
            out += str(p)

        return out

    def __iter__(self) -> CanonBraid:
        self.__iter_index = 0
        return self

    def __next__(self) -> Permutation:
        if self.__iter_index >= len(self.__perms):
            raise StopIteration
        next_perm = self.__perms[self.__iter_index]
        self.__iter_index += 1
        return next_perm

    def n(self) -> int:
        """Getter

        Returns:
            int: Number of strands
        """
        return self.__n

    def m(self) -> int:
        """Getter

        Returns:
            int: Number of leading positive deltas
            (possibly negative)
        """
        return self.__m

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        str_latex = ""
        delta = Permutation.delta(self.__n)
        for j in range(abs(self.__m)):
            if self.__m < 0:
                str_latex += delta.to_latex_helper(x, y + j, context, True)
            else:
                str_latex += delta.to_latex(x, y + j, context)
            context = delta.context_out(context)
        y += abs(self.__m)

        for p in self.__perms:
            str_latex += p.to_latex(x, y, context)
            y += 1
            context = p.context_out(context)

        return str_latex

    def latex_height(self) -> int:
        return abs(self.__m) + len(self.__perms)

    def context_out(
        self, context: Sequence[PrimitiveObject]
    ) -> Sequence[PrimitiveObject]:
        if abs(self.__m) % 2 == 1:
            context = list(reversed(context))

        for p in self.__perms:
            context = p.context_out(context)

        return context


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
                # P-tile
                # Represent su as
                # u' s' where u' >= s'
                # Let u' = alpha(s u)
                # and that determines
                # s'.
                # alpha( s u )
                # = gcd_L( s u, \Delta_n)
                s.concat(u)
                su_perm = s.simple_perm(ignore=True)
                u_prime = s.head()
                # left-gcd can be calced by guessing a gen to
                # divide both a and b and then iterating w/
                # the quotients sig \ a, sig \ b.
                #
                # 4.8 says grid source (u, v) target (u', v')
                # means v' = u \ v and u' = v \ u
                # SO: append inv sig to the word, reverse,
                # and see if something interesting happens?
                # Success would be v' \neq v and fail
                # is v' == v, I think
                s_prime = (
                    Permutation(u_prime.simple_perm())
                    .right_divisor(su_perm)
                    .to_simple()
                )
            else:
                # C-tile
                # Calculate s' = u / s (left complement)
                # u' = s / u
                # then s' u = u' s = LCM_L(s, u) = LCM_L(u, s)
                # also s', u' are simple
                # also GCD_L(s', t') = 1
                # hence C-tile

                # NOTE: according to book page 108, I am
                # doing right complement, not left here.
                # oops? We'll see how this shakes out
                # if len(list(s)) == 3 and len(list(u)) == 1:
                #     print("HI!")

                # below lines worked for first 6
                # u.invert()
                # u.concat(s)
                # (s_prime, u_prime) = u.reverse()
                # s_prime.reverse_gens()
                # u_prime.invert_gens()

                s.invert_gens()
                u.reverse_gens()
                s.concat(u)
                (u_prime, s_prime) = s.reverse()
                u_prime.reverse_gens()
                s_prime.invert_gens()

            u = u_prime
            if len(list(s_prime)) > 0:
                s_primes = [s_prime] + s_primes

        p = Permutation(u.simple_perm())
        if g.pos():
            if p.is_delta():
                self.__m += 1
                self.__ss = s_primes
            else:
                if not p.is_identity():
                    self.__ss = [u] + s_primes
        else:
            if p.is_identity():
                self.__ss = s_primes
            else:
                self.__m -= 1
                p_left_div = p.left_divisor()
                if not p_left_div.is_identity():
                    self.__ss = [p_left_div.to_simple()] + s_primes

    def __iter__(self) -> ProgressiveCanonBraid:
        self.__iter_index = 0
        return self

    def __next__(self) -> Braid:
        if self.__iter_index >= len(self.__ss):
            raise StopIteration
        s = self.__ss[self.__iter_index]
        self.__iter_index += 1
        return s

    def __repr__(self) -> str:
        return f"PCanonBraid(n={self.__n}, Delta^({self.__m}, {self.__ss})"
