#!/usr/bin/env bash
# Poll 2e8 shards. When s3 finishes, start a fourth queue worker.
# When every dump exists, merge. Does not rebuild fi2.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PARTIAL="$ROOT/data/typeI_partial"
tmuxc() { tmux -f /exec-daemon/tmux.portal.conf "$@"; }

started_q4=0
while true; do
  status="$("$ROOT/scripts/n2e8_status.sh")"
  echo "$status" | tee -a "$PARTIAL/watch.log"
  miss="$(printf '%s\n' "$status" | awk '/^MISS/{c++} END{print c+0}')"
  run="$(printf '%s\n' "$status" | awk '/^RUN/{c++} END{print c+0}')"
  done_n="$(printf '%s\n' "$status" | awk '/^DONE/{c++} END{print c+0}')"
  echo "$(date -u +%FT%TZ) watch done=$done_n run=$run miss=$miss" | tee -a "$PARTIAL/watch.log"

  if [[ $started_q4 -eq 0 && -f "$PARTIAL/N2e8_s3.bin" && "$(stat -c%s "$PARTIAL/N2e8_s3.bin")" -eq 800000032 ]]; then
    if ! pgrep -f 'N2E8_WORKER=q4' >/dev/null 2>&1; then
      echo "$(date -u +%FT%TZ) starting q4 after s3 dump" | tee -a "$PARTIAL/watch.log"
      tmuxc has-session -t fi2-n2e8-q4 2>/dev/null || \
        tmuxc new-session -d -s fi2-n2e8-q4 -c "$ROOT" -- \
          bash -lc 'N2E8_WORKER=q4 OMP_NUM_THREADS=1 /workspace/scripts/run_n2e8_queue.sh; echo exit $? $(date -u +%FT%TZ)'
      started_q4=1
    fi
  fi

  if [[ "$miss" -eq 0 && "$run" -eq 0 && "$done_n" -ge 16 ]]; then
    echo "$(date -u +%FT%TZ) all dumps present; merging" | tee -a "$PARTIAL/watch.log"
    "$ROOT/scripts/merge_n2e8.sh" | tee "$PARTIAL/merge.out"
    echo MERGE_OK >"$PARTIAL/merge.done"
    echo "$(date -u +%FT%TZ) merge done; recording notes" | tee -a "$PARTIAL/watch.log"
    python3 "$ROOT/scripts/record_n2e8_harvest.py" | tee -a "$PARTIAL/watch.log"
    echo RECORD_OK >"$PARTIAL/record.done"
    exit 0
  fi
  sleep 90
done
