"""Shifted-greedy (Ionascu–Wilson / López) constructions for n = 4k + 1.

For n = 4k + 1 and t ≥ 0 set the first denominator to k + 1 + t. Then

    4/n − 1/(k + 1 + t) = (4t + 3) / (n (k + 1 + t)).

If the remainder (4t + 3)/M is a sum of two unit fractions, we are done.
By the two-term theorem this happens iff M has factors u, w with
u + w ≡ 0 (mod 4t + 3). In particular, if some divisor w of k+1+t
satisfies w ≡ −1 (mod 4t + 3), the choice u = 1 works.

Special cases:
    t = 0: remainder 3/(n(k+1)). Succeeds if k+1 has a divisor ≡ 2 (mod 3),
           or if k = 3ℓ + 1 / k = 3ℓ + 2 (Ionascu–Wilson 2011).
    t = 1: remainder 7/(n(k+2)). Succeeds if a divisor ≡ 6 (mod 7) exists.

This family is *not* a single polynomial identity in n. It is a
divisor-conditional construction, which is why it can hit quadratic-residue
classes that Mordell's obstruction forbids for polynomial identities.
"""

from __future__ import annotations

from erdos_straus.two_term import two_unit_fractions
from erdos_straus.types import Triple


def shifted_greedy(n: int, t_max: int = 64) -> Triple | None:
    """Try first denominators k+1, k+2, …, k+1+t_max for n = 4k+1."""
    if n < 5 or n % 4 != 1:
        return None
    k = (n - 1) // 4
    for t in range(0, t_max + 1):
        first = k + 1 + t
        numer = 4 * t + 3
        m = n * first
        pair = two_unit_fractions(numer, m)
        if pair is not None:
            return Triple(first, pair[0], pair[1])
    return None


def ionascu_k_mod3(n: int) -> Triple | None:
    """Closed Ionascu–Wilson cases for n = 4k+1 with k ≢ 0 (mod 3).

    k = 3ℓ + 2: k+1 is divisible by 3, so 3/(n(k+1)) is already a unit
    fraction and we pad by splitting it.
    k = 3ℓ + 1: u = 1, w = 2 works in the two-term theorem for 3/(n(k+1))
    because 1+2 ≡ 0 (mod 3) and 2 | (k+1) is *not* required — wait:
    we need u w | n(k+1). u=1, w=2 so 2 | n(k+1). n is odd, so 2 | (k+1),
    i.e. k odd, which holds for k = 3ℓ+1.
    """
    if n < 5 or n % 4 != 1:
        return None
    k = (n - 1) // 4
    first = k + 1
    m = n * first
    if k % 3 == 2:
        # 3/m is the unit 1/(m/3). Split to three terms:
        unit = m // 3
        # 4/n = 1/first + 1/unit; split 1/unit.
        return Triple(first, unit + 1, unit * (unit + 1))
    if k % 3 == 1:
        # u=1, w=2, p=3: t=(1+2)/3=1, y=m, z=m/2.
        if m % 2 != 0:
            return None
        return Triple(first, m // 2, m)
    return None
