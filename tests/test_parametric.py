from erdos_straus.parametric import type_I, type_II
from erdos_straus.verifier import verify


def test_type_II_n_eq_3_mod_4():
    # a=b=e=1: 4 | n+1 ⇒ n ≡ 3 (mod 4)
    for n in range(3, 80, 4):
        t = type_II(n, 1, 1, 1)
        assert t is not None
        assert verify(n, t.x, t.y, t.z)


def test_type_I_n_eq_3_mod_4():
    # a=b=e=1: 4 | n+1 ⇒ n ≡ 3 (mod 4)
    for n in range(3, 80, 4):
        t = type_I(n, 1, 1, 1)
        # Type I with these params: 4abd = n+1, same condition
        if t is not None:
            assert verify(n, t.x, t.y, t.z)


def test_type_II_mod8():
    # Salez 8t-3: a=1, b=2, e=3 ⇒ 8 | n+3 ⇒ n ≡ 5 (mod 8)
    for n in range(5, 80, 8):
        t = type_II(n, 1, 2, 3)
        assert t is not None
        assert verify(n, t.x, t.y, t.z)
