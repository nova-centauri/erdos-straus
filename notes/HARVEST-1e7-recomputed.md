# Type I harvest at \(N=10^7\) recomputed (wave 1)

The reconstructed `enum/fi2.c` (turn-7 constraints, not a redesign)
was run on this machine on 2026-09-06 and **matched the Opus turn-8
table bit-for-bit**:

| | Opus turn 8 | this machine |
| --- | ---: | ---: |
| \(\sum_n f_I\) | 2559629008 | 2559629008 |
| \(\sum_p f_I\) | 454495120 | 454495120 |
| Mordell primes / hits / misses | 20513 / 20513 / 0 | 20513 / 20513 / 0 |
| min/max \(f_I\) per class | 12–656 as recorded | identical |
| \(f_I(3049)\) | 30 | 30 |

Runtime here: 799 s, 4 cores. JSON:
`data/typeI_mordell_1e7_recomputed.json`.

This confirms the enumerator, not a cover. Do not rerun \(10^7\).
