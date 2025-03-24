"""File that generates figures forG
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

non_prim_shade = 0.65
prim_shade = 0.88
below = (0, non_prim_shade, non_prim_shade)
below_prim = (0, prim_shade, prim_shade)
above = (non_prim_shade, non_prim_shade, 0)
above_prim = (prim_shade, prim_shade, 0)
free = (0, 0, 0)

abovest_prim = (1, 0, 0)
abovest = (non_prim_shade * 1.2, 0, 0)

def example_ls() -> tuple[Word, Sequence[PrimitiveObject]]:
    """Makes an example word in L_S"""
    w = Word(5)
    c = [Carrier(0, free)] + [Carrier(0, below if i > 0 else below_prim) for i in range(3)] + [Carrier(0, free)]

    # k = Knit(Bed(True), Dir(True), [Carrier(0, free) for _ in range(3)], c[1:4])
    # l = Layer(1, k, 1)
    # w.append_layer(l)
    w.labels_in = "r_1, s_1, s_2, s_3, r_2".split(", ")

    b = Braid(5)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))

    b.append(BraidGenerator(3, False))

    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(0, False))

    w.append_braid(b)

    # k2 = Knit(Bed(False), Dir(False), list(reversed(c[1:4])), [Carrier(0, free) for _ in range(3)])
    # l = Layer(0, k2, 2)
    # w.append_layer(l)

    w.labels_out = "s_3, s_2, s_1, r_2, r_1".split(", ")
    return (w, c)

def example_ts() -> tuple[Word, Sequence[PrimitiveObject]]:
    """Makes an example word in T^S"""
    w = Word(5)
    c = [Carrier(0, below if i > 0 else below_prim) for i in range(3)] + [Carrier(0, free) for _ in range(2)]

    b = Braid(5)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))

    w.labels_in = "s_1, s_2, s_3, r_1, r_2".split(", ")
    w.labels_out = "r_1, s_1, s_3, s_2, r_2".split(", ")

    w.append_braid(b)

    return (w, c)



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
    w.draw_postamble(0)
    w.draw_preamble(0)
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

def bottom_piece_of_ls() -> tuple[Word, Sequence[PrimitiveObject]]:
    """Constructs a bottom knit for L_S gens"""
    bis : Sequence[PrimitiveObject] = [Carrier(0, below if i > 0 else below_prim) for i in range(3)]
    fis : Sequence[PrimitiveObject] = [Carrier(0, free) for _ in range(3)]
    ins = [Carrier(0, free) for _ in range(3)]
    k =  Knit(
            Bed(True),
            Dir(True),
            ins,
            bis
        )
    # l = Layer(2, k, 1)
    w = Word(6)
    # w.append_layer(l)
    # w.draw_preamble(0)
    # w.draw_postamble(0)

    return (w, fis[:2] + k.outs() + fis[2:])

def draw_layer_gens() -> None:
    """Draws 4 examples of the bottom layer gens"""

    # B, r
    (w, c) = bottom_piece_of_ls()
    # k = Knit(Bed(True), Dir(True), c[2:5], [Carrier(0, free) for _ in range(3)])
    # c = c[:2] + c[4:] + c[2:4]
    b = Braid(6)
    b.append(BraidGenerator(4, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))
    w.append_braid(b)
    # w.append_layer(Layer(3, k, 0))
    w.labels_in = ["", "", "s_1", "s_2", "s_3", "r"]
    w.labels_out = ["", "", "r", "s_1", "s_2", "s_3"]
    w.compile_latex("LB_Br", c)

    # r, B
    (w, c) = bottom_piece_of_ls()
    # c = c[:1] + c[2:4] + c[1:2] + c[4:]
    b = Braid(6)
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(3, True))
    w.append_braid(b)
    # w.append_layer(Layer(1, k, 2))
    w.labels_in = ["", "r", "s_1", "s_2", "s_3", ""]
    w.labels_out = ["", "s_1", "s_2", "s_3", "r", ""]
    w.compile_latex("LB_rB", c)

    # delgen
    (w, c) = bottom_piece_of_ls()
    b = Braid(6)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))
    w.append_braid(b)
    # k.flip()
    # w.append_layer(Layer(2, k, 1))
    w.labels_in = ["", "", "s_1", "s_2", "s_3", ""]
    w.labels_out = ["", "", "s_3", "s_2", "s_1", ""]
    w.compile_latex("LB_del", c)
    # k.flip()

    # sigma conj
    (w, c) = bottom_piece_of_ls()
    b = Braid(6)
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    # w.append_layer(Layer(2, k, 1))
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
    """Draws a small x in T^5"""
    bis : Sequence[PrimitiveObject] = [Carrier(0, (ColorGenerator.ghost(below) if ghost_b2 else below) if i > 0 else below_prim) for i in range(3)]
    if ghost_fi:
        bis[2] = Carrier(0, ColorGenerator.ghost(below))
    fis : Sequence[PrimitiveObject] = [Carrier(0, ColorGenerator.ghost(free) if ghost_fi else free) for _ in range(2)]
    w = Word(5)

    b = Braid(5)
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, False))

    w.append_braid(b)

    w.labels_in = "r_2, s_1, r_1, s_2, s_3".split(", ")
    w.labels_out = "r_1, s_2, s_1, r_2, s_3".split(", ")

    if ghost_b2:
        w.labels_in = "r_2, \\kappa, r_1, , ".split(", ")
        w.labels_out = "r_1, , \\kappa, r_2, ".split(", ")
    if ghost_fi:
        w.labels_in = ", 1, , 2, ".split(", ")
        w.labels_out = ", 2, 1, , ".split(", ")

    return (w, [fis[1], bis[0], fis[0], bis[1], bis[2]])

# def draw_rho_x_no_twist() -> None:
#     """Draws rho_B(x) in T^3 times T^2"""
#     bis : Sequence[PrimitiveObject] = [Loop(0, below) for i in range(1)]
#     fis : Sequence[PrimitiveObject] = [Carrier(0, free) for _ in range(2)]
#     w = Word(3)

#     b = Braid(3)
#     b.append(BraidGenerator(1, True))
#     # twist
#     b.append(BraidGenerator(0, False))
#     b.append(BraidGenerator(1, False))

#     w.append_braid(b)

#     w.labels_in = "r_2, s_1, r_1".split(", ")
#     w.labels_out = "r_1, s_1, r_2".split(", ")

#     w.compile_latex("x_rho", [fis[1], bis[0], fis[0]], False)

def draw_psi_x() -> None:
    """Draws psi_B(x) in T^5"""
    bis : Sequence[PrimitiveObject] = [Carrier(0, below if i > 0 else below_prim) for i in range(3)]
    fis : Sequence[PrimitiveObject] = [Carrier(0, free) for _ in range(2)]
    w = Word(5)
    # k = Knit(Bed(True), Dir(True), [Carrier(0, free) for _ in range(3)], bis)
    # l = Layer(1, k, 1)
    # w.append_layer(l)

    b = Braid(5)
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))

    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))


    b.append(BraidGenerator(0, False))

    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(3, False))

    w.append_braid(b)

    # k = Knit(Bed(False), Dir(False), bis, [Carrier(0, free) for _ in range(2)])
    # l = Layer(1, k, 1)
    # w.append_layer(l)

    w.labels_in = "r_2, s_1, s_2, s_3, r_1".split(", ")
    w.labels_out = "r_1, s_3, s_2, s_1, r_2".split(", ")
    # w.draw_postamble(0)
    # w.draw_preamble(0)

    w.compile_latex("x_psi", [fis[1], bis[0], bis[1], bis[2], fis[0]], False)

def draw_tau_x() -> None:
    """Draws tau_B(x) in T^4"""
    bis : Sequence[PrimitiveObject] = [Carrier(0, above if i > 0 else above_prim) for i in range(2)]
    fis : Sequence[PrimitiveObject] = [Carrier(0, free) for _ in range(2)]
    w = Word(4)
    # k = Knit(Bed(True), Dir(True), [Carrier(0, free) for _ in range(3)], bis)
    # l = Layer(1, k, 1)
    # w.append_layer(l)

    b = Braid(4)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))

    b.append(BraidGenerator(2, True))

    b.append(BraidGenerator(0, False))

    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(2, False))

    w.append_braid(b)

    # k = Knit(Bed(False), Dir(False), bis, [Carrier(0, free) for _ in range(2)])
    # l = Layer(1, k, 1)
    # w.append_layer(l)

    w.labels_in = "r_2, s'_1, s'_2, r_1".split(", ")
    w.labels_out = "r_1, s'_2, s'_1, r_2".split(", ")
    # w.draw_postamble(0)
    # w.draw_preamble(0)

    w.compile_latex("x_tau", [fis[1], bis[0], bis[1], fis[0]], False)

def draw_box_for_x() -> None:
    """Draws the box that's connected to x on both sides"""
    c = [Carrier(0, above_prim), Carrier(0, above)]
    w = Word(2)
    w.append_layer(Layer(0, Knit(Bed(True), Dir(True), c, [Carrier(0, below_prim), Carrier(0, below), Carrier(0, below)]), 0))
    w.draw_preamble(0)
    w.labels_in = "s'_1, s'_2".split(", ")
    w.labels_out = "s_1, s_2, s_3".split(", ")
    w.compile_latex("x_box", c)

