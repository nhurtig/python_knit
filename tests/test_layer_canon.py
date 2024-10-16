"""
Tests for layer
canonicalization
"""

from category.morphism import Knit
from category.object import Carrier, Loop
from common import Bed, Dir
from layer.layer import CanonLayer, Layer
from tests.test_braid import str_to_braid

b0 = str_to_braid(0, "")
l1 = Loop(0)
l1.twist(True)
c1 = Carrier(0)
k01 = Knit(Bed(True), Dir(True), [None], [l1, c1])
b1 = str_to_braid(2, "a")
l21 = Loop(0)
l22 = Loop(0)
c2 = Carrier(0)
k12 = Knit(Bed(False), Dir(True), [c1, l1], [l21, l22, c2])
b2 = str_to_braid(3, "aBab")
l3 = Loop(0)
l3.twist(False)
c3 = Carrier(0)
k23 = Knit(Bed(True), Dir(True), [c2, l21], [l3, c3, None])
b3 = str_to_braid(3, "bA")

lay01 = Layer(0, k01, b1, b0)
lay12 = Layer(0, k12, b2, b1)
lay23 = Layer(0, k23, b3, b2)

def test_basic_example():
    can23 = CanonLayer(lay23)
    can12 = CanonLayer(lay12)
    can01 = CanonLayer(lay01)
    assert True
