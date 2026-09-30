# Erdős–Straus leftover-credit workbench

For every integer \(n \ge 2\), the **Erdős–Straus conjecture** (Erdős–
Straus 1948; Erdős 1950) asks for positive integers \(x,y,z\) with

\[
\frac{4}{n} = \frac{1}{x} + \frac{1}{y} + \frac{1}{z}.
\]

This repository is a durable **workbench for leftover LLM credits**.
It records identities that still check, independently verified Egyptian-
fraction triples, Type I enumerator harvests, and first-R scans. It is
**not a proof**. The conjecture is open. There is **no** full
Mordell-class cover. Do not treat any table here as a covering family.

Leftover-agent rules: `CONVENTIONS.md`. What not to repeat:
`notes/CLOSED.md`. What to measure next: `notes/NEXT.md`.

## What this repo measures

A triple is accepted only on exact arithmetic. Never floats. Either
form is the check:

\[
4xyz - n(xy + xz + yz) = 0
\qquad\text{or}\qquad
\frac{4}{n} = \frac{1}{x} + \frac{1}{y} + \frac{1}{z}
\]

with \(n \ge 2\) and \(x,y,z \ge 1\). The Python verifier uses
`fractions.Fraction` and also prints \(n \bmod 840\).

Recorded here:

- Independently verified triples in `data/triples.csv` (readable copy:
  `notes/TRIPLES.md`). `make check` requires every CSV row to have
  residual `0`.
- Type I enumerator harvests at \(N = 10^6, 10^7, 2\times 10^7,
  5\times 10^7, 10^8, 2\times 10^8\). These count solutions under fixed
  constraints (\(y \le 2n/3\), \(x = n\cdot a\cdot b\cdot d\)). Zero
  misses among Mordell primes in a bound is a **measurement**, not a
  class cover. The \(N = 5\times 10^8\) harvest is incomplete.
- first-R scans on primes \(n \equiv 529 \pmod{840}\) through
  \(8.00\times 10^9\) (no first-R \(\ge 108\)). That is a search log,
  not a cover.
- A first-pass solver census: every \(n\) with \(2 \le n \le 8000\)
  has a verified triple from this solver; all 83 Mordell-hard primes
  \(\le 30000\) were solved here. Literature bounds \(10^{14}\) /
  \(10^{17}\) are citations, not this repo’s computation.

At \(N = 10^8\): \(\sum_n f_I = 37494215304\),
\(\sum_p f_I = 5818322818\), and all 179468 Mordell primes
\(p \le 10^8\) had \(f_I(p) > 0\). At \(N = 2\times 10^8\):
\(\sum_n f_I = 83381351012\), \(\sum_p f_I = 12463112814\). Details:
`notes/HARVEST-1e8.md`, `notes/HARVEST-2e8.md`.

## How to verify a triple

```bash
python3 -m pip install -e ".[dev]"
erdos-straus verify 1009 253 85096 1974822872
erdos-straus verify 2521 636 69748 131876031
erdos-straus check-csv
make check
```

Without installing the package:

```bash
PYTHONPATH=. python3 scripts/verify_triple.py 1009 253 85096 1974822872
PYTHONPATH=. python3 -m erdos_straus.cli verify 2521 636 69748 131876031
PYTHONPATH=. python3 -m erdos_straus.cli check-csv
PYTHONPATH=. python3 -m pytest
make check
```

`make check` runs the pytest suite and then checks `data/triples.csv`
twice (package CLI and `scripts/verify_triple.py`). A row fails unless
the integer residual is exactly `0`.

Other useful commands after `pip install -e ".[dev]"`:

```bash
erdos-straus solve 1009
erdos-straus classify 1009
python3 -m pytest
```

Failure from the solver means “not found with this budget”, not
“counterexample”.

## Settled identities (do not rediscover)

These still check in `erdos_straus/identities.py` / `algebra.py`
(sympy clears the Diophantine polynomial; `tests/test_identities.py`
exercises integer samples). Details: `IDENTITIES.md`.

