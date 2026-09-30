# Closed dead ends (do not repeat)

Leftover-credit work from SuperGrok Heavy and Claude Opus 5 (27–29 Aug 2026)
closed the items below. Do not reopen them, do not invent a new covering
family that “finishes a Mordell class”, and do not rebuild the Type I
enumerator. First-pass search notes that are still valid live in
`NOTES.md` at the repo root; this file supersedes any claim that a
**full** Mordell-class cover exists. None exists.

Anything that claims a full Mordell-class cover is stale.

## Fixed / constant `(a,b,e)` Type I/II

Fixed or constant-`(a,b,e)` Type I/II **cannot** cover a full hard class.
The obstruction is Mordell’s: the six leftover residues
`1, 121, 169, 289, 361, 529 (mod 840)` are squares. Constant parameters
only thin subclasses.

## Bounded shifted-greedy

Bounded shifted-greedy cannot finish the six classes. Unbounded
shifted-greedy is a **search**, not a cover.

## `n ≡ 529 (mod 840)`

- `21 | (n² + n + 1)` produces `q ≡ 3 (mod 4)`, but then `n` is a cube
  root of unity mod `q`. No Ionascu–Wilson construction comes from that
  `q`.
- The same claim was checked and failed for `n² − n + 1`, `n² + 3`, and
  `n² ± n − 1`.
- Missed example: **3049** (still a miss for these constructions).
  An earlier chat claim that the Type I enumerator gave
  `f_I(3049) = 0` was a **truncation artifact**; true
  `f_I(3049) = 30` (Opus turn 8). See `notes/HARVEST-1e7.md`.
- Heavy later: `35 | n² − n + 23` split; max first-`R` seen below
  `3.5 × 10⁵` is **31**.
- Wave 4 first-R scanner (not a cover): 58958 primes
  `n ≡ 529 (mod 840)` in `[5.70×10⁸, 8.00×10⁸)` had **no** first-R
  `≥ 108`. Max seen is **63** at `586775809`.
- Wave 5 (not a cover): 1700954 primes in `[8.00×10⁸, 8.00×10⁹)`
  had **no** first-R `≥ 108`. Max seen is **83** at `3434195209`.
  Continue from `8.00×10⁹` with `scripts/scan_first_r.py`. See
  `notes/FIRST-R-529.md`.

## Constant Type I/II empty on `n ≡ 1` and halves of 121 / 169

Constant Type I/II is empty for the full class `n ≡ 1 (mod 840)` and
for halves of the `121` and `169` classes.

## Lopez / linear-in-`k` / splits on 121 and 169

- Constant-`D` Lopez and linear-in-`k` are empty on `840k + 121`.
- Same emptiness on `n ≡ 169` after the splits `1680 / 2520 / 3360`.
- Quadratic-`u` + linear-`D` is impossible on 169 (`4tf = 169`).
- No 2-split or 3-split on 169.

## Polynomial-parameter Type I/II cannot cover `n ≡ 289`

Polynomial-parameter Type I/II cannot cover `n ≡ 289 (mod 840)`:
`e ≡ 311` versus the bound `e | Y+Z ≤ 211`. Missed example: **13729**.

## Constant-polynomial taxonomy

Among residues with `gcd(r, 840) = 1`, a constant-polynomial identity
covers `r` **iff** `r` is a quadratic non-residue mod 840. Count:
**186 / 192**. The six exceptions are the Mordell squares.

`n ≡ 361`: S1 kill, `e ≡ 719 > 211`. Missed example: **8761**.

## `n ≡ 1 (mod 840)` first-term families A / B / C

Three first-term families, density 1 in the primes of the class, **not**
a cover:

| tag | condition |
| --- | --- |
| A | `q | (4n+1)` and `q ≡ 3 (mod 4)` |
| B | `q | (8n+1)` and `q ≡ 7 (mod 8)` |
| C | `q | (3n+1)/4` and `q ≡ 2 (mod 3)` |

Measurement: **556 / 3426** primes `< 10⁷` miss all three. Quadratics
are dead (`n | 2` or Pell). **2521** misses A, B, and C. Heavy: cubic /
cyclotomic first-term families on `n ≡ 1` are closed.

## `n ≡ 121 (mod 840)` — `P_h` / Type I `s=1` / `n² + 4h`

All **3431** primes `< 10⁷` fire (measurement, not a proof of a cover).
Genus block on `h` with squarefree kernel dividing 210. Deepest `k = 38`
at **5471041**.

## `n ≡ 169` and `n ≡ 529`: Elsholtz–Tao Prop. 1.6

Infinitely many odd squares in each class. Elsholtz–Tao Proposition 1.6
⇒ **no** Type I/II full-class cover. A primes-only cover of those
classes is still open and is **not** a leftover-credit target this
cycle.

## Enumerator BUILD is done (Opus turn 7)

Do **not** rebuild `fi2.c` / `vI.c` / `bruteI2.py`.

Recorded at `N = 10⁶`:

- `Σ_n f_I = 165374532`
- `Σ_p f_I = 34276274`
- `c₀ ≈ 0.1456`

Bugs that were already fixed in that build (do not “rediscover” them):

- `y ≤ 2n/3`
- `x = n · a · b · d`

