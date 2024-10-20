from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from color import color_gen

class PrimitiveObjectType(Enum):
    C = 0
    L = 1

class PrimitiveObject(ABC):
    def __init__(self, identity: int) -> None:
        self.__id = identity
        self.__color = color_gen.get_next_color()

    def id(self) -> int:
        return self.__id

    @abstractmethod
    def twist(self, is_pos: bool) -> None:
        pass

    @abstractmethod
    def twists(self) -> int:
        pass

    def color(self) -> tuple[float, float, float]:
        return self.__color

class Carrier(PrimitiveObject):
    def twist(self, is_pos: bool) -> None:
        pass

    def twists(self) -> int:
        return 0

    def __str__(self) -> str:
        return "c"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Carrier) and self.__id == other.id()

class Loop(PrimitiveObject):
    def __init__(self, identity: int) -> None:
        super().__init__(identity)
        self.__twists: int = 0

    def twist(self, is_pos: bool) -> None:
        self.__twists += 1 if is_pos else -1

    def twists(self) -> int:
        return self.__twists

    def __str__(self) -> str:
        return "l"
