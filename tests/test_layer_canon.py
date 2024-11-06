"""Tests for layer
canonicalization"""

from braid.braid import Braid
from category.morphism import Knit
from category.object import Carrier, Loop
from common.common import Bed, Dir
from layer.layer import Layer
from src.layer.word import Word

l1 = Loop(0)
l1.twist(True)
c1 = Carrier(0)
k01 = Knit(Bed(True), Dir(True), [None], [l1, c1])
b1 = Braid.str_to_braid(2, "a")
l21 = Loop(0)
l22 = Loop(0)
c2 = Carrier(0)
k12 = Knit(Bed(False), Dir(True), [c1, l1], [l21, l22, c2])
b2 = Braid.str_to_braid(3, "aBab")
l3 = Loop(0)
l3.twist(False)
c3 = Carrier(0)
k23 = Knit(Bed(True), Dir(True), [c2, l21], [l3, c3, None])
b3 = Braid.str_to_braid(3, "bA")

lay01 = Layer(0, k01, 0)
lay12 = Layer(0, k12, 0)
lay23 = Layer(0, k23, 1)

word = Word(0)
word.append_layer(lay01)
word.append_braid(b1)
word.append_layer(lay12)
word.append_braid(b2)
word.append_layer(lay23)
word.append_braid(b3)


canon_word = Word(0)
c1 = Carrier(0)
l1 = Loop(0)
canon_word.append_layer(Layer(0, Knit(Bed(False), Dir(False), [None], [c1, l1]), 0))
canon_word.append_braid(Braid(2))
l2 = Loop(0)
l2.twist(False)
l3 = Loop(0)
c2 = Carrier(0)
canon_word.append_layer(
    Layer(0, Knit(Bed(False), Dir(True), [c1, l1], [l2, l3, c2]), 0)
)
canon_word.append_braid(Braid.str_to_braid(3, "ABAABAaabba"))
c3 = Carrier(0)
l4 = Loop(0)
canon_word.append_layer(
    Layer(1, Knit(Bed(False), Dir(False), [l2, c2], [None, c3, l4]), 0)
)
canon_word.append_braid(Braid.str_to_braid(3, "aab"))


def test_basic_example() -> None:
    """Checks that the canonicalization
    of a small word (3 layers) is correct"""
    # can_word = word.copy()
    # can_word.compile_latex("canword", [])
    word.canonicalize()
    # can_word.compile_latex("canword_canon", [])

    assert word == canon_word