def draw_lattice_lr() -> None:
    """Draws a 3, 2 positive lattice both ways"""

    lattice_ins : Sequence[PrimitiveObject] = [Carrier(0, below) for _ in range(3)] + [Carrier(0, above) for _ in range(2)]
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

def draw_snagged() -> None:
    """Draws the move-past snag"""
    w = Word(4)
    bottoms = [Carrier(0, below), Carrier(0, below)]
    tops = [Carrier(0, above), Carrier(0, above)]
    kbot = Knit(Bed(True), Dir(True), [Carrier(0, free) for _ in range(2)], bottoms)
    ktop = Knit(Bed(True), Dir(True), tops, [Carrier(0, free) for _ in range(2)])

    w.append_layer(Layer(1, kbot, 1))
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, True))
    w.append_braid(b)
    w.append_layer(Layer(1, ktop, 1))

    w.draw_preamble(0)
    w.draw_postamble(0)

    w.compile_latex("snagged", [tops[0]] + kbot.ins() + [tops[1]])

def draw_unsnagged() -> None:
    """Draws the move-past snag"""
    w = Word(4)
    bottoms = [Carrier(0, below), Carrier(0, below)]
    tops = [Carrier(0, above), Carrier(0, above)]
    kbot = Knit(Bed(True), Dir(True), [Carrier(0, free) for _ in range(2)], bottoms)
    ktop = Knit(Bed(True), Dir(True), tops, [Carrier(0, free) for _ in range(2)])

    w.append_layer(Layer(1, kbot, 1))
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, False))
    w.append_braid(b)
    w.append_layer(Layer(1, ktop, 1))

    w.draw_preamble(0)
    w.draw_postamble(0)

    w.compile_latex("unsnagged", [tops[0]] + kbot.ins() + [tops[1]])

