"""Layers are a box and their braids above and below. Their
interface exposes equivalence-preserving mutations
like delta conjugation. This module defines the Layer
class and how to canonicalize them into CanonLayers
"""

from typing import Sequence
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from braid.canon.canon_braid import CanonBraid
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

    def __repr__(self) -> str:
        return f"Layer({self.__middle}:{self.__above})"

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

    def layer_canon(self) -> CanonBraid:
        """Canonicalizes the above braid
        and returns it. Can't mutate in
        place because canon braids and
        non-canon braids are different.

        Returns:
            CanonBraid: Canonical form of
            the above braid.
        """
        return CanonBraid(self.__above)

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
                str_latex += f"""\\identity{{{x+i}}}{{{y+j}}}
{{{len(self.__middle.outs()) - len(self.__middle.ins())}}}{{{o}}}{{{r}}}{{{g}}}{{{b}}}\n"""

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


class CanonLayer(Latex):
    """CanonLayer is a class meant to
    capture the canonical form of a layer.
    It isn't meant to be mutated; it only
    stores the above braid
    """

    def __init__(self, layer: Layer) -> None:
        CanonLayer.delta_step(layer)
        CanonLayer.macro_step(layer)
        self.__left = layer.left()
        self.__middle = layer.middle()
        self.__above = layer.layer_canon()

    def __repr__(self) -> str:
        return f"CanonLayer({self.__middle}:{self.__above})"

    @staticmethod
    def delta_step(layer: Layer) -> None:
        """Performs the delta step of the algorithm
        on the layer, mutating it in place

        Args:
            layer (Layer): Layer to be twisted
        """
        while layer.primary_twists() != 0:
            sign = layer.primary_twists() < 0
            layer.delta(Sign(sign))

    @staticmethod
    def macro_step(layer: Layer) -> None:
        """Performs the macro step of the algorithm
        on the layer, mutating it in place

        Args:
            layer (Layer): Layer to be macro
            braided
        """
        for gen in layer.macro_subbraid():
            if gen.i() == layer.left() - 1:
                layer.underline_conj(Dir(False), gen.pos())
            elif gen.i() == layer.left():
                layer.underline_conj(Dir(True), not gen.pos())
            else:
                layer.sigma_conj(gen.i(), Sign(not gen.pos()))

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
                str_latex += f"""\\identity{{{x+i}}}{{{y+j}}}
{{{len(self.__middle.outs()) - len(self.__middle.ins())}}}{{{o}}}{{{r}}}{{{g}}}{{{b}}}\n"""

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
