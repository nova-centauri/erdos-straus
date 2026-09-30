`census.json` is the output of

```bash
PYTHONPATH=. python3 scripts/run_census.py --limit 8000 --hard-limit 30000
```

It is a record of what this solver constructed on this machine, not a
literature bound.

`triples.csv` is the independently verified table from the SuperGrok
Heavy / Claude Opus 5 leftover work (27–29 Aug 2026). Columns:
`n,x,y,z,n_mod_840,notes`. Every row must satisfy
`4xyz − n(xy+xz+yz) = 0`. Check with `make check` or
`erdos-straus check-csv`. Human copy: `notes/TRIPLES.md`. Opus turn 8
added no rows.

`typeI_mordell_1e7.json` is the Opus turn 8 Type I enumerator harvest
at \(N = 10^7\). `typeI_mordell_1e7_recomputed.json` is the same table
from the reconstructed `enum/fi2` on this machine (exact match).
`typeI_mordell_2e7.json` is the wave-1 complete bound \(N=2\times10^7\).
`typeI_mordell_5e7.json` is the wave-2 complete bound \(N=5\times10^7\).
`typeI_mordell_1e8.json` is the wave-3 complete bound \(N=10^8\).
`typeI_mordell_2e8.json` is the wave-4 complete bound \(N=2\times 10^8\).
None of these is a solver census; do not merge them into
`census.json`. Zero misses are a measurement, not a cover.

`first_r_529.json` is the wave-4 shifted-greedy first-R scan of
primes \(n\equiv 529\pmod{840}\) in \([5.70\times 10^8, 8.00\times 10^8)\).
Hits CSV is `first_r_529.csv` (empty this slice). Deepest row:
`first_r_529_deepest.csv`. `first_r_529_from_8e8.json` is the wave-5
scan \([8.00\times 10^8, 8.00\times 10^9)\). Slice checkpoints live
under `data/first_r_slices/`. Not a cover.

`triples.csv` gained six Type I rows in wave 1 (first Mordell prime
\(>10^7\) in each class), twelve in wave 2, six in wave 3
(\(>10^8\)), six in wave 4 (\(>2\times10^8\)), the deepest
\(n\equiv 529\) first-R from the wave-4 scan, and the wave-5
deepest first-R \(3434195209\). Every row must still have residual 0.
