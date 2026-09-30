# Identities

Every identity below is implemented in `erdos_straus/identities.py` and
proved identically in the parameter by `erdos_straus/algebra.py` (sympy
clears `4xyz − n(xy + xz + yz)` to zero). Sample integers are checked
by `tests/test_identities.py` using the exact rational verifier.

## Elementary

### Even `n = 2k`

\[
\frac{4}{2k} = \frac{1}{k} + \frac{1}{2k} + \frac{1}{2k}.
\]

### `n = 4k+3` (Salez’s `4t−1`)

Two-term form

\[
\frac{4}{4k+3} = \frac{1}{k+1} + \frac{1}{(4k+3)(k+1)}.
\]

Three-term split used in code: `(2(k+1), 2(k+1), n(k+1))`.

### `n ≡ 2 (mod 3)`

\[
\frac{4}{n} = \frac{1}{n} + \frac{1}{(n+1)/3} + \frac{1}{n(n+1)/3}.
\]

### `n = 8t−3 ≡ 5 (mod 8)` (Salez)

\[
\frac{4}{n} = \frac{1}{2t} + \frac{1}{tn} + \frac{1}{2tn}.
\]

## Mod 7 (Mordell / this repo’s Type II specialisations)

These were recovered by a linear-parameter search in the Elsholtz–Tao
Type II equations and then proved identically.

### `n = 7t+3`

\[
\frac{4}{n} = \frac{1}{2t+1} + \frac{1}{2n} + \frac{1}{2n(2t+1)}.
\]

Parameters: `a=1`, `b=2t+1`, `e=t+1`, `c=2`, `d=1`.

### `n = 7t+5`

\[
\frac{4}{n} = \frac{1}{2(t+1)} + \frac{1}{n(t+1)} + \frac{1}{2n}.
\]

Parameters: `a=t+1`, `b=2`, `e=t+3`, `c=1`, `d=1`.

### `n = 7t+6`

\[
\frac{4}{n} = \frac{1}{2(t+1)} + \frac{1}{2n} + \frac{1}{2n(t+1)}.
\]

Parameters: `a=1`, `b=t+1`, `e=t+2`, `c=1`, `d=2`.

## The `(1,5,3)` pair (Mordell’s mod-5 cover, rewritten)

A *single* polynomial identity for the whole class `n ≡ 2 (mod 5)` or
`n ≡ 3 (mod 5)` was not found among linear Type I/II parameters (and
Salez’s completeness result for degree-1 prime polynomials makes a
full-class polynomial identity for `5t+2` unlikely unless it is one of
his seven types with constant `4ab | 5`, which is impossible).

What *does* finish Mordell’s CRT is the Elsholtz–Tao pair with
`(a,b,e) = (1,5,3)`:

### Type II: `n ≡ 17 (mod 20)` (hence `n ≡ 2 (mod 5)`)

\[
\frac{4}{n} = \frac{1}{(n+3)/4} + \frac{1}{n(n+3)/10} + \frac{1}{n(n+3)/2}.
\]

### Type I: `n ≡ 13 (mod 20)` (hence `n ≡ 3 (mod 5)`)

\[
\frac{4}{n} = \frac{1}{n(3n+1)/4} + \frac{1}{(3n+1)/10} + \frac{1}{(3n+1)/2}.
\]

Every residue class modulo 840 that survives the 3/4/7/8 identities and
is `2` or `3` (mod 5) is in fact `17` or `13` (mod 20). That is why
these two formulas, together with the elementary list, leave exactly

\[
n \equiv 1,121,169,289,361,529 \pmod{840}
\]

among residues coprime to `210`. This is checked in
`tests/test_identities.py::test_classical_leftover_is_mordell_six`.

## Extra family that thins the hard classes: `(1,11,3)`

Not part of the Mordell CRT leftover (those six residues remain after
the list above). This pair covers a density-`1/11` subset of *each*
hard class, via modulus `9240 = lcm(840, 44)`.

### Type II: `n ≡ 41 (mod 44)`

`d = (n+3)/44`, triple `(11d,\ 4dn,\ 44dn)`.
Includes the first hard prime: `n = 1009`.

### Type I: `n ≡ 29 (mod 44)`

`d = (3n+1)/44`, triple `(11dn,\ 4d,\ 44d)`.

Implemented as `apply_extended` so the Mordell leftover computation
stays exactly the six squares.

## Elsholtz–Tao maps (any `n`)

Type I, if `e | a+b` and `4ab | (ne+1)`:

\[
(x,y,z) = (abdn,\ acd,\ bcd), \qquad d = (ne+1)/(4ab),\ c=(a+b)/e.
\]

Type II, if `e | a+b` and `4ab | (n+e)`:

\[
(x,y,z) = (abd,\ acdn,\ bcdn), \qquad d = (n+e)/(4ab),\ c=(a+b)/e.
\]

Both maps are proved identically in `algebra.prove_type_I_map` and
`prove_type_II_map`.

## Shifted greedy (Ionascu–Wilson / López), `n = 4k+1`

\[
\frac{4}{n} - \frac{1}{k+1+t} = \frac{4t+3}{n(k+1+t)}.
\]

If the right-hand side is a sum of two unit fractions — equivalently,
if `n(k+1+t)` has factors `u,w` with `u+w \equiv 0 \pmod{4t+3}` — we
have a triple. This is *not* a polynomial identity in `n`. It is the
construction that handles the Mordell-hard primes in the solver
(`1009`, `2521`, …).

Special case `t = 0`, `k = 3\ell+2`: `k+1` is divisible by `3`, so the
remainder is already a unit fraction.
