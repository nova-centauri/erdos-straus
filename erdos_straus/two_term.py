"""Write a positive rational as a sum of two unit fractions.

Theorem (standard; see Ionascu–Wilson 2011, Thm. 1.1). If gcd(p, q) = 1,
then p/q = 1/y + 1/z for positive integers y, z if and only if there exist
positive integers u, w such that

    u w divides q    and    u + w ≡ 0 (mod p).

Then t = (u + w)/p, y = q t / u, z = q t / w.

We always reduce p/q first, so the characterisation is complete.
"""

from __future__ import annotations

from math import gcd

from erdos_straus.arith import divisors


def two_unit_fractions(p: int, q: int) -> tuple[int, int] | None:
    """Return (y, z) with y ≤ z and 1/y + 1/z = p/q, or None."""
    if p <= 0 or q <= 0:
        return None
    g = gcd(p, q)
    p //= g
    q //= g
    if p == 1:
        # Already a unit fraction. Split so callers always receive two terms:
        # 1/q = 1/(q + 1) + 1/(q(q + 1)).
        return (q + 1, q * (q + 1))

    # Prefer u = 1: w | q and w ≡ −1 (mod p).
    hit = _scan_complements(1, q, p, q)
    if hit is not None:
        return hit

    for u in divisors(q):
        if u == 1:
            continue
        hit = _scan_complements(u, q // u, p, q)
        if hit is not None:
            return hit
    return None


def _scan_complements(u: int, w_limit_divisor: int, p: int, q: int) -> tuple[int, int] | None:
    """Search w | w_limit_divisor with u + w ≡ 0 (mod p)."""
    residue = (-u) % p
    if residue == 0:
        residue = p
    w = residue
    while w <= w_limit_divisor:
        if w_limit_divisor % w == 0:
            t = (u + w) // p
            y = q * t // u
            z = q * t // w
            return (y, z) if y <= z else (z, y)
        w += p
    return None
