#!/usr/bin/env bash
# Poll 5e8 shards. When every dump exists, merge and record notes.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PARTIAL="$ROOT/data/typeI_partial"

while true; do
  status="$("$ROOT/scripts/n5e8_status.sh")"
  echo "$status" | tee -a "$PARTIAL/watch5e8.log"
  miss="$(printf '%s\n' "$status" | awk '/^MISS/{c++} END{print c+0}')"
  run="$(printf '%s\n' "$status" | awk '/^RUN/{c++} END{print c+0}')"
  done_n="$(printf '%s\n' "$status" | awk '/^DONE/{c++} END{print c+0}')"
  echo "$(date -u +%FT%TZ) watch5e8 done=$done_n run=$run miss=$miss" | tee -a "$PARTIAL/watch5e8.log"

  expect="$(awk '!/^#/ && NF{c++} END{print c+0}' "$ROOT/enum/n5e8_shards.tsv")"
  if [[ "$miss" -eq 0 && "$run" -eq 0 && "$done_n" -eq "$expect" ]]; then
    echo "$(date -u +%FT%TZ) all dumps present; merging" | tee -a "$PARTIAL/watch5e8.log"
    "$ROOT/scripts/merge_n5e8.sh" | tee "$PARTIAL/merge5e8.out"
    echo MERGE_OK >"$PARTIAL/merge5e8.done"
    python3 "$ROOT/scripts/record_n5e8_harvest.py" | tee -a "$PARTIAL/watch5e8.log"
    echo RECORD_OK >"$PARTIAL/record5e8.done"
    echo "$(date -u +%FT%TZ) record done; running make check" | tee -a "$PARTIAL/watch5e8.log"
    make -C "$ROOT" check | tee -a "$PARTIAL/watch5e8.log"
    echo CHECK_OK >"$PARTIAL/check5e8.done"
    cd "$ROOT"
    git add \
      notes/HARVEST-5e8.md notes/HARVEST-partial-5e8.md notes/NEXT.md notes/CLOSED.md \
      data/typeI_mordell_5e8.json data/README.md \
      tests/test_typeI_harvest.py README.md CONVENTIONS.md enum/README.md \
      scripts/watch_n5e8.sh
    if ! git diff --cached --quiet; then
      git commit -m "$(cat <<'EOF'
Record the complete Type I census at N=5e8.

Same fi2 a-range merge. f_I(3049)=30 on the finished dumps.
Measurement, not a cover. Do not rerun this bound.
EOF
)"
      git push -u origin main
    fi
    echo "$(date -u +%FT%TZ) harvest committed" | tee -a "$PARTIAL/watch5e8.log"
    exit 0
  fi
  sleep 90
done
