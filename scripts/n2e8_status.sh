#!/usr/bin/env bash
# Print 2e8 Type I shard status (complete / running / missing).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXPECT_BYTES=800000032
PARTIAL="$ROOT/data/typeI_partial"
done_n=0
run_n=0
miss_n=0
while read -r name lo hi; do
  [[ -z "${name}" || "${name}" == \#* ]] && continue
  bin="$PARTIAL/${name}.bin"
  lock="$PARTIAL/locks/${name}"
  if [[ -f "$bin" && "$(stat -c%s "$bin" 2>/dev/null || echo 0)" -eq "$EXPECT_BYTES" ]]; then
    echo "DONE  $name  a=$lo..$hi"
    done_n=$((done_n + 1))
  elif [[ -d "$lock" ]] && kill -0 "$(cat "$lock/pid" 2>/dev/null)" 2>/dev/null; then
    last="$(grep -E '^a=' "$PARTIAL/${name}.log" 2>/dev/null | tail -1 || true)"
    echo "RUN   $name  a=$lo..$hi  ${last}"
    run_n=$((run_n + 1))
  else
    echo "MISS  $name  a=$lo..$hi"
    miss_n=$((miss_n + 1))
  fi
done <"$ROOT/enum/n2e8_shards.tsv"
echo "--- $done_n done / $run_n running / $miss_n missing ---"
