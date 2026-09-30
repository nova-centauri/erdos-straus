#!/usr/bin/env python3
"""Merge first-R slice JSON files into one measurement log. Not a cover."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_slice(path: Path) -> dict:
    data = json.loads(path.read_text())
    if data.get("cover_claimed"):
        raise SystemExit(f"slice claims a cover: {path}")
    return data


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("slices", nargs="+", type=Path)
    p.add_argument("--json", type=Path, default=ROOT / "data" / "first_r_529_from_8e8.json")
    p.add_argument("--csv", type=Path, default=ROOT / "data" / "first_r_529_from_8e8.csv")
    p.add_argument("--deepest-csv", type=Path, default=ROOT / "data" / "first_r_529_from_8e8_deepest.csv")
    args = p.parse_args(argv)

    slices = [load_slice(path) for path in args.slices]
    slices.sort(key=lambda d: (d["start"], d["stop"]))

    hits: list[dict] = []
    unresolved: list[int] = []
    primes = 0
    max_r = 0
    max_n = 0
    deepest = None
    residue = slices[0]["residue_mod_840"]
    t_max = slices[0]["t_max"]
    min_r = slices[0]["min_R_reported"]
    for d in slices:
        if d["residue_mod_840"] != residue:
            raise SystemExit("mixed residues")
        primes += d["primes_scanned"]
        unresolved.extend(d.get("unresolved_above_t_max") or [])
        hits.extend(d.get("hits") or [])
        if d["max_first_R_seen"] > max_r:
            max_r = d["max_first_R_seen"]
            max_n = d["max_first_R_n"]
            deepest = d.get("deepest")

    # Require abutting ranges so the merged interval has no holes.
    for a, b in zip(slices, slices[1:]):
        if a["stop"] != b["start"]:
            raise SystemExit(f"gap or overlap: {a['stop']} vs {b['start']}")

    fieldnames = ["n", "n_mod_840", "first_R", "t", "x", "y", "z", "residual"]
    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(hits)
    if deepest:
        with args.deepest_csv.open("w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fieldnames)
            w.writeheader()
            w.writerow(deepest)

    summary = {
        "residue_mod_840": residue,
        "start": slices[0]["start"],
        "stop": slices[-1]["stop"],
        "last_prime_scanned": slices[-1]["last_prime_scanned"],
        "primes_scanned": primes,
        "t_max": t_max,
        "min_R_reported": min_r,
        "hits_at_or_above_min_R": len(hits),
        "unresolved_above_t_max": unresolved,
        "unresolved_count": len(unresolved),
        "max_first_R_seen": max_r,
        "max_first_R_n": max_n,
        "deepest": deepest,
        "slices": [
            {
                "start": d["start"],
                "stop": d["stop"],
                "primes_scanned": d["primes_scanned"],
                "max_first_R_seen": d["max_first_R_seen"],
                "max_first_R_n": d["max_first_R_n"],
                "hits_at_or_above_min_R": d["hits_at_or_above_min_R"],
            }
            for d in slices
        ],
        "cover_claimed": False,
        "esc_proved": False,
        "note": "measurement; bounded shifted-greedy is not a class cover",
        "hits": hits,
        "csv": str(args.csv.relative_to(ROOT)) if args.csv.is_relative_to(ROOT) else str(args.csv),
    }
    args.json.write_text(json.dumps(summary, indent=2) + "\n")
    print(
        f"merged {len(slices)} slices [{summary['start']}, {summary['stop']}); "
        f"{primes} primes; max first-R={max_r} at n={max_n}; "
        f"hits≥{min_r}: {len(hits)}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
