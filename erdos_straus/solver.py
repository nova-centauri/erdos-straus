"""Multi-strategy solver for 4/n = 1/x + 1/y + 1/z.

Strategies, in order:
    1. Classical residue identities (even, 3 mod 4, 2 mod 3, 5 mod 8, …).
    2. Multiplicative reduction: if n = m p and 4/p has a triple, scale it.
    3. Ionascu–Wilson closed cases for n = 4k+1, k ≢ 0 (mod 3).
    4. Shifted-greedy remainder split (t = 0, 1, …).
    5. Elsholtz–Tao Type I / Type II parameter search.
    6. Bounded first-denominator scan with an exact two-term split.

Every returned triple is re-checked by the exact verifier before release.
The solver does not claim that failure implies a counterexample: it only
reports that the configured search budget did not find a construction.
"""

from __future__ import annotations

from erdos_straus.arith import factorize, is_prime
from erdos_straus.identities import apply_classical, apply_extended
from erdos_straus.parametric import (
    et_catalog_hit,
    search_type_I_via_e,
    search_type_II_via_e,
)
from erdos_straus.shifted import ionascu_k_mod3, shifted_greedy
from erdos_straus.two_term import two_unit_fractions
from erdos_straus.types import Solution, Triple
from erdos_straus.verifier import verify


def _ok(n: int, triple: Triple, method: str) -> Solution | None:
    if verify(n, triple.x, triple.y, triple.z):
        return Solution(n, triple.x, triple.y, triple.z, method)
    return None


def _smallest_prime_factor(n: int) -> int:
    facts = factorize(n)
    return min(facts)


def solve(
    n: int,
    *,
    t_max: int = 80,
    e_max: int = 120,
    catalog_bound: int = 40,
    x_extra: int = 80,
    reduce_composites: bool = True,
) -> Solution | None:
    """Find a positive integer triple for 4/n, or return None."""
    if n < 2:
        return None

    hit = apply_classical(n)
    if hit is not None:
        name, triple = hit
        sol = _ok(n, triple, f"identity:{name}")
        if sol is not None:
            return sol

    hit = apply_extended(n)
    if hit is not None:
        name, triple = hit
        sol = _ok(n, triple, f"identity:{name}")
        if sol is not None:
            return sol

    if reduce_composites and not is_prime(n):
        p = _smallest_prime_factor(n)
        if p < n:
            inner = solve(
                p,
                t_max=t_max,
                e_max=e_max,
                catalog_bound=catalog_bound,
                x_extra=x_extra,
                reduce_composites=True,
            )
            if inner is not None:
                m = n // p
                scaled = Triple(inner.x * m, inner.y * m, inner.z * m)
                sol = _ok(n, scaled, f"scale:{inner.method}:p={p}")
                if sol is not None:
                    return sol

    trip = ionascu_k_mod3(n)
    if trip is not None:
        sol = _ok(n, trip, "ionascu-k-mod3")
        if sol is not None:
            return sol

    trip = shifted_greedy(n, t_max=t_max)
    if trip is not None:
        sol = _ok(n, trip, f"shifted-greedy:t_max={t_max}")
        if sol is not None:
            return sol

    trip = et_catalog_hit(n, ab_bound=catalog_bound)
    if trip is not None:
        sol = _ok(n, trip, f"elsholtz-tao-catalog:ab≤{catalog_bound}")
        if sol is not None:
            return sol

    trip = search_type_II_via_e(n, e_max=e_max)
    if trip is not None:
        sol = _ok(n, trip, f"type-II-e:e≤{e_max}")
        if sol is not None:
            return sol

    trip = search_type_I_via_e(n, e_max=e_max)
    if trip is not None:
        sol = _ok(n, trip, f"type-I-e:e≤{e_max}")
        if sol is not None:
            return sol

    trip = _first_denom_scan(n, extra=x_extra)
    if trip is not None:
        sol = _ok(n, trip, f"first-denom:extra={x_extra}")
        if sol is not None:
            return sol

    return None


def _first_denom_scan(n: int, extra: int) -> Triple | None:
    x_min = (n + 3) // 4  # ceil(n/4)
    x_max = min(3 * n // 4, x_min + extra)
    for x in range(x_min, x_max + 1):
        numer = 4 * x - n
        if numer <= 0:
            continue
        pair = two_unit_fractions(numer, n * x)
        if pair is not None:
            return Triple(x, pair[0], pair[1])
    return None


def solve_or_raise(n: int, **kwargs) -> Solution:
    sol = solve(n, **kwargs)
    if sol is None:
        raise ValueError(f"no construction found for n={n} with the current budget")
    return sol


def deepen(n: int) -> Solution | None:
    """Larger budget, used for stubborn primes in the census."""
    sol = solve(n, t_max=400, e_max=800, catalog_bound=120, x_extra=400)
    if sol is not None:
        return sol
    return solve(n, t_max=2000, e_max=4000, catalog_bound=200, x_extra=2000)
