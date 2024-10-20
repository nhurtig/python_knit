"""Words are a series of layers; they
are words in the slurped
braided monoidal category. CanonWords
are specific representations of words
that have been canonicalized. This module
describes the algorithm to
canonicalize a word."""

from __future__ import annotations
from typing import Sequence
from category.object import PrimitiveObject
from fig_gen.latex import Latex
from layer.layer import CanonLayer, Layer

# TODO: allow words to alternate
# braids and knits in wacky ways.


class CanonWord(Latex):
    """CanonWords are static representations
    of Words that have been canonicalized.
    They really are just a list of
    CanonLayers."""

    def __init__(self, w: Word) -> None:
        self.__layers: list[CanonLayer] = []
        self.__iter_index = -1
        # TODO: don't copy these
        word_layers: list[Layer] = []
        word_layers.extend(w)
        for layer in reversed(word_layers):
            self.__layers.insert(0, CanonLayer(layer))

    def __iter__(self) -> CanonWord:
        self.__iter_index = 0
        return self

    def __next__(self) -> CanonLayer:
        if self.__iter_index >= len(self.__layers):
            raise StopIteration
        next_layer = self.__layers[self.__iter_index]
        self.__iter_index += 1
        return next_layer

    def __repr__(self) -> str:
        return f"CanonWord({self.__layers})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CanonWord):
            return False
        return list(iter(self)) == list(iter(other))

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


class Word(Latex):
    """Words are a list of Layers."""

    def __init__(self) -> None:
        self.__layers: list[Layer] = []
        self.__iter_index = -1

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

    def __iter__(self) -> Word:
        self.__iter_index = 0
        return self

    def __next__(self) -> Layer:
        if self.__iter_index >= len(self.__layers):
            raise StopIteration
        next_layer = self.__layers[self.__iter_index]
        self.__iter_index += 1
        return next_layer

    def __repr__(self) -> str:
        return f"Word({self.__layers})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return False
        return list(iter(self)) == list(iter(other))

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
