# Type I census toward \(5\times 10^8\) (wave 6)

Do **not** rerun \(N\le 2\times 10^8\). Same `enum/fi2`, a-range dumps,
\(M=333333333\). **Not** a rebuild. Not a cover. **Not complete**
until every row in `enum/n5e8_shards.tsv` exists and is merged to
`data/typeI_mordell_5e8.json`.

Dump size 2000000032 bytes (`FI2A`). Keep `OMP_NUM_THREADS=1`: a
thread-local `fi[]` is 2 GB. Two concurrent shards are a tight fit
on 15 GB. Do not start a third worker. Do not kill running shards.

Queued AP/trial ranges after s3a were split for checkpointing.
Do not merge until all **15** dumps exist.

## Shards

| shard | a-range | dump | status |
| ---: | --- | --- | --- |
| s0 | 1–26 | `N5e8_s0.bin` | **done** (1105 s). \(\sum_n=79173640702\), \(\sum_p=11037096824\) |
| s1 | 27–693 | `N5e8_s1.bin` | **done** (1336 s). \(\sum_n=56433906740\), \(\sum_p=8244613458\) |
| s2 | 694–18257 | `N5e8_s2.bin` | **done** (1574 s). \(\sum_n=46694941602\), \(\sum_p=6759379194\) |
| s3a | 18258–120000 | `N5e8_s3a.bin` | **done** (5259 s). \(\sum_n=20419549980\), \(\sum_p=2942297628\) |
| s3b | 120001–240000 | `N5e8_s3b.bin` | **done** (9304 s). \(\sum_n=6340363512\), \(\sum_p=910338388\) |
| s3c | 240001–360000 | `N5e8_s3c.bin` | **done** (11890 s). \(\sum_n=3416206734\), \(\sum_p=489511530\) |
| s3d | 360001–480750 | `N5e8_s3d.bin` | **done** (14029 s). \(\sum_n=2305484634\), \(\sum_p=329877528\) |
| a480751 | 480751–750000 | `N5e8_a480751.bin` | **done** (37553 s). \(\sum_n=3331516924\), \(\sum_p=475782326\) |
| a750001 | 750001–1050000 | `N5e8_a750001.bin` | **done** (50259 s). \(\sum_n=2349192464\), \(\sum_p=334692964\) |
| a1050001 | 1050001–1302083 | `N5e8_a1050001.bin` | running |
| a1302084 | 1302084–4000000 | `N5e8_a1302084.bin` | running |
| a4000001 | 4000001–12660000 | `N5e8_a4000001.bin` | queue |
| a12660001 | 12660001–40000000 | `N5e8_a12660001.bin` | queue |
| a40000001 | 40000001–120000000 | `N5e8_a40000001.bin` | queue |
| a120000001 | 120000001–333333333 | `N5e8_a120000001.bin` | queue |

s0+s1+s2 already sum to \(f_I(3049)=30\), \(f_I(2521)=12\),
\(f_I(1009)=22\). Later shards add 0 to those small \(n\). The
finished merge must still show those checksums.

```bash
scripts/n5e8_status.sh
N5E8_WORKER=q1 OMP_NUM_THREADS=1 scripts/run_n5e8_queue.sh
# only after status is 15 done / 0 running / 0 missing:
scripts/merge_n5e8.sh
python3 scripts/record_n5e8_harvest.py
make check
```

Zero misses, if any, stay a measurement, not a cover.
