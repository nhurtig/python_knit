"""
Permutations are used in
braid canonicalization to represent
simple (aka positive permutation)
braids
"""

from __future__ import annotations
from typing import Sequence
from braid.braid import Braid, StrandMismatchException
from braid.braid_generator import BraidGenerator
from category.object import Carrier, PrimitiveObject
from latex import Latex

class Permutation(Latex):
    """
    A permutation is a bijective
    map [n] -> [n]
    """

    def __init__(self, perm: list[int]) -> None:
        self.__perm: list[int] = perm

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        return self.to_latex_helper(x, y, context)

    def to_latex_helper(self, x: int, y: int, context: Sequence[PrimitiveObject], inv: bool=False) -> str:
        # draw white of lowest strand
        # draw black of lowest strand
        # repeat for all strands

        # lowest strand is the one that
        # ends up on the left
        str_latex = f"\\begin{{pgfonlayer}}{{swaps}}\n"
        lowest_to_highest = list(range(self.n()))
        if inv:
            lowest_to_highest = list(reversed(lowest_to_highest))
        for i in lowest_to_highest:
            strand_start = self.__perm.index(i)
            o = context[strand_start]
            (r, g, b) = o.color()
            str_latex += f"\\lineknit{{{x+strand_start}}}{{{y}}}{{{i - strand_start}}}{{{o}}}{{{r}}}{{{g}}}{{{b}}}{{line width=\\outlineThickness*\\dx, color=white}}\n"
            str_latex += f"\\identity{{{x+strand_start}}}{{{y}}}{{{i - strand_start}}}{{{o}}}{{{r}}}{{{g}}}{{{b}}}\n"
        str_latex += f"\\end{{pgfonlayer}}\n"

        return str_latex

    def latex_height(self) -> int:
        return 1

    def context_out(self, context: Sequence[PrimitiveObject]) -> list[PrimitiveObject]:
        out: list[PrimitiveObject] = [Carrier(0)] * self.n()
        for i in range(self.n()):
            out[self.__perm[i]] = context[i]
        return out

    def n(self) -> int:
        """Computes number of strands
        in the permutation braid

        Returns:
            int: length of the permutation
        """
        return len(self.__perm)

    def is_delta(self) -> bool:
        """Computes whether this braid
        is the Delta braid

        Returns:
            bool: whether this permutation
            is the reverse permutation
        """
        return self.__perm == list(range(self.n() - 1, -1, -1))

    def is_identity(self) -> bool:
        """Computes whether this braid
        is the identity braid

        Returns:
            bool: whether this permutation
            is the identity permutation
        """
        return self.__perm == list(range(0, self.n()))

    def left_divisor(self) -> Permutation:
        """Computes and returns the left
        divisor of self.

        Returns:
            Permutation: x such
            that x * self = Delta
        """
        new_perm = []
        for i in range(self.n()):
            end = self.n() - i - 1
            middle = self.__perm.index(end)
            new_perm.append(middle)

        return Permutation(new_perm)

    def right_divisor(self, goal: list[int]) -> Permutation:
        """Computes and returns the right
        divisor of self in goal.

        Args:
            goal (Permutation): Permutation
            meant to be reached by self and
            the return value

        Returns:
            Permutation: x such
            that self * x = goal
        """
        if self.n() != len(goal):
            raise StrandMismatchException()

        new_perm = [-1] * self.n()
        for i in range(self.n()):
            # strand name sent to
            # new perm's index i
            strand_id = self.__perm.index(i)
            # goal index
            end = goal[strand_id]
            # I want to send that strand
            # name to that index
            new_perm[i] = end

        return Permutation(new_perm)

    def to_simple(self) -> Braid:
        """Makes a simple braid
        from the permutation

        Returns:
            Braid: Unique simple braid
            that permutes strands
            like the input permutation
        """
        b = Braid(self.n())
        perm = self.__perm.copy()
        while len(perm) > 0:
            rightmost = perm.index(len(perm) - 1)
            for i in range(rightmost, len(perm) - 1):
                b.append(BraidGenerator(i, True))
            # update perm
            perm.pop(rightmost)
        return b

    def __repr__(self) -> str:
        return f"{self.__perm}"
