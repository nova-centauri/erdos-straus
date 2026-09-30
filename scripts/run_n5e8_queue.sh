#!/usr/bin/env bash
# Claim-and-run 5e8 Type I a-range dumps. Same fi2. Do not rebuild.
# Do not rerun N<=2e8. Do not merge until every TSV dump exists.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
N=500000000
EXPECT_BYTES=2000000032
SHARDS="$ROOT/enum/n5e8_shards.tsv"
PARTIAL="$ROOT/data/typeI_partial"
LOCKS="$PARTIAL/locks"
FI2="$ROOT/enum/fi2"
WORKER="${N5E8_WORKER:-$(hostname)-$$}"

mkdir -p "$PARTIAL" "$LOCKS"

dump_ok() {
  local bin="$1"
  [[ -f "$bin" && "$(stat -c%s "$bin")" -eq "$EXPECT_BYTES" ]] || return 1
  [[ "$(head -c 4 "$bin")" == "FI2A" ]]
}

claim() {
  local name="$1" lock="$LOCKS/$name"
  if mkdir "$lock" 2>/dev/null; then
    echo "$$" >"$lock/pid"
    echo "$WORKER" >"$lock/worker"
    date -u +%FT%TZ >"$lock/claimed_at"
    return 0
  fi
  local old
  old="$(cat "$lock/pid" 2>/dev/null || true)"
  if [[ -n "${old}" ]] && ! kill -0 "$old" 2>/dev/null; then
    rm -rf "$lock"
    if mkdir "$lock" 2>/dev/null; then
      echo "$$" >"$lock/pid"
      echo "$WORKER" >"$lock/worker"
      date -u +%FT%TZ >"$lock/claimed_at"
      echo "stole stale lock $name (dead pid $old)" >&2
      return 0
    fi
  fi
  return 1
}

release() {
  rm -rf "$LOCKS/$1"
}

while true; do
  claimed=""
  while read -r name lo hi; do
    [[ -z "${name}" || "${name}" == \#* ]] && continue
    bin="$PARTIAL/${name}.bin"
    if dump_ok "$bin"; then
      continue
    fi
    if claim "$name"; then
      claimed="$name $lo $hi"
      break
    fi
  done <"$SHARDS"

  if [[ -z "${claimed}" ]]; then
    echo "$(date -u +%FT%TZ) $WORKER idle (no claimable shards)"
    exit 0
  fi

  set -- $claimed
  name="$1" lo="$2" hi="$3"
  bin="$PARTIAL/${name}.bin"
  log="$PARTIAL/${name}.log"
  json="$PARTIAL/${name}.json"
  echo "$(date -u +%FT%TZ) $WORKER start $name a=$lo..$hi"
  rm -f "$bin" "$PARTIAL/${name}.done"
  set +e
  OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}" "$FI2" "$N" --a-lo "$lo" --a-hi "$hi" \
    --dump "$bin" >"$json" 2>"$log"
  rc=$?
  set -e
  if [[ $rc -eq 0 ]] && dump_ok "$bin"; then
    echo DONE >"$PARTIAL/${name}.done"
    echo "$(date -u +%FT%TZ) $WORKER done $name rc=0"
    release "$name"
  else
    echo "$(date -u +%FT%TZ) $WORKER FAIL $name rc=$rc" >&2
    rm -f "$bin" "$PARTIAL/${name}.done"
    release "$name"
    exit "$rc"
  fi
done