| class | construction |
| --- | --- |
| \(n\) even | \(1/(n/2) + 1/n + 1/n\) |
| \(n \equiv 3 \pmod{4}\) | Salez / two-term split |
| \(n \equiv 2 \pmod{3}\) | \(1/n + 1/((n+1)/3) + 1/(n(n+1)/3)\) |
| \(n \equiv 5 \pmod{8}\) | Salez \(8t-3\) |
| \(n \equiv 3,5,6 \pmod{7}\) | Type II polynomials |
| \(n \equiv 13\) or \(17 \pmod{20}\) | Type I/II with \((a,b,e)=(1,5,3)\) |

Residues coprime to \(210\) reduce to the Mordell six:

\[
n \equiv 1,\ 121,\ 169,\ 289,\ 361,\ 529 \pmod{840}.
\]

Open core = **primes in those classes**. Anything that claims a full
cover of one of those six is stale — none exists.

A composite \(n = mp\) is never a minimal counterexample: scale a
triple for \(p\). Smallest leftover prime: \(1009\).

## Thin verified families (not covers)

Extra thin, already in the first-pass solver: \((a,b,e)=(1,11,3)\) hits
\(n \equiv 41\) or \(29 \pmod{44}\), density \(1/11\), **not** a full
class.

Two divisor-conditional families from later leftover work (they miss
hard primes; do not promote them):

1. \(q \mid (2n+1)\), \(q \equiv 7 \pmod{8}\):
   \(x=(2n+1)(q+1)/(8q)\), \(y=n(q+1)/4\),
   \(z=n(2n+1)(q+1)/(4q)\). Misses \(2521\).
2. \(q \mid (3n+1)\), \(q \equiv 11 \pmod{12}\):
   \(x=(3n+1)(q+1)/(12q)\), \(y=n(q+1)/4\),
   \(z=n(3n+1)(q+1)/(4q)\). Misses \(2521\). \(9241\) does **not** fit.

## First-pass solver (kept)

The Python solver is useful for small \(n\) and for checking
identities. It is **not** a class cover.

1. Classical residue identities above.
2. Scale from the smallest prime factor if \(n\) is composite.
3. Ionascu’s closed cases \(n=4k+1\), \(k\not\equiv 0\pmod{3}\).
4. Shifted-greedy remainder split (unbounded search, not a cover).
5. Elsholtz–Tao Type I/II search.
6. Bounded scan of the first denominator.

## Layout

```
CONVENTIONS.md    leftover-agent rules (never Fable; spend caps)
notes/CLOSED.md   dead ends — do not repeat
notes/HARVEST-*.md  Type I census notes (measurement, not a cover)
notes/FIRST-R-529.md  first-R scan on n≡529 from 5.70e8
notes/NEXT.md     first-R from 8e9 or Type I toward 5e8
notes/TRIPLES.md  human copy of the verified table
data/triples.csv  n,x,y,z,n_mod_840,notes
data/typeI_mordell_*.json  structured Type I Mordell counts
erdos_straus/     identities, solver, Fraction verifier
scripts/verify_triple.py
enum/             Type I enumerator (`fi2`) and shard tables
IDENTITIES.md     algebra of every shipped identity
NOTES.md          first-pass failed searches
REFERENCES.md     papers actually consulted
LICENSE           MIT
```

The Type I enumerator at \(N = 2\times 10^8\) is done. Do not rebuild
`fi2`. Do not rerun \(\le 2\times 10^8\). Optional leftover work is
first-R from \(8.00\times 10^9\) or Type I toward \(5\times 10^8\)
(`notes/NEXT.md`).

A durable first-R scanner for \(n\equiv 529\pmod{840}\) lives in
`scripts/scan_first_r.py`. Wave 4 through \(8.00\times 10^8\) and
wave 5 through \(8.00\times 10^9\) found no first-R \(\ge 108\)
(`notes/FIRST-R-529.md`).
