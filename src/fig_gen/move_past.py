"""File that generates figures for
the move_past.tex proof"""

from typing import List, Sequence
from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from category.morphism import Knit
from category.object import Carrier, Loop, PrimitiveObject
from fig_gen.color import ColorGenerator, reset_colors
from common.common import Bed, Dir, Sign
from layer.layer import Layer
from layer.word import Word

non_prim_shade = 0.7
below = (0, 0, non_prim_shade)
below_prim = (0, 0, 1)
above = (non_prim_shade, 0, 0)
above_prim = (1, 0, 0)
free = (0, 0, 0)

def typed_n() -> tuple[Word, Sequence[PrimitiveObject]]:
    """Makes an example word in Tn (no layer)"""
    bis : Sequence[PrimitiveObject] = [Carrier(0, below if i > 0 else below_prim) for i in range(3)]
    tis : Sequence[PrimitiveObject] = [Carrier(0, above if i > 0 else above_prim) for i in range(2)]
    fis : Sequence[PrimitiveObject] = [Carrier(0, free) for _ in range(2)]
    w = Word(7)

    b = Braid(7)
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(3, False))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(4, True))
    b.append(BraidGenerator(5, False))

    w.append_braid(b)

    w.labels_in = "f_2, t_1, b_3, b_2, b_1, t_2, f_1".split(", ")
    w.labels_out = "b_1, b_3, f_2, t_1, t_2, f_1, b_2".split(", ")

    return (w, [fis[1], tis[0], bis[2], bis[1], bis[0], tis[1], fis[0]])

def well_typed_n() -> tuple[Word, Sequence[PrimitiveObject]]:
    """Makes an example word in Wn, with layers now. Builds
    off of Tn"""
    bis : Sequence[PrimitiveObject] = [Carrier(0, below if i > 0 else below_prim) for i in range(3)]
    tis : Sequence[PrimitiveObject] = [Carrier(0, above if i > 0 else above_prim) for i in range(2)]
    fis : Sequence[PrimitiveObject] = [Carrier(0, free) for _ in range(2)]

    w = Word(7)
    w.draw_postamble(False)
    w.draw_preamble(False)
    w.append_layer(Layer(
        3,
        Knit(Bed(True), Dir(True), [Carrier(0, free) for _ in range(3)], list(reversed(bis))),
        1
    ))

    b_bot = Braid(7)
    b_bot.append(BraidGenerator(2, True))
    b_bot.append(BraidGenerator(3, True))
    b_bot.append(BraidGenerator(4, True))
    b_bot.append(BraidGenerator(5, False))

    w.append_braid(b_bot)

    x = typed_n()[0]
    for thing in x:
        if isinstance(thing, Braid):
            w.append_braid(thing)
        else:
            w.append_layer(thing)

    b_top = Braid(7)
    b_top.append(BraidGenerator(3, True))
    b_top.append(BraidGenerator(5, False))
    w.append_braid(b_top)

    w.append_layer(Layer(
        3,
        Knit(Bed(True), Dir(True), [tis[1], tis[0]], [Carrier(0, free) for _ in range(2)]),
        2
    ))

    w.labels_in = "f_2, t_1, f_1, b_3, b_2, b_1, t_2".split(", ")
    w.labels_out = "b_1, b_3, f_2, t_2, t_1, b_2, f_1".split(", ")

    return (w, [fis[1], tis[0], fis[0], Carrier(0, free), Carrier(0, free), Carrier(0, free), tis[1]])

def bottom_knit() -> tuple[Knit, Sequence[PrimitiveObject]]:
    """Constructs a bottom knit for L_B gens"""
    bis : Sequence[PrimitiveObject] = [Carrier(0, below if i > 0 else below_prim) for i in range(3)]
    fis : Sequence[PrimitiveObject] = [Carrier(0, free) for _ in range(3)]
    ins = [Carrier(0, free) for _ in range(3)]
    k =  Knit(
            Bed(True),
            Dir(True),
            ins,
            bis
        )

    return (k, fis[:2] + [Carrier(0, free) for _ in range(3)] + fis[2:])

