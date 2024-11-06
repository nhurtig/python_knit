"""Class to wrap around a layer and apply its emittances"""

from __future__ import annotations
from typing import Callable
from braid.braid import Braid
from layer.layer import Layer
from layer.layer_emit import LayerEmit


class LayerWrapper:
    """Stores below and above braids. Exposes some
    equivalence-preserving layer operations"""

    def __init__(self, below: Braid, layer: Layer, above: Braid) -> None:
        self.__below = below
        self.__layer = layer
        self.__above = above

    def __apply(self, emit: LayerEmit) -> None:
        emit.apply(self.__below, self.__above)

    def fuzz(self, rng: Callable[[], float], steps: int) -> None:
        """Fuzzes this layer by performing layer operations; doesn't
        fuzz either braid

        Args:
            rng (Callable[[], float]): Random number generator
            steps (int): Number of mutations to attempt
        """
        self.__apply(self.__layer.fuzz(rng, steps))

    def macro_step(self) -> None:
        """Performs the macro step of the algorithm
        on this layer, mutating it in place
        """
        self.__apply(self.__layer.macro_step(self.__above))

    def delta_step(self) -> None:
        """Performs the delta step of the algorithm
        on this layer, mutating it in place
        """
        self.__apply(self.__layer.delta_step())

    def canonicalize(self) -> None:
        """Canonicalizes this layer, mutating
        it in place. Does not do any braid canonicalization
        """
        self.__apply(self.__layer.canonicalize(self.__above))

    def flip_macro(self) -> None:
        """Does the macro substep of canonicalization
        on this layer while "facing upside down"
        """
        self.__apply(self.__layer.flip_macro(self.__below))

    def macro_subbraid(self) -> Braid:
        """Computes the above macro subbraid of this
        layer

        Returns:
            Braid: macro subbraid of above
        """
        return self.__layer.macro_subbraid(self.__above)
