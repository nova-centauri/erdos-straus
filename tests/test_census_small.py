from erdos_straus.census import run_census


def test_census_to_400():
    result = run_census(400)
    assert result["unsolved"] == []
    assert result["smallest_unsolved"] is None
    assert result["solved"] == 399
