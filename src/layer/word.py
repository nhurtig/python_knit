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

        # Whether zero-length braids at the top and
        # bottom are drawn or not
        self.__draw_preamble = 1
        self.__draw_postamble = 1
        self.labels_in: Sequence[str] = []
        self.labels_out: Sequence[str] = []

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
            self.layer_at(i).canonicalize()
            # l = self.__layers[i]
            # above = self.__braids[i + 1]
            # below = self.__braids[i]
            # emit = l.canonicalize(above)
            # emit.apply(below, above)
            # above.set_canon()
        self.__braids[0].set_canon()

    def attempt_swap(self, index: int) -> bool:
        """Attempts to move a layer up one index.
        Mutates the braid on failure and success;
        always preserves equivalence.

        Args:
            index (int): Index to move up

        Returns:
            bool: Whether the layers are swappable
        """
        self.layer_at(index).macro_step()
        self.layer_at(index + 1).flip_macro()
        return self.__swap_if_identity(index)

    def __swap_if_identity(self, index: int) -> bool:
        middle = self.__braids[index + 1]
        middle.set_canon()
        if len(middle) == 0:
            below = self.__layers[index]
            above = self.__layers[index + 1]
            if below.swap(above):
                self.__layers[index : index + 2] = [above, below]
                self.__braids[index + 1] = Braid(above.n_above())
                return True
            else:
                return False
        else:
            return False

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
        for i in range(len(self.__layers)):
            self.fuzz_layer(i, rng, layer_muts)
            self.fuzz_braid(i, rng, braid_muts)
        self.fuzz_braid(len(self.__layers), rng, braid_muts)
        # for i, l in enumerate(self.__layers):
        #     emit = l.fuzz(rng, layer_muts)
        #     below = self.__braids[i]
        #     above = self.__braids[i + 1]
        #     emit.apply(below, above)
        #     below.fuzz(rng, braid_muts)
        # self.__braids[-1].fuzz(rng, braid_muts)

    def fuzz_layer(self, index: int, rng: Callable[[], float], layer_muts: int) -> None:
        """Fuzzes the layer at the given index

        Args:
            index (int): Index in the layers list
            rng (Callable[[], float]): [0, 1] random number generator
            layer_muts (int): Number of mutation attempts to make
        """
        self.layer_at(index).fuzz(rng, layer_muts)

    def fuzz_braid(self, index: int, rng: Callable[[], float], braid_muts: int) -> None:
        """Fuzzes the braid at the given index

        Args:
            index (int): Index in the braids list
            rng (Callable[[], float]): [0, 1] random number generator
            braid_muts (int): Number of mutation attempts to make
        """
        self.__braids[index].fuzz(rng, braid_muts)

    def draw_preamble(self, draw: int) -> None:
        """Setter

        Args:
            draw (int): How many times to draw empty braid
            at start
        """
        self.__draw_preamble = draw

    def draw_postamble(self, draw: int) -> None:
        """Setter

        Args:
            draw (int): How many times to draw empty
            braid at end
        """
        self.__draw_postamble = draw

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

    def __len__(self) -> int:
        return len(self.__braids) * 2 - 1

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        latex_str = ""
        for i, s in enumerate(self.labels_in):
            latex_str += f"\\knitLabel{{{x+i}}}{{{y-1.3}}}{{${s}$}}\n"
        for i, o in enumerate(self):
            num_iters = 1
            if isinstance(o, Braid):
                if i == 0:
                    num_iters = self.__draw_preamble
                    id_braid = Braid(o.n())
                    for _ in range(num_iters - o.latex_height()):
                        latex_str += id_braid.to_latex(x, y, context)
                        y += id_braid.latex_height()
                        context = id_braid.context_out(context)
                if i == len(self) - 1:
                    num_iters = self.__draw_postamble
            if num_iters > 0:
                latex_str += o.to_latex(x, y, context)
                y += o.latex_height()
                context = o.context_out(context)
            if num_iters > 1 and i == len(self) - 1:
                id_braid = Braid(o.n())
                for _ in range(num_iters - o.latex_height()):
                    latex_str += id_braid.to_latex(x, y, context)
                    y += id_braid.latex_height()
                    context = id_braid.context_out(context)

        for i, s in enumerate(self.labels_out):
            latex_str += f"\\knitLabel{{{x+i}}}{{{y}}}{{${s}$}}\n"
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