def draw_layer_simp() -> None:
    """Draws some word before and after it's been simplified"""
    c = [Carrier(0, free), Carrier(0, below), Carrier(0, free)]
    w = Word(3)
    k = Knit(Bed(True), Dir(True), c[1:2], [Carrier(0, below_prim), Carrier(0, below)])
    l = Layer(1, k, 1)
    w.append_layer(l)
    b = Braid(4)
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.compile_latex("pre_layer_simp", c)

    w = Word(3)
    b = Braid(3)
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, False))
    w.append_braid(b)
    k.flip()
    l = Layer(1, k, 1)
    w.append_layer(l)
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    # w.draw_preamble(7)
    w.compile_latex("post_layer_simp", c)

def draw_layer_swap() -> None:
    """Draws some word before and after a simp-preserving swap is executed"""
    c = [Carrier(0, free) for _ in range(4)]
    w = Word(4)
    kb = Knit(Bed(True), Dir(True), c[:2], [Carrier(0, below_prim), Carrier(0, below)])
    lb = Layer(0, kb, 2)
    w.append_layer(lb)
    b = Braid(4)
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    kt = Knit(Bed(True), Dir(True), c[3:], [Carrier(0, above_prim), Carrier(0, above), Carrier(0, above)])
    lt = Layer(3, kt, 0)
    w.append_layer(lt)
    b = Braid(6)
    b.append(BraidGenerator(4, False))
    w.append_braid(b)
    ks = Knit(Bed(True), Dir(True), [kb.outs()[1], kt.outs()[0]], [Carrier(0, free) for _ in range(2)])
    ls = Layer(2, ks, 2)
    w.append_layer(ls)

    w.draw_preamble(0)
    w.draw_postamble(0)
    w.compile_latex("pre_swap", c)

    w = Word(4)
    lt = Layer(3, kt, 0)
    w.append_layer(lt)
    b = Braid(6)
    b.append(BraidGenerator(4, False))
    w.append_braid(b)
    lb = Layer(0, kb, 4)
    w.append_layer(lb)
    b = Braid(6)
    b.append(BraidGenerator(4, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(4, False))
    w.append_braid(b)
    w.append_layer(ls)

    w.draw_preamble(0)
    w.draw_postamble(0)
    w.compile_latex("post_swap", c)

    w = Word(4)
    lt = Layer(3, kt, 0)
    w.append_layer(lt)
    b = Braid(6)
    b.append(BraidGenerator(4, False))
    w.append_braid(b)
    lb = Layer(0, kb, 4)
    w.append_layer(lb)
    b = Braid(6)
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    w.append_layer(ls)

    w.draw_preamble(0)
    w.draw_postamble(0)
    w.compile_latex("post_swap_simp", c)

def draw_preprocess() -> None:
    """Draws a word before preprocessing,
    after laddering, and after slurping"""
    c = [Carrier(0, above_prim), Carrier(0, below_prim)]
    w = Word(2)
    t1 = Knit(Bed(False), Dir(True), [c[1]], [Carrier(0, below), Carrier(0, below), Carrier(0, below_prim)])
    l1 = Layer(1, t1, 0)
    w.append_layer(l1)
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, False))
    w.append_braid(b)
    t2 = Knit(Bed(True), Dir(True), [c[0]], [Carrier(0, above), Carrier(0, above), Carrier(0, above_prim)])
    l2 = Layer(3, t2, 0)
    w.append_layer(l2)
    b = Braid(6)
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(3, False))
    b.append(BraidGenerator(2, False))
    w.append_braid(b)
    s3 = Knit(Bed(True), Dir(True), t1.outs()[2:] + t2.outs()[:2] + t1.outs()[:2], [Carrier(0, below), Carrier(0, below), Carrier(0, above), Carrier(0, above), Carrier(0, below), Carrier(0, below), Carrier(0, below_prim)])
    l3 = Layer(0, s3, 1)
    w.append_layer(l3)

    w.draw_preamble(2)
    w.draw_postamble(3)
    w.compile_latex("process_pre", c, False)

    w = Word(2)
    t1 = Knit(Bed(False), Dir(True), [c[1]], [Carrier(0, below), Carrier(0, below), Carrier(0, below_prim)])
    l1 = Layer(1, t1, 0)
    w.append_layer(l1)
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, False))
    w.append_braid(b)
    t2 = Knit(Bed(True), Dir(True), [c[0]], [Carrier(0, above), Carrier(0, above), Carrier(0, above_prim)])
    l2 = Layer(3, t2, 0)
    w.append_layer(l2)
    b = Braid(6)
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(3, False))
    b.append(BraidGenerator(2, False))

    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(3, False))

    w.append_braid(b)

    w.draw_preamble(2)
    w.draw_postamble(12)
    w.compile_latex("process_ladder", c, False)

    w = Word(2)
    t1 = Knit(Bed(False), Dir(True), [c[1]], [Carrier(0, below), Carrier(0, below)])
    l1 = Layer(1, t1, 0)
    w.append_layer(l1)
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    t2 = Knit(Bed(True), Dir(True), [c[0]], [Carrier(0, above), Carrier(0, above)])
    l2 = Layer(2, t2, 0)
    w.append_layer(l2)
    b = Braid(4)
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(1, False))
    w.append_braid(b)

    w.compile_latex("process_done", c)

