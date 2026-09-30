#!/usr/bin/env python3
"""Discover polynomial identities for Mordell classes by interpolation."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from erdos_straus.solver import solve  # noqa: E402
from erdos_straus.verifier import verify  # noqa: E402


def smallest_triple(n: int) -> tuple[int, int, int] | None:
    sol = solve(n)
    if sol is None:
        return None
    return tuple(sorted((sol.x, sol.y, sol.z)))


def collect(mod: int, residue: int, count: int = 12) -> list[tuple[int, tuple[int, int, int]]]:
    rows = []
    t = 0
    while len(rows) < count:
        n = mod * t + residue
        t += 1
        if n < 2:
            continue
        trip = smallest_triple(n)
        if trip is None:
            print(f"  FAILED n={n}")
            continue
        assert verify(n, *trip)
        rows.append((n, trip))
        print(f"  n={n} = {mod}*({(n-residue)//mod})+{residue} -> {trip}")
    return rows


def main() -> None:
    # Solver is imported; if it is not ready this script is run later.
    for mod, residue in [(5, 2), (5, 3), (7, 3), (7, 5), (7, 6)]:
        print(f"\n=== n ≡ {residue} (mod {mod}) ===")
        try:
            collect(mod, residue, count=8)
        except Exception as exc:
            print("  error:", exc)


if __name__ == "__main__":
    main()
