"""
This module sets up the Braid class
and canonicalization of braids
"""

from __future__ import annotations
from typing import Callable, List, Sequence, Iterator, Tuple
from braid.braid_generator import BraidGenerator
from braid.sage import canonicalize_braid
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

    def copy(self) -> Braid:
        """Returns a copy of this braid.

        Returns:
            Braid: Copy
        """
        b = Braid(self.n())
        for gen in self:
            b.append(gen)
        return b

    def reset_to(self, other: Braid) -> None:
        """Sets this braid's value to the given braid's value"""
        self.__n = other.n()
        self.__gens = list(other)

    def flip_vertical(self) -> Braid:
        """Flips the braid vertically (reflection,
        not rotation)

        Returns:
            Braid: Flipped braid
        """
        b = Braid(self.n())
        for gen in reversed(list(self)):
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

    def canon(self) -> Braid:
        """Returns the braid in canonical form
        that is equivalent to this braid"""
        out = canonicalize_braid(self.n(), [g.to_sage() for g in self.__gens])
        return Braid.from_sage(out, self.n())

    def set_canon(self) -> None:
        """Makes this braid the canon version of itself"""
        self.__gens = list(self.canon())

    @staticmethod
    def from_sage(sage_out: List[Tuple[str, int]], n: int) -> Braid:
        """Makes a braid from sagemath's output. See sage.py for how
        this output is preprocessed

        Args:
            sage_out (List[Tuple[str, int]]): Syllables of the word
            n (int): Number of strands

        Returns:
            Braid: Braid representing the sagemath output
        """
        b = Braid(n)
        for name, power in sage_out:
            i = int(name[1:]) if n > 2 else 0
            pos = power > 0
            for _ in range(abs(power)):
                b.append(BraidGenerator(i, pos))
        return b

    def n(self) -> int:
        """Simple get function

        Returns:
            int: number of strands of the braid word
        """
        return self.__n

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

    def extend(self, after: Braid) -> None:
        """Extends this braid with another's
        generators

        Args:
            after (Braid): Braid to add after self
        """
        self.__check_compatible(after)
        self.__gens.extend(list(after))

    def intend(self, before: Braid) -> None:
        """Adds the supplied braid's generators
        before this one's

        Args:
            before (Braid): Braid to add before self
        """
        self.__check_compatible(before)
        # TODO: this is why it'd be nice to use linked lists
        self.__gens = list(before) + self.__gens

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
                # uncancel a few times
                for _ in range(self.n()):
                    i = int(rng() * (len(self.__gens) + 1))
                    j = int(rng() * (self.n() - 1))
                    first_inv = rng() < 0.5
                    self.__gens.insert(i, BraidGenerator(j, first_inv))
                    self.__gens.insert(i, BraidGenerator(j, not first_inv))
            else:
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

    def __iter__(self) -> Iterator[BraidGenerator]:
        return iter(self.__gens)

    def __len__(self) -> int:
        return len(self.__gens)

    def __repr__(self) -> str:
        return f"Braid(n={self.__n}, {self.__gens})"

    def __str__(self) -> str:
        return "".join([str(g) for g in self])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Braid):
            return False
        return self.n() == other.n() and list(iter(self)) == list(iter(other))

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        str_latex = ""
        str_latex += (
            f"\\knitBoundBox{{{x}}}{{{y}}}{{{self.n()}}}{{{1}}}\n"
        )
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
        return max(len(self), 1)

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
