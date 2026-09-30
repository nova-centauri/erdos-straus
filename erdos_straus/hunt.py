"""Search for parametric coverings of the Mordell-hard classes.

A polynomial identity for the *full* class n ≡ 1 (mod 840) is impossible
(Mordell: 1 is a quadratic residue). What *is* possible is a covering of
thinner arithmetic progressions inside that class:

    n ≡ −e (mod 4ab)          Type II
    n ≡ −e^{−1} (mod 4ab)     Type I

whenever e | a+b. Intersecting with n ≡ r (mod 840) for a hard residue r
gives an infinite solved subclass, provided the CRT is solvable.

This module enumerates small (a, b, e) and records every such subclass.
It also looks for (a, b, e) that cover a residue class Salez's prime
filters S_m do not list, which would be a new *polynomial* covering of
that class (allowed only when the residue is a non-square).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from erdos_straus.arith import divisors, lcm, quadratic_residues
from erdos_straus.identities import MORDELL_UNCOVERED
from erdos_straus.parametric import type_I, type_II
from erdos_straus.verifier import verify


@dataclass(frozen=True)
class Covering:
    kind: str  # "I" or "II"
    a: int
    b: int
    e: int
    modulus: int  # 4ab
    residue: int  # n mod 4ab
    hard_r: int | None
    combined_mod: int | None
    combined_res: int | None


def _inv_mod(a: int, m: int) -> int | None:
    if gcd(a, m) != 1:
        return None
    return pow(a, -1, m)


def type_II_residue(a: int, b: int, e: int) -> tuple[int, int]:
    m = 4 * a * b
    return m, (-e) % m


def type_I_residue(a: int, b: int, e: int) -> tuple[int, int] | None:
    """n e ≡ −1 (mod 4ab), i.e. n ≡ −e^{−1} (mod 4ab)."""
    m = 4 * a * b
    inv = _inv_mod(e, m)
    if inv is None:
        return None
    return m, (-inv) % m


def crt2(a1: int, m1: int, a2: int, m2: int) -> tuple[int, int] | None:
    """Solve n ≡ a1 (mod m1), n ≡ a2 (mod m2). Returns (res, lcm) or None."""
    g = gcd(m1, m2)
    if (a1 - a2) % g != 0:
        return None
    # Standard CRT for non-coprime moduli.
    m1g, m2g = m1 // g, m2 // g
    inv = _inv_mod(m1g, m2g)
    if inv is None:
        # Should not happen after dividing out g, but be safe.
        return None
    k = ((a2 - a1) // g * inv) % m2g
    n0 = a1 + k * m1
    M = lcm(m1, m2)
    return n0 % M, M


def enumerate_coverings(ab_bound: int = 60) -> list[Covering]:
    found: list[Covering] = []
    seen: set[tuple] = set()
    for a in range(1, ab_bound + 1):
        for b in range(a, ab_bound // a + 1):
            for e in divisors(a + b):
                m2, r2 = type_II_residue(a, b, e)
                key2 = ("II", m2, r2)
                if key2 not in seen:
                    seen.add(key2)
                    found.extend(_with_hard(a, b, e, "II", m2, r2))
                t1 = type_I_residue(a, b, e)
                if t1 is not None:
                    m1, r1 = t1
                    key1 = ("I", m1, r1)
                    if key1 not in seen:
                        seen.add(key1)
                        found.extend(_with_hard(a, b, e, "I", m1, r1))
    return found


def _with_hard(a: int, b: int, e: int, kind: str, mod: int, res: int) -> list[Covering]:
    out: list[Covering] = []
    hit_hard = False
    for hard in sorted(MORDELL_UNCOVERED):
        crt = crt2(res, mod, hard, 840)
        if crt is None:
            continue
        cres, cmod = crt
        hit_hard = True
        out.append(
            Covering(kind, a, b, e, mod, res, hard, cmod, cres)
        )
    if not hit_hard:
        out.append(Covering(kind, a, b, e, mod, res, None, None, None))
    return out


def hard_subprogressions(ab_bound: int = 60) -> list[Covering]:
    return [c for c in enumerate_coverings(ab_bound) if c.hard_r is not None]


def salez_sm_nonresidues(m: int) -> set[int]:
    """Quadratic non-residues mod m (odd prime), including 0 as 'composite'."""
    qrs = quadratic_residues(m)
    return {r for r in range(m) if r not in qrs or r == 0}


def missing_allowed_residues(m: int, covered: set[int]) -> set[int]:
    """Non-residues that a polynomial identity *could* cover but ``covered`` does not."""
    allowed = salez_sm_nonresidues(m)
    return allowed - covered


def sample_verify_covering(c: Covering, samples: int = 5) -> list[int]:
    """Build n = combined_res + k * combined_mod and verify a Type I/II triple."""
    if c.combined_mod is None or c.combined_res is None:
        return []
    failed: list[int] = []
    k = 0
    seen = 0
    while seen < samples:
        n = c.combined_res + k * c.combined_mod
        k += 1
        if n < 2:
            continue
        seen += 1
        trip = type_II(n, c.a, c.b, c.e) if c.kind == "II" else type_I(n, c.a, c.b, c.e)
        if trip is None or not verify(n, trip.x, trip.y, trip.z):
            failed.append(n)
    return failed
