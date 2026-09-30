from fractions import Fraction

from erdos_straus.verifier import (
    equation_holds,
    n_mod_840,
    residual,
    verify,
    verify_triple,
)


def test_known_n5():
    assert verify(5, 2, 4, 20)
    assert verify(5, 2, 5, 10)
    assert verify_triple(5, (2, 4, 20))


def test_rejects_bad_triple():
    assert not verify(5, 2, 3, 7)
    assert not verify(1, 1, 1, 1)
    assert not verify(5, 0, 2, 2)
    assert not verify(5, -1, 2, 2)


def test_integer_form_matches_fractions():
    assert equation_holds(5, 2, 5, 10)
    assert Fraction(4, 5) == Fraction(1, 2) + Fraction(1, 5) + Fraction(1, 10)


def test_n2_allowed_repeats():
    assert verify(2, 1, 2, 2)


def test_residual_and_mod840():
    assert residual(5, 2, 5, 10) == 0
    assert residual(5, 2, 3, 7) != 0
    assert n_mod_840(1009) == 169
    assert n_mod_840(2521) == 1
