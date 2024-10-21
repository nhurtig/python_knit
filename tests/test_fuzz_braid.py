"""Tests braid word canonicalization
using fuzzing"""

import random
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from braid.canon.canon_braid import CanonBraid

MIN_N = 2
MAX_N = 10
WORDS_PER_N = 10
LETTERS_PER_WORD = 10
MUTANTS_PER_WORD = 10
MUTATION_ATTEMPTS_PER_WORD = 100
# Took 208 seconds with the above settings

print(
    f"{len(range(MIN_N, MAX_N+1))*WORDS_PER_N*MUTANTS_PER_WORD} tests, each with {MUTATION_ATTEMPTS_PER_WORD} calls to mutate {LETTERS_PER_WORD} letters"
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
    for n in range(MIN_N, MAX_N + 1):
        for _ in range(WORDS_PER_N):
            # Generate a random braid word
            original_braid = random_braid_word(n, LETTERS_PER_WORD)
            original_canon = CanonBraid(original_braid.copy())

            for _ in range(MUTANTS_PER_WORD):
                # Create a mutant of the original braid by fuzzing it
                mutant_braid = original_braid.copy()
                mutant_braid.fuzz(rng=random.random, steps=MUTATION_ATTEMPTS_PER_WORD)

                # Check that the canonical forms of the original and mutant are equivalent
                mutant_canon = CanonBraid(mutant_braid)
                assert (
                    original_canon == mutant_canon
                ), f"Braid mismatch after fuzzing for n={n}"
