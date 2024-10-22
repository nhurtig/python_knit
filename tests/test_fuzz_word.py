"""Tests word canonicalization
using fuzzing"""

import random
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait

from braid.braid import Braid
from category.morphism import Knit
from category.object import Loop
from common.common import Bed, Dir
from layer.layer import Layer
from layer.word import CanonWord, Word
from tests.test_fuzz_braid import random_braid_word

# Constants
MIN_BOXES = 1
MAX_BOXES = 4
MIN_INS = 0
MAX_INS = 5
MIN_OUTS = 2
MAX_OUTS = 5
WORDS_PER_NUM_BOXES = 1
LETTERS_PER_WORD = 10
MUTANTS_PER_WORD = 20
LAYER_MUTATIONS_PER_LAYER = 3
BRAID_MUTATIONS_PER_BRAID = 15
FUZZ_FOREVER = False
TEST_OUT_INFO = "word_fuzz_out.txt"
TEST_ERROR_INFO = "word_fuzz_err.txt"
UPDATE_FREQ = (MAX_BOXES + 1 - MIN_BOXES) * WORDS_PER_NUM_BOXES * MUTANTS_PER_WORD
THREADS = 4
BASE_SEED = 5000


def random_word(num_boxes: int, rng: random.Random) -> Word:
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
        knit_ins = min(int(rng.random() * (MAX_INS - MIN_INS)) + MIN_INS, prev_b.n())
        knit_outs = int(rng.random() * (MAX_OUTS - MIN_OUTS)) + MIN_OUTS
        k = Knit(
            Bed(rng.random() < 0.5),
            Dir(rng.random() < 0.5),
            [Loop(0) for _ in range(knit_ins)],
            [Loop(0) for _ in range(knit_outs)],
        )
        left = int(rng.random() * (prev_b.n() - knit_ins))
        b = random_braid_word(prev_b.n() + knit_outs - knit_ins, LETTERS_PER_WORD)
        w.append_layer(Layer(left, k, b, prev_b))
        prev_b = b
    return w


def fuzz_word_canonicalization(seed: int, thread_id: int) -> None:
    """Tests the word canonicalization by fuzzing various
    words, computing their canonical forms, and asserting
    the canonical fuzzed is the same as the canonical original.

    Args:
        seed (int): Random seed for this thread
        thread_id (int): Thread identifier for logging
    """
    rng = random.Random(seed)  # Thread-local random generator
    tests = 0
    while FUZZ_FOREVER or tests == 0:
        for num_boxes in range(MIN_BOXES, MAX_BOXES + 1):
            for _ in range(WORDS_PER_NUM_BOXES):
                # Generate a random word
                original = random_word(num_boxes, rng)
                original_canon = CanonWord(original.copy())

                for _ in range(MUTANTS_PER_WORD):
                    # Create a mutant of the original braid by fuzzing it
                    mutant = original.copy()
                    mutant.fuzz(
                        rng.random,
                        LAYER_MUTATIONS_PER_LAYER,
                        BRAID_MUTATIONS_PER_BRAID,
                    )

                    # Check that the canonical forms of the original and mutant are equivalent
                    mutant_canon = CanonWord(mutant)
                    if original_canon != mutant_canon:
                        with open(TEST_ERROR_INFO, "a+", encoding="utf-8") as f:
                            f.write(repr(original))
                            f.write(repr(original_canon))
                            f.write(str(original_canon))
                            f.write(repr(mutant))
                            f.write(repr(mutant_canon))
                            f.write(str(mutant_canon))
                            f.write("\n")
                        assert original_canon == mutant_canon, (
                            f"Thread {thread_id}: Word mismatch after fuzzing"
                            "for num_boxes={num_boxes}"
                        )
                    tests += 1

                    if tests % UPDATE_FREQ == 0:
                        with open(TEST_OUT_INFO, "a+", encoding="utf-8") as f:
                            seed += THREADS
                            rng = random.Random(seed)
                            f.write(
                                f"Thread {thread_id}: tested {tests} words so far, seed {seed}\n"
                            )


def test_word_canonicalization_fuzzing_multithreaded() -> None:
    """Tests word canonicalization by fuzzing across multiple threads."""
    seeds = [BASE_SEED + i for i in range(THREADS)]
    with open(TEST_OUT_INFO, "w+", encoding="utf-8") as _:
        pass
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [
            executor.submit(fuzz_word_canonicalization, seed, i)
            for i, seed in enumerate(seeds)
        ]

        # Wait for the first exception to occur or all threads to finish
        done, _ = wait(futures, return_when=FIRST_EXCEPTION)

        for future in done:
            future.result()


# Run the multithreaded test
if __name__ == "__main__":
    test_word_canonicalization_fuzzing_multithreaded()
