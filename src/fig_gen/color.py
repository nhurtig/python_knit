"""Used for generating the colors in the
tikz figures"""

from __future__ import annotations
import colorsys


# TODO: instead of golden ratio,
# use binary chunking or something
class ColorGenerator:
    """Generator that emits a series
    of colors over its lifetime"""

    def __init__(self) -> None:
        self.__hue = 0.0  # Initial hue value
        self.__ghosting: list[int] = []
        self.__index = 0
        self.__golden_ratio_conjugate = (
            0.61803398875  # Approximate value of the golden ratio conjugate
        )

    def get_next_color(self) -> tuple[float, float, float]:
        """Returns the next color in RGB [0.0, 1.0] format

        Returns:
            tuple[float, float, float]: RGB triple
        """
        # Increment hue by the golden ratio
        self.__hue += self.__golden_ratio_conjugate
        self.__hue %= 1.0  # Ensure hue wraps around between 0 and 1

        # Convert HSL to RGB
        r, g, b = colorsys.hls_to_rgb(
            self.__hue, 0.95 if self.__index in self.__ghosting else 0.35, 1.0
        )  # Lightness is 0.5 for good visibility, Saturation is 0.9
        self.__index += 1
        return (r, g, b)

    def reset(self) -> None:
        """Resets the state of this generator
        so the first color is next. Does not
        change the ghosting"""
        self.__hue = 0.0
        self.__index = 0

    def set_ghosting(self, g: list[int]) -> None:
        """Sets the color indices that should
        be ghosted. These indices' colors will
        be faded out

        Args:
            g (list[int]): Color indices to be
            faded
        """
        self.__ghosting = g


color_gen = ColorGenerator()


def reset_colors(reset_ghosting: bool = True) -> None:
    """Resets the colors of the color generator

    Args:
        reset_ghosting (bool, optional): Whether the
        ghosting indices of the generator should be
        reset to no ghosting as well. Defaults to True.
    """
    color_gen.reset()
    if reset_ghosting:
        set_ghosting([])


def set_ghosting(g: list[int]) -> None:
    """Sets the ghosting indices of the
    color generator

    Args:
        g (list[int]): Indices to be
        faded
    """
    color_gen.set_ghosting(g)