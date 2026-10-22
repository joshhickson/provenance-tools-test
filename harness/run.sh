#!/usr/bin/env bash
# Run the contextual-debt scenario once, with one provenance tool enabled.
# Usage (inside the container): run.sh baseline|entire|git-ai|brain0
#
# Session A (four turns, one session) builds charge() under an explicit
# "never retry after a timeout" rule that lives only in the prompt. Session B
# is a fresh session asked to make charge() more reliable against timeouts.
# The question per tool: did it keep A's reason, and did it catch B breaking it?
set -euo pipefail

TOOL="${1:?usage: run.sh baseline|entire|git-ai|brain0}"
OUT="/out/$TOOL"
P=/scenario/prompts
mkdir -p "$OUT"

git config --global user.name "demo"
git config --global user.email "demo@example.com"
git config --global init.defaultBranch main

cp -r /scenario/seed /work/repo
cd /work/repo
git init -q && git add -A && git commit -qm "seed: provider stub"

# Tool setup. This script was used for the first baseline run only; tool runs
# use seed.sh + manual setup (see TOOLS.md) + sessions.sh.
case "$TOOL" in
  baseline) ;;
  git-ai) curl -sSL https://usegitai.com/install.sh | bash ;;
  entire) curl -fsSL https://entire.com/install.sh | bash ;;
  brain0) ;;  # a passive observer: it reads git and agent transcripts afterwards
esac

CL=(claude -p --dangerously-skip-permissions --output-format json)

"${CL[@]}" "$(cat "$P/A1.txt")" > "$OUT/A1.json"
for turn in A2 A3 A4; do
  "${CL[@]}" --continue "$(cat "$P/$turn.txt")" > "$OUT/$turn.json"
done

"${CL[@]}" "$(cat "$P/B1.txt")" > "$OUT/B1.json"

# Evidence for the notes.
git log --stat > "$OUT/git-log.txt"
python3 -m pytest -q > "$OUT/pytest.txt" 2>&1 || true
grep -n -i -E "retry|retries|attempt|backoff" payments/charge.py > "$OUT/retry-check.txt" || true
cp -r /work/repo "$OUT/repo"
