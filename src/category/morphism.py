"""Defines boxes and knits, which
are black boxes that take some strands
to other strands"""

from __future__ import annotations
from typing import Dict, Optional, Sequence, TypeGuard
from category.object import Loop, PrimitiveObject
from common.common import Bed, Dir
from fig_gen.latex import Latex


class Knit(Latex):
    """Represents a knit, split, or tuck. There
    must be one loop coming out of it; otherwise
    it would have laddered away"""

    def __init__(
        self,
        bed: Bed,
        d: Dir,
        ins: list[Optional[PrimitiveObject]],
        outs: list[Optional[PrimitiveObject]],
    ) -> None:
        self.__bed = bed
        self.__dir = d
        # TODO: check this is a valid knit
        self.__ins = ins
        self.__outs = outs

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Knit):
            return False
        return (
            self.bed() == other.bed()
            and self.dir() == other.dir()
            and all(i1.eqv(i2) for (i1, i2) in zip(self.ins(), other.ins()))
            and all(o1.eqv(o2) for (o1, o2) in zip(self.outs(), other.outs()))
            and self.dropped_ins() == other.dropped_ins()
            and self.dropped_outs() == other.dropped_outs()
        )

    def flip_vertical(self) -> Knit:
        """Returns a Knit that represents this
        Knit reflected vertically (across a
        horizontal axis)

        Returns:
            Knit: Flipped Knit
        """
        return Knit(self.bed(), self.dir(), self.__outs, self.__ins)

    def bed(self) -> Bed:
        """Getter

        Returns:
            Bed: Knit's bed
        """
        return self.__bed

    def dir(self) -> Dir:
        """Getter

        Returns:
            Dir: Knit's dir
        """
        return self.__dir

    def copy(self, copied_object_dict: Dict[PrimitiveObject, PrimitiveObject]) -> Knit:
        """Copies this Knit

        Returns:
            Knit: A copy of the Knit
        """
        return Knit(
            self.__bed,
            self.__dir,
            [o.copy(copied_object_dict) if o is not None else None for o in self.__ins],
            [
                o.copy(copied_object_dict) if o is not None else None
                for o in self.__outs
            ],
        )

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        latex_str = ""
        width = max(len(self.ins()), len(self.outs()))
        latex_str += f"""\\knit{{{self.__dir}}}{{{self.__bed}}}
{{{width}}}{{{width}}}{{{x}}}{{{y}}}\n"""
        for i, o in enumerate(self.outs()):
            (r, g, b) = o.color()
            for j in range(abs(o.twists())):
                latex_str += f"""\\twist{{{'pos' if o.twists() > 0 else 'neg'}}}
{{{x+i}}}{{{y+j+1}}}{{{r}}}{{{g}}}{{{b}}}\n"""
            for j in range(abs(o.twists()), self.__max_twists()):
                latex_str += f"\\identity{{{x+i}}}{{{y+j+1}}}{{{0}}}{{{o}}}{{{r}}}{{{g}}}{{{b}}}\n"
        return latex_str

    def latex_height(self) -> int:
        return 1 + self.__max_twists()

    def context_out(self, context: Sequence[PrimitiveObject]) -> list[PrimitiveObject]:
        return self.outs()

    def __max_twists(self) -> int:
        max_twists = 0
        for o in self.outs():
            max_twists = max(max_twists, abs(o.twists()))
        return max_twists

    @staticmethod
    def __is_not_none(x: Optional[PrimitiveObject]) -> TypeGuard[PrimitiveObject]:
        return x is not None

    def outs(self) -> list[PrimitiveObject]:
        """Computes the objects that come
        out (on the top) of the knit

        Returns:
            list[PrimitiveObject]: Output objects
        """
        return list(filter(Knit.__is_not_none, self.__outs))

    def ins(self) -> list[PrimitiveObject]:
        """Computes the objects that come
        in (on the bottom) the knit

        Returns:
            list[PrimitiveObject]: Input objects
        """
        return list(filter(Knit.__is_not_none, self.__ins))

    def dropped_ins(self) -> list[bool]:
        """Returns a list of the in strands,
        with True for dropped (slurped) strands

        Returns:
            list[bool]: Indices where strands are dropped
        """
        return [i is None for i in self.__ins]

    def dropped_outs(self) -> list[bool]:
        """Returns a list of the out strands,
        with True for dropped (slurped) strands

        Returns:
            list[bool]: Indices where strands are dropped
        """
        return [o is None for o in self.__outs]

    def primary(self) -> Loop:
        """Returns the primary Loop object
        coming out of the knit

        Raises:
            ValueError: when the Knit is misconfigured
            and the primary loop isn't a loop

        Returns:
            Loop: Primary output loop
        """
        o = self.__outs[self.__primary_index_pre_slurp()]
        if not isinstance(o, Loop):
            raise ValueError
        return o

    def flip(self) -> None:
        """Flips the knit over. Doesn't
        twist the inputs and outputs"""
        self.__ins.reverse()
        self.__outs.reverse()
        # TODO: use flippable here.
        self.__bed = Bed(not self.__bed.front())
        self.__dir = Dir(not self.__dir.right())

    def __primary_index_pre_slurp(self) -> int:
        match (self.__bed.front(), self.__dir.right()):
            case (True, True):
                return 0
            case (True, False):
                return 1
            case (False, True):
                return len(self.__outs) - 2
            case (False, False):
                return len(self.__outs) - 1
        raise ValueError

    def primary_index(self) -> int:
        """Returns the index of the primary
        object in the true output objects
        (ignoring the slurped objects)

        Returns:
            int: 0-index from left
        """
        i = self.__primary_index_pre_slurp()
        before = self.__outs[:i]
        for o in before:
            if o is None:
                i -= 1
        return i

    def __repr__(self) -> str:
        return f"Knit(front={repr(self.__bed.front())}, right={repr(self.__dir.right())}, ins={len(self.ins())}, outs={len(self.outs())})"

    def __str__(self) -> str:
        return f"""[{", ".join(["slurped" if o is None else str(o) for o in self.__outs])}]
{self.__bed} {self.__dir}
[{", ".join(["slurped" if i is None else str(i) for i in self.__ins])}]"""