The `10⁷` harvest is done (Opus turn 8). Do not rerun it. See
`notes/HARVEST-1e7.md`. The `5×10⁷` and `10⁸` harvests are also done
(`notes/HARVEST-5e7.md`, `notes/HARVEST-1e8.md`). The `2×10⁸` harvest
is also done (`notes/HARVEST-2e8.md`). Next leftover spend is
`notes/NEXT.md` (same constraints — not a rebuild).

## Type I harvest at `10⁷` is measurement, not a cover (Opus turn 8)

Recorded 2026-09-05 from chat `425b3bdb`. Full table:
`notes/HARVEST-1e7.md`, `data/typeI_mordell_1e7.json`.

- `Σ_{n≤10⁷} f_I(n) = 2559629008`
- `Σ_{p≤10⁷} f_I(p) = 454495120`
- Fit: `c₀ = 0.14420`, `c₁ = 0.496`, observed
  `P/(M ln² M) = 0.17495` (compare `c₀ ≈ 0.1456` at `10⁶`)
- Runtime: 1633 s, eight slices, one core
- All **20513** Mordell primes `p ≤ 10⁷` had `f_I(p) > 0` (zero misses)
- No new triples; ESC unproved

**Zero Type I misses among Mordell primes ≤ 10⁷ is not a full-class
cover.** Do not harvest `10⁷` again.

## Type I harvest at `2×10⁷` is measurement, not a cover (wave 1)

Reconstructed `enum/fi2` (2026-09-06). Full table: `notes/HARVEST-2e7.md`,
`data/typeI_mordell_2e7.json`.

- `Σ_{n≤2×10⁷} f_I(n) = 5772274472`
- `Σ_{p≤2×10⁷} f_I(p) = 982580024`
- observed `P/(M ln² M) = 0.17384` (was 0.17495 at `10⁷`)
- Runtime: 2860 s, 4 cores
- All **39391** Mordell primes `p ≤ 2×10⁷` had `f_I(p) > 0` (zero misses)
- The `10⁷` table was recomputed here and matched Opus exactly

**Zero Type I misses through 2×10⁷ is not a full-class cover.**
Do not harvest `2×10⁷` again.

## Type I harvest at `5×10⁷` is measurement, not a cover (wave 2)

Same `enum/fi2`, checkpointed a-range merge. Full table:
`notes/HARVEST-5e7.md`, `data/typeI_mordell_5e7.json`.

- `Σ_{n≤5×10⁷} f_I(n) = 16795310188`
- `Σ_{p≤5×10⁷} f_I(p) = 2709141549`
- observed `P/(M ln² M) = 0.17241` (was 0.17384 at `2×10⁷`)
- All **93457** Mordell primes `p ≤ 5×10⁷` had `f_I(p) > 0` (zero misses)
- Checksums: `f_I(3049)=30`, `f_I(2521)=12`, `f_I(1009)=22`

**Zero Type I misses through 5×10⁷ is not a full-class cover.**
Do not harvest `5×10⁷` again.

## Type I harvest at `10⁸` is measurement, not a cover (wave 3)

Same `enum/fi2`, checkpointed a-range merge. Full table:
`notes/HARVEST-1e8.md`, `data/typeI_mordell_1e8.json`.

- `Σ_{n≤10⁸} f_I(n) = 37494215304`
- `Σ_{p≤10⁸} f_I(p) = 5818322818`
- observed `P/(M ln² M) = 0.17147` (was 0.17241 at `5×10⁷`)
- All **179468** Mordell primes `p ≤ 10⁸` had `f_I(p) > 0` (zero misses)
- Checksums: `f_I(3049)=30`, `f_I(2521)=12`, `f_I(1009)=22`

**Zero Type I misses through 10⁸ is not a full-class cover.**
Do not harvest `10⁸` again.

## Type I harvest at `2×10⁸` is measurement, not a cover (wave 4)

Same `enum/fi2`, checkpointed a-range merge. Full table:
`notes/HARVEST-2e8.md`, `data/typeI_mordell_2e8.json`.

- `Σ_{n≤2×10⁸} f_I(n) = 83381351012`
- `Σ_{p≤2×10⁸} f_I(p) = 12463112814`
- observed `P/(M ln² M) = 0.17057` (was 0.17147 at `10⁸`; same \(N\ln^2 N\) convention)
- All **345608** Mordell primes `p ≤ 2×10⁸` had `f_I(p) > 0` (zero misses)
- Checksums: `f_I(3049)=30`, `f_I(2521)=12`, `f_I(1009)=22`

**Zero Type I misses through 2×10⁸ is not a full-class cover.**
Do not harvest `2×10⁸` again. Next leftover spend is `notes/NEXT.md`.


## Thin families that are not covers

These identities check when the divisor condition holds. They miss
hard primes. Do not promote them to class covers.

1. `q | (2n+1)`, `q ≡ 7 (mod 8)`:

   `x = (2n+1)(q+1)/(8q)`, `y = n(q+1)/4`,
   `z = n(2n+1)(q+1)/(4q)`.

   Misses **2521**.

2. `q | (3n+1)`, `q ≡ 11 (mod 12)`:

   `x = (3n+1)(q+1)/(12q)`, `y = n(q+1)/4`,
   `z = n(3n+1)(q+1)/(4q)`.

   Misses **2521**. **9241 does not fit.**

Extra thin (already in the first-pass solver): `(a,b,e) = (1,11,3)`
covers `n ≡ 41` or `29 (mod 44)`, density `1/11`, **not** a full Mordell
class. First leftover prime `1009` is `41 (mod 44)`.
