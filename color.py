from __future__ import annotations
import colorsys

# TODO: instead of golden ratio,
# use binary chunking or something
class ColorGenerator:
    def __init__(self) -> None:
        self.hue = 0.0  # Initial hue value
        self.ghosting = []
        self.index = 0
        self.golden_ratio_conjugate = 0.61803398875  # Approximate value of the golden ratio conjugate

    def get_next_color(self) -> tuple[float, float, float]:
        # Increment hue by the golden ratio
        self.hue += self.golden_ratio_conjugate
        self.hue %= 1.0  # Ensure hue wraps around between 0 and 1

        # Convert HSL to RGB
        r, g, b = colorsys.hls_to_rgb(self.hue, 0.95 if self.index in self.ghosting else 0.35, 1.0)  # Lightness is 0.5 for good visibility, Saturation is 0.9
        self.index += 1
        return (r, g, b)

    def reset(self) -> None:
        self.hue = 0.0
        self.index = 0

    def set_ghosting(self, g: list[int]) -> None:
        self.ghosting = g

color_gen = ColorGenerator()

def reset_colors(reset_ghosting: bool=True):
    color_gen.reset()
    if reset_ghosting:
        set_ghosting([])

def set_ghosting(g: list[int]) -> None:
    color_gen.set_ghosting(g)