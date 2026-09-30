"""Command-line interface for the Erdős–Straus toolkit."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from erdos_straus.classify import classification
from erdos_straus.solver import deepen, solve
from erdos_straus.verifier import (
    DEFAULT_TRIPLES_CSV,
    check_csv,
    load_triples_csv,
    n_mod_840,
    residual,
    verify,
)


def _cmd_solve(args: argparse.Namespace) -> int:
    n = args.n
    sol = deepen(n) if args.deep else solve(n)
    if sol is None:
        print(f"no construction found for n={n}", file=sys.stderr)
        return 1
    print(f"n = {n}")
    print(f"4/{n} = 1/{sol.x} + 1/{sol.y} + 1/{sol.z}")
    print(f"method: {sol.method}")
    print(f"n%840 = {n_mod_840(n)}")
    print(f"residual = {residual(n, sol.x, sol.y, sol.z)}")
    print(f"verified: {verify(n, sol.x, sol.y, sol.z)}")
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    n, x, y, z = args.n, args.x, args.y, args.z
    r = residual(n, x, y, z)
    ok = verify(n, x, y, z)
    print("ok" if ok else "FAIL")
    print(f"n%840 = {n_mod_840(n)}")
    print(f"residual 4xyz-n(xy+xz+yz) = {r}")
    return 0 if ok else 1


def _cmd_check_csv(args: argparse.Namespace) -> int:
    path = Path(args.path) if args.path else DEFAULT_TRIPLES_CSV
    errors = check_csv(path)
    if errors:
        print(f"FAIL {len(errors)} problem(s) in {path}", file=sys.stderr)
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    rows = load_triples_csv(path)
    print(f"ok {len(rows)} row(s) residual 0 in {path}")
    return 0


def _cmd_classify(args: argparse.Namespace) -> int:
    print(json.dumps(classification(args.n), indent=2))
    return 0


def _cmd_census(args: argparse.Namespace) -> int:
    from erdos_straus.census import run_census

    result = run_census(args.limit, deep=args.deep)
    print(json.dumps(result, indent=2))
    return 0 if result["unsolved"] == [] else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="erdos-straus")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("solve", help="construct a triple for a given n")
    s.add_argument("n", type=int)
    s.add_argument("--deep", action="store_true", help="use a larger search budget")
    s.set_defaults(func=_cmd_solve)

    v = sub.add_parser("verify", help="check 4/n = 1/x + 1/y + 1/z exactly")
    v.add_argument("n", type=int)
    v.add_argument("x", type=int)
    v.add_argument("y", type=int)
    v.add_argument("z", type=int)
    v.set_defaults(func=_cmd_verify)

    k = sub.add_parser("check-csv", help="verify every row of data/triples.csv")
    k.add_argument(
        "path",
        nargs="?",
        default=str(DEFAULT_TRIPLES_CSV),
        help="CSV with columns n,x,y,z[,n_mod_840,notes]",
    )
    k.set_defaults(func=_cmd_check_csv)

    c = sub.add_parser("classify", help="residue-class status of n")
    c.add_argument("n", type=int)
    c.set_defaults(func=_cmd_classify)

    u = sub.add_parser("census", help="solve every n in 2..limit")
    u.add_argument("--limit", type=int, default=2000)
    u.add_argument("--deep", action="store_true")
    u.set_defaults(func=_cmd_census)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

