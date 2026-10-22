#!/usr/bin/env bash
# brain0 step before session B: index git (facts) + Claude Code transcripts (intents),
# then attach brain0's MCP server so session B's agent can query it, per the README.
set -x
export PATH="$HOME/.npm-global/bin:$PATH"
cd /work/repo
D="$HOME/b0"
B0=(--db "$D/index.db" --payload "$D/payload" --key-file "$D/keyring.key")
mkdir -p "$D"
brain0 ingest --repo demo/payments "${B0[@]}"
brain0 observe --repo demo/payments "${B0[@]}"
brain0 report --repo demo/payments --db "$D/index.db" --md
claude mcp add brain0 -- "$HOME/.npm-global/bin/brain0" mcp --db "$D/index.db" --repo demo/payments
claude mcp list
