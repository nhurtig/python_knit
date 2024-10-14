"""
Braid generators! Not much
algorithm going on here.
"""

from __future__ import annotations
from common import Sign

class BraidGenerator:
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

    def __eq__(self, other) -> bool:
        if not isinstance(other, BraidGenerator):
            return False
        return self.i() == other.i() and self.pos() == other.pos()
