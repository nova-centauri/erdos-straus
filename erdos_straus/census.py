"""Census: attempt a construction for every n in a range."""

from __future__ import annotations

from collections import Counter

from erdos_straus.identities import is_mordell_hard
from erdos_straus.solver import deepen, solve
from erdos_straus.verifier import verify


def run_census(limit: int, deep: bool = False) -> dict:
    if limit < 2:
        return {
            "limit": limit,
            "solved": 0,
            "unsolved": [],
            "smallest_unsolved": None,
            "methods": {},
            "mordell_hard_solved": 0,
            "mordell_hard_unsolved": [],
        }
    methods: Counter[str] = Counter()
    unsolved: list[int] = []
    hard_unsolved: list[int] = []
    hard_solved = 0
    solved = 0
    finder = deepen if deep else solve
    for n in range(2, limit + 1):
        sol = finder(n)
        if sol is None or not verify(n, sol.x, sol.y, sol.z):
            unsolved.append(n)
            if is_mordell_hard(n):
                hard_unsolved.append(n)
            continue
        solved += 1
        methods[sol.method.split(":")[0]] += 1
        if is_mordell_hard(n):
            hard_solved += 1
    return {
        "limit": limit,
        "solved": solved,
        "unsolved": unsolved,
        "smallest_unsolved": unsolved[0] if unsolved else None,
        "methods": dict(methods),
        "mordell_hard_solved": hard_solved,
        "mordell_hard_unsolved": hard_unsolved,
    }
