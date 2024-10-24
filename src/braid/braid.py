"""
This module sets up the Braid class
and canonicalization of braids
"""

from __future__ import annotations
from typing import Callable, Sequence
from braid.braid_generator import BraidGenerator
from category.object import PrimitiveObject
from fig_gen.latex import Latex


class Braid(Latex):
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

    def copy(self) -> Braid:
        """Returns a copy of this braid.

        Returns:
            Braid: Copy
        """
        b = Braid(self.n())
        for gen in self:
            b.append(gen)
        return b

    @staticmethod
    def str_to_braid(n: int, s: str) -> Braid:
        """Constructs a braid word
        from the string

        Args:
            n (int): Number of strands
            s (str): Alphabetical string representing
            characters

        Returns:
            Braid: braid word on
            n strands described
            by the string
        """
        b = Braid(n)
        gens = [BraidGenerator.from_char(c) for c in s]
        for g in gens:
            b.append(g)
        return b

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

    @staticmethod
    def delta(n: int, pos: bool = True) -> Braid:
        """Constructs the delta braid
        on n strands

        Args:
            n (int): Number of strands
            pos (bool, optional): Whether the
            crossings are positive. Defaults to True.

        Returns:
            Braid: Delta braid
        """
        d = Braid(n)
        for i in range(n - 1, -1, -1):
            # strand 0 to index i
            for j in range(i):
                d.append(BraidGenerator(j, pos))
        return d

    def left_gcd(self, other: Braid) -> Braid:
        """Computes the left GCD of this braid
        and the other one.

        Args:
            other (Braid): Braid to compute
            GCD with

        Raises:
            StrandMismatchException: self and other
            have different amount of strands

        Returns:
            Braid: Maximal braid x such that
            there exists y such that x y = self
            and y' such that x y' = other
        """
        if self.n() != other.n():
            raise StrandMismatchException()

        gcd = Braid(self.__n)

        for i in range(self.n() - 1):
            g1 = Braid(self.n())
            g1.append(BraidGenerator(i, False))
            g1.concat(self)

            (self_quotient, leftovers) = g1.reverse()

            if len(list(leftovers)) != 0:
                continue

            g2 = Braid(self.n())
            g2.append(BraidGenerator(i, False))
            g2.concat(other)

            (other_quotient, leftovers) = g2.reverse()

            if len(list(leftovers)) != 0:
                continue

            sub_gcd = self_quotient.left_gcd(other_quotient)
            gcd.append(BraidGenerator(i, True))
            for g in sub_gcd:
                gcd.append(g)
            return gcd

        return gcd

    def head(self) -> Braid:
        """Computes the head, or
        alpha, of the braid

        Returns:
            Braid: Largest simple
            divisor of self
        """
        return self.left_gcd(Braid.delta(self.n()))

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
        while True:
            for gen_index, g1 in enumerate(self):
                if gen_index + 1 == len(self.__gens):
                    continue
                g2 = self.__gens[gen_index + 1]
                if not g1.pos() and g2.pos():
                    i = g1.i()
                    j = g2.i()

                    prefix = self.__gens[:gen_index]
                    middle = Braid.reverse_helper(i, j)
                    suffix = self.__gens[gen_index + 2 :]

                    self.__gens = prefix + middle + suffix
                    break  # break the for loop, doesn't
                    # go to else, while True makes
                    # this go to next loop
            else:
                # for wasn't broken; no swaps
                # were made
                break  # break the while True

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

    def simple_perm(self, ignore: bool = False) -> list[int]:
        """Converts to a permutation.
        Raises NotSimpleError if
        this list doesn't represent a permutation
        and ignore is False

        Args:
            ignore (bool): default False to
            raise NotSimpleError when not simple;
            True to ignore errors

        Raises:
            NotSimpleError: Raised if
            the braid isn't simple and
            ignore is False

        Returns:
            list[int]: image of the permutation
            if the braid is simple or ignore
            is True
        """
        perm: list[int] = list(range(self.n()))
        crossings: set[int] = set()
        for g in self:
            if not ignore and not g.pos():
                raise NotSimpleError()
            over = perm.index(g.i())
            under = perm.index(g.i() + 1)

            key = over * self.n() + under
            if not ignore and key in crossings:
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
                return [
                    BraidGenerator(j, True),
                    BraidGenerator(i, True),
                    BraidGenerator(j, False),
                    BraidGenerator(i, False),
                ]
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

    def subbraid(self, keep: set[int]) -> Braid:
        """Computes and returns a subbraid of
        this braid

        Args:
            keep (set[int]): 0-indices of
            the starting strands that should
            remain in the subbraid

        Returns:
            Braid: Subbraid on len(keep)
            strands
        """
        b = Braid(len(keep))
        for g in self:
            i = g.i()
            if i in keep:
                if i + 1 in keep:
                    j = 0
                    for x in keep:
                        if x < i:
                            j += 1
                    b.append(BraidGenerator(j, g.pos()))
                else:
                    keep.remove(i)
                    keep.add(i + 1)
            else:
                if i + 1 in keep:
                    keep.remove(i + 1)
                    keep.add(i)
        return b

    def fuzz(self, rng: Callable[[], float], steps: int) -> None:
        """Fuzzes the braid word by applying a series
        of rewrite rules, preserving its equivalence but
        changing ts generators.

        Args:
            rng (Callable[[], float]): Random number generator
            steps (int): Number of rewrite rules to apply
        """
        for _ in range(steps):
            if not self.__gens:
                continue

            # Select a random index in the list of generators
            i = int(rng() * len(self.__gens))

            # Apply a random braid relation at this index
            self.__fuzz_index(i, rng)

    def __fuzz_index(self, i: int, rng: Callable[[], float]) -> None:
        """Attempts to apply a braid word equivalence at this
        index. If none work, has a chance to uncancel a pair
        at this index.

        Args:
            i (int): 0-index in the braid word's length
            rng (Callable[[], float]): Random number generator
        """
        if not 0 < i < len(self.__gens) - 1:
            return
        g1 = self.__gens[i - 1]
        g2 = self.__gens[i]
        g3 = self.__gens[i + 1]

        # Yang-baxter?
        if (
            g1.i() == g3.i()
            and abs(g1.i() - g2.i()) == 1
            and g1.pos() == g2.pos() == g3.pos()
        ):
            self.__gens[i - 1 : i + 2] = [g2, g1, g2]
        # Cancel?
        elif g1.i() == g2.i() and g1.pos() != g2.pos():
            # Remove both generators
            del self.__gens[i - 1 : i + 1]
        # Swap?
        elif abs(g1.i() - g2.i()) >= 2:
            self.__gens[i - 1 : i + 1] = [g2, g1]
        else:
            # Uncancel?
            if rng() < 0.3:
                j = int(rng() * (self.n() - 1))
                first_inv = rng() < 0.5
                self.__gens.insert(i, BraidGenerator(j, first_inv))
                self.__gens.insert(i, BraidGenerator(j, not first_inv))

    def __iter__(self) -> Braid:
        self.__iter_index = 0
        return self

    def __next__(self) -> BraidGenerator:
        if self.__iter_index >= len(self.__gens):
            raise StopIteration
        next_gen = self.__gens[self.__iter_index]
        self.__iter_index += 1
        return next_gen

    def __repr__(self) -> str:
        return f"Braid(n={self.__n}, {self.__gens})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Braid):
            return False
        return self.n() == other.n() and list(iter(self)) == list(iter(other))

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        str_latex = ""
        for g in self:
            str_latex += g.to_latex(x, y, context)
            y += g.latex_height()
            context = g.context_out(context)

        if self.__gens == []:
            for i, o in enumerate(context):
                (r, gr, b) = o.color()
                str_latex += (
                    f"\\identity{{{x+i}}}{{{y}}}{{{0}}}{{{o}}}{{{r}}}{{{gr}}}{{{b}}}\n"
                )

        return str_latex

    def latex_height(self) -> int:
        return max(len(list(self)), 1)

    def context_out(
        self, context: Sequence[PrimitiveObject]
    ) -> Sequence[PrimitiveObject]:
        for g in self:
            context = g.context_out(context)

        return context


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
