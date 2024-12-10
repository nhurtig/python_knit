from __future__ import annotations
from typing import Optional, Tuple


class TnInfo:
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

    def __repr__(self) -> str:
        return repr((self.n, self.bottom_outs, self.top_ins))


class TnType:
    """Bottom gets the first strands, then top, then the free strands. Least
    strand is primary"""

    def __init__(self, perm: list[int]) -> None:
        self.perm = perm
        self.n = len(perm)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TnType):
            return False
        return self.perm == other.perm

    def __hash__(self) -> int:
        h = 0
        for i in self.perm:
            h *= self.n
            h += i
        return h

    def __repr__(self) -> str:
        return repr(self.perm)


class TnGen:
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TnGen):
            return False
        return (
            self.info == other.info
            and self.input == other.input
            and self.output == other.output
            and self.index == other.index
            and self.pos == other.pos
        )

    def __repr__(self) -> str:
        return "|" * self.index + "**" + "|" * (self.info.n - self.index - 2)

    def __hash__(self) -> int:
        return hash(self.input) * self.index


def simp(word: list[TnGen]) -> list[TnGen]:
    return simp_helper(word)[0]

def simp_helper(word: list[TnGen]) -> Tuple[list[TnGen], bool]:
    if len(word) < 2:
        return (word, False)
    [g1, g2] = word[:2]
    changed = False
    if abs(g1.index - g2.index) >= 2 and g2.index < g1.index:
        old_g1 = g1
        old_g2 = g2
        g1 = TnGen(g2.info, g1.input, g2.index, g2.pos)
        g2 = TnGen(old_g1.info, g1.output, old_g1.index, old_g1.pos)
        assert old_g2.output == g2.output
        changed = True
    (post, changed2) = simp_helper([g2] + word[2:])
    new_word = [g1] + post

    if changed2:
        return (simp(new_word), True)
    else:
        return (new_word, changed)


def pi_b_type(t: TnType, bottom_outs: int) -> TnType:
    new_perm = [
        x - bottom_outs + 1 if x >= bottom_outs else -1 if x != 0 else 0 for x in t.perm
    ]
    new_new_perm = []
    for x in new_perm:
        if x >= 0:
            new_new_perm.append(x)
    return TnType(new_new_perm)


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
                return TnGen(
                    TnInfo(proj_input.n, 1, 1),
                    proj_input,
                    proj_input.perm.index(new_s1),
                    g.pos,
                )
    else:
        if s1 < g.info.bottom_outs:
            # s1 ignored
            return None
        else:
            # s1 non-primary
            if s2 < g.info.bottom_outs and s2 == 0:
                # s1 non-primary, s2 primary
                new_s1 = s1 - g.info.bottom_outs + 1
                return TnGen(
                    TnInfo(proj_input.n, 1, 1),
                    proj_input,
                    proj_input.perm.index(new_s1),
                    g.pos,
                )
            else:
                if s2 < g.info.bottom_outs:
                    # s2 ignored
                    return None
                else:
                    # s1 non-primary, s2 non-primary
                    new_s1 = s1 - g.info.bottom_outs + 1
                    return TnGen(
                        TnInfo(proj_input.n, 1, 1),
                        proj_input,
                        proj_input.perm.index(new_s1),
                        g.pos,
                    )


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
            for iswap in reversed(
                range(new_input.perm.index(0), new_input.perm.index(0) + bottom_outs)
            ):
                new_g = TnGen(info, new_input, iswap, g.pos)
                gens.append(new_g)
                new_input = new_g.output
            return gens
    else:
        # s1 non-primary
        if s2 == 0:
            # s1 non-primary, s2 primary
            gens = []
            for iswap in range(
                new_input.perm.index(0) - 1, new_input.perm.index(0) + bottom_outs - 1
            ):
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
        phi_pi_g = phi_b(pi_g, g.info)
        # print(f"psi_b: {g} -> {pi_g} -> {phi_pi_g}")
        return phi_pi_g
    else:
        return []


# TOP


def pi_t_type(t: TnType, bottom_outs: int, top_ins: int) -> TnType:
    new_perm = [
        (
            x
            if x < bottom_outs
            else (
                x - top_ins + 1
                if x >= bottom_outs + top_ins
                else -1 if x != bottom_outs else bottom_outs
            )
        )
        for x in t.perm
    ]
    new_new_perm = []
    for x in new_perm:
        if x >= 0:
            new_new_perm.append(x)
    return TnType(new_new_perm)


