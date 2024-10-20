from typing import Sequence
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from category.morphism import Knit
from category.object import Carrier, PrimitiveObject
from color import reset_colors
from common import Bed, Dir, Sign
from layer.layer import Layer
from word import Word

def sigma_cancel() -> None:
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
    reset_colors()
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(3)]
    w = Word()
    b = Braid(3)
    k = Knit(Bed(True), Dir(True), [], [])
    l = Layer(0, k, b, Braid(3))
    w.append_layer(l)
    k = Knit(Bed(True), Dir(True), list(context[:2]), [Carrier(0) for _ in range(2)])
    l = Layer(0, k, Braid(3), b)
    w.append_layer(l)

    w.compile_latex("sigma_underline_before", context)

    l.underline_conj(Dir(True), True)

    w.compile_latex("sigma_underline_after", context)

def sigma_conj() -> None:
    reset_colors()
    context = [Carrier(0) for _ in range(3)]
    w = Word()
    b = Braid(3)
    l = Layer(0, Knit(Bed(True), Dir(True), [], []), b, Braid(3))
    w.append_layer(l)
    k = Knit(Bed(True), Dir(True), [context[0]], [Carrier(0)])
    l = Layer(0, k, Braid(3), b)
    w.append_layer(l)

    w.compile_latex("sigma_conj_before", context)

    l.sigma_conj(1, Sign(True))

    w.compile_latex("sigma_conj_after", context)

def delta_conj() -> None:
    reset_colors()
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(3)]
    w = Word()
    b = Braid(3)
    w.append_layer(Layer(0, Knit(Bed(True), Dir(True), [], []), b, Braid(3)))
    l = Layer(0, Knit(Bed(True), Dir(True), list(context), [Carrier(0) for _ in range(3)]), Braid(3), b)
    w.append_layer(l)

    w.compile_latex("delta_conj_before", context)
    l.delta(Sign(True))
    w.compile_latex("delta_conj_after", context)
