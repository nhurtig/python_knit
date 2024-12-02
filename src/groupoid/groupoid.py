from __future__ import annotations
from typing import Optional

class TnInfo():
    """Data class for the signature of a Tn"""
    def __init__(self, n: int, bottom_outs: int, top_ins: int) -> None:
        self.n = n
        self.bottom_outs = bottom_outs
        self.top_ins = top_ins

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TnInfo):
            return False
        return (
            self.n == other.n
            and self.bottom_outs == other.bottom_outs
            and self.top_ins == other.top_ins
        )

class TnType():
    """Bottom gets the first strands, then top, then the free strands. Least
    strand is primary"""
    def __init__(self, perm: list[int]) -> None:
        self.perm = perm
        self.n = len(perm)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TnType):
            return False
        return self.perm == other.perm

class TnGen():
    def __init__(self, info: TnInfo, input_type: TnType, index: int, pos: bool):
        self.info = info
        self.input = input_type
        self.index = index
        self.pos = pos
        out_perm = input_type.perm.copy()
        tmp = out_perm[index]
        out_perm[index] = out_perm[index + 1]
        out_perm[index + 1] = tmp
        self.output = TnType(out_perm)

def pi_b_type(t: TnType, bottom_outs: int) -> TnType:
    new_perm = [x - bottom_outs + 1 if x >= bottom_outs else -1 if x != 0 else 0 for x in t.perm]
    return TnType(new_perm)

def pi_b(g: TnGen) -> Optional[TnGen]:
    s1 = g.input.perm[g.index]
    s2 = g.input.perm[g.index + 1]
    proj_input = pi_b_type(g.input, g.info.bottom_outs)
    if s1 < g.info.bottom_outs and s1 == 0:
        # s1 primary
        if s2 < g.info.bottom_outs and s2 == 0:
            # s1 primary, s2 primary???
            raise ValueError("permutation not valid!")
        else:
            if s2 < g.info.bottom_outs:
                # s2 ignored
                return None
            else:
                # s1 primary, s2 non-primary
                new_s1 = 0
                return TnGen(TnInfo(proj_input.n, 1, 1), proj_input, proj_input.perm.index(new_s1), g.pos)
    else:
        if s1 < g.info.bottom_outs:
            # s1 ignored
            return None
        else:
            # s1 non-primary
            if s2 < g.info.bottom_outs and s2 == 0:
                # s1 non-primary, s2 primary
                new_s1 = s1 - g.info.bottom_outs + 1
                return TnGen(TnInfo(proj_input.n, 1, 1), proj_input, proj_input.perm.index(new_s1), g.pos)
            else:
                if s2 < g.info.bottom_outs:
                    # s2 ignored
                    return None
                else:
                    # s1 non-primary, s2 non-primary
                    new_s1 = s1 - g.info.bottom_outs + 1
                    return TnGen(TnInfo(proj_input.n, 1, 1), proj_input, proj_input.perm.index(new_s1), g.pos)

def phi_b_type(t: TnType, bottom_outs: int) -> TnType:
    new_perm: list[int] = []
    for x in t.perm:
        if x == 0:
            new_perm.extend(range(bottom_outs))
        else:
            new_perm.append(x + bottom_outs - 1)
    return TnType(new_perm)

def phi_b(g: TnGen, info: TnInfo) -> list[TnGen]:
    bottom_outs = info.bottom_outs
    new_input = phi_b_type(g.input, bottom_outs)
    s1 = g.input.perm[g.index]
    s2 = g.input.perm[g.index + 1]
    if s1 == 0:
        # s1 primary
        if s2 == 0:
            # both primary?
            raise ValueError
        else:
            # s1 primary, s2 non-primary
            gens = []
            for iswap in reversed(range(new_input.perm.index(0), new_input.perm.index(0) + bottom_outs)):
                new_g = TnGen(info, new_input, iswap, g.pos)
                gens.append(new_g)
                new_input = new_g.output
            return gens
    else:
        # s1 non-primary
        if s2 == 0:
            # s1 non-primary, s2 primary
            gens = []
            for iswap in range(new_input.perm.index(0) - 1, new_input.perm.index(0) + bottom_outs - 1):
                new_g = TnGen(info, new_input, iswap, g.pos)
                gens.append(new_g)
                new_input = new_g.output
            return gens
        else:
            # both non-primary
            s1_new = s1 + bottom_outs - 1
            return [TnGen(info, new_input, new_input.perm.index(s1_new), g.pos)]

def psi_b(g: TnGen) -> list[TnGen]:
    pi_g = pi_b(g)
    if pi_g is not None:
        return phi_b(pi_g, g.info)
    else:
        return []
