"""
This is just a placeholder module; Nat will
expand this later to be an actual app
"""

from fig_gen.basic_rewrites import (
    delta_conj,
    morph_swap,
    sigma_cancel,
    sigma_conj,
    sigma_underline,
    yang_baxter,
)
from fig_gen.canon_example import word_sigma, word_delta
from fig_gen.full_example import display_word_steps


def main() -> None:
    sigma_cancel()
    morph_swap()
    sigma_underline()
    sigma_conj()
    delta_conj()
    yang_baxter()
    word_sigma()
    word_delta()
    display_word_steps()


if __name__ == "__main__":
    main()
