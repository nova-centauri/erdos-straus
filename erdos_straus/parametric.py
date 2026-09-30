"""Elsholtz–Tao / Rosati Type I and Type II constructions.

Type I (n divides exactly one denominator):
    4 a b d = n e + 1,    c e = a + b
    (x, y, z) = (a b d n, a c d, b c d)

Type II (n divides exactly two denominators):
    4 a b d = n + e,      c e = a + b
    (x, y, z) = (a b d, a c d n, b c d n)

These are the maps π^I and π^II of Elsholtz–Tao (2013), J. Aust. Math. Soc.
94:50–105, arXiv:1107.1010. A Type I (resp. II) solution exists iff there
are a, b, e > 0 with e | a+b and 4ab | (n e + 1) (resp. 4ab | (n + e)).

Polynomial identities for a residue class n ≡ r (mod q) exist only when r
is a quadratic non-residue mod q (Mordell 1967; Schinzel). The (a, b, e)
family realises that obstruction: n ≡ −e or n ≡ −e^{−1} (mod 4ab).
"""

from __future__ import annotations

from erdos_straus.arith import divisors
from erdos_straus.types import Triple


def type_I(n: int, a: int, b: int, e: int) -> Triple | None:
    if a < 1 or b < 1 or e < 1:
        return None
    if (a + b) % e != 0:
        return None
    denom = 4 * a * b
    ne1 = n * e + 1
    if ne1 % denom != 0:
        return None
    d = ne1 // denom
    c = (a + b) // e
    if c < 1 or d < 1:
        return None
    return Triple(a * b * d * n, a * c * d, b * c * d)


def type_II(n: int, a: int, b: int, e: int) -> Triple | None:
    if a < 1 or b < 1 or e < 1:
        return None
    if (a + b) % e != 0:
        return None
    denom = 4 * a * b
    if (n + e) % denom != 0:
        return None
    d = (n + e) // denom
    c = (a + b) // e
    if c < 1 or d < 1:
        return None
    return Triple(a * b * d, a * c * d * n, b * c * d * n)


def search_type_I(n: int, bound: int) -> Triple | None:
    """Search Type I solutions with 1 ≤ a, b ≤ bound."""
    for a in range(1, bound + 1):
        for b in range(a, bound + 1):  # a ≤ b w.l.o.g. up to swap
            s = a + b
            for e in divisors(s):
                t = type_I(n, a, b, e)
                if t is not None:
                    return t
                if a != b:
                    t = type_I(n, b, a, e)
                    if t is not None:
                        return t
    return None


def search_type_II(n: int, bound: int) -> Triple | None:
    """Search Type II solutions with 1 ≤ a, b ≤ bound."""
    for a in range(1, bound + 1):
        for b in range(a, bound + 1):
            s = a + b
            for e in divisors(s):
                t = type_II(n, a, b, e)
                if t is not None:
                    return t
                if a != b:
                    t = type_II(n, b, a, e)
                    if t is not None:
                        return t
    return None


def search_type_I_via_e(n: int, e_max: int) -> Triple | None:
    """Complete Type I search over e ≤ e_max, factoring (n e + 1)/4."""
    for e in range(1, e_max + 1):
        m = n * e + 1
        if m % 4 != 0:
            continue
        m //= 4
        for a in divisors(m):
            m1 = m // a
            for b in divisors(m1):
                if (a + b) % e == 0:
                    d = m1 // b
                    c = (a + b) // e
                    if c >= 1 and d >= 1:
                        return Triple(a * b * d * n, a * c * d, b * c * d)
    return None


def search_type_II_via_e(n: int, e_max: int) -> Triple | None:
    """Complete Type II search over e ≤ e_max, factoring (n + e)/4."""
    for e in range(1, e_max + 1):
        m = n + e
        if m % 4 != 0:
            continue
        m //= 4
        for a in divisors(m):
            m1 = m // a
            for b in divisors(m1):
                if (a + b) % e == 0:
                    d = m1 // b
                    c = (a + b) // e
                    if c >= 1 and d >= 1:
                        return Triple(a * b * d, a * c * d * n, b * c * d * n)
    return None


def et_catalog_hit(n: int, ab_bound: int = 80) -> Triple | None:
    """Try the Elsholtz–Tao (a, b, e) catalog with a b ≤ ab_bound."""
    for a in range(1, ab_bound + 1):
        b_max = ab_bound // a
        for b in range(1, b_max + 1):
            for e in divisors(a + b):
                t = type_II(n, a, b, e)
                if t is not None:
                    return t
                t = type_I(n, a, b, e)
                if t is not None:
                    return t
    return None
