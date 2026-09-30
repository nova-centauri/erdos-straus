# Type I enumerator harvest at \(N = 2\times 10^7\) (wave 1)

Source: reconstructed `enum/fi2.c` on this machine, 2026-09-06.
Same turn-7 constraints as the Opus \(10^6\) / \(10^7\) harvests.
Structured copy: `data/typeI_mordell_2e7.json`.

This is a **measurement**. ESC is unproved. Zero Type I misses among
Mordell primes \(p \le 2\times 10^7\) is **not** a full-class cover.

## Totals

| bound | \(\sum_n f_I(n)\) | \(\sum_p f_I(p)\) | observed \(P/(M\ln^2 M)\) |
| --- | ---: | ---: | ---: |
| \(N=10^6\) | 165374532 | 34276274 | — |
| \(N=10^7\) | 2559629008 | 454495120 | 0.17495 |
| \(N=2\times 10^7\) | 5772274472 | 982580024 | 0.17384 |

Runtime at \(2\times 10^7\): 2860 s (~48 min), 4 cores.

The \(10^7\) row was recomputed here and matched Opus turn 8 exactly
(`notes/HARVEST-1e7-recomputed.md`). Do not rerun \(10^6\) or \(10^7\).

## Mordell primes \(p \le 2\times 10^7\)

Every prime in each leftover class had \(f_I(p) > 0\) (zero misses).

| residue mod 840 | #primes | hits | misses | min \(f_I\) | max \(f_I\) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 6556 | 6556 | 0 | 12 | 620 |
| 121 | 6594 | 6594 | 0 | 24 | 720 |
| 169 | 6551 | 6551 | 0 | 22 | 764 |
| 289 | 6594 | 6594 | 0 | 28 | 696 |
| 361 | 6556 | 6556 | 0 | 14 | 734 |
| 529 | 6540 | 6540 | 0 | 30 | 738 |
| **total** | **39391** | **39391** | **0** | | |

Class minima are unchanged from \(10^7\) (still realised at the small
checksum primes: \(f_I(2521)=12\), \(f_I(1801)=24\), \(f_I(1009)=22\),
\(f_I(1129)=28\), \(f_I(1201)=14\), \(f_I(3049)=30\)).

## What this wave did not do

- Did not finish \(N=10^8\) (several times the \(2\times 10^7\) cost
  on this box). Pickup: `notes/NEXT.md`.
- Did not invent a covering family.
- Did not claim a Mordell-class cover.
