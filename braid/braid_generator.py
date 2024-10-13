"""
Braid generators! Not much
algorithm going on here.
"""

from common import Sign

class BraidGenerator:
    """
    The sigma_i^e that make up
    braid words. i represents the
    0-index of the left strand;
    sign is pos when the left strand
    goes over the right
    """
    def __init__(self, i: int, sign: Sign) -> None:
        self.__i = i
        self.__sign = sign

    def i(self) -> int:
        """Getter

        Returns:
            int: left index of the swapped strands
        """
        return self.__i

    def sign(self) -> Sign:
        """Getter

        Returns:
            Sign: pos if left over right else neg
        """
        return self.__sign
