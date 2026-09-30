# first-R scan on \(n \equiv 529 \pmod{840}\) (wave 4)

Durable replacement for the SuperGrok Heavy first-R bites. Helper:
`erdos_straus/first_r.py`, CLI `scripts/scan_first_r.py`. first-R is
the shifted-greedy remainder numerator \(4t+3\) at the first \(t\)
that splits. Published checksums: \(8803369\to 107\),
\(287567281\to 83\), \(794037841\to 63\), \(496609\to 51\).

This is a **search log**, not a class cover. Bounded shifted-greedy
cannot finish a Mordell class (`notes/CLOSED.md`). Elsholtz–Tao
Prop. 1.6 still forbids a Type I/II cover of the full class
\(n\equiv 529\pmod{840}\).

## Wave 4 slice

Resume after Heavy’s closed frontier \(5.70\times 10^8\).

| field | value |
| --- | ---: |
| range | \([5.70\times 10^8,\ 8.00\times 10^8)\) |
| primes scanned | 58958 |
| \(t_{\max}\) | 40 (detects first-R \(\le 163\)) |
| hits with first-R \(\ge 108\) | 0 |
| unresolved (\(t>40\)) | 0 |
| max first-R | 63 at \(n=586775809\) |

JSON: `data/first_r_529.json`. Hits CSV (empty this slice):
`data/first_r_529.csv`. Deepest row:
`data/first_r_529_deepest.csv`. The deepest triple is also in
`data/triples.csv` (residual 0).

```bash
PYTHONPATH=. python3 scripts/scan_first_r.py \
  --start 800000000 --stop 900000000 \
  --csv data/first_r_529.csv --json data/first_r_529.json
```

Raise `--start` to the last `stop` to continue. Do not claim a
first-R bound is a cover.

## Wave 5 slice

Resume at \(8.00\times 10^8\). Checkpointed 300 M–1 G chunks in
`data/first_r_slices/`, merged by `scripts/merge_first_r_slices.py`.

| field | value |
| --- | ---: |
| range | \([8.00\times 10^8,\ 8.00\times 10^9)\) |
| primes scanned | 1700954 |
| \(t_{\max}\) | 40 (detects first-R \(\le 163\)) |
| hits with first-R \(\ge 108\) | 0 |
| unresolved (\(t>40\)) | 0 |
| max first-R | 83 at \(n=3434195209\) |

JSON: `data/first_r_529_from_8e8.json`. Hits CSV (empty this slice):
`data/first_r_529_from_8e8.csv`. Deepest row:
`data/first_r_529_from_8e8_deepest.csv`. The deepest triple is also in
`data/triples.csv` (residual 0).

```bash
PYTHONPATH=. python3 scripts/scan_first_r.py \
  --start 8000000000 --stop 9000000000 \
  --csv data/first_r_slices/4000_5000.csv \
  --json data/first_r_slices/4000_5000.json
PYTHONPATH=. python3 scripts/merge_first_r_slices.py data/first_r_slices/*.json
```

Still a search, not a cover. Continue from the last `stop`.
