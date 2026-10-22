#!/usr/bin/env bash
# Step 3 of a tool run: run sessions A (4 turns) and B (fresh), then save evidence.
# Usage: sessions.sh <label>
set -euo pipefail
LABEL="${1:?usage: sessions.sh <label>}"
OUT="/out/$LABEL"
P=/scenario/prompts
mkdir -p "$OUT"
cd /work/repo

CL=(claude -p --dangerously-skip-permissions --output-format json)
# MODEL=haiku (etc.) pins the model for every session.
if [ -n "${MODEL:-}" ]; then CL+=(--model "$MODEL"); fi

"${CL[@]}" "$(cat "$P/A1.txt")" > "$OUT/A1.json"
for turn in A2 A3 A4; do
  "${CL[@]}" --continue "$(cat "$P/$turn.txt")" > "$OUT/$turn.json"
done
# VARIANT=erosion adds a fresh "tidy up" session between A and B.
if [ "${VARIANT:-}" = "erosion" ]; then
  "${CL[@]}" "$(cat "$P/C1.txt")" > "$OUT/C1.json"
  git show HEAD:payments/charge.py > "$OUT/charge-after-cleanup.py" 2>/dev/null || true
fi
# PRE_B runs a tool step before session B (e.g. ingest A/C and attach an MCP server).
if [ -n "${PRE_B:-}" ]; then bash -c "$PRE_B" > "$OUT/pre-b.txt" 2>&1 || true; fi
"${CL[@]}" "$(cat "$P/B1.txt")" > "$OUT/B1.json"

git log --stat > "$OUT/git-log.txt"
python3 -m pytest -q > "$OUT/pytest.txt" 2>&1 || true
grep -n -i -E "retry|retries|attempt|backoff" payments/charge.py > "$OUT/retry-check.txt" || true
rm -rf "$OUT/repo" && cp -r /work/repo "$OUT/repo"
echo "sessions done: $LABEL"
