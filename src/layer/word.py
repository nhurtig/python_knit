"""Words are a series of layers; they
are words in the slurped
braided monoidal category. CanonWords
are specific representations of words
that have been canonicalized. This module
describes the algorithm to
canonicalize a word."""

from __future__ import annotations
from typing import Callable, Iterator, Sequence
from category.object import PrimitiveObject
from fig_gen.latex import Latex
from layer.layer import Layer

# TODO: allow words to alternate
# braids and knits in wacky ways.


class Word(Latex):
    """Words are a list of Layers."""

    def __init__(self) -> None:
        self.__layers: list[Layer] = []

    def copy(self) -> Word:
        """Copies the word and
        its layers. The bottom braid
        must have n=0.

        Returns:
            Word: Not-shallow
            copy
        """
        w = Word()
        layers = list(self)
        copied_object_dict = {}
        if layers:
            prev_b = layers[0].below()
            for l in layers:
                (l_copy, new_b) = l.copy(prev_b, copied_object_dict)
                w.append_layer(l_copy)
                prev_b = new_b
        return w

    def canonicalize(self) -> None:
        """Canonicalizes the word in place"""
        for l in reversed(self.__layers):
            l.canonicalize()

    def fuzz(self, rng: Callable[[], float], layer_muts: int, braid_muts: int) -> None:
        """Fuzzes the word in place. Executes layer_muts layer mutations
        at each layer, then braid_muts braid mutations at each
        layer

        Args:
            rng (Callable[[], float]): Random number generator
            layer_muts (int): Number of layer mutations at
            each layer
            braid_muts (int): Number of braid word mutations at
            each layer
        """
        for l in self:
            l.fuzz_layer(rng, layer_muts)
        for l in self:
            l.fuzz_braid(rng, braid_muts)

    # TODO: keep track of the above braid
    # and construct the Layer from a Knit
    # and the Braid (good for building from another form)
    def append_layer(self, l: Layer) -> None:
        """Adds a layer on top of this word,
        mutating it in place. Currently, the
        user is responsible for the bottom of
        the layer to match the top of the
        currently top layer. TODO: fix this.

        Args:
            l (Layer): Layer to be added
            to the top/end of the word
        """
        self.__layers.append(l)

    def __iter__(self) -> Iterator[Layer]:
        return iter(self.__layers)

    def __repr__(self) -> str:
        return f"Word({self.__layers})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return False
        return list(self) == list(other)

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        latex_str = ""
        for l in self:
            latex_str += l.to_latex(x, y, context)
            y += l.latex_height()
            context = l.context_out(context)
        return latex_str

    def latex_height(self) -> int:
        h = 0
        for l in self:
            h += l.latex_height()
        return h

    def context_out(
        self, context: Sequence[PrimitiveObject]
    ) -> Sequence[PrimitiveObject]:
        # TODO: implement
        raise NotImplementedError
