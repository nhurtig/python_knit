from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from category.morphism import Knit
from category.object import Carrier
from common.common import Bed, Dir
from fig_gen.color import reset_colors
from layer.layer import Layer
from layer.word import Word


def pre_commute():
    reset_colors()
    context = [Carrier(0) for _ in range(3)]
    and_out = Carrier(0)
    w = Word(3)
    w.labels_in = ["x_1", "x_2", "x_3"]
    w.append_layer(Layer(1, Knit(Bed(True), Dir(True), [context[1]], [Carrier(0) for _ in range(2)]), 1))
    b = Braid(4)
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    w.append_layer(Layer(1, Knit(Bed(True), Dir(True), [context[2], context[0]], [and_out]), 1))
    b = Braid(3)
    b.append(BraidGenerator(1, False))
    w.append_braid(b)

    w.labels_out = ["y_1", "y_2", "y_3"]
    w.compile_latex("blog_circuit_pre_commute", context, cleanup=False)


def post_commute():
    reset_colors()
    context = [Carrier(0) for _ in range(3)]
    w = Word(3)
    w.labels_in = ["x_1", "x_2", "x_3"]
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    w.append_layer(Layer(1, Knit(Bed(True), Dir(True), [context[2], context[0]], [Carrier(0)]), 0))
    w.append_layer(Layer(0, Knit(Bed(True), Dir(True), [context[1]], [Carrier(0) for _ in range(2)]), 1))

    w.labels_out = ["y_1", "y_2", "y_3"]
    w.compile_latex("blog_circuit_post_commute", context, cleanup=False)
