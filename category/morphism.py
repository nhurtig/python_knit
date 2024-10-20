from __future__ import annotations
from typing import Optional, Sequence, TypeGuard
from category.object import Loop, PrimitiveObject
from common import Bed, Dir
from latex import Latex


class Knit(Latex):
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

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        latex_str = ""
        latex_str += f"""\\knit{{{self.__dir}}}{{{self.__bed}}}
{{{len(self.ins())}}}{{{len(self.outs())}}}{{{x}}}{{{y}}}\n"""
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
        return list(filter(Knit.__is_not_none, self.__outs))

    def ins(self) -> list[PrimitiveObject]:
        return list(filter(Knit.__is_not_none, self.__ins))

    def primary(self) -> Loop:
        o = self.__outs[self.__primary_index_pre_slurp()]
        if not isinstance(o, Loop):
            raise ValueError
        return o

    def flip(self) -> None:
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
        i = self.__primary_index_pre_slurp()
        before = self.__outs[:i]
        for o in before:
            if o is None:
                i -= 1
        return i

    def __repr__(self) -> str:
        return f"Knit(front={self.__bed.front()}, right={self.__dir.right()}"
