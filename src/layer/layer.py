"""Layers are a box and their braids above and below. Their
interface exposes equivalence-preserving mutations
like delta conjugation. This module defines the Layer
class and how to canonicalize them into CanonLayers
"""

from __future__ import annotations
from typing import Callable, Dict, Sequence, Set
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from category.morphism import Knit
from category.object import PrimitiveObject
from common.common import Dir, Sign
from fig_gen.latex import Latex
from layer.layer_emit import LayerEmit


class Layer(Latex):
    """Layers are a box with a braid
    above and below
    """

    def __init__(self, left: int, middle: Knit, right: int) -> None:
        self.__left = left
        self.__middle = middle
        self.__right = right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Layer):
            return False
        return self.left() == other.left() and self.middle() == other.middle()

    def identity_emit(self) -> LayerEmit:
        """Constructs the identity LayerEmit for
        this layer's above and below strands

        Returns:
            LayerEmit: identity emit
        """
        return LayerEmit(self.n_below(), self.n_above())

    def copy(self, copied_object_dict: Dict[PrimitiveObject, PrimitiveObject]) -> Layer:
        """Copies the layer.

        Args:
            copied_object_dict (Dict[PrimitiveObject, PrimitiveObject]): Dictionary
            of already-copied primitives to maintain connections

        Returns:
            Layer: copy of this layer
        """
        l = Layer(self.left(), self.middle().copy(copied_object_dict), self.right())
        return l

    def __repr__(self) -> str:
        return f"Layer({self.__left}:{repr(self.__middle)}):{self.__right}"

    def n_above(self) -> int:
        """Calculates how many strands are above
        this layer

        Returns:
            int: Number of strands above this layer
        """
        return self.__left + len(self.__middle.outs()) + self.__right

    def n_below(self) -> int:
        """Calculates how many strands are below
        this layer

        Returns:
            int: Number of strands below this layer
        """
        return self.__left + len(self.__middle.ins()) + self.__right

    def left(self) -> int:
        """Getter

        Returns:
            int: Count of identity strands left of the box
        """
        return self.__left

    def right(self) -> int:
        """Getter

        Returns:
            int: Count of identity strands right of the box
        """
        return self.__right

    def middle(self) -> Knit:
        """Getter

        Returns:
            Knit: Box that the layer surrounds
        """
        return self.__middle

    def macro_subset(self) -> Set[int]:
        """Gets the macro subbraid (identity
        braids and the primary loop)'s braid
        indices for above this box

        Returns:
            Set[int]: macro subbraid indices
        """
        keep = set()
        for i in range(self.n_above()):
            if i < self.__left:
                keep.add(i)
            elif i >= self.__left + len(self.__middle.outs()):
                keep.add(i)
        keep.add(self.__left + self.__middle.primary_index())

        return keep

    def macro_subbraid(self, above: Braid) -> Braid:
        """Computes the above macro subbraid of this
        layer, given the above braid

        Args:
            above (Braid): above braid

        Returns:
            Braid: macro subbraid of above
        """
        return above.subbraid(self.macro_subset())

    def primary_twists(self) -> int:
        """Returns the number of times
        (possibly negative) that the
        box's primary loop has been
        twisted

        Returns:
            int: number of times the loop
            has been twisted
        """
        return self.__middle.primary().twists()

    def delta(self, sign: Sign) -> LayerEmit:
        """Delta conjugates the box

        Args:
            sign (Sign): Sign of the
            twist (and the delta) above
            the box

        Returns:
            LayerEmit: Emitted braids from
            this op
        """
        emit = self.identity_emit()

        self.__middle.flip()
        i = self.__left
        n = len(self.__middle.outs())
        for j in range(n):
            o = self.__middle.outs()[j]
            o.twist(sign.pos())
        for j in range(i, i + n):
            # take strand i to index j
            for k in range(j - 1, i - 1, -1):
                emit.emit_above(BraidGenerator(k, sign.pos()))

        m = len(self.__middle.ins())
        for j in range(m):
            o = self.__middle.ins()[j]
            o.twist(not sign.pos())
        for j in range(i + m - 1, i - 1, -1):
            # take strand i to index j
            for k in range(i, j):
                emit.emit_below(BraidGenerator(k, not sign.pos()))

        return emit

    def sigma_conj(self, i: int, sign: Sign) -> LayerEmit:
        """Performs the sigma conjugation rule on either
        side of this layer's box

        Args:
            i (int): index of swap in macro subspace
            sign (Sign): sign of sigma on top of box

        Raises:
            ValueError: i is too near the box

        Returns:
            LayerEmit: Emitted braids from
            this op
        """
        if i in [self.__left - 1, self.__left]:
            raise ValueError

        if i < self.__left - 1:
            above_i = i
            below_i = i
        else:
            above_i = i + len(self.__middle.outs()) - 1
            below_i = i + len(self.__middle.ins()) - 1

        emit = self.identity_emit()
        emit.emit_above(BraidGenerator(above_i, sign.pos()))
        emit.emit_below(BraidGenerator(below_i, not sign.pos()))

        return emit

    def underline_conj(self, d: Dir, above: bool) -> LayerEmit:
        """Performs the underline conj rule on either side
        of this layer's box

        Args:
            dir (Dir): Original location of the strand w.r.t.
            the box (was to the "dir" of the box)
            above (bool): Whether the strand goes above
            the box's inputs and outputs or not

        Returns:
            LayerEmit: Emitted braids from
            this op
        """
        i = self.__left
        n = len(self.__middle.outs())
        m = len(self.__middle.ins())

        emit = self.identity_emit()
        match d.right():
            case False:
                sign = not above
                for j in range(i - 1, i + n - 1):
                    emit.emit_above(BraidGenerator(j, sign))

                sign = not sign
                for j in range(i - 1, i + m - 1):
                    emit.emit_below(BraidGenerator(j, sign))

                self.__left -= 1
            case True:
                sign = above
                for j in range(i + n - 1, i - 1, -1):
                    emit.emit_above(BraidGenerator(j, sign))

                sign = not sign
                for j in range(i + m - 1, i - 1, -1):
                    emit.emit_below(BraidGenerator(j, sign))

                self.__left += 1

        return emit

    def flip_vertical(self) -> Layer:
        """Returns a Layer that represents this
        layer flipped upside down (not rotated,
        instead reflected)

        Returns:
            Layer: flipped layer
        """
        return Layer(self.left(), self.middle().flip_vertical(), self.right())

    def flip_macro(self, below: Braid) -> LayerEmit:
        """Does the macro substep of canonicalization
        on this layer while "facing upside down"

        Args:
            below (Braid): below braid, not flipped yet

        Returns:
            LayerEmit: layer that's equivalent to this
            layer in a looking-down canonical form
        """
        upside_down = self.flip_vertical()
        emit = upside_down.macro_step(below.flip_vertical())
        return emit.flip_vertical()

    def canonicalize(self, above: Braid) -> LayerEmit:
        """Canonicalizes this layer, mutating
        it in place. Does not do any braid canonicalization

        Args:
            above (Braid): braid that's above
            this layer (for macro)

        Returns:
            LayerEmit: Emitted braids from
            this op
        """
        emit = self.macro_step(above)
        emit.extend(self.delta_step())
        return emit

    def delta_step(self) -> LayerEmit:
        """Performs the delta step of the algorithm
        on this layer, mutating it in place

        Returns:
            LayerEmit: Emitted braids from
            this op
        """
        emit = self.identity_emit()
        while self.primary_twists() != 0:
            sign = self.primary_twists() < 0
            emit.extend(self.delta(Sign(sign)))
        return emit

    def macro_step(self, above: Braid) -> LayerEmit:
        """Performs the macro step of the algorithm
        on this layer, mutating it in place

        Returns:
            LayerEmit: Emitted braids from
            this op
        """
        emit = self.identity_emit()
        for gen in self.macro_subbraid(above):
            if gen.i() == self.left() - 1:
                emit.extend(self.underline_conj(Dir(False), gen.pos()))
            elif gen.i() == self.left():
                emit.extend(self.underline_conj(Dir(True), not gen.pos()))
            else:
                emit.extend(self.sigma_conj(gen.i(), Sign(not gen.pos())))
        return emit

    def fuzz_layer(self, rng: Callable[[], float], steps: int) -> LayerEmit:
        """Fuzzes this layer by performing layer operations; doesn't
        fuzz either braid

        Args:
            rng (Callable[[], float]): Random number generator
            steps (int): Number of mutations to attempt

        Returns:
            LayerEmit: Emitted braids from this
            op
        """
        emit = self.identity_emit()
        num_macro_strands = self.n_below() - len(self.__middle.ins()) + 1
        for _ in range(steps):
            r = rng()
            if r < 0.3:
                # sigma conj
                i = int(rng() * (num_macro_strands - 1))
                if i in [self.__left, self.__left - 1]:
                    continue  # can't sigma conj here
                emit.extend(self.sigma_conj(i, Sign(rng() < 0.5)))
            elif r < 0.85:
                # underline conj
                right = rng() < 0.5
                # Boundary conditions
                if not right:
                    if self.__left == 0:
                        continue
                else:
                    if self.__left + len(self.__middle.ins()) == self.n_below():
                        continue

                emit.extend(self.underline_conj(Dir(right), rng() < 0.5))
            else:
                # delta conj
                emit.extend(self.delta(Sign(rng() < 0.5)))
        return emit

    def to_latex(self, x: int, y: int, context: Sequence[PrimitiveObject]) -> str:
        str_latex = ""
        box_context_in = context[self.__left : self.__left + len(self.__middle.ins())]
        str_latex += self.__middle.to_latex(x + self.__left, y, box_context_in)
        box_height = self.__middle.latex_height()
        for i in range(self.__left):
            o = context[i]
            (r, g, b) = o.color()
            for j in range(box_height):
                str_latex += (
                    f"\\identity{{{x+i}}}{{{y+j}}}{{{0}}}{{{o}}}{{{r}}}{{{g}}}{{{b}}}\n"
                )

        for i in range(self.__left + len(self.__middle.ins()), len(context)):
            o = context[i]
            (r, g, b) = o.color()
            for j in range(box_height):
                str_latex += f"""\\identity{{{
                    x+i if j == 0 else
                    x + i + len(self.__middle.outs()) - len(self.__middle.ins())}}}{{{y+j}}}
{{{len(self.__middle.outs()) - len(self.__middle.ins()) if j == 0 else 0}}}
{{{o}}}{{{r}}}{{{g}}}{{{b}}}\n"""
        return str_latex

    def latex_height(self) -> int:
        return self.__middle.latex_height()

    def context_out(
        self, context: Sequence[PrimitiveObject]
    ) -> Sequence[PrimitiveObject]:
        box_context_in = context[self.__left : self.__left + len(self.__middle.ins())]
        return (
            list(context[: self.__left])
            + list(self.__middle.context_out(box_context_in))
            + list(context[self.__left + len(self.__middle.ins()) :])
        )
