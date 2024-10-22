"""Collection of functions for making large
random examples for the poster"""

import random
from typing import Callable, Optional
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from category.morphism import Knit
from category.object import Carrier, Loop, PrimitiveObject
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

dummy_loop = Loop(0) # so colors don't get messed up

random.seed(31)

def random_word(num_boxes: int, rng: Callable[[], float]) -> Word:
    """Generates a random Word.

    Args:
        num_boxes (int): Number of boxes
        rng (random.Random): Thread-specific random number generator

    Returns:
        Word: Random layer
    """
    w = Word()
    prev_b = Braid(0)
    for _ in range(num_boxes):
        knit_ins = min(int(rng() * (MAX_INS - MIN_INS)) + MIN_INS, prev_b.n())
        knit_outs = int(rng() * (MAX_OUTS - MIN_OUTS)) + MIN_OUTS
        dummy_knit = Knit(
            Bed(rng() < 0.5),
            Dir(rng() < 0.5),
            # TODO: match knit structure
            [dummy_loop for _ in range(knit_ins)],
            [dummy_loop for _ in range(knit_outs)],
        )
        i = dummy_knit.primary_index()
        carrier_index = -1
        if knit_outs > 1:
            carrier_index = i
            while carrier_index == i:
                carrier_index = int(rng() * knit_outs)
        outs: list[Optional[PrimitiveObject]] = []
        for j in range(knit_outs):
            if j == carrier_index:
                outs.append(Carrier(0))
            else:
                l = Loop(0)
                twist_chance = 0.5
                if j == i:
                    twist_chance = 0.9
                twist_sign = rng() < 0.5
                while True:
                    if rng() < twist_chance:
                        l.twist(twist_sign)
                    else:
                        break
                outs.append(l)
        k = Knit(
            Bed(rng() < 0.5), Dir(rng() < 0.5), [dummy_loop for _ in range(knit_ins)], outs
        )

        left = int(rng() * (prev_b.n() - knit_ins))
        b = random_braid_word(
            prev_b.n() + knit_outs - knit_ins, int(rng() * MAX_LETTERS_PER_WORD), rng
        )
        w.append_layer(Layer(left, k, b, prev_b))
        prev_b = b

    # w.fuzz(rng, 3, 20)
    return w


def random_braid_word(n: int, length: int, rng: Callable[[], float]) -> Braid:
    """Generates a random braid word.

    Args:
        n (int): Number of strands
        length (int): Number of generators

    Returns:
        Braid: Random braid word
    """
    word = Braid(n)
    if n >= 2:
        for _ in range(length):
            i = int(rng() * (n - 1))  # generator index
            pos = rng() < 0.5
            word.append(BraidGenerator(i, pos))
    return word


def draw_poster_word() -> None:
    """Draws a random word fit for the poster."""
    reset_colors()
    w = Word()
    l11 = Loop(0)
    l11.twist(True)
    c11 = Carrier(0)
    k1 = Knit(Bed(True), Dir(True), [], [l11, c11])
    b1 = Braid.str_to_braid(2, "A")
    l1 = Layer(0, k1, b1, Braid(0))
    w.append_layer(l1)

    l21 = Loop(0)
    l21.twist(False)
    l22 = Loop(0)
    c21 = Carrier(0)
    k2 = Knit(Bed(False), Dir(True), [c11, l11], [l21, l22, c21])
    b2 = Braid.str_to_braid(3, "AAB")
    l2 = Layer(0, k2, b2, b1)
    w.append_layer(l2)

    l31 = Loop(0)
    l31.twist(True)
    c31 = Carrier(0)
    l32 = Loop(0)
    l32.twist(True)
    l32.twist(True)
    k3 = Knit(Bed(True), Dir(True), [c21, l22], [l31, c31, l32])
    b3 = Braid.str_to_braid(4, "ABCbCBC")
    l3 = Layer(1, k3, b3, b2)
    w.append_layer(l3)

    l41 = Loop(0)
    l41.twist(True)
    k4 = Knit(Bed(True), Dir(False), [l31, l21, c31], [l41])
    b4 = Braid.str_to_braid(2, "aa")
    l4 = Layer(0, k4, b4, b3)
    w.append_layer(l4)

    w.compile_latex("poster_word", [])