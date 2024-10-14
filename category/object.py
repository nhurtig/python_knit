from __future__ import annotations
from enum import Enum
from abc import ABC, abstractmethod

class PrimitiveObjectType(Enum):
    C = 0
    L = 1

class PrimitiveObject(ABC):
    @abstractmethod
    def twist(self, is_pos: bool) -> None:
        pass

    @abstractmethod
    def twists(self) -> int:
        pass

class Carrier(PrimitiveObject):
    def __init__(self, id: int) -> None:
        self.__id = id
    
    def twist(self, is_pos: bool) -> None:
        pass

    def twists(self) -> int:
        return 0

class Loop(PrimitiveObject):
    def __init__(self, id: int) -> None:
        self.__id = id
        self.__twists: int = 0

    def twist(self, is_pos: bool) -> None:
        self.__twists += 1 if is_pos else -1

    def twists(self) -> int:
        return self.__twists
