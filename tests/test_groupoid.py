"""Tests braid word canonicalization
using fuzzing"""

import random
import math
from groupoid.groupoid import TnGen, TnInfo, TnType, psi_b, psi_t, simp

NUM_TESTS = 50
UPDATE_FREQ = 1000
RUN_FOREVER = True # overrides NUM_TESTS when True
INOUTS_AVG = 4
INDEPENDENT_STRANDS_AVG = 3
BASE_SEED = 0

random.seed(BASE_SEED)
rng = random.random


def geometric(average: float) -> int:
    """Samples from a geometric distribution

    Args:
        average (float): Expected value

    Returns:
        int: Sample
    """
    u = rng()
    num: float = math.log(1 - u)
    denom: float = math.log(1 - (1 / (average + 1)))
    return int(num / denom)

def random_info() -> TnInfo:
    bottom_outs = geometric(INOUTS_AVG - 2) + 2
    top_ins = geometric(INOUTS_AVG - 2) + 2
    n = bottom_outs + top_ins + geometric(INDEPENDENT_STRANDS_AVG)
    return TnInfo(n, bottom_outs, top_ins)

def random_type(strands: int) -> TnType:
    perm = list(range(strands))
    random.shuffle(perm)
    return TnType(perm)

def random_gen(info: TnInfo, in_type: TnType) -> TnGen:
    idx = int(rng() * (info.n - 1))
    pos = rng() < 0.5
    return TnGen(info, in_type, idx, pos)

def super_random_gen() -> TnGen:
    info = random_info()
    return random_gen(info, random_type(info.n))

def flatten(xss):
    return [x for xs in xss for x in xs]

def test_commute_gens() -> None:
    """Fuzzes many words with layers that can move past
    each other. Asserts that the layers are able to move
    past each other and after doing that twice, this is
    equivalent to the original"""
    i = BASE_SEED
    while True:
        for _ in range(NUM_TESTS):
            if i % UPDATE_FREQ == 0:
                print(i)

            random.seed(i)
            gen1 = super_random_gen()

            # s1 = gen1.input.perm[gen1.index]
            # s2 = gen1.input.perm[gen1.index + 1]
            # top_primary = gen1.info.bottom_outs
            # double_prim = False
            # if s1 == 0 or s2 == 0:
            #     if s1 == top_primary or s2 == top_primary:
            #         # i += 1
            #         double_prim = True
            # if not double_prim:
            #     i += 1
            #     continue

            random.seed(i)
            gen2 = super_random_gen()

            assert gen1 == gen2

            # print(gen1.info)
            # print(gen1.input)
            # print(gen1)

            pgen1 = flatten([psi_t(x) for x in psi_b(gen1)])
            pgen2 = flatten([psi_b(x) for x in psi_t(gen2)])

            # print(pgen1)
            # print(pgen2)

            # print(simp(pgen1))
            # print(simp(pgen2))
            # if len(pgen1) != 0:
            #     print("hi")
            #     print(gen1)
            #     print(pgen1)

            assert simp(pgen1) == simp(pgen2)

            i += 1
        if not RUN_FOREVER:
            break

def test_specific_commute() -> None:
    info = TnInfo(4, 2, 2)
    input_type = TnType([1, 0, 2, 3])
    # 0, 2 are primaries
    gen1 = TnGen(info, input_type, 1, True)
    gen2 = TnGen(info, input_type, 1, True)

    assert gen1 == gen2

    pgen1 = flatten([psi_t(x) for x in psi_b(gen1)])
    pgen2 = flatten([psi_b(x) for x in psi_t(gen2)])
    # if len(pgen1) != 0:
    #     print("hi")
    #     print(gen1)
    #     print(pgen1)
    #     print(pgen2)

    assert simp(pgen1) == simp(pgen2)