# preprocess, but with Jenny's mid-laddering
# def draw_preprocess() -> None:
#     """Draws a word before preprocessing,
#     after laddering, and after slurping"""
#     c = [Carrier(0, above_prim), Carrier(0, below_prim)]
#     w = Word(2)
#     t1 = Knit(Bed(False), Dir(True), [c[1]], [Carrier(0, below), Carrier(0, below), Carrier(0, below_prim)])
#     l1 = Layer(1, t1, 0)
#     w.append_layer(l1)
#     b = Braid(4)
#     b.append(BraidGenerator(0, True))
#     b.append(BraidGenerator(1, True))
#     b.append(BraidGenerator(2, False))
#     w.append_braid(b)
#     t2 = Knit(Bed(True), Dir(True), [c[0]], [Carrier(0, above), Carrier(0, above), Carrier(0, above_prim)])
#     l2 = Layer(3, t2, 0)
#     w.append_layer(l2)
#     b = Braid(6)
#     b.append(BraidGenerator(1, False))
#     b.append(BraidGenerator(0, False))
#     b.append(BraidGenerator(2, False))
#     b.append(BraidGenerator(1, False))
#     b.append(BraidGenerator(3, False))
#     b.append(BraidGenerator(2, False))
#     b.append(BraidGenerator(2, True))
#     b.append(BraidGenerator(3, True))
#     w.append_braid(b)
#     s3 = Knit(Bed(True), Dir(True), t1.outs()[2:] + t2.outs()[:2] + t1.outs()[:2], [Carrier(0, below_prim), Carrier(0, below_prim), Carrier(0, above), Carrier(0, below), Carrier(0, below), Carrier(0, above), Carrier(0, below_prim)])
#     l3 = Layer(0, s3, 1)
#     w.append_layer(l3)

#     w.draw_preamble(2)
#     w.draw_postamble(3)
#     w.compile_latex("process_pre", c, False)

#     w = Word(2)
#     t1 = Knit(Bed(False), Dir(True), [c[1]], [Carrier(0, below), Carrier(0, below), Carrier(0, below_prim)])
#     l1 = Layer(1, t1, 0)
#     w.append_layer(l1)
#     b = Braid(4)
#     b.append(BraidGenerator(0, True))
#     b.append(BraidGenerator(1, True))
#     b.append(BraidGenerator(2, False))
#     w.append_braid(b)
#     t2 = Knit(Bed(True), Dir(True), [c[0]], [Carrier(0, above), Carrier(0, above), Carrier(0, above_prim)])
#     l2 = Layer(3, t2, 0)
#     w.append_layer(l2)
#     b = Braid(6)
#     b.append(BraidGenerator(1, False))
#     b.append(BraidGenerator(0, False))
#     b.append(BraidGenerator(2, False))
#     b.append(BraidGenerator(1, False))
#     b.append(BraidGenerator(3, False))
#     b.append(BraidGenerator(2, False))
#     b.append(BraidGenerator(2, True))
#     b.append(BraidGenerator(3, True))

#     b.append(BraidGenerator(0, False))
#     b.append(BraidGenerator(1, False))
#     b.append(BraidGenerator(2, False))
#     b.append(BraidGenerator(3, False))

#     w.append_braid(b)

#     w.draw_preamble(2)
#     w.draw_postamble(12)
#     w.compile_latex("process_ladder", c, False)

#     w = Word(2)
#     t1 = Knit(Bed(False), Dir(True), [c[1]], [Carrier(0, below), Carrier(0, below)])
#     l1 = Layer(1, t1, 0)
#     w.append_layer(l1)
#     b = Braid(3)
#     b.append(BraidGenerator(0, True))
#     b.append(BraidGenerator(1, True))
#     w.append_braid(b)
#     t2 = Knit(Bed(True), Dir(True), [c[0]], [Carrier(0, above), Carrier(0, above)])
#     l2 = Layer(2, t2, 0)
#     w.append_layer(l2)
#     b = Braid(4)
#     b.append(BraidGenerator(1, False))
#     b.append(BraidGenerator(0, False))
#     b.append(BraidGenerator(2, False))
#     b.append(BraidGenerator(1, False))
#     b.append(BraidGenerator(1, True))
#     b.append(BraidGenerator(2, True))
#     w.append_braid(b)

#     w.compile_latex("process_done", c)

