from typing import Sequence
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from category.morphism import Knit
from category.object import Carrier, Loop, PrimitiveObject
from color import reset_colors, set_ghosting
from common import Bed, Dir, Sign
from layer.layer import Layer
from word import CanonWord, Word


def init_word() -> tuple[Word, Layer, Layer, Sequence[PrimitiveObject]]:
    reset_colors(reset_ghosting=False)
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(4)]
    w = Word()
    b = Braid(4)
    l1 = Layer(0, Knit(Bed(True), Dir(True), [], []), b, Braid(4))
    w.append_layer(l1)
    loop = Loop(0)
    loop.twist(True)
    above_braid = Braid(4)
    above_braid.append(BraidGenerator(2, False))
    above_braid.append(BraidGenerator(1, False))
    above_braid.append(BraidGenerator(0, True))
    l = Layer(
        0,
        Knit(Bed(True), Dir(True), list(context[:2]), [loop, Carrier(0)]),
        above_braid,
        b,
    )
    w.append_layer(l)
    return (w, l1, l, context)


def display_word_steps() -> None:
    (w, _, layer, context) = init_word()
    w.compile_latex("full_0", context)

    layer.delta(Sign(False))
    w.compile_latex("full_1", context)

    reset_colors()
    set_ghosting([0, 1, 5])

    (w, l1, layer, context) = init_word()
    layer.delta(Sign(False))
    w.compile_latex("full_1_ghost", context)

    layer.sigma_conj(1, Sign(True))
    w.compile_latex("full_2_ghost", context)

    layer.underline_conj(Dir(True), False)
    w.compile_latex("full_3_ghost", context)

    w_new = Word()
    w_new.append_layer(layer)
    CanonWord(w_new).compile_latex("full_4_ghost", l1.context_out(context))

    set_ghosting([])
    (w, l1, layer, context) = init_word()
    layer.delta(Sign(False))
    layer.sigma_conj(1, Sign(True))
    layer.underline_conj(Dir(True), False)
    w.compile_latex("full_3", context)
    w_new = Word()
    w_new.append_layer(layer)
    CanonWord(w_new).compile_latex("full_4", l1.context_out(context))
