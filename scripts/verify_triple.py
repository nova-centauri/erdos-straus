#!/usr/bin/env python3
"""Check 4/n = 1/x + 1/y + 1/z with fractions.Fraction and print n%840.

Usage:
    PYTHONPATH=. python3 scripts/verify_triple.py N X Y Z
    PYTHONPATH=. python3 scripts/verify_triple.py --csv data/triples.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from erdos_straus.verifier import (  # noqa: E402
    DEFAULT_TRIPLES_CSV,
    check_csv,
    n_mod_840,
    residual,
    verify,
)


def _print_one(n: int, x: int, y: int, z: int) -> int:
    r = residual(n, x, y, z)
    ok = verify(n, x, y, z)
    print(f"n = {n}")
    print(f"x,y,z = {x}, {y}, {z}")
    print(f"n%840 = {n_mod_840(n)}")
    print(f"residual 4xyz-n(xy+xz+yz) = {r}")
    print("ok" if ok else "FAIL")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("n", nargs="?", type=int)
    p.add_argument("x", nargs="?", type=int)
    p.add_argument("y", nargs="?", type=int)
    p.add_argument("z", nargs="?", type=int)
    p.add_argument("--csv", nargs="?", const=str(DEFAULT_TRIPLES_CSV))
    args = p.parse_args(argv)

    if args.csv:
        errors = check_csv(args.csv)
        if errors:
            print(f"FAIL {len(errors)} row(s) in {args.csv}", file=sys.stderr)
            for err in errors:
                print(err, file=sys.stderr)
            return 1
        print(f"ok every row residual 0 in {args.csv}")
        return 0

    if None in (args.n, args.x, args.y, args.z):
        p.error("pass N X Y Z, or --csv [path]")
    return _print_one(args.n, args.x, args.y, args.z)


if __name__ == "__main__":
    raise SystemExit(main())
