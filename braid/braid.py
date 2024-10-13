"""
This module sets up the Braid class
and canonicalization of braids
"""

from __future__ import annotations
from braid_generator import BraidGenerator

class Braid:
    """
    Represents a word in the braid
    group using a list of generators.

    Keeps track of how many strands
    it has and complains loudly if
    a generator doesn't match up.
    """
    def __init__(self, n: int) -> None:
        self.__n = n
        self.__gens: list[BraidGenerator] = []

    # def set_gens(self, gens: list[BraidGenerator]) -> None:
    #     """Sets the generators of this braid word; expects
    #     braid word to be empty to start.

    #     Args:
    #         gens (list[BraidGenerator]): new generators

    #     Raises:
    #         WordNotEmptyException: if the word is not empty
    #             to begin with
    #     """
    #     if self.__gens != []:
    #         raise WordNotEmptyException()
    #     self.__gens = gens

    def n(self) -> int:
        """Simple get function

        Returns:
            int: number of strands of the braid word
        """
        return self.__n

    def __check_compatible(self, other: Braid) -> None:
        """Raises an exception when the braids can't
            be concatenated; otherwise does nothing

        Args:
            other (Braid): Braid to check compatibility with

        Raises:
            StrandMismatchException: when braids can't be
                concatenated
        """
        if self.n() != other.n():
            raise StrandMismatchException()

    def concat(self, second: Braid) -> None:
        """Appends one braid to the other,
        mutating in place

        Args:
            next (Braid): the second braid to be added

        Raises:
            StrandMismatchException: when the
                braids don't line up in their n
        """
        self.__check_compatible(second)
        # pylint: disable=protected-access
        self.__gens.extend(second.__gens)

    def __check_gen_valid(self, gen: BraidGenerator) -> None:
        """Raises an exception when the gen can't go in
            this word; otherwise does nothing

        Args:
            gen (BraidGenerator): candidate to be added

        Raises:
            GeneratorOutOfBoundsException: when gen can't
                be added
        """
        if gen.i() < 0 or gen.i() > self.n() - 2:
            raise GeneratorOutOfBoundsException()


    def append(self, after: BraidGenerator) -> None:
        """Puts a generator at the end of a word

        Args:
            after (BraidGenerator): gen to be added

        Raises:
            GeneratorOutOfBoundsException: when gen can't
                be added
        """
        self.__check_gen_valid(after)

        self.__gens.append(after)

    def prepend(self, before: BraidGenerator) -> None:
        """Puts a generator at the start of a word

        Args:
            before (BraidGenerator): gen to be added

        Raises:
            GeneratorOutOfBoundsException: when gen can't
                be added
        """
        self.__check_gen_valid(before)

        self.__gens = [before] + self.__gens

class StrandMismatchException(Exception):
    """
    Raised whenever you try to concatenate
    two things together that shouldn't go
    together
    """

class GeneratorOutOfBoundsException(Exception):
    """
    Raised when a generator is attempted to be
    added to a braid word where the generator
    doesn't fit
    """

class WordNotEmptyException(Exception):
    """
    Raised when a braid word was supposed
    to be empty but wasn't (setting a
    word's generators)
    """
