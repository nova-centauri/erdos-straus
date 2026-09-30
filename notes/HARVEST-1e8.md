# Type I enumerator harvest at \(N = 10^8\) (wave 3)

Source: same reconstructed `enum/fi2.c` as the \(10^6\) / \(10^7\) /
\(2\times 10^7\) / \(5\times 10^7\) harvests, 2026-09-06. Checkpointed
as a-range dumps and merged. Same turn-7 constraints. Structured copy:
`data/typeI_mordell_1e8.json`.

This is a **measurement**. ESC is unproved. Zero Type I misses among
Mordell primes \(p \le 10^8\) is **not** a full-class cover.
Elsholtz–Tao Prop. 1.6 still forbids a Type I/II cover of the full
classes \(n \equiv 169\) or \(529 \pmod{840}\).

Do **not** rerun \(10^6\), \(10^7\), \(2\times 10^7\), \(5\times 10^7\),
or this \(10^8\) bound.

## Totals

| bound | \(\sum_n f_I(n)\) | \(\sum_p f_I(p)\) | observed \(P/(M\ln^2 M)\) |
| --- | ---: | ---: | ---: |
| \(N=10^6\) | 165374532 | 34276274 | — |
| \(N=10^7\) | 2559629008 | 454495120 | 0.17495 |
| \(N=2\times 10^7\) | 5772274472 | 982580024 | 0.17384 |
| \(N=5\times 10^7\) | 16795310188 | 2709141549 | 0.17241 |
| \(N=10^8\) | 37494215304 | 5818322818 | 0.17147 |

Checksums on the merge: \(f_I(3049)=30\), \(f_I(2521)=12\),
\(f_I(1009)=22\). \(\pi(10^8)=5761455\). Shard \(\sum_n\) / \(\sum_p\)
add to the merge totals exactly.

## Mordell primes \(p \le 10^8\)

Every prime in each leftover class had \(f_I(p) > 0\) (zero misses).

| residue mod 840 | #primes | hits | misses | min \(f_I\) | max \(f_I\) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 30061 | 30061 | 0 | 12 | 934 |
| 121 | 29900 | 29900 | 0 | 24 | 1078 |
| 169 | 29898 | 29898 | 0 | 22 | 1080 |
| 289 | 29907 | 29907 | 0 | 28 | 1102 |
| 361 | 29828 | 29828 | 0 | 14 | 1148 |
| 529 | 29874 | 29874 | 0 | 30 | 1358 |
| **total** | **179468** | **179468** | **0** | | |

Class minima are unchanged from \(10^7\) (still realised at the small
checksum primes: \(f_I(2521)=12\), \(f_I(1801)=24\), \(f_I(1009)=22\),
\(f_I(1129)=28\), \(f_I(1201)=14\), \(f_I(3049)=30\)).

## How it was run

`Dmax = M/a` with \(M=2N/3=66666666\), so \(a\) runs through \(M\).
Five a-range dumps (gitignored under `data/typeI_partial/`) cover
\([1,M]\) with no gaps. s0 and s1 finished in wave 2; s2 / s3a / s3b
finished in wave 3.

| shard | \(a\)-range | shard \(\sum_n f_I\) | shard seconds |
| ---: | --- | ---: | ---: |
| s0 | 1–90 | 17269536640 | 209 |
| s1 | 91–8164 | 11545317908 | 271 |
| s2 | 8165–737424 | 6716856322 | 8712 |
| s3a | 737425–7010000 | 1552262340 | 4646 |
| s3b | 7010001–66666666 | 410242094 | 6760 |

```bash
./enum/fi2 --merge 100000000 \
  data/typeI_partial/N1e8_s{0,1,2,3a,3b}.bin
```

Same factoring path as the \(5\times 10^7\) harvest (trial to
\(p\le 4000\), then Miller–Rabin / Pollard). Not an enumerator rebuild.

## What this wave did not do

- Did not invent a covering family.
- Did not claim a Mordell-class cover.
- Did not rerun any finished smaller bound.
