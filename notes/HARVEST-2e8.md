# Type I enumerator harvest at \(N = 2\times 10^8\) (wave 4)

Source: same reconstructed `enum/fi2.c` as the \(10^6\) / \(10^7\) /
\(2\times 10^7\) / \(5\times 10^7\) / \(10^8\) harvests, 2026-09-06.
Checkpointed as a-range dumps and merged. Same turn-7 constraints.
Structured copy: `data/typeI_mordell_2e8.json`.

This is a **measurement**. ESC is unproved. Zero Type I misses among
Mordell primes \(p \le 2\times 10^8\) is **not** a full-class cover.
Elsholtz–Tao Prop. 1.6 still forbids a Type I/II cover of the full
classes \(n \equiv 169\) or \(529 \pmod{840}\).

Do **not** rerun \(10^6\), \(10^7\), \(2\times 10^7\), \(5\times 10^7\),
\(10^8\), or this \(2\times 10^8\) bound.

## Totals

| bound | \(\sum_n f_I(n)\) | \(\sum_p f_I(p)\) | observed \(P/(M\ln^2 M)\) |
| --- | ---: | ---: | ---: |
| \(N=10^6\) | 165374532 | 34276274 | — |
| \(N=10^7\) | 2559629008 | 454495120 | 0.17495 |
| \(N=2\times 10^7\) | 5772274472 | 982580024 | 0.17384 |
| \(N=5\times 10^7\) | 16795310188 | 2709141549 | 0.17241 |
| \(N=10^8\) | 37494215304 | 5818322818 | 0.17147 |
| \(N=2\times 10^8\) | 83381351012 | 12463112814 | 0.17057 |

The ratio column is \(P/(N\ln^2 N)\) with \(N\) the bound (same
convention as the \(10^7\)–\(10^8\) tables). Checksums on the merge:
\(f_I(3049)=30\), \(f_I(2521)=12\), \(f_I(1009)=22\).
\(\pi(2\times 10^8)=11078937\). Shard \(\sum_n\) / \(\sum_p\) add to
the merge totals exactly.

## Mordell primes \(p \le 2\times 10^8\)

Every prime in each leftover class had \(f_I(p) > 0\) (zero misses).

| residue mod 840 | #primes | hits | misses | min \(f_I\) | max \(f_I\) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 57840 | 57840 | 0 | 12 | 1140 |
| 121 | 57631 | 57631 | 0 | 24 | 1274 |
| 169 | 57496 | 57496 | 0 | 22 | 1246 |
| 289 | 57595 | 57595 | 0 | 28 | 1466 |
| 361 | 57492 | 57492 | 0 | 14 | 1390 |
| 529 | 57554 | 57554 | 0 | 30 | 1464 |
| **total** | **345608** | **345608** | **0** | | |

Class minima are unchanged from \(10^7\) (still realised at the small
checksum primes: \(f_I(2521)=12\), \(f_I(1801)=24\), \(f_I(1009)=22\),
\(f_I(1129)=28\), \(f_I(1201)=14\), \(f_I(3049)=30\)).

## How it was run

`Dmax = M/a` with \(M=2N/3=133333333\), so \(a\) runs through \(M\).
Sixteen a-range dumps (gitignored under `data/typeI_partial/`) cover
\([1,M]\) with no gaps. List: `enum/n2e8_shards.tsv`.

| shard | \(a\)-range | shard \(\sum_n f_I\) | shard seconds |
| ---: | --- | ---: | ---: |
| N2e8_s0 | 1–23 | 28394398410 | 505 |
| N2e8_s1 | 24–511 | 19328365258 | 551 |
| N2e8_s2 | 512–11547 | 16199159952 | 624 |
| N2e8_s3 | 11548–260991 | 11250882630 | 12847 |
| N2e8_a260992 | 260992–330000 | 649394018 | 5271 |
| N2e8_a330001 | 330001–400000 | 511841984 | 5933 |
| N2e8_a400001 | 400001–470000 | 414744764 | 6464 |
| N2e8_a470001 | 470001–520833 | 257689920 | 4992 |
| N2e8_a520834 | 520834–1200000 | 1899465986 | 3968 |
| N2e8_a1200001 | 1200001–3000000 | 1691313208 | 5288 |
| N2e8_a3000001 | 3000001–5899053 | 987270300 | 4522 |
| N2e8_a5899054 | 5899054–12000000 | 811967614 | 5696 |
| N2e8_a12000001 | 12000001–25000000 | 617093902 | 6478 |
| N2e8_a25000001 | 25000001–50000000 | 345706016 | 6444 |
| N2e8_a50000001 | 50000001–85000000 | 21209746 | 4574 |
| N2e8_a85000001 | 85000001–133333333 | 847304 | 4854 |

```bash
scripts/merge_n2e8.sh
```

Same factoring path as the \(10^8\) harvest (trial to
\(p\le 4000\), then Miller–Rabin / Pollard). Not an enumerator rebuild.

## What this wave did not do

- Did not invent a covering family.
- Did not claim a Mordell-class cover.
- Did not rerun any finished smaller bound.
