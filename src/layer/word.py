"""Words are a series of layers; they
are words in the slurped
braided monoidal category. This module
starts the description of the algorithm to
canonicalize a word."""

from __future__ import annotations
from typing import Callable, Sequence, Union
from braid.braid import Braid, StrandMismatchException
from category.object import PrimitiveObject
from fig_gen.latex import Latex
from layer.layer import Layer
from layer.layer_wrapper import LayerWrapper


class Word(Latex):
    """Words are a list of Layers and the
    Braids between them"""

    def __init__(self, bottom_strands: int = 0) -> None:
        # TODO: the connections of PrimitiveObjects between layers
        # is a graph structure. Leverage that?
        self.__layers: list[Layer] = []
        self.__braids: list[Braid] = [Braid(bottom_strands)]
        self.__iter_index = 0
        self.__iter_braid_next = True
        # braids[i] is below layers[i];
        # braids[i+1] is above.
        # len(braids) = len(layers) + 1 always

    def copy(self) -> Word:
        """Copies the word and
        its layers.

        Returns:
            Word: Not-shallow
            copy
        """
        w = Word(self.__braids[0].n())  # guaranteed at least one braid
        copied_object_dict: dict[PrimitiveObject, PrimitiveObject] = {}
        for i, l in enumerate(self.__layers):
            below_braid = self.__braids[i]
            w.append_braid(below_braid.copy())
            w.append_layer(l.copy(copied_object_dict))
        w.append_braid(self.__braids[-1])
        return w

    def layer_at(self, index: int) -> LayerWrapper:
        """Returns a wrapper around the layer at this
        index. The wrapper applies any emitted effects
        to the neighboring braids

        Args:
            index (int): index in the layer list

        Returns:
            LayerWrapper: Wrapper around the indexed layer
        """
        return LayerWrapper(
            self.__braids[index], self.__layers[index], self.__braids[index + 1]
        )

    def braid_at(self, index: int) -> Braid:
        """Getter that wraps the braid list

        Args:
            index (int): Index in the braid list

        Returns:
            Braid: Braid at that index
        """
        return self.__braids[index]

    def append_layer(self, l: Layer) -> None:
        """Adds a layer on top of this word

        Args:
            l (Layer): Layer to be added
            to the top/end of the word
        """
        if l.n_below() != self.__braids[-1].n():
            raise StrandMismatchException
        self.__layers.append(l)
        self.__braids.append(Braid(l.n_above()))

    def append_braid(self, b: Braid) -> None:
        """Adds a braid on top of this word

        Args:
            b (Braid): Braid to be added on top
            of the word
        """
        self.__braids[-1].extend(b)

    def canonicalize(self) -> None:
        """Canonicalizes the word in place"""
        for i in range(len(self.__layers) - 1, -1, -1):
            l = self.__layers[i]
            above = self.__braids[i + 1]
            below = self.__braids[i]
            emit = l.canonicalize(above)
            emit.apply(below, above)
            above.set_canon()
        self.__braids[0].set_canon()

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
        for i, l in enumerate(self.__layers):
            emit = l.fuzz(rng, layer_muts)
            below = self.__braids[i]
            above = self.__braids[i + 1]
            emit.apply(below, above)
            below.fuzz(rng, braid_muts)
        self.__braids[-1].fuzz(rng, braid_muts)

    def __repr__(self) -> str:
        repr_str = ":".join([repr(obj) for obj in self])
        return f"Word({repr_str})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return False
        return list(self) == list(other)

    def __iter__(self) -> Word:
        self.__iter_index = 0
        self.__iter_braid_next = True
        return self

    def __next__(self) -> Union[Braid, Layer]:
        if self.__iter_braid_next:
            b = self.__braids[self.__iter_index]
            self.__iter_braid_next = False
            return b
        else:
            if self.__iter_index >= len(self.__layers):
                raise StopIteration
            l = self.__layers[self.__iter_index]
            self.__iter_braid_next = True
            self.__iter_index += 1
            return l

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        latex_str = ""
        for o in self:
            latex_str += o.to_latex(x, y, context)
            y += o.latex_height()
            context = o.context_out(context)
        return latex_str

    def latex_height(self) -> int:
        h = 0
        for o in self:
            h += o.latex_height()
        return h

    def context_out(
        self, context: Sequence[PrimitiveObject]
    ) -> Sequence[PrimitiveObject]:
        for o in self:
            context = o.context_out(context)
        return context
