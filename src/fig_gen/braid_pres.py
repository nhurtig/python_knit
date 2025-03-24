"""
Figures for the braid group presentation for the bobbin
lace undergrads, 03/03/25
"""

from braid.braid import Braid
from category.object import Carrier
from fig_gen.color import reset_colors
from layer.word import Word


def ident_5():
    """Identity on 5 strands"""
    reset_colors()
    b = Braid(5)
    w = Word(5)
    w.append_braid(b)
    w.draw_postamble(4)
    w.compile_latex("ident-5", [Carrier(0, (0, 0, 0)) for _ in range(5)])


def interesting_5():
    """Two interesting braids on 5 strands"""
    reset_colors()
    b = Braid.str_to_braid(5, "AbaC")
    w = Word(5)
    w.append_braid(b)
    w.compile_latex("inter-5", [Carrier(0, (0, 0, 0)) for _ in range(5)])

    b = Braid.str_to_braid(5, "cABa")
    w = Word(5)
    w.append_braid(b)
    w.compile_latex("inter-5-inv", [Carrier(0, (0, 0, 0)) for _ in range(5)])

    reset_colors()
    b = Braid.str_to_braid(5, "BaCd")
    w = Word(5)
    w.append_braid(b)
    w.compile_latex("inter-5-2", [Carrier(0, (0, 0, 0)) for _ in range(5)])

def interesting_4():
    """Interesting braid on 4 strands"""
    b = Braid.str_to_braid(4, "BaCa")
    w = Word(4)
    w.append_braid(b)
    w.compile_latex("inter-4", [Carrier(0, (0, 0, 0)) for _ in range(4)])

def gens_3():
    """Draws generators and inverses of braid on 3 strands"""
    reset_colors()
    b = Braid.str_to_braid(3, "a")
    b.compile_latex("gen-1", [Carrier(0, (0, 0, 0)) for _ in range(3)])
    reset_colors()
    b = Braid.str_to_braid(3, "b")
    b.compile_latex("gen-2", [Carrier(0, (0, 0, 0)) for _ in range(3)])
    reset_colors()
    b = Braid.str_to_braid(3, "A")
    b.compile_latex("gen-3", [Carrier(0, (0, 0, 0)) for _ in range(3)])
    reset_colors()
    b = Braid.str_to_braid(3, "B")
    b.compile_latex("gen-4", [Carrier(0, (0, 0, 0)) for _ in range(3)])

def synonyms_3():
    """Draws two braid words that mean the same thing"""
    reset_colors()
    b = Braid.str_to_braid(3, "abAbB")
    b.compile_latex("syn-1", [Carrier(0, (0, 0, 0)) for _ in range(3)])
    reset_colors()
    b = Braid.str_to_braid(3, "abA")
    b.compile_latex("syn-2", [Carrier(0, (0, 0, 0)) for _ in range(3)])

def comm_diagrams():
    """Draws the commutative diagrams of the braid group"""
    reset_colors()
    b = Braid.str_to_braid(3, "aba")
    b.compile_latex("yb-1", [Carrier(0) for _ in range(3)])
    reset_colors()
    b = Braid.str_to_braid(3, "bab")
    b.compile_latex("yb-2", [Carrier(0) for _ in range(3)])

    reset_colors()
    b = Braid.str_to_braid(4, "ac")
    b.compile_latex("comm-1", [Carrier(0) for _ in range(4)])
    reset_colors()
    b = Braid.str_to_braid(4, "ca")
    b.compile_latex("comm-2", [Carrier(0) for _ in range(4)])

def draw_braid_pres():
    """Draws some figures for the braid presentation"""
    # ident_5()
    # interesting_5()
    # gens_3()
    # interesting_4()
    # synonyms_3()
    comm_diagrams()
