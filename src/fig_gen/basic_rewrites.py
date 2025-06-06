"""Draws examples of the axiomatic rewrite rules"""

from typing import Sequence
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from category.morphism import Knit
from category.object import Carrier, PrimitiveObject
from fig_gen.color import reset_colors
from common.common import Bed, Dir, Sign
from layer.layer import Layer
from layer.word import Word


def sigma_cancel() -> None:
    """Draws two swaps canceling
    each other out"""
    reset_colors()
    b = Braid(2)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(0, False))
    context = [Carrier(0) for _ in range(2)]
    b.compile_latex("sigmacancel_before", context)

    reset_colors()
    b = Braid(2)
    context = [Carrier(0) for _ in range(2)]
    b.compile_latex("sigmacancel_after", context)


def yang_baxter() -> None:
    """Draws the yang-baxter equation"""
    reset_colors()
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    context = [Carrier(0) for _ in range(3)]
    b.compile_latex("yangbaxter_before", context)

    reset_colors()
    b = Braid(3)
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    context = [Carrier(0) for _ in range(3)]
    b.compile_latex("yangbaxter_after", context)


def morph_swap() -> None:
    """Draws the vertical morphism slide-past-each-other
    move through 2 generators on 4 braids"""
    reset_colors()
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, True))
    context = [Carrier(0) for _ in range(4)]
    b.compile_latex("morph_swap_before", context)

    reset_colors()
    b = Braid(4)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, True))
    context = [Carrier(0) for _ in range(4)]
    b.compile_latex("morph_swap_after", context)


def sigma_underline() -> None:
    """Draws an example of the sigma underline rule"""
    reset_colors()
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(3)]
    w = Word(3)
    k = Knit(Bed(True), Dir(True), list(context[:2]), [Carrier(0) for _ in range(2)])
    l = Layer(0, k, 1)
    w.append_layer(l)

    w.draw_postamble(2)
    w.draw_preamble(2)

    w.compile_latex("sigma_underline_before", context)

    w.layer_at(0).underline_conj(Dir(True), True)

    w.compile_latex("sigma_underline_after", context)


def sigma_conj() -> None:
    """Draws an example of the sigma conjugation rule"""
    reset_colors()
    context = [Carrier(0) for _ in range(3)]
    w = Word(3)
    k = Knit(Bed(True), Dir(True), [context[0]], [Carrier(0)])
    l = Layer(0, k, 2)
    w.append_layer(l)

    w.compile_latex("sigma_conj_before", context)

    w.layer_at(0).sigma_conj(1, Sign(True))

    w.compile_latex("sigma_conj_after", context)


def delta_conj(num_amble: int = 3, n=3) -> None:
    """Draws an example of the delta conjugation rule"""
    reset_colors()
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(n)]
    w = Word(n)
    l = Layer(
        0, Knit(Bed(True), Dir(True), list(context), [Carrier(0) for _ in range(n)]), 0
    )
    w.append_layer(l)

    w.draw_postamble(num_amble)
    w.draw_preamble(num_amble)
    w.compile_latex(f"delta_conj_before{'' if num_amble == 3 else num_amble}", context)
    w.layer_at(0).delta(Sign(True))
    w.compile_latex(f"delta_conj_after{'' if num_amble == 3 else num_amble}", context, True)
    w.layer_at(0).delta(Sign(True))
    w.compile_latex(f"delta_conj_double{'' if num_amble == 3 else num_amble}", context, True)
