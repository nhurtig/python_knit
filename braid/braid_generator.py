"""
Braid generators! Not much
algorithm going on here.
"""

from __future__ import annotations
from typing import Sequence
from category.object import PrimitiveObject
from common import Sign
from latex import Latex

class BraidGenerator(Latex):
    """
    The sigma_i^e that make up
    braid words. i represents the
    0-index of the left strand;
    sign is pos when the left strand
    goes over the right
    """
    def __init__(self, i: int, sign: bool) -> None:
        self.__i = i
        self.__sign = Sign(sign)

    def i(self) -> int:
        """Getter

        Returns:
            int: left index of the swapped strands
        """
        return self.__i

    def pos(self) -> bool:
        """Essentially a getter

        Returns:
            bool: True if left over right else False
        """
        return self.__sign.pos()

    @staticmethod
    def from_char(c: str) -> BraidGenerator:
        """Converts an alphabetic character to
        a braid generator. Uppercase are inverse,
        lower are regular. "a" is index 0 and
        "z" is 25.

        Args:
            c (str): input character

        Raises:
            ValueError: when c is not
            alphabetic

        Returns:
            BraidGenerator: representative
            of the input character
        """
        if not c.isalpha():
            raise ValueError()
        i = ord(c.lower()) - ord('a')
        return BraidGenerator(i, c.islower())

    def __repr__(self) -> str:
        return chr(ord('a' if self.pos() else 'A') + self.i())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BraidGenerator):
            return False
        return self.i() == other.i() and self.pos() == other.pos()

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        str_latex = ""

        o_left = context[self.i()]
        (rl, gl, bl) = o_left.color()
        o_right = context[self.i() + 1]
        (rr, gr, br) = o_right.color()

        if self.pos():
            str_latex += f"\\identity{{{x+self.i()+1}}}{{{y}}}{{{-1}}}{{{o_right}}}{{{rr}}}{{{gr}}}{{{br}}}\n"
            str_latex += f"\\lineknit{{{x+self.i()}}}{{{y}}}{{{1}}}{{{o_left}}}{{{1}}}{{{1}}}{{{1}}}{{line width=\\outlineThickness*\\dx, color=white}}\n"
            str_latex += f"\\identity{{{x+self.i()}}}{{{y}}}{{{1}}}{{{o_left}}}{{{rl}}}{{{gl}}}{{{bl}}}\n"
        else:
            str_latex += f"\\identity{{{x+self.i()}}}{{{y}}}{{{1}}}{{{o_left}}}{{{rl}}}{{{gl}}}{{{bl}}}\n"
            str_latex += f"\\lineknit{{{x+self.i()+1}}}{{{y}}}{{{-1}}}{{{o_right}}}{{{1}}}{{{1}}}{{{1}}}{{line width=\\outlineThickness*\\dx, color=white}}\n"
            str_latex += f"\\identity{{{x+self.i()+1}}}{{{y}}}{{{-1}}}{{{o_right}}}{{{rr}}}{{{gr}}}{{{br}}}\n"
        
        for i, o in enumerate(context):
            if i not in [self.i(), self.i() + 1]:
                (r, g, b) = o.color()
                str_latex += f"\\identity{{{x+i}}}{{{y}}}{{{0}}}{{{o}}}{{{r}}}{{{g}}}{{{b}}}\n"

        return str_latex

    def latex_height(self) -> int:
        return 1

    def context_out(self, context: Sequence[PrimitiveObject]) -> Sequence[PrimitiveObject]:
        new_context = list(context) # shallow copy
        o_left = new_context[self.i()]
        new_context[self.i()] = new_context[self.i() + 1]
        new_context[self.i() + 1] = o_left
        return new_context
