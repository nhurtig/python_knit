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
from fig_gen.blog_post import post_commute, pre_commute
from fig_gen.braid_pres import draw_braid_pres, interesting_5
from fig_gen.canon_example import word_sigma, word_delta
from fig_gen.full_example import display_word_steps
from fig_gen.move_past import draw_move_past
from fig_gen.poster_example import draw_poster_word
from fig_gen.acm_paper_seven_rewrites import l3, make_all_seven_diagram_rules


def main() -> None:
    """Executes many PDF-PNG drawing commands
    used in the presentation"""
    # sigma_cancel()
    # morph_swap()
    # sigma_underline()
    # sigma_conj()
    # yang_baxter()
    # word_sigma()
    # word_delta()
    # display_word_steps()
    # draw_poster_word()
    draw_braid_pres()
    # pre_commute()
    # post_commute()

    # STUFF ACTUALLY IN THE PAPER
    # delta_conj()
    # delta_conj(2, 2)
    # draw_move_past()
    # make_all_seven_diagram_rules()


if __name__ == "__main__":
    main()
