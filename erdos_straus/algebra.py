"""Sympy verification of polynomial identities.

Every function here proves an algebraic identity identically in the
parameter, not just on sample integers. If a check fails, it raises.
"""

from __future__ import annotations

import sympy as sp

# Identities are written inline in the proofs so the check does not
# depend on Python-int constructors.


def _clear_equation(n, x, y, z) -> sp.Expr:
    """4xyz − n(xy + xz + yz), simplified."""
    return sp.simplify(4 * x * y * z - n * (x * y + x * z + y * z))


def prove_even() -> None:
    k = sp.symbols("k", integer=True, positive=True)
    n = 2 * k
    x, y, z = n / 2, n, n
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"even identity residual {residual}")


def prove_mod4_eq3() -> None:
    k = sp.symbols("k", integer=True, nonnegative=True)
    n = 4 * k + 3
    t = k + 1
    x, y, z = 2 * t, 2 * t, n * t
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod4 identity residual {residual}")
    # Two-term form 1/t + 1/(n t)
    residual2 = sp.simplify(sp.Integer(1) / t + sp.Integer(1) / (n * t) - 4 / n)
    if residual2 != 0:
        raise AssertionError(f"mod4 two-term residual {residual2}")


def prove_mod3_eq2() -> None:
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = 3 * t + 2
    x, y, z = n, (n + 1) / 3, n * (n + 1) / 3
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod3 identity residual {residual}")


def prove_mod8_eq5() -> None:
    t = sp.symbols("t", integer=True, positive=True)
    n = 8 * t - 3
    x, y, z = 2 * t, t * n, 2 * t * n
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod8 identity residual {residual}")


def prove_type_I_map() -> None:
    a, b, c, d, e, n = sp.symbols("a b c d e n", integer=True, positive=True)
    # Assume 4abd = n e + 1 and c e = a + b.
    x = a * b * d * n
    y = a * c * d
    z = b * c * d
    residual = 4 * x * y * z - n * (x * y + x * z + y * z)
    residual = residual.subs({c: (a + b) / e})
    residual = residual.subs({d: (n * e + 1) / (4 * a * b)})
    residual = sp.simplify(residual)
    if residual != 0:
        raise AssertionError(f"Type I map residual {residual}")


def prove_type_II_map() -> None:
    a, b, c, d, e, n = sp.symbols("a b c d e n", integer=True, positive=True)
    x = a * b * d
    y = a * c * d * n
    z = b * c * d * n
    residual = 4 * x * y * z - n * (x * y + x * z + y * z)
    residual = residual.subs({c: (a + b) / e})
    residual = residual.subs({d: (n + e) / (4 * a * b)})
    residual = sp.simplify(residual)
    if residual != 0:
        raise AssertionError(f"Type II map residual {residual}")


def prove_shifted_remainder() -> None:
    """4/n − 1/(k+1+t) = (4t+3)/(n(k+1+t)) identically when n = 4k+1."""
    k, t = sp.symbols("k t", integer=True, nonnegative=True)
    n = 4 * k + 1
    first = k + 1 + t
    lhs = 4 / n - 1 / first
    rhs = (4 * t + 3) / (n * first)
    if sp.simplify(lhs - rhs) != 0:
        raise AssertionError("shifted remainder identity failed")


def prove_ionascu_k_eq2() -> None:
    """k = 3ℓ+2: 4/n = 1/(k+1) + 1/(n(k+1)/3)."""
    ell = sp.symbols("ell", integer=True, nonnegative=True)
    k = 3 * ell + 2
    n = 4 * k + 1
    first = k + 1
    unit = n * first / 3
    residual = sp.simplify(1 / first + 1 / unit - 4 / n)
    if residual != 0:
        raise AssertionError(f"ionascu k≡2 residual {residual}")


def prove_mod7_eq3() -> None:
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = 7 * t + 3
    x, y, z = 2 * t + 1, 2 * n, 2 * n * (2 * t + 1)
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod7≡3 residual {residual}")


def prove_mod7_eq5() -> None:
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = 7 * t + 5
    x, y, z = 2 * (t + 1), n * (t + 1), 2 * n
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod7≡5 residual {residual}")


def prove_mod20_eq17() -> None:
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = 20 * t + 17
    x = (n + 3) / 4
    y = n * (n + 3) / 10
    z = n * (n + 3) / 2
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod20≡17 residual {residual}")


def prove_mod20_eq13() -> None:
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = 20 * t + 13
    x = n * (3 * n + 1) / 4
    y = (3 * n + 1) / 10
    z = (3 * n + 1) / 2
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod20≡13 residual {residual}")


def prove_mod7_eq6() -> None:
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = 7 * t + 6
    x, y, z = 2 * (t + 1), 2 * n, 2 * n * (t + 1)
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod7≡6 residual {residual}")


def prove_mod44_eq41() -> None:
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = 44 * t + 41
    d = t + 1
    x, y, z = 11 * d, 4 * d * n, 44 * d * n
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod44≡41 residual {residual}")


def prove_mod44_eq29() -> None:
    t = sp.symbols("t", integer=True, nonnegative=True)
    n = 44 * t + 29
    d = 3 * t + 2
    x, y, z = 11 * d * n, 4 * d, 44 * d
    residual = _clear_equation(n, x, y, z)
    if residual != 0:
        raise AssertionError(f"mod44≡29 residual {residual}")


def prove_all() -> None:
    prove_even()
    prove_mod4_eq3()
    prove_mod3_eq2()
    prove_mod8_eq5()
    prove_mod7_eq3()
    prove_mod7_eq5()
    prove_mod7_eq6()
    prove_mod20_eq17()
    prove_mod20_eq13()
    prove_mod44_eq41()
    prove_mod44_eq29()
    prove_type_I_map()
    prove_type_II_map()
    prove_shifted_remainder()
    prove_ionascu_k_eq2()


if __name__ == "__main__":
    prove_all()
    print("all algebraic identities check out")
