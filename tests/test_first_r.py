import json
import subprocess
import sys
from pathlib import Path

from erdos_straus.first_r import KNOWN_HARD_FIRST_R, first_r
from erdos_straus.verifier import residual, verify

REPO = Path(__file__).resolve().parents[1]
SCAN = REPO / "data" / "first_r_529.json"
SCAN_8E8 = REPO / "data" / "first_r_529_from_8e8.json"


def test_published_hard_first_r_figures():
    for n, r, residue in KNOWN_HARD_FIRST_R:
        hit = first_r(n, t_max=40, n_is_prime=True)
        assert hit is not None, n
        assert hit.first_r == r
        assert hit.n % 840 == residue
        assert hit.t == (r - 3) // 4
        assert verify(n, hit.x, hit.y, hit.z)
        assert residual(n, hit.x, hit.y, hit.z) == 0


def test_3049_has_small_first_r():
    # Checksum leftover prime n≡529; not a hard first-R example.
    hit = first_r(3049, t_max=20, n_is_prime=True)
    assert hit is not None
    assert hit.first_r >= 3
    assert hit.first_r < 107
    assert verify(3049, hit.x, hit.y, hit.z)


def test_first_r_529_scan_is_measurement():
    data = json.loads(SCAN.read_text())
    assert data["residue_mod_840"] == 529
    assert data["start"] == 570_000_000
    assert data["stop"] == 800_000_000
    assert data["primes_scanned"] == 58958
    assert data["hits_at_or_above_min_R"] == 0
    assert data["unresolved_count"] == 0
    assert data["max_first_R_seen"] == 63
    assert data["max_first_R_n"] == 586775809
    assert data["cover_claimed"] is False
    assert data["esc_proved"] is False
    deep = data["deepest"]
    assert deep["first_R"] == 63
    assert deep["residual"] == 0
    assert verify(deep["n"], deep["x"], deep["y"], deep["z"])


def test_first_r_529_from_8e8_is_measurement():
    data = json.loads(SCAN_8E8.read_text())
    assert data["residue_mod_840"] == 529
    assert data["start"] == 800_000_000
    assert data["stop"] == 8_000_000_000
    assert data["primes_scanned"] == 1_700_954
    assert data["hits_at_or_above_min_R"] == 0
    assert data["unresolved_count"] == 0
    assert data["max_first_R_seen"] == 83
    assert data["max_first_R_n"] == 3434195209
    assert data["cover_claimed"] is False
    assert data["esc_proved"] is False
    deep = data["deepest"]
    assert deep["first_R"] == 83
    assert deep["residual"] == 0
    assert verify(deep["n"], deep["x"], deep["y"], deep["z"])


def test_scan_first_r_cli_tiny(tmp_path):
    csv = tmp_path / "h.csv"
    js = tmp_path / "h.json"
    subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "scan_first_r.py"),
            "--start",
            "5569",
            "--stop",
            "7000",
            "--t-max",
            "20",
            "--csv",
            str(csv),
            "--json",
            str(js),
        ],
        check=True,
        cwd=REPO,
    )
    data = json.loads(js.read_text())
    assert data["residue_mod_840"] == 529
    assert data["primes_scanned"] >= 1
    assert data["cover_claimed"] is False
    assert csv.is_file()
