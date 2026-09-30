# Type I enumerator harvest at \(N = 10^7\) (Opus turn 8)

Source: Claude Opus 5 High leftover burn (2026-09-05).
Structured copy: `data/typeI_mordell_1e7.json`.

This is a **measurement**. ESC is unproved. Zero Type I misses among
Mordell primes \(p \le 10^7\) is **not** a full-class cover and is
**not** an algebraic identity. Elsholtz–Tao Prop. 1.6 still forbids a
Type I/II cover of the full classes \(n \equiv 169\) or \(529
\pmod{840}\). Do not promote this table.

No new triples were produced. No search-breaking miss.

Do **not** rebuild `fi2`. Constraints that stayed in force:

- \(y \le 2n/3\)
- \(x = n \cdot a \cdot b \cdot d\)

## Totals

| bound | \(\sum_n f_I(n)\) | \(\sum_p f_I(p)\) | \(c_0\) |
| --- | ---: | ---: | ---: |
| \(N = 10^6\) (turn 7) | 165374532 | 34276274 | \(\approx 0.1456\) |
| \(N = 10^7\) (turn 8) | 2559629008 | 454495120 | \(0.14420\) |

Turn 8 runtime: 1633 s (~27 min), eight slices, one core.

Fit at \(10^7\): \(c_0 = 0.14420\), \(c_1 = 0.496\), observed
\(P / (M \ln^2 M) = 0.17495\). The third decade supports removing
\(\log\log\) only weakly.

## Mordell primes \(p \le 10^7\)

Every prime in each leftover class had \(f_I(p) > 0\) (zero misses).

| residue mod 840 | #primes | hits | misses | min \(f_I\) | max \(f_I\) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 3426 | 3426 | 0 | 12 | 570 |
| 121 | 3431 | 3431 | 0 | 24 | 568 |
| 169 | 3400 | 3400 | 0 | 22 | 560 |
| 289 | 3454 | 3454 | 0 | 28 | 646 |
| 361 | 3391 | 3391 | 0 | 14 | 640 |
| 529 | 3411 | 3411 | 0 | 30 | 656 |
| **total** | **20513** | **20513** | **0** | | |

## Correction: \(f_I(3049)\)

An earlier chat claim that \(f_I(3049) = 0\) was a **truncation
artifact**. True count: \(f_I(3049) = 30\).

3049 remains a miss for the other constructions listed under
\(n \equiv 529\) in `notes/CLOSED.md`. Only the Type I enumerator
count was wrong.
