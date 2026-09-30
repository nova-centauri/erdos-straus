from scripts.typeI_count_ref import f_I


def test_harvest_checksum_primes():
    assert f_I(3049) == 30
    assert f_I(2521) == 12
    assert f_I(1009) == 22
    assert f_I(1801) == 24
    assert f_I(1129) == 28
    assert f_I(1201) == 14
