"""Tests braid word canonicalization
using fuzzing"""

import random
import math
from category.morphism import Knit
from category.object import Loop
from common.common import Bed, Dir
from layer.layer import Layer
from layer.word import Word

NUM_TESTS = 50
UPDATE_FREQ = 5
RUN_FOREVER = False  # overrides NUM_TESTS when True
N_AVERAGE = 10  # number of strands in the middle braid
AVERAGE_OUTIN = 2.5  # number of inputs/outputs of top/bottom box
LAYER_MUTATIONS_AVERAGE = 15
BRAID_MUTATIONS_AVERAGE = 100
AVERAGE_TWISTS = 2

BASE_SEED = 0

random.seed(BASE_SEED)
rng = random.random


def geometric(average: float) -> int:
    """Samples from a geometric distribution

    Args:
        average (float): Expected value

    Returns:
        int: Sample
    """
    u = rng()
    num: float = math.log(1 - u)
    denom: float = math.log(1 - (1 / (average + 1)))
    return int(num / denom)


def random_swappable_word() -> Word:
    """Generates a random swappable word with 3 layers;
    the last 2 layers can be swapped

    Returns:
        Word: random swappable word
    """
    n = 0
    bottom_outs = 1
    top_ins = 1
    bottom_ins = 1
    bottom_index = 0
    top_index = 0
    while (
        bottom_index + bottom_outs > n  # too big
        or top_index + top_ins > n  # too big
        or (
            bottom_index < top_index + top_ins
            and top_index < bottom_index + bottom_outs  # overlap
        )
        or n - bottom_outs + bottom_ins < 2  # bottomest box needs 2 outputs
    ):
        n = geometric(N_AVERAGE - 4) + 4  # at least 4 strands
        bottom_ins = geometric(AVERAGE_OUTIN)
        bottom_outs = geometric(AVERAGE_OUTIN - 2) + 2  # ensure >= 2 out
        top_ins = geometric(AVERAGE_OUTIN - 2) + 2  # ensure >= 2 in (for vertical flip)
        top_outs = geometric(AVERAGE_OUTIN - 2) + 2  # so we can canonicalize
        bottom_index = int(rng() * n)
        top_index = int(rng() * n)

    context_in = [Loop(i) for i in range(n - bottom_outs + bottom_ins)]
    bottomest_box = Knit(Bed(rng() < 0.5), Dir(rng() < 0.5), [], context_in)
    bottom_box = Knit(
        Bed(rng() < 0.5),
        Dir(rng() < 0.5),
        context_in[bottom_index : bottom_index + bottom_ins],
        [Loop(i + n - bottom_outs + bottom_ins) for i in range(bottom_outs)],
    )
    top_box = Knit(
        Bed(rng() < 0.5),
        Dir(rng() < 0.5),
        (
            context_in[top_index : top_index + top_ins]
            if top_index < bottom_index
            else context_in[
                top_index
                - bottom_outs
                + bottom_ins : top_index
                - bottom_outs
                + bottom_ins
                + top_ins
            ]
        ),
        [Loop(i + n * n) for i in range(top_outs)],
    )
    for loop in bottom_box.outs() + bottom_box.ins() + top_box.outs():
        pos = rng() < 0.5
        for _ in range(geometric(AVERAGE_TWISTS)):
            loop.twist(pos)

    bottomest_layer = Layer(0, bottomest_box, 0)
    bottom_layer = Layer(bottom_index, bottom_box, n - bottom_index - bottom_outs)
    top_layer = Layer(top_index, top_box, n - top_index - top_ins)

    word = Word(0)
    word.append_layer(bottomest_layer)
    word.append_layer(bottom_layer)
    word.append_layer(top_layer)

    return word


def test_fuzz_move_past() -> None:
    """Fuzzes many words with layers that can move past
    each other. Asserts that the layers are able to move
    past each other and after doing that twice, this is
    equivalent to the original"""
    i = BASE_SEED
    while True:
        for _ in range(NUM_TESTS):
            if i % UPDATE_FREQ == 0:
                print(i)
            random.seed(i)

            original_word = random_swappable_word()

            original_word_keepsafe = original_word.copy()
            original_word_keepsafe.canonicalize()

            # BEGIN FUZZING
            original_word.fuzz_layer(1, rng, geometric(LAYER_MUTATIONS_AVERAGE))
            original_word.fuzz_layer(2, rng, geometric(LAYER_MUTATIONS_AVERAGE))
            original_word.fuzz_braid(2, rng, geometric(BRAID_MUTATIONS_AVERAGE))
            # END FUZZING

            # BEGIN MOVE-PAST ALGO
            success = original_word.attempt_swap(1)
            assert success
            success = original_word.attempt_swap(1)
            assert success
            # END MOVE-PAST ALGO

            # BEGIN VALIDITY TEST
            original_word.canonicalize()
            assert original_word == original_word_keepsafe
            # END VALIDITY TEST

            i += 1
        if not RUN_FOREVER:
            break
