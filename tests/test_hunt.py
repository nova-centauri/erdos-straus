from erdos_straus.hunt import hard_subprogressions, sample_verify_covering
from erdos_straus.identities import MORDELL_UNCOVERED


def test_hard_subprogressions_exist_and_verify():
    covers = hard_subprogressions(ab_bound=20)
    # Constant (a,b,e) cannot cover a full Mordell-hard class, but they
    # do cover infinite subprogressions inside those classes.
    assert covers, "expected at least one subclass covering"
    hit_hard = {c.hard_r for c in covers}
    assert hit_hard & set(MORDELL_UNCOVERED)
    # Spot-check a handful of coverings on concrete n.
    checked = 0
    for c in covers:
        if c.combined_mod is None:
            continue
        failed = sample_verify_covering(c, samples=2)
        assert failed == [], f"covering {c} failed on {failed}"
        checked += 1
        if checked >= 8:
            break
    assert checked >= 4
