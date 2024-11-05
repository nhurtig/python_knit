"""Class to represent the emittances from layer operations"""

from __future__ import annotations
from braid.braid import Braid
from braid.braid_generator import BraidGenerator


class LayerEmit:
    """Records the below and above braids. Can be extended
    with other LayerEmits to concatenate their operations"""

    def __init__(self, below: int, above: int) -> None:
        self.__below = Braid(below)
        self.__above = Braid(above)

    def above(self) -> Braid:
        """Getter

        Returns:
            Braid: above braid
        """
        return self.__above

    def below(self) -> Braid:
        """Getter

        Returns:
            Braid: below braid
        """
        return self.__below

    def emit_above(self, g: BraidGenerator) -> None:
        """Emits a generator above the layer

        Args:
            g (BraidGenerator): Generator to be emitted
        """
        self.__above.prepend(g)

    def emit_below(self, g: BraidGenerator) -> None:
        """Emits a generator below the layer

        Args:
            g (BraidGenerator): Generator to be emitted
        """
        self.__below.append(g)

    def extend(self, next_emit: LayerEmit) -> None:
        """Adds the supplied LayerEmit to this one,
        assuming self was applied before the supplied
        one

        Args:
            next_emit (LayerEmit): LayerEmit that was emitted
            second
        """
        next_emit.apply(self.__below, self.__above)

    def apply(self, below: Braid, above: Braid) -> None:
        """Applies this layer emittance to braids

        Args:
            below (Braid): braid below the layer
            above (Braid): braid above the layer
        """
        below.extend(self.below())
        above.intend(self.above())

    def flip_vertical(self) -> LayerEmit:
        """Flips this LayerEmit vertically
        (reflection, not rotation)

        Returns:
            LayerEmit: vertically flipped LayerEmit
        """
        flipped = LayerEmit(self.above().n(), self.below().n())
        for g in self.__above: # reads inside to out
            flipped.emit_above(g)
        for g in reversed(list(self.__below)): # inside to out
            flipped.emit_below(g)
        return flipped
