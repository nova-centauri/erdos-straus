# Type I enumerator (`fi2`)

Reconstructed from the Opus turn-7 reductions after the Claude sandbox
was lost. Same constraints as the recorded \(10^6\) / \(10^7\) harvests:

- \(x = n \cdot a \cdot b \cdot d\)
- \(a \le b\), \(y = acd\), \(n/4 < y \le 2n/3\)
- \(\gcd(a,c)=1\)
- \(f_I(n)\) counts both \((x,y,z)\) and \((x,z,y)\) when \(a < b\)

Validated against the workbench checksums:

| \(N\) | \(\sum_n f_I\) | \(\sum_p f_I\) | \(f_I(3049)\) |
| ---: | ---: | ---: | ---: |
| \(10^6\) | 165374532 | 34276274 | 30 |
| \(10^7\) | 2559629008 | 454495120 | 30 |
| \(2\times10^7\) | 5772274472 | 982580024 | 30 |
| \(5\times10^7\) | 16795310188 | 2709141549 | 30 |
| \(10^8\) | 37494215304 | 5818322818 | 30 |
| \(2\times 10^8\) | 83381351012 | 12463112814 | 30 |

This is a measurement tool, not a covering family. Do not rebuild it
from scratch; keep these constraints.

```bash
gcc -O3 -fopenmp -std=c11 -o enum/fi2 enum/fi2.c -lm
OMP_NUM_THREADS=4 ./enum/fi2 1000000
# checkpoint an a-range, then merge dumps
OMP_NUM_THREADS=1 ./enum/fi2 N --a-lo A --a-hi B --dump data/typeI_partial/tag.bin
./enum/fi2 --merge N dump1.bin dump2.bin ...
# N=2e8 checkpoint queue (do not rerun finished dumps)
scripts/n2e8_status.sh
N2E8_WORKER=q1 OMP_NUM_THREADS=1 scripts/run_n2e8_queue.sh
scripts/merge_n2e8.sh
# N=5e8 (not complete unless every n5e8 dump exists)
scripts/n5e8_status.sh
N5E8_WORKER=q1 OMP_NUM_THREADS=1 scripts/run_n5e8_queue.sh
```
