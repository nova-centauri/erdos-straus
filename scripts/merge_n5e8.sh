#!/usr/bin/env bash
# Merge every 5e8 Type I dump listed in enum/n5e8_shards.tsv.
# Refuses to run if any dump is missing or the wrong size.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
N=500000000
EXPECT_BYTES=2000000032
PARTIAL="$ROOT/data/typeI_partial"
OUT="${1:-$ROOT/data/typeI_mordell_5e8.json}"
FI2="$ROOT/enum/fi2"

dumps=()
while read -r name lo hi; do
  [[ -z "${name}" || "${name}" == \#* ]] && continue
  bin="$PARTIAL/${name}.bin"
  if [[ ! -f "$bin" || "$(stat -c%s "$bin")" -ne "$EXPECT_BYTES" ]]; then
    echo "missing or short dump: $bin (need $EXPECT_BYTES)" >&2
    exit 1
  fi
  dumps+=("$bin")
done <"$ROOT/enum/n5e8_shards.tsv"

echo "checksumming ${#dumps[@]} dumps" >&2
python3 - "$N" "${dumps[@]}" <<'PY'
import struct, sys
N = int(sys.argv[1])
want = {1009: 22, 2521: 12, 3049: 30}
got = {n: 0 for n in want}

def fi_at(path, n):
    with open(path, "rb") as f:
        mag = f.read(4)
        if mag != b"FI2A":
            raise SystemExit(f"bad magic {path}")
        f.seek(28 + n * 4)
        return struct.unpack("<I", f.read(4))[0]

for path in sys.argv[2:]:
    for n in want:
        got[n] += fi_at(path, n)
for n, w in want.items():
    print(f"f_I({n})={got[n]} (want {w})", flush=True)
    if got[n] != w:
        raise SystemExit(f"checksum fail f_I({n})")
print("checksums ok", flush=True)
PY

echo "merging ${#dumps[@]} dumps -> $OUT" >&2
"$FI2" --merge "$N" "${dumps[@]}" >"$OUT"
echo "wrote $OUT" >&2
python3 - "$OUT" <<'PY'
import json, math, sys
p = sys.argv[1]
d = json.load(open(p))
assert d["N"] == 500000000
assert d["cover_claimed"] is False
assert d["esc_proved"] is False
assert d["mordell_primes"]["zero_misses_is_not_a_cover"] is True
assert d["sums"]["primes"] == 26355867
N = 500000000
P = d["sums"]["f_I_p"]
ratio = P / (N * (math.log(N) ** 2))
print(f"f_I_n={d['sums']['f_I_n']} f_I_p={P} primes={d['sums']['primes']}")
print(f"mordell totals={d['mordell_primes']['totals']}")
print(f"P/(N ln^2 N)={ratio:.5f}")
PY
