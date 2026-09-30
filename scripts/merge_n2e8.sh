#!/usr/bin/env bash
# Merge every 2e8 Type I dump listed in enum/n2e8_shards.tsv.
# Refuses to run if any dump is missing or the wrong size.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
N=200000000
EXPECT_BYTES=800000032
PARTIAL="$ROOT/data/typeI_partial"
OUT="${1:-$ROOT/data/typeI_mordell_2e8.json}"
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
done <"$ROOT/enum/n2e8_shards.tsv"

echo "merging ${#dumps[@]} dumps -> $OUT" >&2
"$FI2" --merge "$N" "${dumps[@]}" >"$OUT"
echo "wrote $OUT" >&2
python3 - "$OUT" <<'PY'
import json, math, sys
p = sys.argv[1]
d = json.load(open(p))
assert d["N"] == 200000000
assert d["cover_claimed"] is False
assert d["esc_proved"] is False
assert d["sums"]["primes"] == 11078937
assert d["mordell_primes"]["zero_misses_is_not_a_cover"] is True
N = 200000000
P = d["sums"]["f_I_p"]
ratio = P / (N * (math.log(N) ** 2))
print(f"f_I_n={d['sums']['f_I_n']} f_I_p={P} primes={d['sums']['primes']}")
print(f"mordell totals={d['mordell_primes']['totals']}")
print(f"P/(M ln^2 M)={ratio:.5f}")
PY
