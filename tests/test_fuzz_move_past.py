"""Tests braid word canonicalization
using fuzzing"""

import random
import math
import subprocess
from braid.braid import Braid
from category.morphism import Knit
from category.object import Carrier, Loop
from common.common import Bed, Dir
from layer.layer import Layer
from layer.word import Word
from tests.test_fuzz_braid import random_braid_word

# out of 1000 tests:
# Do nothing and hope the fuzzing cancels out: 3/1000
# Canonicalize the braid between: 115/1000
# Canonicalize the bottom layer: 842/1000
# Top then bottom layer: 819/1000
# Bottom then top-flip: 886/1000
# Bottom then top-flip then bottom: 1000/1000

# OLD RESULTS (slightly invalid b/c different randomness)
# Canonicalize top then bottom: 888/1000
# Bottom then top: 952/1000 (makes sense that this is the same)
# Top then bottom twice: 888/1000 (makes sense that this is the same)
# Bottom then top then bottom: 952/1000
NUM_TESTS = 10000000000000000000000000
N_AVERAGE = 10  # number of strands in between layer
AVERAGE_OUTIN = 2.5  # number of inputs/outputs of top/bottom box
LAYER_MUTATIONS_AVERAGE = 15
BRAID_MUTATIONS_AVERAGE = 100
# AVERAGE_ABOVE_BRAID_LENGTH = 10
# AVERAGE_TWISTS = 2

BASE_SEED = 215000

random.seed(BASE_SEED)
rng = random.random


def geometric(average: float) -> int:
    """Samples from a geometric distribution

    Args:
        average (float): Expected value

    Returns:
        int: Sample
    """
    # return int(average)
    u = rng()
    num: float = math.log(1 - u)
    denom: float = math.log(1 - (1 / (average + 1)))
    return int(num / denom)


