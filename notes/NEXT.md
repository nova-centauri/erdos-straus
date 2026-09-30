# Next leftover spend

The Type I harvest at \(N = 2\times 10^8\) is **done**. Do **not**
rerun \(10^6\), \(10^7\), \(2\times 10^7\), \(5\times 10^7\),
\(10^8\), or \(2\times 10^8\).

Wave 6 is finishing Type I at \(N=5\times 10^8\) on the same `enum/fi2`.
**9/15 dumps exist. Do not merge yet.** Last status 2026-09-08 05:41 UTC:

- **done (do not rerun):** s0, s1, s2, s3a, s3b, s3c, s3d, a480751, a750001
- **running (do not kill):** `N5e8_a1050001` (\(a\approx 1189265\) of 1050001–1302083, last AP),
  `N5e8_a1302084` (\(a\approx 2063940\) of 1302084–4000000, first trial)
- **still missing:** a4000001, a12660001, a40000001, a120000001

Keep two `OMP_NUM_THREADS=1` workers (`tmux` `fi2-n5e8-q1` / `q2`).
`scripts/watch_n5e8.sh` will merge, record, `make check`, and commit
once all 15 `FI2A` dumps are 2000000032 bytes. Pickup:

```bash
scripts/n5e8_status.sh
N5E8_WORKER=q1 OMP_NUM_THREADS=1 scripts/run_n5e8_queue.sh
# only when 15/15 dumps exist:
scripts/merge_n5e8.sh
python3 scripts/record_n5e8_harvest.py
make check
```

Expect \(f_I(3049)=30\) on the finished merge. See
`notes/HARVEST-partial-5e8.md`. Not a cover.

The 529 first-R scan through \(8.00\times 10^9\) is **done**
(no first-R \(\ge 108\); max 83 at \(3434195209\)). Continue from
\(8.00\times 10^9\) only after a complete 5e8, and only as a
secondary burn. Not a cover.

**Do not do this:** rebuild `fi2`; invent a covering family; claim a
Type I/II full-class cover; try to prove ESC; reopen
`notes/CLOSED.md`; spend a fresh Anthropic week; use Fable; rerun
any finished Type I bound.

## Recorded complete totals (do not harvest again)

| \(N\) | \(\sum_n f_I\) | \(\sum_p f_I\) |
| ---: | ---: | ---: |
| \(10^6\) | 165374532 | 34276274 |
| \(10^7\) | 2559629008 | 454495120 |
| \(2\times 10^7\) | 5772274472 | 982580024 |
| \(5\times 10^7\) | 16795310188 | 2709141549 |
| \(10^8\) | 37494215304 | 5818322818 |
| \(2\times 10^8\) | 83381351012 | 12463112814 |

Keep \(y\le 2n/3\), \(x=n\cdot a\cdot b\cdot d\), \(a\le b\),
\(\gcd(a,c)=1\).
