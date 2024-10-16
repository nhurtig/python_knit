from braid.braid import Braid
from braid.braid_generator import BraidGenerator
from braid.canon.canon_braid import CanonBraid
from category.morphism import Knit
from common import Dir, Sign

class Layer:
    def __init__(self, left: int, middle: Knit, above: Braid, below: Braid) -> None:
        self.__left = left
        self.__middle = middle
        # TODO: check that n() of above, below match left, mid, right
        self.__above = above
        self.__below = below

    def __repr__(self) -> str:
        return f"Layer({self.__middle}:{self.__above})"

    def left(self) -> int:
        return self.__left

    def middle(self) -> Knit:
        return self.__middle

    def macro_subbraid(self) -> Braid:
        keep = set()
        for i in range(self.__above.n()):
            if i < self.__left:
                keep.add(i)
            elif i >= self.__left + len(self.__middle.outs()):
                keep.add(i)
        keep.add(self.__left + self.__middle.primary_index())

        return self.__above.subbraid(keep)

    def primary_twists(self) -> int:
        return self.__middle.primary().twists()

    def delta(self, sign: Sign) -> None:
        self.__middle.flip()
        i = self.__left
        n = len(self.__middle.outs())
        for j in range(i, i+n):
            o = self.__middle.outs()[j]
            o.twist(sign.pos())
        for j in range(i, i + n):
            # take strand i to index j
            for k in range(i, j):
                self.__above.prepend(BraidGenerator(k, sign.pos()))

        m = len(self.__middle.ins())
        for j in range(i, i+m):
            o = self.__middle.ins()[j]
            o.twist(not sign.pos())
        for j in range(i + m - 1, i - 1, -1):
            # take strand i to index j
            for k in range(i, j):
                self.__below.append(BraidGenerator(k, not sign.pos()))

    def sigma_conj(self, i: int, sign: Sign) -> None:
        """Performs the sigma conjugation rule on either
        side of this layer's box

        Args:
            i (int): index of swap in macro subspace
            sign (Sign): sign of sigma on top of box

        Raises:
            ValueError: i is too near the box
        """
        if i in [self.__left - 1, self.__left]:
            raise ValueError

        if i < self.__left - 1:
            above_i = i
            below_i = i
        else:
            above_i = i + len(self.__middle.outs()) - 1
            below_i = i + len(self.__middle.ins()) - 1

        self.__above.prepend(BraidGenerator(above_i, sign.pos()))
        self.__below.append(BraidGenerator(below_i, not sign.pos()))

    def underline_conj(self, dir: Dir, above: bool) -> None:
        """Performs the underline conj rule on either side
        of this layer's box

        Args:
            dir (Dir): Original location of the strand w.r.t.
            the box (was to the "dir" of the box)
            above (bool): Whether the strand goes above
            the box's inputs and outputs or not
        """
        i = self.__left
        n = len(self.__middle.outs())
        m = len(self.__middle.ins())

        match dir.right():
            case False:
                sign = not above
                for j in range(i - 1, i + n - 1):
                    self.__above.prepend(BraidGenerator(j, sign))

                sign = not sign
                for j in range(i - 1, i + m - 1):
                    self.__below.append(BraidGenerator(j, sign))

                self.__left -= 1
            case True:
                sign = above
                for j in range(i + n - 1, i - 1, -1):
                    self.__above.prepend(BraidGenerator(j, sign))

                sign = not sign
                for j in range(i + m - 1, i - 1, -1):
                    self.__below.append(BraidGenerator(j, sign))

                self.__left += 1

    def layer_canon(self) -> CanonBraid:
        return CanonBraid(self.__above)

class CanonLayer:
    def __init__(self, layer: Layer) -> None:
        CanonLayer.delta_step(layer)
        CanonLayer.macro_step(layer)
        self.__left = layer.left()
        self.__middle = layer.middle()
        self.__above = layer.layer_canon()

    def __repr__(self) -> str:
        return f"CanonLayer({self.__middle}:{self.__above})"

    @staticmethod
    def delta_step(layer: Layer) -> None:
        while layer.primary_twists() != 0:
            sign = layer.primary_twists() < 0
            layer.delta(Sign(sign))

    @staticmethod
    def macro_step(layer: Layer) -> None:
        for gen in layer.macro_subbraid():
            if gen.i() == layer.left() - 1:
                layer.underline_conj(Dir(False), gen.pos())
            elif gen.i() == layer.left():
                layer.underline_conj(Dir(True), not gen.pos())
            else:
                layer.sigma_conj(gen.i(), Sign(not gen.pos()))
