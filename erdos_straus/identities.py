"""Closed-form constructive identities for 4/n = 1/x + 1/y + 1/z.

Every identity here is an explicit map n ↦ (x, y, z) that is integer on
the stated residue class. Algebraic verification is in
``erdos_straus.algebra`` and the test suite.

Classical sources:
    Mordell, *Diophantine Equations*, Academic Press, 1967, pp. 287–290.
    Salez, arXiv:1406.6307 (2014), explicit 3t−1, 4t−1, 8t−3 forms.
    The mod-3 identity is the standard textbook example (see Wikipedia).

Mordell's combined list (mod 3, 4, 5, 7, 8) covers every n except
possibly those with

    n ≡ 1, 121, 169, 289, 361, or 529  (mod 840).

Those six residues are squares, which is required by Mordell's
quadratic-residue obstruction: a polynomial identity for n ≡ r (mod q)
can exist only when r is a quadratic non-residue mod q.
"""

from __future__ import annotations

from collections.abc import Callable

from erdos_straus.types import Triple


def even_identity(n: int) -> Triple:
    """n even: 4/n = 1/(n/2) + 1/n + 1/n."""
    return Triple(n // 2, n, n)


def mod4_eq3(n: int) -> Triple:
    """n = 4k+3: 4/n = 1/(k+1) + 1/(n(k+1)); split the first term equally.

    Equivalent two-term form (Salez): 4/(4t−1) = 1/t + 1/(t(4t−1)).
    """
    k = (n - 3) // 4
    t = k + 1
    return Triple(2 * t, 2 * t, n * t)


def mod3_eq2(n: int) -> Triple:
    """n ≡ 2 (mod 3): 4/n = 1/n + 1/((n+1)/3) + 1/(n(n+1)/3)."""
    return Triple(n, (n + 1) // 3, n * (n + 1) // 3)


def mod8_eq5(n: int) -> Triple:
    """n = 8t−3 ≡ 5 (mod 8): 4/n = 1/(2t) + 1/(t n) + 1/(2 t n)."""
    t = (n + 3) // 8
    return Triple(2 * t, t * n, 2 * t * n)


def mod7_eq3(n: int) -> Triple:
    """n = 7t+3. Type II with a=1, b=2t+1, e=t+1, c=2, d=1.

    4/n = 1/(2t+1) + 1/(2n) + 1/(2n(2t+1)).
    """
    t = (n - 3) // 7
    return Triple(2 * t + 1, 2 * n, 2 * n * (2 * t + 1))


def mod7_eq5(n: int) -> Triple:
    """n = 7t+5. Type II with a=t+1, b=2, e=t+3, c=1, d=1.

    4/n = 1/(2(t+1)) + 1/(n(t+1)) + 1/(2n).
    """
    t = (n - 5) // 7
    return Triple(2 * (t + 1), n * (t + 1), 2 * n)


def mod20_eq17(n: int) -> Triple:
    """n ≡ 17 (mod 20). Type II with a=1, b=5, e=3.

    This is the usable form of Mordell's “n ≡ 2 (mod 5)” cover: every
    leftover after the 3/4/7/8 identities that is 2 (mod 5) is in fact
    17 (mod 20). Explicitly

        x = (n+3)/4,  y = n(n+3)/10,  z = n(n+3)/2.
    """
    return Triple((n + 3) // 4, n * (n + 3) // 10, n * (n + 3) // 2)


def mod20_eq13(n: int) -> Triple:
    """n ≡ 13 (mod 20). Type I with a=1, b=5, e=3.

    Usable form of Mordell's “n ≡ 3 (mod 5)” cover: leftover 3-mod-5
    values after 3/4/7/8 are 13 (mod 20). Explicitly

        x = n(3n+1)/4,  y = (3n+1)/10,  z = (3n+1)/2.
    """
    return Triple(n * (3 * n + 1) // 4, (3 * n + 1) // 10, (3 * n + 1) // 2)


def mod7_eq6(n: int) -> Triple:
    """n = 7t+6. Type II with a=1, b=t+1, e=t+2, c=1, d=2.

    4/n = 1/(2(t+1)) + 1/(2n) + 1/(2n(t+1)).
    """
    t = (n - 6) // 7
    return Triple(2 * (t + 1), 2 * n, 2 * n * (t + 1))


IdentityFn = Callable[[int], Triple]

# Only identities that are polynomial (or even-split) and integer on the
# whole residue class go in this table. Mod-5 and mod-7 covers are applied
# in ``apply_mordell_extended`` after their polynomials are proven.
_IDENTITY_TABLE: list[tuple[str, Callable[[int], bool], IdentityFn]] = [
    ("even", lambda n: n % 2 == 0, even_identity),
    ("n≡3(mod 4)", lambda n: n % 4 == 3, mod4_eq3),
    ("n≡2(mod 3)", lambda n: n % 3 == 2, mod3_eq2),
    ("n≡5(mod 8)", lambda n: n % 8 == 5, mod8_eq5),
    ("n≡3(mod 7)", lambda n: n % 7 == 3, mod7_eq3),
    ("n≡5(mod 7)", lambda n: n % 7 == 5, mod7_eq5),
    ("n≡6(mod 7)", lambda n: n % 7 == 6, mod7_eq6),
    ("n≡17(mod 20)", lambda n: n % 20 == 17, mod20_eq17),
    ("n≡13(mod 20)", lambda n: n % 20 == 13, mod20_eq13),
]


def mod44_eq41(n: int) -> Triple:
    """n ≡ 41 (mod 44). Type II with a=1, b=11, e=3.

    Covers a 1/11-density subclass of every Mordell-hard residue
    (n ≡ 1009, 1801, 3649, 7081, 8401, 8929 (mod 9240)).
    """
    d = (n + 3) // 44
    # c = (a+b)/e = 4; x = abd = 11d, y = acdn = 4dn, z = bcdn = 44dn
    return Triple(11 * d, 4 * d * n, 44 * d * n)


def mod44_eq29(n: int) -> Triple:
    """n ≡ 29 (mod 44). Type I with a=1, b=11, e=3."""
    d = (3 * n + 1) // 44
    return Triple(11 * d * n, 4 * d, 44 * d)


_EXTENDED_TABLE: list[tuple[str, Callable[[int], bool], IdentityFn]] = [
    ("n≡41(mod 44)", lambda n: n % 44 == 41, mod44_eq41),
    ("n≡29(mod 44)", lambda n: n % 44 == 29, mod44_eq29),
]


def apply_classical(n: int) -> tuple[str, Triple] | None:
    """Apply the first classical identity whose residue predicate matches."""
    if n < 2:
        return None
    for name, pred, ctor in _IDENTITY_TABLE:
        if pred(n):
            return name, ctor(n)
    return None


def apply_extended(n: int) -> tuple[str, Triple] | None:
    """Extra families that thin the Mordell-hard classes. Not used in the
    CRT leftover computation for Mordell's six residues."""
    if n < 2:
        return None
    for name, pred, ctor in _EXTENDED_TABLE:
        if pred(n):
            return name, ctor(n)
    return None


MORDELL_UNCOVERED: frozenset[int] = frozenset({1, 121, 169, 289, 361, 529})


def is_mordell_hard(n: int) -> bool:
    return n % 840 in MORDELL_UNCOVERED


def is_hard_mod24(n: int) -> bool:
    return n % 24 == 1