def test_braid_fuzzing_preserves_equivalence() -> None:
    """Playground to experiment with move-past algorithms"""
    fails = 0
    for i in range(NUM_TESTS):
        if i % 100 == 0:
            print(i)
        random.seed(BASE_SEED + i)
        n = 0
        bottom_outs = 1
        top_ins = 1
        bottom_index = 0
        top_index = 0
        while (
            bottom_index + bottom_outs > n  # too big
            or top_index + top_ins > n  # too big
            or (
                bottom_index < top_index + top_ins
                and top_index < bottom_index + bottom_outs  # overlap
            )
            or n - bottom_outs + bottom_ins <= 2  # bottomest box needs 2 outputs
        ):
            n = geometric(N_AVERAGE - 4) + 4  # at least 4 strands
            bottom_ins = geometric(AVERAGE_OUTIN)
            bottom_outs = geometric(AVERAGE_OUTIN - 2) + 2  # ensure >= 2 out
            top_ins = (
                geometric(AVERAGE_OUTIN - 2) + 2
            )  # ensure >= 2 in (for vertical flip)
            top_outs = geometric(AVERAGE_OUTIN - 2) + 2  # so we can canonicalize
            bottom_index = int(rng() * n)
            top_index = int(rng() * n)

        context_in = [Loop(i) for i in range(n - bottom_outs + bottom_ins)]
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
        # for loop in bottom_box.outs() + bottom_box.ins() + top_box.outs():
        #     pos = rng() < 0.5
        #     for _ in range(geometric(AVERAGE_TWISTS)):
        #         loop.twist(pos)

        below_braid = Braid(n - bottom_outs + bottom_ins)  # no ins for bottom
        # above_braid = random_braid_word(n - top_ins + top_outs, geometric(AVERAGE_ABOVE_BRAID_LENGTH))
        above_braid = Braid(n - top_ins + top_outs)
        middle_braid = Braid(n)

        # JUST FOR DRAWING
        bottomest_box = Knit(Bed(True), Dir(True), [], context_in)
        bottomest_layer = Layer(0, bottomest_box, below_braid, Braid(0))

        bottom_layer = Layer(bottom_index, bottom_box, middle_braid, below_braid)

        top_layer = Layer(top_index, top_box, above_braid, middle_braid)

        original_word = Word()
        original_word.append_layer(bottomest_layer)
        original_word.append_layer(bottom_layer)
        original_word.append_layer(top_layer)

        # try:
        # original_word = Word()
        # original_word.append_layer(bottomest_layer)
        # original_word.append_layer(bottom_layer)
        # original_word.append_layer(top_layer)
        # original_word.compile_latex(f"{i}_1_orig")
        # except subprocess.CalledProcessError as e:
        # print(e)

        original_word_keepsafe = original_word.copy()
        original_word_keepsafe.canonicalize()

        # BEGIN FUZZING
        bottom_layer.fuzz_layer(rng, geometric(LAYER_MUTATIONS_AVERAGE))
        # try:
        #     original_word = Word()
        #     original_word.append_layer(bottomest_layer)
        #     original_word.append_layer(bottom_layer)
        #     original_word.append_layer(top_layer)
        #     original_word.compile_latex(f"{i}_2_bot")
        # except subprocess.CalledProcessError as e:
        #     print(e)

        top_layer.fuzz_layer(rng, geometric(LAYER_MUTATIONS_AVERAGE))
        # try:
        #     original_word = Word()
        #     original_word.append_layer(bottomest_layer)
        #     original_word.append_layer(bottom_layer)
        #     original_word.append_layer(top_layer)
        #     original_word.compile_latex(f"{i}_3_top")
        # except subprocess.CalledProcessError as e:
        #     print(e)
        bottom_layer.fuzz_braid(rng, geometric(BRAID_MUTATIONS_AVERAGE))
        # try:
        #     original_word = Word()
        #     original_word.append_layer(bottomest_layer)
        #     original_word.append_layer(bottom_layer)
        #     original_word.append_layer(top_layer)
        #     original_word.compile_latex(f"{i}_4_mid")
        # except subprocess.CalledProcessError as e:
        #     print(e)
        # END FUZZING

        # BEGIN MOVE-PAST ALGO
        # bottom_layer.layer_canon()
        # bottom_layer.canonicalize()
        # bottom_layer.delta_step()
        # no canon for bottom
        bottom_layer.macro_step()
        # try:
        #     original_word = Word()
        #     original_word.append_layer(bottomest_layer)
        #     original_word.append_layer(bottom_layer)
        #     original_word.append_layer(top_layer)
        #     original_word.compile_latex(f"{i}_5_top_macro")
        # except subprocess.CalledProcessError as e:
        #     print(e)
        # top_layer = top_layer.flip_canonicalize_delta()
        top_layer = top_layer.flip_macro()
        bottom_layer = Layer(
            bottom_layer.left(),
            bottom_layer.middle(),
            top_layer.below(),
            bottom_layer.below(),
        )

        # H2 check
        assert len(bottom_layer.macro_subbraid().canon()) == 0

        # try:
        #     original_word = Word()
        #     original_word.append_layer(bottomest_layer)
        #     original_word.append_layer(bottom_layer)
        #     original_word.append_layer(top_layer)
        #     original_word.compile_latex(f"{i}_6_bot_macro")
        # except subprocess.CalledProcessError as e:
        #     print(e)
        # bottom_layer.canonicalize()
        # bottom_layer.macro_step()
        bottom_layer.layer_canon()
        try:
            original_word = Word()
            original_word.append_layer(bottomest_layer)
            original_word.append_layer(bottom_layer)
            original_word.append_layer(top_layer)
            # original_word.compile_latex(f"{i}_7_layer_canon")
        except subprocess.CalledProcessError as e:
            print(e)
        # top_layer.canonicalize()
        # bottom_layer.canonicalize()
        # END MOVE-PAST ALGO

        if not len(bottom_layer.above()) == 0:
            print(f"FAIL ON SEED {BASE_SEED + i}")
            assert False

        # if not old_left == new_left:
        # fails += 1
        # assert False

        # BEGIN VALIDITY TEST
        # new_word = Word()
        # new_bottomest_layer = Layer(0, bottomest_box, bottom_layer.below(), Braid(0))
        # new_word.append_layer(bottomest_layer)
        # new_word.append_layer(bottom_layer)
        # new_word.append_layer(top_layer)
        # new_word.canonicalize()
        # original_word.canonicalize()
        # original_word_keepsafe.canonicalize()

        # assert original_word == original_word_keepsafe
        # END VALIDITY TEST

    succeeded = NUM_TESTS - fails
    assert succeeded == NUM_TESTS
