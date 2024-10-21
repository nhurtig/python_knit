"""
Sets up common classes like
Sign and Bed and Dir
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Flippable(ABC):  # pylint: disable=too-few-public-methods
    """
    Abstract class that represents
    objects that are really just
    booleans
    """

    def flip(self) -> Flippable:
        """Flips the object

        Returns:
            Flippable: The inverse of
            whatever this is
        """
        return Flippable._from_bool(not self._to_bool())

    @staticmethod
    @abstractmethod
    def _from_bool(b: bool) -> Flippable:
        """Makes a new Flippable from a bool

        Args:
            b (bool): input bool

        Returns:
            Flippable: Flippable made from b
        """

    @abstractmethod
    def _to_bool(self) -> bool:
        """Converts a Flippable into a bool

        Returns:
            bool: bool that represents this
                Flippable
        """

    @abstractmethod
    def __str__(self) -> str:
        pass


class Sign(Flippable):
    """
    Used for morphisms that
    have inverses
    """

    def __init__(self, is_pos: bool) -> None:
        self.__is_pos = is_pos

    def pos(self) -> bool:
        """Getter

        Returns:
            bool: whether this sign is positive
        """
        return self.__is_pos

    @staticmethod
    def _from_bool(b: bool) -> Sign:
        return Sign(is_pos=b)

    def _to_bool(self) -> bool:
        return self.__is_pos

    def __str__(self) -> str:
        if self.pos():
            return "pos"
        else:
            return "neg"


class Dir(Flippable):
    """
    Used for the direction of
    the carrier strand in a knit
    """

    def __init__(self, is_right: bool) -> None:
        self.__is_right = is_right

    def right(self) -> bool:
        """Getter

        Returns:
            bool: whether this dir is right
        """
        return self.__is_right

    @staticmethod
    def _from_bool(b: bool) -> Dir:
        return Dir(is_right=b)

    def _to_bool(self) -> bool:
        return self.__is_right

    def __str__(self) -> str:
        if self.right():
            return "right"
        return "left"


class Bed(Flippable):
    """
    The front and back beds of
    a v-bed knitting machine
    """

    def __init__(self, is_front: bool) -> None:
        self.__is_front = is_front

    def front(self) -> bool:
        """Getter

        Returns:
            bool: whether this bed is front
        """
        return self.__is_front

    @staticmethod
    def _from_bool(b: bool) -> Bed:
        return Bed(is_front=b)

    def _to_bool(self) -> bool:
        return self.__is_front

    def __str__(self) -> str:
        if self.front():
            return "front"
        return "back"
