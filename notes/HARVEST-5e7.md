# Type I enumerator harvest at \(N = 5\times 10^7\) (wave 2)

Source: same reconstructed `enum/fi2.c` as the \(10^6\) / \(10^7\) /
\(2\times 10^7\) harvests, 2026-09-06. Checkpointed as a-range dumps
and merged. Same turn-7 constraints. Structured copy:
`data/typeI_mordell_5e7.json`.

This is a **measurement**. ESC is unproved. Zero Type I misses among
Mordell primes \(p \le 5\times 10^7\) is **not** a full-class cover.
Elsholtz–Tao Prop. 1.6 still forbids a Type I/II cover of the full
classes \(n \equiv 169\) or \(529 \pmod{840}\).

Do **not** rerun \(10^6\), \(10^7\), \(2\times 10^7\), or this
\(5\times 10^7\) bound.

## Totals

| bound | \(\sum_n f_I(n)\) | \(\sum_p f_I(p)\) | observed \(P/(M\ln^2 M)\) |
| --- | ---: | ---: | ---: |
| \(N=10^6\) | 165374532 | 34276274 | — |
| \(N=10^7\) | 2559629008 | 454495120 | 0.17495 |
| \(N=2\times 10^7\) | 5772274472 | 982580024 | 0.17384 |
| \(N=5\times 10^7\) | 16795310188 | 2709141549 | 0.17241 |

Checksums on the merge: \(f_I(3049)=30\), \(f_I(2521)=12\),
\(f_I(1009)=22\). \(\pi(5\times 10^7)=3001134\).

## Mordell primes \(p \le 5\times 10^7\)

Every prime in each leftover class had \(f_I(p) > 0\) (zero misses).

| residue mod 840 | #primes | hits | misses | min \(f_I\) | max \(f_I\) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 15668 | 15668 | 0 | 12 | 934 |
| 121 | 15575 | 15575 | 0 | 24 | 862 |
| 169 | 15539 | 15539 | 0 | 22 | 882 |
| 289 | 15558 | 15558 | 0 | 28 | 924 |
| 361 | 15558 | 15558 | 0 | 14 | 910 |
| 529 | 15559 | 15559 | 0 | 30 | 1114 |
| **total** | **93457** | **93457** | **0** | | |

Class minima are unchanged from \(10^7\) (still realised at the small
checksum primes: \(f_I(2521)=12\), \(f_I(1801)=24\), \(f_I(1009)=22\),
\(f_I(1129)=28\), \(f_I(1201)=14\), \(f_I(3049)=30\)).

## How it was run

`Dmax = M/a` with \(M=2N/3=33333333\), so \(a\) runs through \(M\).
Seven a-range dumps (gitignored under `data/typeI_partial/`) cover
\([1,M]\) with no gaps:

| shard | \(a\)-range | shard \(\sum_n f_I\) | shard seconds |
| ---: | --- | ---: | ---: |
| s0 | 1–79 | 7867999366 | 79 |
| s1 | 80–5799 | 5077334548 | 111 |
| s2a | 5800–50400 | 1761168182 | 453 |
| s2b | 50401–439999 | 1220265514 | 2053 |
| s3a | 440000–3832000 | 688281274 | 1717 |
| s3b | 3832001–13400000 | 176451358 | 1308 |
| s3c | 13400001–33333333 | 3809946 | 1127 |

```bash
./enum/fi2 --merge 50000000 data/typeI_partial/N5e7_s{0,1,2a,2b,3a,3b,3c}.bin
```

The small-`Dmax` path stops trial division at \(p\le 4000\) and
finishes with Miller–Rabin / Pollard Rho. Same factors as full trial
division; \(N=10^4\) checksum still \(537076\) / \(165361\). That is
a factoring speedup, not an enumerator rebuild.

## What this wave did not do

- Did not finish \(N=10^8\) in the same sitting (shards started; see
  `notes/HARVEST-partial-1e8.md` / `notes/NEXT.md`).
- Did not invent a covering family.
- Did not claim a Mordell-class cover.
