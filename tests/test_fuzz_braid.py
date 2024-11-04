"""Tests braid word canonicalization
using fuzzing"""

import random
from time import perf_counter
from braid.braid import Braid
from braid.braid_generator import BraidGenerator

# TODO: make these fuzzing tests geometric instead of uniform distributions
MIN_N = 5
MAX_N = 50
WORDS_PER_N = 1
LETTERS_PER_WORD = 10
MUTANTS_PER_WORD = 5
MUTATION_ATTEMPTS_PER_WORD = 100
# Took ~35 seconds with the above settings

print(
    (
        f"{len(range(MIN_N, MAX_N+1))*WORDS_PER_N*MUTANTS_PER_WORD} tests, each"
        f"with {MUTATION_ATTEMPTS_PER_WORD} calls to mutate {LETTERS_PER_WORD} letters"
    )
)

rng = random.random
random.seed(42)


def random_braid_word(n: int, length: int) -> Braid:
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


def test_braid_fuzzing_preserves_equivalence() -> None:
    """Tests the braid canonicalization by fuzzing various
    braids, computing their canonical forms, and asserting
    the canonical fuzzed is the same as the canonical original."""
    times = []
    for n in range(MIN_N, MAX_N + 1, 5):
        time = 0
        for i in range(WORDS_PER_N):
            print("i:", i)
            # Generate a random braid word
            original_braid = random_braid_word(n, LETTERS_PER_WORD)
            original_canon = original_braid.canon()

            for _ in range(MUTANTS_PER_WORD):
                # Create a mutant of the original braid by fuzzing it
                mutant_braid = original_braid.copy()
                mutant_braid.fuzz(rng=random.random, steps=MUTATION_ATTEMPTS_PER_WORD)

                # Check that the canonical forms of the original and mutant are equivalent
                start = perf_counter()
                mutant_canon = mutant_braid.canon()
                end = perf_counter()
                time += end - start

                mutant_canon_canon = mutant_canon.canon()

                # print()
                # print(repr(list(original_braid)))
                # print([repr(g) for g in list(mutant_braid)])
                assert (
                    original_canon == mutant_canon
                ), f"Braid mismatch after fuzzing for n={n}"
                assert mutant_canon == mutant_canon_canon, "Sage conversion error!"
        times.append(time)
    print(times)
