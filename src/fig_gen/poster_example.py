"""Collection of functions for making large
random examples for the poster"""

import random
from braid.braid import Braid
from category.morphism import Knit
from category.object import Carrier, Loop
from common.common import Bed, Dir
from fig_gen.color import reset_colors
from layer.layer import Layer
from layer.word import Word

MIN_INS: int = 0
MAX_INS: int = 4
MIN_OUTS: int = 1
MAX_OUTS: int = 4
MAX_LETTERS_PER_WORD: int = 8
NUM_BOXES: int = 5

dummy_loop = Loop(0)  # so colors don't get messed up

random.seed(31)


def draw_poster_word() -> None:
    """Draws a random word fit for the poster."""
    reset_colors()
    w = Word()
    l11 = Loop(0)
    l11.twist(True)
    c11 = Carrier(0)
    k1 = Knit(Bed(True), Dir(True), [None], [l11, c11])
    b1 = Braid.str_to_braid(2, "A")
    l1 = Layer(0, k1, 0)
    w.append_layer(l1)
    w.append_braid(b1)

    l21 = Loop(0)
    l21.twist(False)
    l22 = Loop(0)
    c21 = Carrier(0)
    k2 = Knit(Bed(False), Dir(True), [c11, l11], [l21, l22, c21])
    b2 = Braid.str_to_braid(3, "AAB")
    l2 = Layer(0, k2, 0)
    w.append_layer(l2)
    w.append_braid(b2)

    l31 = Loop(0)
    l31.twist(True)
    c31 = Carrier(0)
    l32 = Loop(0)
    l32.twist(True)
    l32.twist(True)
    k3 = Knit(Bed(True), Dir(True), [c21, l22], [l31, c31, l32])
    b3 = Braid.str_to_braid(4, "ABCbCBC")
    l3 = Layer(1, k3, 0)
    w.append_layer(l3)
    w.append_braid(b3)

    l41 = Loop(0)
    l41.twist(True)
    k4 = Knit(Bed(True), Dir(False), [l31, l21, c31], [None, l41, None, None])
    b4 = Braid.str_to_braid(2, "aa")
    l4 = Layer(0, k4, 1)
    w.append_layer(l4)
    w.append_braid(b4)

    w.compile_latex("poster_word", [])
    w.canonicalize()
    w.compile_latex("poster_word_canon", [])
