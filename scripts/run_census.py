#!/usr/bin/env python3
"""Run a construction census and print a JSON summary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from erdos_straus.arith import is_prime
from erdos_straus.census import run_census
from erdos_straus.identities import is_mordell_hard
from erdos_straus.solver import deepen
from erdos_straus.verifier import verify


def hard_primes(limit: int) -> list[int]:
    return [n for n in range(2, limit + 1) if is_mordell_hard(n) and is_prime(n)]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=5000)
    p.add_argument("--hard-limit", type=int, default=20000)
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()

    census = run_census(args.limit)
    hard = hard_primes(args.hard_limit)
    hard_failed = []
    hard_ok = 0
    for n in hard:
        sol = deepen(n)
        if sol is None or not verify(n, sol.x, sol.y, sol.z):
            hard_failed.append(n)
        else:
            hard_ok += 1
    report = {
        "census": census,
        "hard_primes_checked": len(hard),
        "hard_primes_solved": hard_ok,
        "hard_primes_failed": hard_failed,
        "smallest_unsolved_anywhere": census["smallest_unsolved"] or (
            hard_failed[0] if hard_failed else None
        ),
    }
    text = json.dumps(report, indent=2)
    print(text)
    if args.out:
        args.out.write_text(text + "\n")


if __name__ == "__main__":
    main()
