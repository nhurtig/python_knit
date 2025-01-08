"""Module for drawing a very basic example of two words that
share a canonical form"""

from typing import Sequence
from braid.braid import Braid
from category.morphism import Knit
from category.object import Carrier, Loop, PrimitiveObject
from fig_gen.color import reset_colors
from common.common import Bed, Dir, Sign
from layer.layer import Layer
from layer.word import Word


def word_basic() -> tuple[Word, Sequence[PrimitiveObject]]:
    """Returns a simple word in its canonical form along with
    its context

    Returns:
        tuple[Word, Sequence[PrimitiveObject]]: The word
        and its input object context
    """
    reset_colors()
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(2)]
    w = Word(2)
    # b = Braid(2)
    l = Layer(
        1,
        Knit(Bed(True), Dir(True), list(context[1:]), [Loop(0), Loop(0), Carrier(0)]),
        0,
    )
    w.append_layer(l)
    return (w, context)


def word_sigma() -> None:
    """Draws the basic word and the word
    after a sigma underline move"""
    (w, context) = word_basic()
    w.compile_latex("word_orig", context)
    w.layer_at(0).underline_conj(Dir(False), True)
    w.compile_latex("word_sigma", context)


def word_delta() -> None:
    """Draws the basic word after a delta
    move and its inverse"""
    (w, context) = word_basic()
    w.layer_at(0).delta(Sign(True))
    w.compile_latex("word_delta", context, True)
    w.layer_at(0).delta(Sign(False))
    w.compile_latex("word_delta_2", context, True)
