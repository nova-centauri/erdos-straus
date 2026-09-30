import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HARVEST = REPO / "data" / "typeI_mordell_1e7.json"
HARVEST_1E6 = REPO / "data" / "typeI_mordell_1e6.json"
HARVEST_1E7_RE = REPO / "data" / "typeI_mordell_1e7_recomputed.json"
HARVEST_2E7 = REPO / "data" / "typeI_mordell_2e7.json"
HARVEST_5E7 = REPO / "data" / "typeI_mordell_5e7.json"
HARVEST_1E8 = REPO / "data" / "typeI_mordell_1e8.json"
HARVEST_2E8 = REPO / "data" / "typeI_mordell_2e8.json"


def test_typeI_1e7_totals_and_zero_miss_table():
    data = json.loads(HARVEST.read_text())
    assert data["N"] == 10_000_000
    assert data["sums"]["f_I_n"] == 2_559_629_008
    assert data["sums"]["f_I_p"] == 454_495_120
    assert data["new_triples"] == 0
    assert data["esc_proved"] is False
    assert data["mordell_primes"]["zero_misses_is_not_a_cover"] is True

    classes = data["mordell_primes"]["classes"]
    assert len(classes) == 6
    assert sum(c["primes"] for c in classes) == 20513
    assert sum(c["hits"] for c in classes) == 20513
    assert sum(c["misses"] for c in classes) == 0
    assert data["mordell_primes"]["totals"] == {
        "primes": 20513,
        "hits": 20513,
        "misses": 0,
    }
    for c in classes:
        assert c["hits"] == c["primes"]
        assert c["misses"] == 0
        assert c["min_f_I"] > 0

    corr = data["corrections"][0]
    assert corr["n"] == 3049
    assert corr["n_mod_840"] == 529
    assert corr["true_f_I"] == 30


def test_reconstructed_fi2_matches_1e6_harvest():
    data = json.loads(HARVEST_1E6.read_text())
    assert data["N"] == 1_000_000
    assert data["sums"]["f_I_n"] == 165_374_532
    assert data["sums"]["f_I_p"] == 34_276_274
    assert data["cover_claimed"] is False
    assert data["mordell_primes"]["totals"]["misses"] == 0
    assert data["mordell_primes"]["totals"]["primes"] == 2370


def test_recomputed_1e7_matches_opus_table():
    opus = json.loads(HARVEST.read_text())
    rec = json.loads(HARVEST_1E7_RE.read_text())
    assert rec["N"] == 10_000_000
    assert rec["sums"]["f_I_n"] == opus["sums"]["f_I_n"]
    assert rec["sums"]["f_I_p"] == opus["sums"]["f_I_p"]
    assert rec["mordell_primes"]["totals"] == opus["mordell_primes"]["totals"]
    assert rec["cover_claimed"] is False
    for a, b in zip(rec["mordell_primes"]["classes"], opus["mordell_primes"]["classes"]):
        assert a["residue_mod_840"] == b["residue_mod_840"]
        assert a["primes"] == b["primes"]
        assert a["hits"] == b["hits"]
        assert a["misses"] == b["misses"]
        assert a["min_f_I"] == b["min_f_I"]
        assert a["max_f_I"] == b["max_f_I"]


def test_typeI_2e7_harvest_is_measurement():
    data = json.loads(HARVEST_2E7.read_text())
    assert data["N"] == 20_000_000
    assert data["sums"]["f_I_n"] == 5_772_274_472
    assert data["sums"]["f_I_p"] == 982_580_024
    assert data["cover_claimed"] is False
    assert data["esc_proved"] is False
    assert data["mordell_primes"]["zero_misses_is_not_a_cover"] is True
    assert data["mordell_primes"]["totals"] == {
        "primes": 39391,
        "hits": 39391,
        "misses": 0,
    }
    mins = {c["residue_mod_840"]: c["min_f_I"] for c in data["mordell_primes"]["classes"]}
    assert mins == {1: 12, 121: 24, 169: 22, 289: 28, 361: 14, 529: 30}


def test_typeI_5e7_harvest_is_measurement():
    data = json.loads(HARVEST_5E7.read_text())
    assert data["N"] == 50_000_000
    assert data["sums"]["f_I_n"] == 16_795_310_188
    assert data["sums"]["f_I_p"] == 2_709_141_549
    assert data["sums"]["primes"] == 3_001_134
    assert data["cover_claimed"] is False
    assert data["esc_proved"] is False
    assert data["mordell_primes"]["zero_misses_is_not_a_cover"] is True
    assert data["mordell_primes"]["totals"] == {
        "primes": 93457,
        "hits": 93457,
        "misses": 0,
    }
    mins = {c["residue_mod_840"]: c["min_f_I"] for c in data["mordell_primes"]["classes"]}
    assert mins == {1: 12, 121: 24, 169: 22, 289: 28, 361: 14, 529: 30}


def test_typeI_1e8_harvest_is_measurement():
    data = json.loads(HARVEST_1E8.read_text())
    assert data["N"] == 100_000_000
    assert data["sums"]["f_I_n"] == 37_494_215_304
    assert data["sums"]["f_I_p"] == 5_818_322_818
    assert data["sums"]["primes"] == 5_761_455
    assert data["cover_claimed"] is False
    assert data["esc_proved"] is False
    assert data["mordell_primes"]["zero_misses_is_not_a_cover"] is True
    assert data["mordell_primes"]["totals"] == {
        "primes": 179468,
        "hits": 179468,
        "misses": 0,
    }
    mins = {c["residue_mod_840"]: c["min_f_I"] for c in data["mordell_primes"]["classes"]}
    assert mins == {1: 12, 121: 24, 169: 22, 289: 28, 361: 14, 529: 30}


def test_typeI_2e8_harvest_is_measurement():
    data = json.loads(HARVEST_2E8.read_text())
    assert data["N"] == 200_000_000
    assert data["sums"]["f_I_n"] == 83381351012
    assert data["sums"]["f_I_p"] == 12463112814
    assert data["sums"]["primes"] == 11_078_937
    assert data["cover_claimed"] is False
    assert data["esc_proved"] is False
    assert data["mordell_primes"]["zero_misses_is_not_a_cover"] is True
    assert data["mordell_primes"]["totals"] == {
        "primes": 345608,
        "hits": 345608,
        "misses": 0,
    }
    mins = {c["residue_mod_840"]: c["min_f_I"] for c in data["mordell_primes"]["classes"]}
    assert mins == {1: 12, 121: 24, 169: 22, 289: 28, 361: 14, 529: 30}