def draw_big_example() -> None:
    """Draws the big example, at start, simp, swap, and canon"""
    c = [Carrier(0, free) for _ in range(3)]
    w = Word(3)
    k1 = Knit(Bed(False), Dir(False), [c[0]], [Carrier(0, below_prim), Carrier(0, below)])
    w.append_layer(Layer(0, k1, 2))
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(0, False))
    w.append_braid(b)
    k2 = Knit(Bed(True), Dir(True), [k1.outs()[1], c[1]], [Carrier(0, abovest), Carrier(0, abovest), Carrier(0, abovest_prim)])
    w.append_layer(Layer(1, k2, 1))
    b = Braid(5)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(3, False))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))
    w.append_braid(b)
    k3 = Knit(Bed(True), Dir(True), [c[2], k1.outs()[0]], [Carrier(0, above), Carrier(0, above_prim)])
    w.append_layer(Layer(3, k3, 0))
    b = Braid(5)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(3, False))
    b.append(BraidGenerator(2, False))
    w.append_braid(b)
    w.compile_latex("example_start", c)

    # after first layer
    c = [Carrier(0, free) for _ in range(3)]
    w = Word(3)
    k1 = Knit(Bed(False), Dir(False), [c[0]], [Carrier(0, below_prim), Carrier(0, below)])
    w.append_layer(Layer(0, k1, 2))
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(0, False))
    w.append_braid(b)
    k2 = Knit(Bed(True), Dir(True), [k1.outs()[1], c[1]], [Carrier(0, abovest), Carrier(0, abovest), Carrier(0, abovest_prim)])
    w.append_layer(Layer(1, k2, 1))
    b = Braid(5)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(3, False))
    w.append_braid(b)
    k3 = Knit(Bed(False), Dir(False), list(reversed([c[2], k1.outs()[0]])), list(reversed([Carrier(0, above), Carrier(0, above_prim)])))
    w.append_layer(Layer(2, k3, 1))
    b = Braid(5)
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.compile_latex("example_layer1", c)

    # after second layer
    c = [Carrier(0, free) for _ in range(3)]
    w = Word(3)
    k1 = Knit(Bed(False), Dir(False), [c[0]], [Carrier(0, below_prim), Carrier(0, below)])
    w.append_layer(Layer(0, k1, 2))
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    k2 = Knit(Bed(False), Dir(False), list(reversed([k1.outs()[1], c[1]])), list(reversed([Carrier(0, abovest), Carrier(0, abovest), Carrier(0, abovest_prim)])))
    w.append_layer(Layer(0, k2, 2))
    b = Braid(5)
    b = Braid.str_to_braid(5, "BACD")
    w.append_braid(b)
    k3 = Knit(Bed(False), Dir(False), list(reversed([c[2], k1.outs()[0]])), list(reversed([Carrier(0, above), Carrier(0, above_prim)])))
    w.append_layer(Layer(2, k3, 1))
    b = Braid(5)
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.compile_latex("example_layer2", c)

    # post layer, pre swap
    c = [Carrier(0, free) for _ in range(3)]
    w = Word(3)
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    k1 = Knit(Bed(True), Dir(True), [c[0]], list(reversed([Carrier(0, below_prim), Carrier(0, below)])))
    w.append_layer(Layer(1, k1, 1))
    b = Braid(4)
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    k2 = Knit(Bed(False), Dir(False), list(reversed([k1.outs()[1], c[1]])), list(reversed([Carrier(0, abovest), Carrier(0, abovest), Carrier(0, abovest_prim)])))
    w.append_layer(Layer(0, k2, 2))
    b = Braid(5)
    b = Braid.str_to_braid(5, "BACD")
    w.append_braid(b)
    k3 = Knit(Bed(False), Dir(False), list(reversed([c[2], k1.outs()[0]])), list(reversed([Carrier(0, above), Carrier(0, above_prim)])))
    w.append_layer(Layer(2, k3, 1))
    b = Braid(5)
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.compile_latex("example_layered", c)

    # post swap
    c = [Carrier(0, free) for _ in range(3)]
    w = Word(3)
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    k1 = Knit(Bed(True), Dir(True), [c[0]], list(reversed([Carrier(0, below_prim), Carrier(0, below)])))
    w.append_layer(Layer(1, k1, 1))
    b = Braid(4)
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    k3 = Knit(Bed(False), Dir(False), list(reversed([c[2], k1.outs()[0]])), list(reversed([Carrier(0, above), Carrier(0, above_prim)])))
    w.append_layer(Layer(2, k3, 0))
    k2 = Knit(Bed(False), Dir(False), list(reversed([k1.outs()[1], c[1]])), list(reversed([Carrier(0, abovest), Carrier(0, abovest), Carrier(0, abovest_prim)])))
    w.append_layer(Layer(0, k2, 2))
    b = Braid(5)
    b = Braid.str_to_braid(5, "BACDAa")
    # b = Braid.str_to_braid(5, "bCDAa")
    w.append_braid(b)
    w.compile_latex("example_swapped", c)

    # canon
    c = [Carrier(0, free) for _ in range(3)]
    w = Word(3)
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    k1 = Knit(Bed(True), Dir(True), [c[0]], list(reversed([Carrier(0, below_prim), Carrier(0, below)])))
    w.append_layer(Layer(1, k1, 1))
    b = Braid(4)
    w.append_braid(b)
    k3 = Knit(Bed(False), Dir(False), list(reversed([c[2], k1.outs()[0]])), list(reversed([Carrier(0, above), Carrier(0, above_prim)])))
    w.append_layer(Layer(2, k3, 0))
    k2 = Knit(Bed(False), Dir(False), list(reversed([k1.outs()[1], c[1]])), list(reversed([Carrier(0, abovest), Carrier(0, abovest), Carrier(0, abovest_prim)])))
    w.append_layer(Layer(0, k2, 2))
    b = Braid(5)
    b = Braid.str_to_braid(5, "BACD")
    # b = Braid.str_to_braid(5, "bCDAa")
    w.append_braid(b)
    w.compile_latex("example_canon", c)

