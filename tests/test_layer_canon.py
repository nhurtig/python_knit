"""Tests for layer
canonicalization"""

from braid.braid import Braid
from category.morphism import Knit
from category.object import Carrier, Loop
from common.common import Bed, Dir
from layer.layer import Layer
from src.layer.word import Word

b0 = Braid.str_to_braid(0, "")
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

lay01 = Layer(0, k01, b1, b0)
lay12 = Layer(0, k12, b2, b1)
lay23 = Layer(0, k23, b3, b2)

word = Word()
word.append_layer(lay01)
word.append_layer(lay12)
word.append_layer(lay23)


def test_basic_example() -> None:
    """Checks that the canonicalization
    of a small word (3 layers) is correct"""
    can_word = word.copy()
    can_word.canonicalize()
    out = str(can_word)

    assert out == (
        """Word([Layer(Knit(front=False, right=False:Braid(n=2, [])), """
        """Layer(Knit(front=False, right=True:Braid(n=3, """
        """[(0, False), (1, False), (0, False), (0, False), """
        """(1, False), (0, False), (0, True), (0, True), """
        """(1, True), (1, True), (0, True)])), """
        """Layer(Knit(front=False, right=False:Braid(n=3, """
        """[(0, True), (0, True), (1, True)]))])"""
    )
