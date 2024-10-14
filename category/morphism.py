from __future__ import annotations
from typing import Optional
from category.object import Loop, PrimitiveObject
from common import Bed, Dir


class Knit:
    def __init__(self, bed: Bed, dir: Dir, ins: list[Optional[PrimitiveObject]], outs: list[Optional[PrimitiveObject]]) -> None:
        self.__bed = bed
        self.__dir = dir
        # TODO: check this is a valid knit
        self.__ins = ins
        self.__outs = outs

    def outs(self) -> list[PrimitiveObject]:
        return list(filter(lambda x: x is not None, self.__outs))

    def ins(self) -> list[PrimitiveObject]:
        return list(filter(lambda x: x is not None, self.__ins))

    def primary(self) -> Loop:
        o = self.__outs[self.__primary_index_pre_slurp()]
        if not isinstance(o, Loop):
            raise ValueError
        return o

    def flip(self) -> None:
        self.__ins.reverse()
        self.__outs.reverse()
        self.__bed = self.__bed.flip()
        self.__dir = self.__dir.flip()

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
