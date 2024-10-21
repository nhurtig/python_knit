"""Tests word canonicalization
using fuzzing"""

import random

from braid.braid import Braid
from category.morphism import Knit
from category.object import Loop
from common.common import Bed, Dir
from layer.layer import Layer
from layer.word import CanonWord, Word
from tests.test_fuzz_braid import random_braid_word

MIN_BOXES = 1
MAX_BOXES = 5
MIN_INS = 0
MAX_INS = 5
MIN_OUTS = 2
MAX_OUTS = 5
WORDS_PER_NUM_BOXES = 20
LETTERS_PER_WORD = 10
MUTANTS_PER_WORD = 20
LAYER_MUTATIONS_PER_LAYER = 3
BRAID_MUTATIONS_PER_BRAID = 15
FUZZ_FOREVER = False
TEST_OUT_INFO = "word_fuzz_out.txt"
UPDATE_FREQ = 100
# Took around 50 seconds last time

rng = random.random
random.seed(28)


def random_word(num_boxes: int) -> Word:
    """Generates a random Word.

    Args:
        num_boxes (int): Number of boxes

    Returns:
        Word: Random layer
    """
    w = Word()
    prev_b = Braid(0)
    for _ in range(num_boxes):
        knit_ins = min(int(rng() * (MAX_INS - MIN_INS)) + MIN_INS, prev_b.n())
        knit_outs = int(rng() * (MAX_OUTS - MIN_OUTS)) + MIN_OUTS
        k = Knit(
            Bed(rng() < 0.5),
            Dir(rng() < 0.5),
            [Loop(0) for _ in range(knit_ins)],
            [Loop(0) for _ in range(knit_outs)],
        )
        left = int(rng() * (prev_b.n() - knit_ins))
        b = random_braid_word(prev_b.n() + knit_outs - knit_ins, LETTERS_PER_WORD)
        w.append_layer(Layer(left, k, b, prev_b))
        prev_b = b
    return w


def test_word_canonicalization_fuzzing() -> None:
    """Tests the word canonicalization by fuzzing various
    words, computing their canonical forms, and asserting
    the canonical fuzzed is the same as the canonical original."""
    tests = 0
    while FUZZ_FOREVER:
        for num_boxes in range(MIN_BOXES, MAX_BOXES + 1):
            for _ in range(WORDS_PER_NUM_BOXES):
                # Generate a random word
                original = random_word(num_boxes)
                original_canon = CanonWord(original.copy())

                for _ in range(MUTANTS_PER_WORD):
                    # Create a mutant of the original braid by fuzzing it
                    mutant = original.copy()
                    mutant.fuzz(
                        random.random,
                        LAYER_MUTATIONS_PER_LAYER,
                        BRAID_MUTATIONS_PER_BRAID,
                    )

                    # Check that the canonical forms of the original and mutant are equivalent
                    mutant_canon = CanonWord(mutant)
                    assert (
                        original_canon == mutant_canon
                    ), f"Word mismatch after fuzzing for num_boxes={num_boxes}"
                    tests += 1

                    if tests % UPDATE_FREQ == 0:
                        with open(TEST_OUT_INFO, "w+", encoding='utf-8') as f:
                            f.write(f"tested {tests} words so far")
