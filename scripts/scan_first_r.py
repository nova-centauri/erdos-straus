#!/usr/bin/env python3
"""Scan leftover primes for large shifted-greedy first-R.

Default: n ≡ 529 (mod 840) after Heavy's closed frontier 5.70e8,
looking for first-R > 107. Writes CSV + JSON under data/. This is a
search log, not a class cover. Resume by raising --start to the last
scanned n.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from erdos_straus.arith import primes_in_class
from erdos_straus.first_r import HEAVY_529_FRONTIER, FirstR, first_r
from erdos_straus.verifier import residual


def row_of(hit: FirstR) -> dict[str, int]:
    return {
        "n": hit.n,
        "n_mod_840": hit.n_mod_840,
        "first_R": hit.first_r,
        "t": hit.t,
        "x": hit.x,
        "y": hit.y,
        "z": hit.z,
        "residual": residual(hit.n, hit.x, hit.y, hit.z),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start", type=int, default=HEAVY_529_FRONTIER)
    p.add_argument("--stop", type=int, default=HEAVY_529_FRONTIER + 2_000_000)
    p.add_argument("--residue", type=int, default=529)
    p.add_argument("--modulus", type=int, default=840)
    p.add_argument("--min-R", type=int, default=108, dest="min_r")
    p.add_argument("--t-max", type=int, default=40)
    p.add_argument("--csv", type=Path, default=ROOT / "data" / "first_r_529.csv")
    p.add_argument("--json", type=Path, default=ROOT / "data" / "first_r_529.json")
    args = p.parse_args(argv)

    if args.stop <= args.start:
        print("empty range", file=sys.stderr)
        return 2

    primes = primes_in_class(args.start, args.stop, args.residue, args.modulus)
    hits: list[dict[str, int]] = []
    unresolved: list[int] = []
    deepest: dict[str, int] | None = None
    max_r = 0
    max_n = 0
    last_n = args.start
    for i, n in enumerate(primes, 1):
        last_n = n
        hit = first_r(n, t_max=args.t_max, n_is_prime=True)
        if hit is None:
            unresolved.append(n)
            continue
        rec = row_of(hit)
        if hit.first_r > max_r:
            max_r = hit.first_r
            max_n = n
            deepest = rec
        if hit.first_r >= args.min_r:
            hits.append(rec)
        if i % 200 == 0:
            print(f"progress {i}/{len(primes)} last={n} max_R={max_r}", flush=True)

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["n", "n_mod_840", "first_R", "t", "x", "y", "z", "residual"]
    with args.csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(hits)

    summary = {
        "residue_mod_840": args.residue,
        "start": args.start,
        "stop": args.stop,
        "last_prime_scanned": last_n,
        "primes_scanned": len(primes),
        "t_max": args.t_max,
        "min_R_reported": args.min_r,
        "hits_at_or_above_min_R": len(hits),
        "unresolved_above_t_max": unresolved,
        "unresolved_count": len(unresolved),
        "max_first_R_seen": max_r,
        "max_first_R_n": max_n,
        "deepest": deepest,
        "cover_claimed": False,
        "esc_proved": False,
        "note": "measurement; bounded shifted-greedy is not a class cover",
        "hits": hits,
        "csv": str(args.csv.relative_to(ROOT)) if args.csv.is_relative_to(ROOT) else str(args.csv),
    }
    args.json.write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"scanned {len(primes)} primes n≡{args.residue} (mod {args.modulus}) "
        f"in [{args.start}, {args.stop}); max first-R={max_r} at n={max_n}; "
        f"hits≥{args.min_r}: {len(hits)}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
