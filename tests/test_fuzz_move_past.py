"""Tests braid word canonicalization
using fuzzing"""

import random
import math
from braid.braid import Braid
from category.morphism import Knit
from category.object import Loop
from common.common import Bed, Dir
from layer.layer import Layer
from layer.word import Word

NUM_TESTS = 100
N_AVERAGE = 5  # number of strands in between layer
AVERAGE_OUTIN = 1.5  # number of inputs/outputs of top/bottom box
LAYER_MUTATIONS_AVERAGE = 5
BRAID_MUTATIONS_AVERAGE = 20

rng = random.random
random.seed(43)


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


def test_braid_fuzzing_preserves_equivalence() -> None:
    """Playground to experiment with move-past algorithms"""
    fails = 0
    for _ in range(NUM_TESTS):
        n = 0
        bottom_outs = 1
        top_ins = 1
        bottom_index = 0
        top_index = 0
        while (
            bottom_index + bottom_outs > n
            or top_index + top_ins > n
            or (
                bottom_index < top_index + top_ins
                and top_index < bottom_index + bottom_outs
            )
        ):
            n = geometric(N_AVERAGE - 1) + 1
            bottom_outs = geometric(AVERAGE_OUTIN - 1) + 1
            top_ins = geometric(AVERAGE_OUTIN)
            bottom_index = int(rng() * n)
            top_index = int(rng() * n)

        original_word = Word()
        bottom_box = Knit(
            Bed(rng() < 0.5), Dir(rng() < 0.5), [], [Loop(0)] * bottom_outs
        )
        top_box = Knit(
            Bed(rng() < 0.5), Dir(rng() < 0.5), [Loop(0)] * top_ins, [Loop(0)]
        )

        below_braid = Braid(n - bottom_outs)  # no ins for bottom
        above_braid = Braid(n - top_ins + 1)  # one in for top
        middle_braid = Braid(n)

        bottom_layer = Layer(bottom_index, bottom_box, middle_braid, below_braid)
        original_word.append_layer(bottom_layer)

        top_layer = Layer(top_index, top_box, above_braid, middle_braid)
        original_word.append_layer(top_layer)

        bottom_layer.fuzz_layer(rng, geometric(LAYER_MUTATIONS_AVERAGE))
        top_layer.fuzz_layer(rng, geometric(LAYER_MUTATIONS_AVERAGE))
        bottom_layer.fuzz_braid(rng, geometric(BRAID_MUTATIONS_AVERAGE))

        # do something here
        if not len(middle_braid.canon()) == 0:
            fails += 1

    assert fails == 0
