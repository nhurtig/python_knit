"""Computes and draws a small
but complete (all rules
represented) canonicalization"""

from typing import Sequence, Tuple
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from category.morphism import Knit
from category.object import Carrier, Loop, PrimitiveObject
from fig_gen.color import reset_colors, set_ghosting
from common.common import Bed, Dir, Sign
from layer.layer import Layer
from layer.word import Word


def init_word() -> Tuple[Word, Sequence[PrimitiveObject]]:
    """Constructs a small word"""
    reset_colors(reset_ghosting=False)
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(4)]
    w = Word(4)
    # b = Braid(4)
    # l1 = Layer(0, Knit(Bed(True), Dir(True), [], []), b, Braid(4))
    # w.append_layer(l1)
    loop = Loop(0)
    loop.twist(True)
    above_braid = Braid(4)
    above_braid.append(BraidGenerator(2, False))
    above_braid.append(BraidGenerator(1, False))
    above_braid.append(BraidGenerator(0, True))
    l = Layer(0, Knit(Bed(True), Dir(True), list(context[:2]), [loop, Carrier(0)]), 2)
    w.append_layer(l)
    w.append_braid(above_braid)
    return (w, context)


def display_word_steps() -> None:
    """Displays each of the steps of the
    words' canonicalization, using
    ghosting to show the macro braid step"""
    (w, context) = init_word()
    w.compile_latex("full_0", context)

    w.layer_at(0).delta_step()
    # w.delta(0, Sign(False))
    # layer.delta(Sign(False))
    w.compile_latex("full_1", context)

    reset_colors()
    set_ghosting([0, 1, 5])

    (w, context) = init_word()
    w.layer_at(0).delta_step()
    w.compile_latex("full_1_ghost", context)

    w.layer_at(0).sigma_conj(1, Sign(True))
    w.compile_latex("full_2_ghost", context)

    w.layer_at(0).underline_conj(Dir(True), False)
    w.compile_latex("full_3_ghost", context)

    # layer.sigma_conj(1, Sign(True))
    # w.layer_at(0).macro_step()
    w.compile_latex("full_3_ghost", context)

    # layer.underline_conj(Dir(True), False)
    # w.compile_latex("full_3_ghost", context)

    w_new = w.copy()
    w_new.canonicalize()
    w_new.compile_latex("full_4_ghost", context)

    set_ghosting([])
    (w, context) = init_word()
    w.layer_at(0).delta_step()
    w.layer_at(0).macro_step()
    # layer.delta(Sign(False))
    # layer.sigma_conj(1, Sign(True))
    # layer.underline_conj(Dir(True), False)
    w.compile_latex("full_3", context)
    w.canonicalize()
    w.compile_latex("full_4", context)
