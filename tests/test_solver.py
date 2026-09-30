from erdos_straus.identities import is_mordell_hard
from erdos_straus.solver import solve
from erdos_straus.verifier import verify


def test_solve_small_range():
    missing = []
    for n in range(2, 400):
        sol = solve(n)
        if sol is None or not verify(n, sol.x, sol.y, sol.z):
            missing.append(n)
    assert missing == [], f"unsolved: {missing}"


def test_solve_hard_mod24_upto_300():
    missing = []
    for n in range(25, 301, 24):
        sol = solve(n)
        if sol is None or not verify(n, sol.x, sol.y, sol.z):
            missing.append(n)
    assert missing == [], f"unsolved 1 mod 24: {missing}"


def test_famous_values():
    for n in (73, 193, 1009, 2521):
        sol = solve(n) or __import__("erdos_straus.solver", fromlist=["deepen"]).deepen(n)
        assert sol is not None, f"failed n={n}"
        assert verify(n, sol.x, sol.y, sol.z)
        if n in (1009, 2521):
            assert is_mordell_hard(n)
    assert solve(1009).method.startswith("identity:n≡41")