def draw_bottom_layer_gens() -> None:
    """Draws 5 examples of the bottom layer gens"""
    # id
    (k, c) = bottom_knit()
    w = Word(6)
    w.draw_preamble(False)
    w.append_layer(Layer(2, k, 1))
    w.compile_latex("LB_id", c)

    # r, B
    (k, c) = bottom_knit()
    # c = c[:2] + c[4:] + c[2:4]
    w = Word(6)
    w.draw_preamble(False)
    w.append_layer(Layer(3, k, 0))
    b = Braid(6)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(4, True))
    w.append_braid(b)
    w.labels_in = ["", "", "r", "b_1", "b_2", "b_3"]
    w.labels_out = ["", "", "b_1", "b_2", "b_3", "r"]
    w.compile_latex("LB_rB", c)

    # B, r
    (k, c) = bottom_knit()
    # c = c[:1] + c[2:4] + c[1:2] + c[4:]
    w = Word(6)
    w.draw_preamble(False)
    w.append_layer(Layer(1, k, 2))
    b = Braid(6)
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    w.labels_in = ["", "b_1", "b_2", "b_3", "r", ""]
    w.labels_out = ["", "r", "b_1", "b_2", "b_3", ""]
    w.compile_latex("LB_Br", c)

    # delgen
    (k, c) = bottom_knit()
    k.flip()
    w = Word(6)
    w.draw_preamble(False)
    w.append_layer(Layer(2, k, 1))
    b = Braid(6)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))
    w.append_braid(b)
    w.labels_in = ["", "", "b_3", "b_2", "b_1", ""]
    w.labels_out = ["", "", "b_1", "b_2", "b_3", ""]
    w.compile_latex("LB_del", c)

    # sigma conj
    (k, c) = bottom_knit()
    w = Word(6)
    w.draw_preamble(False)
    w.append_layer(Layer(2, k, 1))
    b = Braid(6)
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.labels_in = ["r_1", "r_2", "", "", "", ""]
    w.labels_out = ["r_2", "r_1", "", "", "", ""]
    w.compile_latex("LB_rr", c)

    # (w, c) = bottom_layer_word()
    # b = Braid(5)
    # b.append(BraidGenerator(1, True))
    # b.append(BraidGenerator(2, True))
    # w.append_braid(b)
    # w.compile_latex("LB_rB", c)

def x(ghost_b2: bool = False, ghost_fi: bool=False) -> tuple[Knit, list[PrimitiveObject]]:
    """Draws a small x in T^4"""
    bis : Sequence[PrimitiveObject] = [Carrier(0, (ColorGenerator.ghost(below) if ghost_b2 else below) if i > 0 else below_prim) for i in range(2)]
    fis : Sequence[PrimitiveObject] = [Carrier(0, ColorGenerator.ghost(free) if ghost_fi else free) for _ in range(2)]
    w = Word(4)

    b = Braid(4)
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, False))

    w.append_braid(b)

    w.labels_in = "f_2, b_1, f_1, b_2".split(", ")
    w.labels_out = "f_1, b_2, b_1, f_2".split(", ")

    if ghost_b2:
        w.labels_in = [x if x != "b_2" else "" for x in w.labels_in]
        w.labels_out = [x if x != "b_2" else "" for x in w.labels_out]
    if ghost_fi:
        w.labels_in = [x if x[0] != "f" else "" for x in w.labels_in]
        w.labels_out = [x if x[0] != "f" else "" for x in w.labels_out]

    return (w, [fis[1], bis[0], fis[0], bis[1]])

def draw_rho_x_no_twist() -> None:
    """Draws rho_B(x) in T^3 times T^2"""
    bis : Sequence[PrimitiveObject] = [Loop(0, below) for i in range(1)]
    fis : Sequence[PrimitiveObject] = [Carrier(0, free) for _ in range(2)]
    w = Word(3)

    b = Braid(3)
    b.append(BraidGenerator(1, True))
    # twist
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, False))

    w.append_braid(b)

    w.labels_in = "f_2, b_1, f_1".split(", ")
    w.labels_out = "f_1, b_1, f_2".split(", ")

    w.compile_latex("x_rho", [fis[1], bis[0], fis[0]], False)

def draw_psi_x() -> None:
    """Draws psi_B(x) in T^4"""
    bis : Sequence[PrimitiveObject] = [Carrier(0, below if i > 0 else below_prim) for i in range(2)]
    fis : Sequence[PrimitiveObject] = [Carrier(0, free) for _ in range(2)]
    w = Word(4)

    b = Braid(4)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(2, False))

    w.append_braid(b)

    w.labels_in = "f_2, b_1, b_2, f_1".split(", ")
    w.labels_out = "f_1, b_2, b_1, f_2".split(", ")

    w.compile_latex("x_psi", [fis[1], bis[0], bis[1], fis[0]])

def draw_lattice_lr() -> None:
    """Draws a 3, 2 positive lattice both ways"""

    lattice_ins : Sequence[PrimitiveObject] = [Carrier(0, below_prim) for _ in range(3)] + [Carrier(0, above_prim) for _ in range(2)]
    lattice_labels_in = "a_1, a_2, a_3, b_1, b_2".split(", ")
    lattice_labels_out = "b_1, b_2, a_1, a_2, a_3".split(", ")

    w = Word(5)

    b = Braid(5)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))

    w.append_braid(b)

    w.labels_in = lattice_labels_in
    w.labels_out = lattice_labels_out

    w.compile_latex("lattice_left", lattice_ins)

    w = Word(5)

    b = Braid(5)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))

    w.append_braid(b)

    w.labels_in = lattice_labels_in
    w.labels_out = lattice_labels_out

    w.compile_latex("lattice_right", lattice_ins)

def draw_move_past() -> None:
    """Draws the figures from this file"""
    # (w, c) = typed_n()
    # w.compile_latex("Tn", c)
    # (w, c) = well_typed_n()
    # w.compile_latex("Wn", c)

    # draw_bottom_layer_gens()

    # (w, c) = x()
    # w.compile_latex("x", c)
    # (w, c) = x(True, False)
    # w.compile_latex("x_pi", c)
    # (w, c) = x(False, True)
    # w.compile_latex("x_delta", c)
    # draw_rho_x_no_twist()
    # # draw_psi_x()

    draw_lattice_lr()