def draw_tau_examples() -> None:
    """Draws some tau junk. I'm tired."""
    c = [Carrier(0, free), Carrier(0, below_prim), Carrier(0, below), Carrier(0, below)]
    w = Word(4)
    w.labels_in = "r, s_1, s_2, s_3".split(", ")
    w.labels_out = "s_1, s_2, s_3, r".split(", ")
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))
    w.append_braid(b)
    w.compile_latex("tau11", c)

    c = [Carrier(0, free), Carrier(0, above_prim), Carrier(0, above)]
    w = Word(3)
    w.labels_in = "r, s'_1, s'_2".split(", ")
    w.labels_out = "s'_1, s'_2, r".split(", ")
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    w.draw_postamble(3)
    w.compile_latex("tau12", c)

    c = [Carrier(0, below_prim), Carrier(0, below), Carrier(0, below)]
    w = Word(3)
    w.labels_in = "s_1, s_2, s_3".split(", ")
    w.labels_out = "s_3, s_2, s_1".split(", ")
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.compile_latex("tau21", c)

    c = [Carrier(0, above_prim), Carrier(0, above)]
    w = Word(2)
    w.labels_in = "s'_1, s'_2".split(", ")
    w.labels_out = "s'_2, s'_1".split(", ")
    b = Braid(2)
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.draw_preamble(2)
    w.draw_postamble(2)
    w.compile_latex("tau22", c)

    c = [Carrier(0, free), Carrier(0, free), Carrier(0, below_prim), Carrier(0, below)]
    w = Word(4)
    w.labels_in = "r_1, r_2, s_1, s_2".split(", ")
    w.labels_out = "r_2, r_1, s_1, s_2".split(", ")
    b = Braid(4)
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.compile_latex("tau31", c)

    c = [Carrier(0, free), Carrier(0, free), Carrier(0, above_prim)]
    w = Word(3)
    w.labels_in = "r_1, r_2, s'_1".split(", ")
    w.labels_out = "r_2, r_1, s'_1".split(", ")
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.compile_latex("tau32", c)

    c = [Carrier(0, below_prim), Carrier(0, below)]
    w = Word(2)
    w.labels_in = "s_1, s_2".split(", ")
    w.labels_out = "s_2, s_1".split(", ")
    b = Braid(2)
    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.compile_latex("tau41", c)

    c = [Carrier(0, above_prim)]
    w = Word(1)
    w.labels_in = ["s'_1"]
    w.labels_out = ["s'_1"]
    w.compile_latex("tau42", c)

    c = [Carrier(0, below_prim), Carrier(0, below)]
    w = Word(2)
    w.labels_in = "s_1, s_2".split(", ")
    w.labels_out = "s_1, s_2".split(", ")
    b = Braid(2)
    w.append_braid(b)
    w.compile_latex("tau43", c)

def minimal_stable() -> None:
    """Draws whatever Jenny's minimal stable
    figure is"""

def knitout_confusing() -> None:
    """Draws a confusing loop crossing both ways"""
    c = [Carrier(0, below_prim), Carrier(0, free), Carrier(0, free)]
    w = Word(3)
    b = Braid(3)
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, False))
    w.append_braid(b)
    w.labels_in = ['c', '\\textnormal{loop}', '']
    w.labels_out = ['', '\\textnormal{loop}', 'c']
    w.draw_postamble(3) # for the drop
    w.compile_latex("confusing-1", c, False)

    w = Word(3)
    b = Braid(3)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    w.labels_in = ['c', '\\textnormal{loop}', '']
    w.labels_out = ['', '\\textnormal{loop}', 'c']
    w.draw_postamble(3) # for the drop
    w.compile_latex("confusing-2", c, False)

def alpha_x_y_beta() -> None:
    """Draws a labelled generator for the braid groupoid"""
    c = [Carrier(0, free) for _ in range(3)] + [Carrier(0, below), Carrier(0, above)] + [Carrier(0, free) for _ in range(5)]
    w = Word(10)
    b = Braid(10)
    b.append(BraidGenerator(3, True))
    w.append_braid(b)
    w.labels_in = ['', '\\alpha', '', 'x', 'y', '', '', '\\beta', '', '']
    w.labels_out = ['', '\\alpha', '', 'y', 'x', '', '', '\\beta', '', '']
    w.compile_latex("alpha-x-y-beta", c, False)

def ts_strict() -> None:
    """Calculates a stupid braid in T^S with nothing but S strands"""
    c = [Carrier(0, below), Carrier(0, below_prim), Carrier(0, below)]
    w = Word(3)
    b = Braid(3)
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, False))
    w.append_braid(b)
    w.labels_in = ['s_2', 's_1', 's_3']
    w.labels_out = ['s_2', 's_3', 's_1']
    w.compile_latex("TS-strict", c)

