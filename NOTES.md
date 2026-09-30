# Failed approaches and dead ends (first pass)

This file exists so the next person does not rerun searches that already
failed, and so that “we could not find X” is a documented negative
result rather than an omission.

**Later closures supersede cover claims in this file.** SuperGrok Heavy
and Claude Opus 5 (27–29 Aug 2026) closed constant Type I/II covers,
bounded shifted-greedy as a finisher, several first-term families, and
the enumerator rebuild. Read `notes/CLOSED.md` first and do not repeat
those. Next leftover spend is `notes/NEXT.md`, not a new identity hunt.

## A single polynomial identity for all `n ≡ 2 (mod 5)`

Tried:

- Constant `(a,b,e)` Type I/II. Then `4ab` must divide `5` (the
  difference of consecutive values of `n+e` or `ne+1`), which is
  impossible for `4ab ≥ 4`.
- Linear `a(t), b(t), e(t)` Type I and Type II with small integer
  coefficients (`a_i, b_i ≤ 5`, `e_i ≤ 6`). No hit for `n = 5t+2` or
  `n = 5t+3`.
- Salez (14a) with constant `B,C,D ≤ 30`: no hit.
- Interpolating solver triples on the *uncovered* subsequence of
  `n ≡ 2 (mod 5)` (those not already even / `3 (mod 4)` / `2 (mod 3)` /
  `5 (mod 8)`). Degree-2 interpolation did not fit.

Conclusion, used in the writeup: Mordell’s “`2` or `3` (mod `5`)”
cover, in the form needed to finish the CRT, is the thinner pair
`n ≡ 13, 17 (mod 20)`, not a single formula for the whole mod-`5`
class. Those two formulas were found by a linear Type I/II search on
the leftover `840`-classes `193, 337, 457, 673, 697, 793`.

A full-class polynomial identity for `5t+2` is not forbidden by
Mordell’s quadratic-residue obstruction (`2` is a non-residue mod `5`),
but Salez’s completeness theorem for degree-1 prime polynomials says
it would have to be one of seven modular equations. The constant-`4ab`
cases of those equations cannot divide `5`. We did **not** exhaust
every higher-degree specialisation of Salez’s seven types; we only
exhausted linear Type I/II with small coefficients.

## Polynomial identities for a full Mordell-hard class

Searched linear Type I/II for

- `n = 840t + r` with `r ∈ {1, 121, 169, 289, 361, 529}`,
- `n = 24t + 1`,
- `n = 264t + 193` and `264t + 145` (the `1 (mod 24)` lifts of the
  non-residues `2, 6 (mod 11)` that Salez’s filter `S_{11}` does not
  list),
- `n = 11t + 2` and `11t + 6`.

No hits. This is the expected Mordell / Schinzel obstruction for the
square classes, and for `11t+2` / `11t+6` it is consistent with Salez:
those residues are non-squares mod `11`, so an identity is *allowed*,
but it need not exist, and Salez’s `S_{11} = {0, 7, 8, 10}` suggests
nobody has a simple polynomial identity for `2` or `6` (mod `11`)
inside `n ≡ 1 (mod 24)`.

We did **not** prove that no polynomial identity exists for
`n ≡ 2 (mod 11)`. We only failed to find a linear Type I/II one with
small coefficients.

## Covering systems of polynomial identities

Mordell already showed this cannot finish the conjecture: `1` is a
square modulo every `q > 1`, so some residue is always uncovered.
This repo does not attempt to “complete the covering” in that sense.

Constant `(a,b,e)` *do* cover infinite **subprogressions** of each
hard class (CRT of `n ≡ −e (mod 4ab)` or `n ≡ −e^{-1} (mod 4ab)`
against `n ≡ r (mod 840)`). Those are catalogued by `scripts/hunt_report.py`.
They thin the hard set; they do not reduce it to a finite check.

## First-denominator interpolation on hard primes

Taking the smallest `x` in solutions for `n = 840t + 1009` (etc.) and
fitting a low-degree polynomial in `t` does not yield a formula that
continues to the next hard prime. The shifted-greedy `t` that works
jumps around with the divisor structure of `k+1+t`.

## Claiming a computational bound we did not run

Literature bounds (`10^{14}` Swett, `10^{17}` Salez, later claims of
`10^{18}`) are cited only as citations. This repo’s own bound is
whatever `scripts/run_census.py` has actually executed. Do not copy a
literature bound into `smallest_unsolved` unless this solver ran that
far.

## Lean 4

Skipped. Formalising the sympy-checked identities is possible and
would be a clean stretch, but it would not change the mathematical
status of the conjecture and would have blocked the computational
attack.

## What still looks promising

Leftover credit is **not** for reopening the items above. The `10⁷`
Type I harvest is done (`notes/HARVEST-1e7.md`) and was recomputed
here. \(N=2\times10^7\) is also done (`notes/HARVEST-2e7.md`).
Queued spend is `notes/NEXT.md` (`5\times10^7` then `10^8`).

Bounded shifted-greedy cannot finish the classes; unbounded
shifted-greedy is a search (`notes/CLOSED.md`). Constant `(a,b,e)`
cannot cover a full hard class. Do not invent a new covering family
on leftover credit.

1. Larger `(a,b,e)` catalogs (Salez-style modular filters `S_m`) still
   thin hard primes before a first-denominator search. That is
   literature method, not a leftover-credit target this cycle.
2. A primes-only cover of `n ≡ 169` or `529` is still open
   (Elsholtz–Tao Prop. 1.6 kills a full Type I/II class cover, not
   a primes-only statement). Do not treat that as a proof task here.
3. The first-pass hypothesis that “a new identity family can cover
   the remaining residue classes” is closed for polynomial / constant
   Type I/II: the six Mordell squares stay.
