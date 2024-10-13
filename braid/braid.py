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
        self.__iter_index: int = -1



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
        self.__gens.extend(second)

    def reverse(self) -> tuple[Braid, Braid]:
        """Puts a braid word into its reversed
        form; returns braid words
        that make it up

        Returns:
            tuple[Braid, Braid]: (x, y) where
            x is all pos, y is all neg, and x * y
            is the original
        """
        for (gen_index, g1) in enumerate(self):
            g2 = self.__gens[gen_index+1]
            if not g1.pos() and g2.pos():
                i = g1.i()
                j = g2.i()

                prefix = self.__gens[:gen_index]
                middle = Braid.reverse_helper(i, j)
                suffix = self.__gens[gen_index + 2:]

                self.__gens = prefix + middle + suffix
                self.reverse()

        leading_pos = Braid(self.n())
        ending_neg = Braid(self.n())

        for gen in self:
            if gen.pos():
                leading_pos.append(gen)
            else:
                ending_neg.append(gen)

        return (leading_pos, ending_neg)

    def reverse_gens(self) -> None:
        """Reverses the order of
        generators in the braid word
        """
        self.__gens.reverse()

    def invert_gens(self) -> None:
        """Inverts each of the generators,
        but doesn't change their order
        """
        for i, g in enumerate(self.__gens):
            self.__gens[i] = BraidGenerator(g.i(), not g.pos())

    def invert(self) -> None:
        """Converts into the exact inverse
        of the given braid word
        """
        self.reverse_gens()
        self.invert_gens()

    def simple_perm(self) -> list[int]:
        """Converts to a permutation.
        Raises NotSimpleError if
        this list doesn't represent a permutation

        Raises:
            NotSimpleError: Raised if
            the braid isn't simple

        Returns:
            list[int]: image of the permutation
            if the braid is simple
        """
        perm: list[int] = list(range(self.n()))
        crossings: set[int] = set()
        for g in self:
            if not g.pos():
                raise NotSimpleError()
            over = perm.index(g.i())
            under = perm.index(g.i() + 1)

            key = over * self.n() + under
            if key in crossings:
                raise NotSimpleError()
            crossings.add(key)

            perm[over] = g.i() + 1
            perm[under] = g.i()

        return perm

    @staticmethod
    def reverse_helper(i: int, j: int) -> list[BraidGenerator]:
        """Rewrites sigma_i^{-1} sigma_j
        according to reversing rules

        Args:
            i (int): index of first, inverse
            j (int): index of second, noninverse

        Returns:
            list[BraidGenerator]: new reversed word
            equivalent to the original
        """
        match abs(i - j):
            case 0:
                return []
            case 1:
                return [BraidGenerator(j, True), BraidGenerator(i, True),
                        BraidGenerator(j, False), BraidGenerator(i, False)]
            case _:
                return [BraidGenerator(j, True), BraidGenerator(i, False)]

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

    def __iter__(self) -> Braid:
        self.__iter_index = 0
        return self

    def __next__(self) -> BraidGenerator:
        if self.__iter_index >= len(self.__gens):
            raise StopIteration
        next_gen = self.__gens[self.__iter_index]
        self.__iter_index += 1
        return next_gen

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
class NotSimpleError(Exception):
    """
    Raised whenever a braid was expected
    to be simple but wasn't
    """
