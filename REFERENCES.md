# References

Only works actually consulted (PDF, HTML, or a standard bibliographic
record with matching title/year) are listed. Titles and years are not
invented.

## Primary

- Paul Erdős, “Az \(1/x_1 + \cdots + 1/x_n = a/b\) egyenlet egész számú
  megoldásairól (On a Diophantine Equation)”, *Mat. Lapok* **1** (1950),
  192–210. MR 0043117. (The conjecture was formulated with Ernst G.
  Straus in 1948 and published here.)

- Richard Obláth, “Sur l’équation diophantienne \(4/n = 1/x_1+1/x_2+1/x_3\)”,
  *Mathesis* **59** (1950), 308–316. MR 0038999.

- L. J. Mordell, *Diophantine Equations*, Academic Press, 1967, pp. 287–290.
  Identities for `n ≡ 3 (mod 4)`, `2` or `3 (mod 5)`, `3,5,6 (mod 7)`,
  `5 (mod 8)`; quadratic-residue obstruction; leftover
  `{1, 121, 169, 289, 361, 529} (mod 840)`.

- Luigi Antonio Rosati, “Sull’equazione diofantea
  \(4/n = 1/x_1 + 1/x_2 + 1/x_3\)”, *Boll. Un. Mat. Ital.* (3) **9**
  (1954), 59–63. MR 0060526. (Parametrisation that Mordell reports.)

- Koichi Yamamoto, “On the Diophantine equation \(4/n = 1/x + 1/y + 1/z\)”,
  *Mem. Fac. Sci. Kyushu Univ. Ser. A* **19** (1965), 37–47.
  doi:10.2206/kyushumfs.19.37. Verification to `10^7`.

- W. A. Webb, “On \(4/n = 1/x_1 + 1/x_2 + 1/x_3\)”, *Proc. Amer. Math. Soc.*
  **25** (1970), 578–584. Density of possible counterexamples is zero.

- R. C. Vaughan, “On a problem of Erdős, Straus and Schinzel”,
  *Mathematika* **17** (1970), 193–198. Exceptional set
  \(\ll N \exp(-c (\log N)^{2/3})\).

- Wacław Sierpiński, “Sur les décompositions de nombres rationnels en
  fractions primaires”, *Mathesis* **65** (1956), 16–32. The `5/n`
  analogue; credits the general `k/n` form to Schinzel.

## Computational surveys

- Allan Swett, “The Erdős–Straus conjecture”, notes dated 1999
  (often cited as a verification to `10^{14}`). The original page
  `http://math.uindy.edu/swett/esc.htm` is cited by Salez; this repo
  did not independently retrieve a live copy.

- Serge E. Salez, “The Erdős-Straus conjecture. New modular equations
  and checking up to \(N = 10^{17}\)”, arXiv:1406.6307, 2014.
  Seven modular equations; sieve; claimed verification to `10^{17}`.
  **This repo did not rerun that sieve.**

## Structure of solutions

- Christian Elsholtz and Terence Tao, “Counting the number of solutions
  to the Erdős–Straus equation on unit fractions”, *J. Aust. Math. Soc.*
  **94** (2013), 50–105. arXiv:1107.1010. Type I / Type II; complete
  list of polynomial-solvable primitive residue classes; polylog
  average number of solutions on primes.

- Eugen J. Ionascu and Andrew Wilson, “On the Erdős–Straus conjecture”,
  *Rev. Roumaine Math. Pures Appl.* **56** (2011), 21–30. arXiv:1001.1100.
  Greedy split of `3/((k+1)n)` for `n = 4k+1`; leftover `n ≡ 1 (mod 24)`.

- Miguel Ángel López, “Structure and form of the solutions of the
  Erdos-Straus conjecture”, arXiv:2206.10319, 2022. `(du, dv, duv)`
  criterion and the `t`-divisor condition on `k+1+t`.

## Background pages consulted

- Wikipedia, “Erdős–Straus conjecture”, retrieved 2026-08-27.
  Used as a map of the literature, then checked against the sources
  above. Not treated as a primary source for theorems.

## Not used as evidence

Later preprints that this session saw in search snippets but did not
read in full (for example arXiv:2404.01508, arXiv:2509.00128,
arXiv:2602.20036, arXiv:2608.24035) are **not** cited for any
numerical bound, identity, or theorem in the README.
