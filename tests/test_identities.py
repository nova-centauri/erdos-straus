from math import gcd

from erdos_straus.identities import (
    apply_classical,
    even_identity,
    is_mordell_hard,
    mod3_eq2,
    mod4_eq3,
    mod8_eq5,
)
from erdos_straus.verifier import verify


def test_even_range():
    for n in range(2, 200, 2):
        t = even_identity(n)
        assert verify(n, t.x, t.y, t.z)


def test_mod4_eq3_range():
    for n in range(3, 400, 4):
        t = mod4_eq3(n)
        assert verify(n, t.x, t.y, t.z)


def test_mod3_eq2_range():
    for n in range(2, 400):
        if n % 3 == 2:
            t = mod3_eq2(n)
            assert verify(n, t.x, t.y, t.z)


def test_mod8_eq5_range():
    for n in range(5, 400, 8):
        t = mod8_eq5(n)
        assert verify(n, t.x, t.y, t.z)


def test_mod7_identities():
    from erdos_straus.identities import mod7_eq3, mod7_eq5, mod7_eq6

    for n in range(3, 400):
        if n % 7 == 3:
            t = mod7_eq3(n)
            assert verify(n, t.x, t.y, t.z)
        if n % 7 == 5:
            t = mod7_eq5(n)
            assert verify(n, t.x, t.y, t.z)
        if n % 7 == 6:
            t = mod7_eq6(n)
            assert verify(n, t.x, t.y, t.z)


def test_mod20_identities():
    from erdos_straus.identities import mod20_eq13, mod20_eq17

    for n in range(13, 500):
        if n % 20 == 17:
            t = mod20_eq17(n)
            assert verify(n, t.x, t.y, t.z)
        if n % 20 == 13:
            t = mod20_eq13(n)
            assert verify(n, t.x, t.y, t.z)


def test_mod44_extended_identities():
    from erdos_straus.identities import apply_extended, mod44_eq29, mod44_eq41

    for n in range(29, 500):
        if n % 44 == 41:
            t = mod44_eq41(n)
            assert verify(n, t.x, t.y, t.z)
            assert apply_extended(n) is not None
        if n % 44 == 29:
            t = mod44_eq29(n)
            assert verify(n, t.x, t.y, t.z)
            assert apply_extended(n) is not None
    # First Mordell-hard prime is in this family.
    t = mod44_eq41(1009)
    assert verify(1009, t.x, t.y, t.z)


def test_classical_leftover_is_mordell_six():
    """Our explicit identities leave exactly Mordell's six residues mod 840."""
    leftover = []
    for r in range(840):
        n = r if r >= 2 else r + 840
        if (
            n % 2 == 0
            or n % 4 == 3
            or n % 3 == 2
            or n % 8 == 5
            or n % 7 in (3, 5, 6)
            or n % 20 in (13, 17)
        ):
            continue
        leftover.append(r)
    # Composites divisible by 3 or 5 can miss every residue predicate
    # (e.g. 9, 25, 49) and are handled by scaling, not by a congruence.
    primitive = {r for r in leftover if gcd(r, 210) == 1}
    assert primitive == {1, 121, 169, 289, 361, 529}


def test_apply_classical_hits_its_predicates():
    missed = []
    for n in range(2, 400):
        if not (
            n % 2 == 0
            or n % 4 == 3
            or n % 3 == 2
            or n % 8 == 5
            or n % 7 in (3, 5, 6)
            or n % 20 in (13, 17)
        ):
            continue
        hit = apply_classical(n)
        if hit is None:
            missed.append(n)
    assert missed == []


def test_mordell_hard_list():
    assert 1009 % 840 == 169
    assert is_mordell_hard(1009)
    assert is_mordell_hard(2521)
    assert not is_mordell_hard(5)
    assert not is_mordell_hard(73)  # 73 mod 840 = 73, not a listed square
