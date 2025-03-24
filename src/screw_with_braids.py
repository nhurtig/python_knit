# pylint: disable=no-name-in-module
from sage.all import BraidGroup  # type: ignore

# want to check
# psi_B(y)^{-1} ; tau'_T(x) ; y = tau'_T(x)
# when psi_T(y) = \epsilon, psi_B(x) = \epsilon

class TypedBraid:
    def __init__(self, braid, in_perm):
        assert braid.strands() == len(in_perm)
        self.braid = braid.left_normal_form()
        self.in_perm = in_perm
        self.out_perm = in_perm * braid.permutation()

    def __mul__(self, other):
        assert self.out_perm == other.in_perm
        return TypedBraid(self.braid * other.braid, self.in_perm)

def gamma(b, S):
    ret = BraidGroup(b.braid.strands())([])
    perm = []
    in_list = list(b.in_perm)
    for obj in in_list:
        if obj not in S:
            perm.append(obj)
        elif obj == S[0]:
            perm.append(obj)
    orig_perm = perm
    for gen in str(b.braid).split("*"):
        gen = gen.strip("s").split("^")
        (idx, pos) = (None, None)
        if len(gen) == 1:
            idx = int(gen[0])
            pos = True
        else:
            idx = int(gen[0])
            pos = False
        left = perm[idx]
        right = perm[idx+1]
        if left == S[0]:
            if right 