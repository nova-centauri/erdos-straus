from erdos_straus.classify import classification
from erdos_straus.identities import is_mordell_hard


def test_classification_1009():
    c = classification(1009)
    assert c["prime"] is True
    assert c["mordell_hard"] is True
    assert c["hard_mod24"] is True
    assert c["minimal_candidate"] is True
    assert is_mordell_hard(1009)


def test_classification_composite_hard_residue():
    c = classification(121)
    assert c["prime"] is False
    assert c["mordell_hard"] is True
    assert c["minimal_candidate"] is False
