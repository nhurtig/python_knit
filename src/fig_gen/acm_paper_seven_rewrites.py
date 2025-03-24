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


def b1() -> None:
    """Draws two swaps canceling
    each other out"""
    reset_colors()
    b = Braid(2)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(0, False))
    context = [Carrier(0) for _ in range(2)]
    b.compile_latex("B1First", context)

    reset_colors()
    w = Word(2)
    w.draw_preamble(2)
    b = Braid(2)
    context = [Carrier(0) for _ in range(2)]
    w.append_braid(b)
    w.compile_latex("B1Second", context)


def b3() -> None:
    """Draws the yang-baxter equation"""
    reset_colors()
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    context = [Carrier(0) for _ in range(3)]
    b.compile_latex("B3First", context)

    reset_colors()
    b = Braid(3)
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    context = [Carrier(0) for _ in range(3)]
    b.compile_latex("B3second", context)


def b2() -> None:
    """Draws the vertical morphism slide-past-each-other
    move through 2 generators on 4 braids"""
    reset_colors()
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, True))
    context = [Carrier(0) for _ in range(4)]
    b.compile_latex("B2First", context)

    reset_colors()
    b = Braid(4)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, True))
    context = [Carrier(0) for _ in range(4)]
    b.compile_latex("B2second", context)


def l1() -> None:
    """Draws an example of the sigma underline rule"""
    reset_colors()
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(3)]
    w = Word(3)
    k = Knit(Bed(True), Dir(True), list(context[:2]), [Carrier(0) for _ in range(2)])
    l = Layer(0, k, 1)
    w.append_layer(l)

    w.draw_postamble(2)
    w.draw_preamble(2)
    w.compile_latex("L1First", context)

    w.layer_at(0).underline_conj(Dir(True), True)

    w.compile_latex("L1Second", context)


def l2() -> None:
    """Draws an example of the sigma conjugation rule"""
    reset_colors()
    context = [Carrier(0) for _ in range(4)]
    w = Word(4)
    k = Knit(Bed(True), Dir(True), context[:2], [Carrier(0) for _ in range(2)])
    l = Layer(0, k, 2)
    w.append_layer(l)

    w.compile_latex("L2First", context)

    w.layer_at(0).sigma_conj(1, Sign(True))

    w.compile_latex("L2Second", context)


def l3() -> None:
    """Draws an example of the delta conjugation rule"""
    reset_colors()
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(3)]
    w = Word(3)
    l = Layer(
        0, Knit(Bed(True), Dir(True), list(context), [Carrier(0) for _ in range(3)]), 0
    )
    w.append_layer(l)
    w.draw_postamble(3)
    w.draw_preamble(3)

    w.compile_latex("L3First", context)
    w.layer_at(0).delta(Sign(True))
    w.compile_latex("L3Second", context, True)

def s1() -> None:
    """Draws an example of the box swap rule"""
    reset_colors()
    context = [Carrier(0) for _ in range(4)]
    lay1 = Layer(
        0, Knit(Bed(True), Dir(True), context[:2], [Carrier(0) for _ in range(2)]), 2
    )
    lay2 = Layer(
        2, Knit(Bed(True), Dir(True), context[2:], [Carrier(0) for _ in range(2)]), 0
    )

    w = Word(4)
    w.append_layer(lay1)
    w.append_layer(lay2)
    w.compile_latex("S1First", context)

    w = Word(4)
    w.append_layer(lay2)
    w.append_layer(lay1)
    w.compile_latex("S1Second", context)

def make_all_seven_diagram_rules() -> None:
    """Draws all the diagram rules for the paper"""
    l1()
    l2()
    l3()
    b1()
    b2()
    b3()
    s1()