def braid_canon_example() -> None:
    """Draws 4 figs for braid greedy normal form"""
    reset_colors()
    c_goid = [Carrier(0) for _ in range(5)]
    c_grp = [Carrier(0, free) for _ in range(5)]
    w = Word(5)
    b = Braid(5)
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    w.compile_latex("braid-no-canon", c_grp)
    w.labels_in = "a, b, c, d, e".split(", ")
    w.labels_out = "b, e, a, c, d".split(", ")
    w.compile_latex("braid-no-canon-goid", c_goid)

    w = Word(5)
    b = Braid(5)
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(3, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(1, True))
    w.append_braid(b)
    w.compile_latex("braid-canon", c_grp)
    w.labels_in = "a, b, c, d, e".split(", ")
    w.labels_out = "b, e, a, c, d".split(", ")
    w.compile_latex("braid-canon-goid", c_goid)

def layer_example() -> None:
    """Draws a simple word and an obfuscated word by L1, L2, L3. Then, draws
    both of them after \\Lr{}"""
    c = [Carrier(0, free), Carrier(0, below), Carrier(0, below), Carrier(0, free)]
    w = Word(4)
    w.labels_in = "r_1, s'_1, s'_2, r_2".split(", ")
    w.labels_out = "s_1, r_1, s_2, r_2".split(', ')
    w.append_layer(Layer(1, Knit(Bed(True), Dir(True), c[1:3], [Carrier(0, below_prim), Carrier(0, below)]), 1))
    b = Braid(4)
    b.append(BraidGenerator(0, False))
    w.append_braid(b)
    w.compile_latex("layer-init", c, False)

    w = Word(4)
    w.labels_in = "r_1, s'_1, s'_2, r_2".split(", ")
    w.labels_out = "s_1, r_1, s_2, r_2".split(', ')
    b = Braid(4)
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, False))
    w.append_braid(b)
    w.append_layer(Layer(0, Knit(Bed(True), Dir(True), c[1:3], [Carrier(0, below_prim), Carrier(0, below)]), 2))
    b = Braid(4)
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(0, False))
    w.append_braid(b)
    w.compile_latex("layer-init-after", c, False)

    w = Word(4)
    w.labels_in = "r_1, s'_1, s'_2, r_2".split(", ")
    w.labels_out = "s_1, r_1, s_2, r_2".split(', ')
    b = Braid(4)
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(2, False))
    w.append_braid(b)
    w.append_layer(Layer(2, Knit(Bed(False), Dir(False), list(reversed(c[1:3])), list(reversed([Carrier(0, below_prim), Carrier(0, below)]))), 0))
    b = Braid(4)
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, False))
    w.append_braid(b)
    w.compile_latex("layer-obfus", c, False)

    w = Word(4)
    w.labels_in = "r_1, s'_1, s'_2, r_2".split(", ")
    w.labels_out = "s_1, r_1, s_2, r_2".split(', ')
    b = Braid(4)
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(1, False))
    w.append_braid(b)
    w.append_layer(Layer(0, Knit(Bed(True), Dir(True), c[1:3], [Carrier(0, below_prim), Carrier(0, below)]), 2))
    b = Braid(4)
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(1, False))
    b.append(BraidGenerator(0, False))
    b.append(BraidGenerator(2, False))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, True))
    b.append(BraidGenerator(1, True))
    b.append(BraidGenerator(2, True))
    b.append(BraidGenerator(0, False))
    w.append_braid(b)
    w.compile_latex("layer-obfus-after", c, False)

def draw_half_compat() -> None:
    """Attempts to draw the half compat visual proof figs"""
    c = [Carrier(0, below) for _ in range(3)] + [Carrier(0, above) for _ in range(2)]
    ins = "a_1, a_2, a_3, b_1, b_2".split(", ")
    outs = list(reversed(ins))
    w = Word(5)
    b = Braid(5)
    b.append(BraidGenerator(2, True))

    b.append(BraidGenerator(0, True))
    w.append_braid(b)
    w.labels_in = ins
    w.labels_out = outs
    w.compile_latex("half_compat_proof", c, False)

def draw_overview_diagram() -> None:
    """Draws the 8-stitch diagram for the overview"""
    c = [Carrier(0, free)]
    w = Word(1)
    w.draw_preamble(0)
    w.append_layer(Layer(0, Knit(Bed(True), Dir(True), c, [Carrier(0, free) for _ in range(3)]), 0))
    w.append_layer(Layer(2, Knit(Bed(False), Dir(True), c, [Carrier(0, free) for _ in range(3)]), 0))
    w.append_layer(Layer(4, Knit(Bed(True), Dir(True), c, [Carrier(0, free) for _ in range(3)]), 0))
    b = Braid(7)
    b.append(BraidGenerator(5, True))
    b.append(BraidGenerator(4, True))
    w.append_braid(b)
    w.append_layer(Layer(2, Knit(Bed(False), Dir(False), [Carrier(0, free) for _ in range(3)], [Carrier(0, free) for _ in range(3)]), 2))
    w.append_layer(Layer(0, Knit(Bed(True), Dir(False), [Carrier(0, free) for _ in range(3)], [Carrier(0, free) for _ in range(3)]), 4))

    w.append_layer(Layer(0, Knit(Bed(True), Dir(True), [Carrier(0, free) for _ in range(3)], [Carrier(0, free) for _ in range(3)]), 4))
    w.append_layer(Layer(2, Knit(Bed(False), Dir(True), [Carrier(0, free) for _ in range(3)], [Carrier(0, free) for _ in range(3)]), 2))
    w.append_layer(Layer(4, Knit(Bed(True), Dir(True), [Carrier(0, free) for _ in range(3)], [Carrier(0, free) for _ in range(3)]), 0))
    w.compile_latex("overview-diagram", c)

