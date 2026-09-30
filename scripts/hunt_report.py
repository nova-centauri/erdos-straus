#!/usr/bin/env python3
"""Enumerate Elsholtz–Tao subclass coverings of the Mordell-hard residues."""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from erdos_straus.hunt import hard_subprogressions, sample_verify_covering


def main() -> None:
    covers = hard_subprogressions(ab_bound=40)
    by_hard: dict[int, list] = defaultdict(list)
    for c in covers:
        if c.hard_r is None or c.combined_mod is None:
            continue
        by_hard[c.hard_r].append(c)

    print(f"subclass coverings with ab ≤ 40: {sum(len(v) for v in by_hard.values())}")
    for hard in sorted(by_hard):
        rows = by_hard[hard]
        # Prefer smaller combined modulus
        rows.sort(key=lambda c: (c.combined_mod or 10**9, c.a, c.b, c.e))
        best = rows[0]
        failed = sample_verify_covering(best, samples=3)
        status = "OK" if not failed else f"FAIL {failed}"
        print(
            f"  n≡{hard:3d} (mod 840): {len(rows):4d} coverings; "
            f"thinnest {best.kind} a={best.a} b={best.b} e={best.e} "
            f"→ n≡{best.combined_res} (mod {best.combined_mod}) {status}"
        )


if __name__ == "__main__":
    main()
