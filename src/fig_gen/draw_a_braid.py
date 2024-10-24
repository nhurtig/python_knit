"""
Example for how to draw a braid word
"""

from braid.braid import Braid
from category.object import Carrier

def draw_my_braid() -> None:
    """Draws an example braid word"""
    my_number_of_strands = 7
    my_braid_string_rep = "ABdaBdAeAb"
    my_braid = Braid.str_to_braid(my_number_of_strands, my_braid_string_rep)
    my_braid.compile_latex("my_example_filename", [Carrier(0) for _ in range(my_number_of_strands)])