from fig_gen.color import ColorGenerator 
def draw_jim_fig_6() -> None:
    c = ColorGenerator()
    colors = [c.get_next_color() for _ in range(10)]
    c = [Carrier(0, free)] + sum([[Carrier(0, colors[i]) for _ in range(2)] for i in range(5)], [])

    w = Word(11)
    w.append_layer(Layer(0, Knit(Bed(True), Dir(True), c[:3], [Carrier(0, colors[5]), Carrier(0, colors[5]), Carrier(0, free)]), 8))
    w.append_layer(Layer(2, Knit(Bed(True), Dir(True), [c[0]], [Carrier(0, colors[6]), Carrier(0, colors[6]), Carrier(0, free)]), 8))
    w.append_layer(Layer(4, Knit(Bed(True), Dir(True), [c[0] for _ in range(5)], [Carrier(0, colors[7]), Carrier(0, colors[7]), Carrier(0, free)]), 4))
    b = Braid(11)
    b.append(BraidGenerator(8, True))
    b.append(BraidGenerator(9, True))
    b.append(BraidGenerator(7, True))
    b.append(BraidGenerator(8, True))
    w.append_braid(b)
    w.append_layer(Layer(6, Knit(Bed(True), Dir(True), [c[0] for _ in range(5)], [Carrier(0, colors[8]), Carrier(0, colors[8]), Carrier(0, free)]), 0))
    w.append_layer(Layer(8, Knit(Bed(True), Dir(True), [c[0] for _ in range(1)], [Carrier(0, colors[9]), Carrier(0, colors[9]), Carrier(0, free)]), 0))
    w.compile_latex("KODA-6a", c, False)

    w = Word(11)
    b = Braid(11)
    b.append(BraidGenerator(8, True))
    b.append(BraidGenerator(9, True))
    b.append(BraidGenerator(7, True))
    b.append(BraidGenerator(8, True))
    w.append_braid(b)
    w.append_layer(Layer(0, Knit(Bed(True), Dir(True), c[:3], [Carrier(0, colors[5]), Carrier(0, colors[5]), Carrier(0, free)]), 8))
    w.append_layer(Layer(2, Knit(Bed(True), Dir(True), [c[0]], [Carrier(0, colors[6]), Carrier(0, colors[6]), Carrier(0, free)]), 8))
    w.append_layer(Layer(4, Knit(Bed(True), Dir(True), [c[0] for _ in range(5)], [Carrier(0, colors[7]), Carrier(0, colors[7]), Carrier(0, free)]), 4))
    w.append_layer(Layer(6, Knit(Bed(True), Dir(True), [c[0] for _ in range(5)], [Carrier(0, colors[8]), Carrier(0, colors[8]), Carrier(0, free)]), 0))
    w.append_layer(Layer(8, Knit(Bed(True), Dir(True), [c[0] for _ in range(1)], [Carrier(0, colors[9]), Carrier(0, colors[9]), Carrier(0, free)]), 0))
    w.compile_latex("KODA-6b", c, False)


def draw_move_past() -> None:
    """Draws the figures from this file"""
    # (w, c) = typed_n()
    # w.compile_latex("Tn", c)
    # (w, c) = well_typed_n()
    # w.compile_latex("Wn", c)

    # draw_layer_gens()

    # (w, c) = x()
    # w.compile_latex("x", c, False)
    # (w, c) = x(True, False)
    # w.compile_latex("x_pi", c)
    # w.labels_in = "r_2, s_1, r_1, , ".split(", ")
    # w.labels_out = "r_1, , s_1, r_2, ".split(", ")
    # w.compile_latex("x-gamma-cross", c, False)
    # (w, c) = x(False, True)
    # w.compile_latex("x_delta", c)
    # w.labels_in = ", s_1, , s_2, ".split(", ")
    # w.labels_out = ", s_2, s_1, , ".split(", ")
    # w.compile_latex("x-delta-cross", c, False)
    # # draw_rho_x_no_twist()
    # draw_psi_x()
    # draw_tau_x()
    draw_box_for_x()

    # draw_lattice_lr()

    # (w, c) = example_ls()
    # w.compile_latex("LS", c)

    # (w, c) = example_ts()
    # w.compile_latex("TS", c)

    # draw_snagged()
    # draw_unsnagged()

    # draw_layer_simp()
    # draw_layer_swap()

    # draw_preprocess()

    # draw_big_example()

    # draw_tau_examples()

    # knitout_confusing()
    # alpha_x_y_beta()
    # ts_strict()

    # braid_canon_example()
    # layer_example()
    # draw_half_compat()

    # draw_overview_diagram()

    # draw_jim_fig_6()
