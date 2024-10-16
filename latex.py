from abc import ABC, abstractmethod

from category.object import PrimitiveObject

class Latex(ABC):
    @abstractmethod
    def to_latex(self, x: int, y: int, context: list[PrimitiveObject]) -> str:
        pass

    @abstractmethod
    def latex_height(self) -> int:
        pass

    @abstractmethod
    def context_out(self, context: list[PrimitiveObject]) -> list[PrimitiveObject]:
        pass
