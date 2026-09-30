"""Constructive toolkit for the Erdős–Straus conjecture.

Conjecture (Erdős–Straus, 1948): for every integer n ≥ 2 there exist
positive integers x, y, z such that

    4/n = 1/x + 1/y + 1/z.

This package does not claim a proof of the full conjecture. It reconstructs
the standard constructive identities, searches the Elsholtz–Tao / Salez
parametric families, and finds a verified triple for every n that the
solver is asked to handle.
"""

from erdos_straus.solver import Solution, solve
from erdos_straus.verifier import residual, verify, verify_triple

__all__ = ["Solution", "solve", "residual", "verify", "verify_triple"]
__version__ = "0.2.0"
