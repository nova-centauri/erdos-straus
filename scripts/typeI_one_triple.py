#!/usr/bin/env python3
"""Emit one residual-0 Type I triple for n (a ≤ b, y ≤ 2n/3, x = n*a*b*d)."""

from __future__ import annotations

import argparse
import sys
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from erdos_straus.verifier import n_mod_840, residual, verify
from scripts.typeI_count_ref import _divisors


def one_triple(n: int) -> tuple[int, int, int] | None:
    lo = n // 4 + 1
    hi = (2 * n) // 3
    for y in range(lo, hi + 1):
        f = 4 * y - n
        if f <= 0:
            continue
        for a in _divisors(y):
            y1 = y // a
            for c in _divisors(y1):
                d = y1 // c
                F = 4 * a * a * d + 1
                if F % f:
                    continue
                e = F // f
                if e < 1 or (n * a + c) % f:
                    continue
                b = (n * a + c) // f
                if b < 1 or a > b:
                    continue
                if a + b != c * e:
                    continue
                if gcd(gcd(a, b), c) != 1:
                    continue
                x = a * b * d * n
                z = b * c * d
                if verify(n, x, y, z):
                    return x, y, z
    return None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("n", type=int)
    args = p.parse_args(argv)
    t = one_triple(args.n)
    if t is None:
        print(f"no Type I triple for n={args.n}", file=sys.stderr)
        return 1
    x, y, z = t
    print(f"{args.n},{x},{y},{z},{n_mod_840(args.n)},Type I a<=b y<=2n/3 residual={residual(args.n, x, y, z)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
