"""Layers are a box and their braids above and below. Their
interface exposes equivalence-preserving mutations
like delta conjugation. This module defines the Layer
class and how to canonicalize them into CanonLayers
"""

from __future__ import annotations
from typing import Callable, Dict, Sequence
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from category.morphism import Knit
from category.object import PrimitiveObject
from common.common import Dir, Sign
from fig_gen.latex import Latex


class Layer(Latex):
    """Layers are a box with a braid
    above and below
    """

    def __init__(self, left: int, middle: Knit, above: Braid, below: Braid) -> None:
        self.__left = left
        self.__middle = middle
        # TODO: check that n() of above, below match left, mid, right
        self.__above = above
        self.__below = below

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Layer):
            return False
        return (
            self.left() == other.left()
            and self.middle() == other.middle()
            and self.above() == other.above()
        )

    def copy(self, below: Braid, copied_object_dict: Dict[PrimitiveObject, PrimitiveObject]) -> tuple[Layer, Braid]:
        """Copies the layer. Takes the below braid
        of the copied layer and returns the copy of
        the above braid. This is so Words can have their
        Layers share braids.

        Args:
            below (Braid): Already-copied below braid

        Returns:
            tuple[Layer, Braid]: Copied layer, that layers'
            above braid
        """
        above_copy = self.__above.copy()
        l = Layer(self.left(), self.middle().copy(copied_object_dict), above_copy, below)
        return (l, above_copy)

    def __repr__(self) -> str:
        return f"Layer({repr(self.__middle)}:{repr(self.__above)})"

    def left(self) -> int:
        """Getter

        Returns:
            int: Count of identity strands left of the box
        """
        return self.__left

    def middle(self) -> Knit:
        """Getter

        Returns:
            Knit: Box that the layer surrounds
        """
        return self.__middle

    def macro_subbraid(self) -> Braid:
        """Gets the macro subbraid (identity
        braids and the primary loop) above
        the box from this layer

        Returns:
            Braid: macro subbraid
        """
        keep = set()
        for i in range(self.__above.n()):
            if i < self.__left:
                keep.add(i)
            elif i >= self.__left + len(self.__middle.outs()):
                keep.add(i)
        keep.add(self.__left + self.__middle.primary_index())

        return self.__above.subbraid(keep)

    def below(self) -> Braid:
        """Getter

        Returns:
            Braid: Below braid
        """
        return self.__below

    def above(self) -> Braid:
        """Getter

        Returns:
            Braid: above braid
        """
        return self.__above

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

    def delta(self, sign: Sign) -> None:
        """Delta conjugates the box

        Args:
            sign (Sign): Sign of the
            twist (and the delta) above
            the box
        """
        self.__middle.flip()
        i = self.__left
        n = len(self.__middle.outs())
        for j in range(n):
            o = self.__middle.outs()[j]
            o.twist(sign.pos())
        for j in range(i, i + n):
            # take strand i to index j
            for k in range(j - 1, i - 1, -1):
                self.__above.prepend(BraidGenerator(k, sign.pos()))

        m = len(self.__middle.ins())
        for j in range(m):
            o = self.__middle.ins()[j]
            o.twist(not sign.pos())
        for j in range(i + m - 1, i - 1, -1):
            # take strand i to index j
            for k in range(i, j):
                self.__below.append(BraidGenerator(k, not sign.pos()))

    def sigma_conj(self, i: int, sign: Sign) -> None:
        """Performs the sigma conjugation rule on either
        side of this layer's box

        Args:
            i (int): index of swap in macro subspace
            sign (Sign): sign of sigma on top of box

        Raises:
            ValueError: i is too near the box
        """
        if i in [self.__left - 1, self.__left]:
            raise ValueError

        if i < self.__left - 1:
            above_i = i
            below_i = i
        else:
            above_i = i + len(self.__middle.outs()) - 1
            below_i = i + len(self.__middle.ins()) - 1

        self.__above.prepend(BraidGenerator(above_i, sign.pos()))
        self.__below.append(BraidGenerator(below_i, not sign.pos()))

    def underline_conj(self, d: Dir, above: bool) -> None:
        """Performs the underline conj rule on either side
        of this layer's box

        Args:
            dir (Dir): Original location of the strand w.r.t.
            the box (was to the "dir" of the box)
            above (bool): Whether the strand goes above
            the box's inputs and outputs or not
        """
        i = self.__left
        n = len(self.__middle.outs())
        m = len(self.__middle.ins())

        match d.right():
            case False:
                sign = not above
                for j in range(i - 1, i + n - 1):
                    self.__above.prepend(BraidGenerator(j, sign))

                sign = not sign
                for j in range(i - 1, i + m - 1):
                    self.__below.append(BraidGenerator(j, sign))

                self.__left -= 1
            case True:
                sign = above
                for j in range(i + n - 1, i - 1, -1):
                    self.__above.prepend(BraidGenerator(j, sign))

                sign = not sign
                for j in range(i + m - 1, i - 1, -1):
                    self.__below.append(BraidGenerator(j, sign))

                self.__left += 1

    def flip_vertical(self) -> Layer:
        """Returns a Layer that represents this
        layer flipped upside down (not rotated,
        instead reflected)

        Returns:
            Layer: flipped layer
        """
        return Layer(self.left(), self.middle().flip_vertical(), self.below().flip_vertical(), self.above().flip_vertical())

    def flip_canonicalize(self) -> Layer:
        """Canonicalizes this layer while
        "facing upside down"

        Returns:
            Layer: layer that's equivalent to this
            layer in a looking-down canonical form
        """
        upside_down = self.flip_vertical()
        # upside_down.canonicalize()
        # TODO: revert to make layerCanon happen?
        upside_down.macro_step()
        return upside_down.flip_vertical()

    def flip_canonicalize_delta(self) -> Layer:
        """Canonicalizes this layer while
        "facing upside down"

        Returns:
            Layer: layer that's equivalent to this
            layer in a looking-down canonical form
        """
        # TODO: this is terrible. Change it back
        upside_down = self.flip_vertical()
        # upside_down.canonicalize()
        # TODO: revert to make layerCanon happen?
        upside_down.delta_step()
        return upside_down.flip_vertical()


    def canonicalize(self) -> None:
        """Canonicalizes this layer, mutating
        it in place"""
        self.delta_step()
        self.macro_step()
        self.layer_canon()

    def delta_step(self) -> None:
        """Performs the delta step of the algorithm
        on this layer, mutating it in place
        """
        while self.primary_twists() != 0:
            sign = self.primary_twists() < 0
            self.delta(Sign(sign))

    def macro_step(self) -> None:
        """Performs the macro step of the algorithm
        on this layer, mutating it in place
        """
        for gen in self.macro_subbraid():
            if gen.i() == self.left() - 1:
                self.underline_conj(Dir(False), gen.pos())
            elif gen.i() == self.left():
                self.underline_conj(Dir(True), not gen.pos())
            else:
                self.sigma_conj(gen.i(), Sign(not gen.pos()))

    def layer_canon(self) -> None:
        """Canonicalizes the above braid of this
        layer, mutating it in place"""
        self.__above.reset_to(self.__above.canon())

    def fuzz_layer(self, rng: Callable[[], float], steps: int) -> None:
        """Fuzzes this layer by performing layer operations; doesn't
        fuzz either braid

        Args:
            rng (Callable[[], float]): Random number generator
            steps (int): Number of mutations to attempt
        """
        num_macro_strands = self.__below.n() - len(self.__middle.ins()) + 1
        for _ in range(steps):
            r = rng()
            if r < 0.3:
                # sigma conj
                i = int(rng() * (num_macro_strands - 1))
                if i in [self.__left, self.__left - 1]:
                    continue  # can't sigma conj here
                self.sigma_conj(i, Sign(rng() < 0.5))
            elif r < 0.85:
                # underline conj
                right = rng() < 0.5
                # Boundary conditions
                if not right:
                    if self.__left == 0:
                        continue
                else:
                    if self.__left + len(self.__middle.ins()) == self.__below.n():
                        continue

                self.underline_conj(Dir(right), rng() < 0.5)
            else:
                # delta conj
                self.delta(Sign(rng() < 0.5))

    def fuzz_braid(self, rng: Callable[[], float], steps: int) -> None:
        """Fuzzes the above braid using its fuzzing algorithm

        Args:
            rng (Callable[[], float]): Random number generator
            steps (int): Number of mutations
        """
        self.__above.fuzz(rng, steps)

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

        str_latex += self.__above.to_latex(
            x,
            y + box_height,
            list(context[: self.__left])
            + list(self.__middle.context_out(box_context_in))
            + list(context[self.__left + len(self.__middle.ins()) :]),
        )
        return str_latex

    def latex_height(self) -> int:
        return self.__middle.latex_height() + self.__above.latex_height()

    def context_out(
        self, context: Sequence[PrimitiveObject]
    ) -> Sequence[PrimitiveObject]:
        box_context_in = context[self.__left : self.__left + len(self.__middle.ins())]
        return self.__above.context_out(
            list(context[: self.__left])
            + list(self.__middle.context_out(box_context_in))
            + list(context[self.__left + len(self.__middle.ins()) :])
        )
