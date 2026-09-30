# Type I census toward \(10^8\) — complete (wave 3)

The \(N=10^8\) harvest is **done**. See `notes/HARVEST-1e8.md` and
`data/typeI_mordell_1e8.json`.

Do **not** rerun \(N=10^6\), \(10^7\), \(2\times 10^7\),
\(5\times 10^7\), or \(10^8\).

Pickup if someone still has the gitignored dumps:

```bash
./enum/fi2 --merge 100000000 \
  data/typeI_partial/N1e8_s{0,1,2,3a,3b}.bin
```

Zero misses through \(10^8\) stay a measurement, not a cover.
