"""Module for drawing a very basic example of two words that
share a canonical form"""

from typing import Sequence
from braid.braid import Braid
from category.morphism import Knit
from category.object import Carrier, Loop, PrimitiveObject
from color import reset_colors
from common import Bed, Dir, Sign
from layer.layer import Layer
from word import Word


def word_basic() -> tuple[Word, Layer, Sequence[PrimitiveObject]]:
    """Returns a simple word in its canonical form along with
    some pieces of the word

    Returns:
        tuple[Word, Layer, Sequence[PrimitiveObject]]: The word,
        its interesting top layer, and its input object context
    """
    reset_colors()
    context: Sequence[PrimitiveObject] = [Carrier(0) for _ in range(2)]
    w = Word()
    b = Braid(2)
    l = Layer(0, Knit(Bed(True), Dir(True), [], []), b, Braid(2))
    w.append_layer(l)
    l = Layer(
        1,
        Knit(Bed(True), Dir(True), list(context[1:]), [Loop(0), Loop(0), Carrier(0)]),
        Braid(4),
        b,
    )
    w.append_layer(l)
    return (w, l, context)


def word_sigma() -> None:
    """Draws the basic word and the word
    after a sigma underline move"""
    (w, layer, context) = word_basic()
    w.compile_latex("word_orig", context)
    layer.underline_conj(Dir(False), True)
    w.compile_latex("word_sigma", context)


def word_delta() -> None:
    """Draws the basic word after a delta
    move and its inverse"""
    (w, layer, context) = word_basic()
    layer.delta(Sign(True))
    w.compile_latex("word_delta", context)
    layer.delta(Sign(False))
    w.compile_latex("word_delta_2", context)
