from __future__ import annotations
import colorsys

class ColorGenerator:
    def __init__(self) -> None:
        self.hue = 0.0  # Initial hue value
        self.golden_ratio_conjugate = 0.61803398875  # Approximate value of the golden ratio conjugate

    def get_next_color(self) -> tuple[float, float, float]:
        # Increment hue by the golden ratio
        self.hue += self.golden_ratio_conjugate
        self.hue %= 1.0  # Ensure hue wraps around between 0 and 1

        # Convert HSL to RGB
        r, g, b = colorsys.hls_to_rgb(self.hue, 0.35, 1.0)  # Lightness is 0.5 for good visibility, Saturation is 0.9
        return (r, g, b)

color_gen = ColorGenerator()
