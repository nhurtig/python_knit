from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod
from color import color_gen

class PrimitiveObjectType(Enum):
    C = 0
    L = 1

class PrimitiveObject(ABC):
    def __init__(self) -> None:
        self.__color = color_gen.get_next_color()

    @abstractmethod
    def twist(self, is_pos: bool) -> None:
        pass

    @abstractmethod
    def twists(self) -> int:
        pass

    def color(self) -> tuple[float, float, float]:
        return self.__color

class Carrier(PrimitiveObject):
    def __init__(self, id: int) -> None:
        super().__init__()
        self.__id = id

    def twist(self, is_pos: bool) -> None:
        pass

    def twists(self) -> int:
        return 0

    def __str__(self) -> str:
        return "c"

class Loop(PrimitiveObject):
    def __init__(self, id: int) -> None:
        super().__init__()
        self.__id = id
        self.__twists: int = 0

    def twist(self, is_pos: bool) -> None:
        self.__twists += 1 if is_pos else -1

    def twists(self) -> int:
        return self.__twists

    def __str__(self) -> str:
        return "l"