def pi_t(g: TnGen) -> Optional[TnGen]:
    s1 = g.input.perm[g.index]
    s2 = g.input.perm[g.index + 1]
    proj_input = pi_t_type(g.input, g.info.bottom_outs, g.info.top_ins)
    if (
        s1 >= g.info.bottom_outs
        and s1 < g.info.bottom_outs + g.info.top_ins
        and s1 == g.info.bottom_outs
    ):
        # s1 primary
        if (
            s2 >= g.info.bottom_outs
            and s2 < g.info.bottom_outs + g.info.top_ins
            and s2 == g.info.bottom_outs
        ):
            # s1 primary, s2 primary???
            raise ValueError("permutation not valid!")
        else:
            if s2 >= g.info.bottom_outs and s2 < g.info.bottom_outs + g.info.top_ins:
                # s2 ignored
                return None
            else:
                # s1 primary, s2 non-primary
                new_s1 = g.info.bottom_outs
                return TnGen(
                    TnInfo(proj_input.n, 1, 1),
                    proj_input,
                    proj_input.perm.index(new_s1),
                    g.pos,
                )
    else:
        if s1 >= g.info.bottom_outs and s1 < g.info.bottom_outs + g.info.top_ins:
            # s1 ignored
            return None
        else:
            # s1 non-primary
            if (
                s2 >= g.info.bottom_outs
                and s2 < g.info.bottom_outs + g.info.top_ins
                and s2 == g.info.bottom_outs
            ):
                # s1 non-primary, s2 primary
                new_s1 = s1 if s1 < g.info.bottom_outs else s1 - g.info.top_ins + 1
                return TnGen(
                    TnInfo(proj_input.n, 1, 1),
                    proj_input,
                    proj_input.perm.index(new_s1),
                    g.pos,
                )
            else:
                if (
                    s2 >= g.info.bottom_outs
                    and s2 < g.info.bottom_outs + g.info.top_ins
                ):
                    # s2 ignored
                    return None
                else:
                    # s1 non-primary, s2 non-primary
                    new_s1 = s1 if s1 < g.info.bottom_outs else s1 - g.info.top_ins + 1
                    return TnGen(
                        TnInfo(proj_input.n, 1, 1),
                        proj_input,
                        proj_input.perm.index(new_s1),
                        g.pos,
                    )


def phi_t_type(t: TnType, bottom_outs: int, top_ins: int) -> TnType:
    new_perm: list[int] = []
    for x in t.perm:
        if x < bottom_outs:
            new_perm.append(x)
        elif x == bottom_outs:
            new_perm.extend(range(bottom_outs, bottom_outs + top_ins))
        else:
            new_perm.append(x + top_ins - 1)
    return TnType(new_perm)


def phi_t(g: TnGen, info: TnInfo) -> list[TnGen]:
    bottom_outs = info.bottom_outs
    top_ins = info.top_ins
    new_input = phi_t_type(g.input, bottom_outs, top_ins)
    s1 = g.input.perm[g.index]
    s2 = g.input.perm[g.index + 1]
    if s1 == bottom_outs:
        # s1 primary
        if s2 == bottom_outs:
            # both primary?
            raise ValueError
        else:
            # s1 primary, s2 non-primary
            gens = []
            for iswap in reversed(
                range(
                    new_input.perm.index(bottom_outs),
                    new_input.perm.index(bottom_outs) + top_ins,
                )
            ):
                new_g = TnGen(info, new_input, iswap, g.pos)
                gens.append(new_g)
                new_input = new_g.output
            return gens
    else:
        # s1 non-primary
        if s2 == bottom_outs:
            # s1 non-primary, s2 primary
            gens = []
            for iswap in range(
                new_input.perm.index(bottom_outs) - 1,
                new_input.perm.index(bottom_outs) + top_ins - 1,
            ):
                new_g = TnGen(info, new_input, iswap, g.pos)
                gens.append(new_g)
                new_input = new_g.output
            return gens
        else:
            # both non-primary
            s1_new = s1 if s1 < bottom_outs else s1 + top_ins - 1
            return [TnGen(info, new_input, new_input.perm.index(s1_new), g.pos)]


def psi_t(g: TnGen) -> list[TnGen]:
    pi_g = pi_t(g)
    if pi_g is not None:
        phi_pi_g = phi_t(pi_g, g.info)
        # print(f"psi_t: {g} -> {pi_g} -> {phi_pi_g}")
        return phi_pi_g
    else:
        return []
