"""Shifted-greedy first-R for n = 4k+1.

For t ≥ 0 the first denominator is k+1+t and the remainder is
(4t+3) / (n (k+1+t)). The first-R recorded in the Heavy / Opus notes
is the remainder numerator 4t+3 at the smallest t that splits into two
unit fractions (8803369 → 107, 287567281 → 83, 496609 → 51).

This is a search measurement, not a cover. Bounded shifted-greedy
cannot finish a Mordell class (`notes/CLOSED.md`).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from erdos_straus.arith import factorize, is_prime
from erdos_straus.two_term import two_unit_fractions
from erdos_straus.verifier import residual, verify


@dataclass(frozen=True)
class FirstR:
    n: int
    t: int
    first_r: int  # 4*t + 3
    x: int
    y: int
    z: int

    @property
    def n_mod_840(self) -> int:
        return self.n % 840


def _divisors_from_factors(facts: dict[int, int]) -> list[int]:
    divs = [1]
    for p, exp in facts.items():
        nxt: list[int] = []
        mul = 1
        for _ in range(exp + 1):
            nxt.extend(d * mul for d in divs)
            mul *= p
        divs = nxt
    return divs


def _factors_of_q(n: int, first: int, n_is_prime: bool) -> dict[int, int]:
    """Factor q = n * first without trial-dividing the product."""
    facts = dict(factorize(first))
    if n_is_prime:
        facts[n] = facts.get(n, 0) + 1
    else:
        for p, e in factorize(n).items():
            facts[p] = facts.get(p, 0) + e
    return facts


def remainder_splits(t: int, n: int, first: int, *, n_is_prime: bool = True) -> tuple[int, int] | None:
    """Two-term split of (4t+3) / (n*first), or None.

    Uses the two-term theorem on the already-factored denominator so a
    10^8-scale first-R scan does not factor n*first as a blob.
    """
    p = 4 * t + 3
    q = n * first
    g = gcd(p, q)
    p //= g
    q //= g
    if p == 1:
        return (q + 1, q * (q + 1))

    facts = _factors_of_q(n, first, n_is_prime)
    # Remove the gcd that was divided out of q.
    rest = g
    for prime in sorted(facts):
        while rest % prime == 0 and facts[prime] > 0:
            facts[prime] -= 1
            rest //= prime
            if facts[prime] == 0:
                del facts[prime]
    if rest > 1:
        # g had a prime that sat in p's cofactor; leftover is 1 after the
        # p/q reduction, so this should not happen for our (p, n*first).
        return two_unit_fractions(p, q)

    divs = _divisors_from_factors(facts)
    # uw | q and u+w ≡ 0 (mod p). Walk the divisor list, not 0..q.
    for u in divs:
        if q % u:
            continue
        limit = q // u
        for w in divs:
            if w > limit or limit % w:
                continue
            if (u + w) % p != 0:
                continue
            tt = (u + w) // p
            if tt < 1:
                continue
            y = q * tt // u
            z = q * tt // w
            return (y, z) if y <= z else (z, y)
    return None


def first_r(n: int, t_max: int = 80, *, n_is_prime: bool | None = None) -> FirstR | None:
    """Smallest shifted-greedy success with first-R = 4t+3, or None."""
    if n < 5 or n % 4 != 1:
        return None
    if n_is_prime is None:
        n_is_prime = is_prime(n)
    k = (n - 1) // 4
    for t in range(0, t_max + 1):
        first = k + 1 + t
        pair = remainder_splits(t, n, first, n_is_prime=n_is_prime)
        if pair is None:
            continue
        y, z = pair
        if verify(n, first, y, z) and residual(n, first, y, z) == 0:
            return FirstR(n=n, t=t, first_r=4 * t + 3, x=first, y=y, z=z)
    return None


# Published Heavy / Opus first-R figures (n, first-R, n mod 840).
KNOWN_HARD_FIRST_R: tuple[tuple[int, int, int], ...] = (
    (496609, 51, 169),
    (8803369, 107, 169),
    (287567281, 83, 1),
    (794037841, 63, 121),
)

# Heavy closed the n≡529 (mod 840) first-R>107 hunt through here.
HEAVY_529_FRONTIER = 570_000_000
