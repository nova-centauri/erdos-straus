from pathlib import Path

from erdos_straus.verifier import (
    DEFAULT_TRIPLES_CSV,
    check_csv,
    load_triples_csv,
    n_mod_840,
    residual,
    verify,
)

REPO = Path(__file__).resolve().parents[1]
CSV = REPO / "data" / "triples.csv"

# Hard first-R figures from the Heavy / Opus chats (n, R, residue).
HARD_FIRST_R = {
    8803369: (107, 169),
    287567281: (83, 1),
    794037841: (63, 121),
    496609: (51, 169),
    586775809: (63, 529),
    3434195209: (83, 529),
}

MORDELL = {1, 121, 169, 289, 361, 529}


def test_default_csv_path():
    assert DEFAULT_TRIPLES_CSV.resolve() == CSV.resolve()
    assert CSV.is_file()


def test_every_csv_row_residual_zero():
    errors = check_csv(CSV)
    assert errors == [], errors


def test_csv_row_count_and_residues():
    rows = load_triples_csv(CSV)
    assert len(rows) == 77
    assert {rec.n for rec in rows}
    assert len({rec.n for rec in rows}) == 71
    for rec in rows:
        assert rec.n % 840 in MORDELL
        assert rec.n_mod_840 == n_mod_840(rec.n)
        assert residual(rec.n, rec.x, rec.y, rec.z) == 0
        assert verify(rec.n, rec.x, rec.y, rec.z)


def test_hard_first_r_notes():
    rows = load_triples_csv(CSV)
    by_n = {rec.n: rec for rec in rows}
    for n, (r, residue) in HARD_FIRST_R.items():
        rec = by_n[n]
        assert rec.n_mod_840 == residue
        assert f"first-R={r}" in rec.notes
        assert residual(n, rec.x, rec.y, rec.z) == 0
