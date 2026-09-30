"""Exact rational verification of Erdős–Straus triples.

All checks use ``fractions.Fraction`` (or the integer cross-multiplication
form 4xyz − n(xy + xz + yz) = 0). Floating-point arithmetic is never used.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import Iterable

DEFAULT_TRIPLES_CSV = Path(__file__).resolve().parents[1] / "data" / "triples.csv"


def residual(n: int, x: int, y: int, z: int) -> int:
    """Integer residual ``4xyz − n(xy + xz + yz)``. Zero iff the identity holds."""
    return 4 * x * y * z - n * (x * y + x * z + y * z)


def n_mod_840(n: int) -> int:
    return n % 840


def verify(n: int, x: int, y: int, z: int) -> bool:
    """Return True iff n ≥ 2 and 4/n = 1/x + 1/y + 1/z in positive integers."""
    if not isinstance(n, int) or not isinstance(x, int):
        return False
    if not isinstance(y, int) or not isinstance(z, int):
        return False
    if n < 2 or x < 1 or y < 1 or z < 1:
        return False
    if residual(n, x, y, z) != 0:
        return False
    return Fraction(4, n) == Fraction(1, x) + Fraction(1, y) + Fraction(1, z)


def verify_triple(n: int, triple: Iterable[int]) -> bool:
    vals = tuple(triple)
    if len(vals) != 3:
        return False
    return verify(n, vals[0], vals[1], vals[2])


def equation_holds(n: int, x: int, y: int, z: int) -> bool:
    """Integer form: 4xyz = n(xy + xz + yz), with the same positivity checks."""
    if n < 2 or x < 1 or y < 1 or z < 1:
        return False
    return residual(n, x, y, z) == 0


def require(n: int, x: int, y: int, z: int) -> None:
    if not verify(n, x, y, z):
        raise ValueError(f"invalid triple for n={n}: ({x}, {y}, {z})")


@dataclass(frozen=True)
class TripleRecord:
    n: int
    x: int
    y: int
    z: int
    n_mod_840: int
    notes: str
    line: int


def load_triples_csv(path: str | Path | None = None) -> list[TripleRecord]:
    """Load ``data/triples.csv`` (or another CSV with the same columns)."""
    csv_path = Path(path) if path is not None else DEFAULT_TRIPLES_CSV
    rows: list[TripleRecord] = []
    with csv_path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        required = {"n", "x", "y", "z"}
        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError(f"{csv_path}: missing columns {sorted(required)}")
        for i, raw in enumerate(reader, start=2):
            if not raw or all((v or "").strip() == "" for v in raw.values()):
                continue
            n = int(raw["n"])
            x = int(raw["x"])
            y = int(raw["y"])
            z = int(raw["z"])
            listed = raw.get("n_mod_840", "").strip()
            mod = int(listed) if listed else n_mod_840(n)
            notes = (raw.get("notes") or "").strip()
            rows.append(TripleRecord(n, x, y, z, mod, notes, i))
    return rows


def check_csv(path: str | Path | None = None) -> list[str]:
    """Return a list of error strings. Empty list means every row residual is 0."""
    csv_path = Path(path) if path is not None else DEFAULT_TRIPLES_CSV
    errors: list[str] = []
    rows = load_triples_csv(csv_path)
    if not rows:
        errors.append(f"{csv_path}: no data rows")
        return errors
    for rec in rows:
        loc = f"{csv_path}:{rec.line} n={rec.n}"
        if rec.n_mod_840 != n_mod_840(rec.n):
            errors.append(
                f"{loc}: n_mod_840 column {rec.n_mod_840} != {n_mod_840(rec.n)}"
            )
        r = residual(rec.n, rec.x, rec.y, rec.z)
        if r != 0 or not verify(rec.n, rec.x, rec.y, rec.z):
            errors.append(f"{loc}: residual {r} (expected 0)")
    return errors
