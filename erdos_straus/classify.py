"""Residue-class bookkeeping: settled vs still open.

Settled by a *polynomial* identity (Mordell / Salez / this repo):
    n even
    n ≡ 3 (mod 4)
    n ≡ 2 (mod 3)
    n ≡ 5 (mod 8)
    n ≡ 2 or 3 (mod 5)     [Mordell; constructions in the solver]
    n ≡ 3, 5, or 6 (mod 7) [Mordell; constructions in the solver]

After combining the above via the Chinese remainder theorem, the only
surviving classes modulo 840 are the six squares

    1, 121, 169, 289, 361, 529.

Every n ≢ 1 (mod 24) is already settled by the greedy algorithm plus the
mod-3 identity (Ionascu–Wilson; Wikipedia). So the computationally and
theoretically hard family is

    n ≡ 1 (mod 24),
    and among those, the Mordell-hard subclass n ≡ r (mod 840) for
    r in the six squares above.

A composite n is never a minimal counterexample: if 4/p has a triple then
so does 4/(m p). The remaining work is therefore about primes in the
Mordell-hard classes (the smallest such prime is 1009).
"""

from __future__ import annotations

from erdos_straus.arith import is_prime
from erdos_straus.identities import MORDELL_UNCOVERED, is_hard_mod24, is_mordell_hard


def classification(n: int) -> dict:
    """Describe which buckets ``n`` falls into."""
    return {
        "n": n,
        "prime": is_prime(n),
        "even": n % 2 == 0,
        "mod24": n % 24,
        "mod840": n % 840,
        "hard_mod24": is_hard_mod24(n),
        "mordell_hard": is_mordell_hard(n),
        "minimal_candidate": is_prime(n) and is_mordell_hard(n),
    }


def mordell_uncovered_residues() -> frozenset[int]:
    return MORDELL_UNCOVERED


def crt_filter(moduli_residues: list[tuple[int, set[int]]]) -> tuple[int, list[int]]:
    """Residues modulo the product that avoid every given 'covered' set.

    Each pair is (m, covered_residues_mod_m). We return (M, leftover)
    where M is the product of the m's (must be pairwise coprime) and
    leftover is the list of r in 0..M-1 that lie in none of the covered
    sets when reduced mod each m.
    """
    M = 1
    for m, _ in moduli_residues:
        M *= m
    leftover = []
    for r in range(M):
        covered = False
        for m, good in moduli_residues:
            if (r % m) in good:
                covered = True
                break
        if not covered:
            leftover.append(r)
    return M, leftover
