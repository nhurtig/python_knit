"""Objects are the arrows in the diagrams; carriers
and loops. They each have colors and keep track of their
twists"""

from __future__ import annotations
from abc import ABC, abstractmethod
from fig_gen.color import color_gen


class PrimitiveObject(ABC):
    """Abstract class for either a Carrier
    or a Loop"""

    def __init__(self, identity: int) -> None:
        self.__id = identity
        self.__color = color_gen.get_next_color()

    def id(self) -> int:
        """Getter

        Returns:
            int: ID of the object (useful
            for modeling colors of yarn)
        """
        return self.__id

    @abstractmethod
    def twist(self, is_pos: bool) -> None:
        """Twists this object

        Args:
            is_pos (bool): whether the twist
            is positive or negative
        """

    @abstractmethod
    def twists(self) -> int:
        """Returns the number of twists
        (possibly negative) in the object

        Returns:
            int: Twist count
        """

    def color(self) -> tuple[float, float, float]:
        """Getter

        Returns:
            tuple[float, float, float]: RGB [0.0, 1.0]
            triple
        """
        return self.__color


class Carrier(PrimitiveObject):
    """Carrier yarn; a single thread. Doesn't
    keep track of twists; is always untwisted"""

    def twist(self, is_pos: bool) -> None:
        pass

    def twists(self) -> int:
        return 0

    def __str__(self) -> str:
        return "c"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Carrier) and self.__id == other.id()


class Loop(PrimitiveObject):
    """Two yarns that are never separated. Keeps
    track of twists."""

    def __init__(self, identity: int) -> None:
        super().__init__(identity)
        self.__twists: int = 0

    def twist(self, is_pos: bool) -> None:
        self.__twists += 1 if is_pos else -1

    def twists(self) -> int:
        return self.__twists

    def __str__(self) -> str:
        return "l"
