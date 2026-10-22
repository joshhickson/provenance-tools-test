# Tool setup, exactly as run (inside each container, after `seed.sh`)

All commands run as the non-root `tester` user in `/work/repo`. Nothing was installed on the host.

## Entire CLI 0.12.0

```bash
curl -fsSL https://entire.com/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
entire enable --agent claude-code --telemetry=false --absolute-git-hook-path
# → 10 Claude Code hooks (.claude/settings.json), git hooks: commit-msg, post-commit,
#   post-rewrite, pre-push, prepare-commit-msg; config in .entire/settings.json
```

Then `sessions.sh` with `PATH` including `~/.local/bin`. Why check:

```bash
git checkout -q <commit before B>          # the cleanup commit
entire why payments/charge.py:<line of the bare `raise` in except ProviderTimeout>
entire checkpoint explain <checkpoint id from the line above>
git checkout -q main
```

Notes: `entire checkpoint search` needs an `origin` remote and `entire login`; `why` and `explain` work offline.

## Git AI 1.7.5

```bash
curl -sSL https://usegitai.com/install.sh | bash      # hooks Claude Code globally, sets global trace2, starts a daemon
export PATH="$HOME/.git-ai/bin:$PATH"
git-ai config set telemetry_oss off                   # the key shown by `git-ai config` is telemetry_oss_disabled, but that one can't be set
git-ai config set feature_flags.daemon_log_upload false
# Haiku run only:
git-ai config set prompt_storage notes                # prompt text is opt-in
git-ai install --skills                               # adds ask / git-ai-search / prompt-analysis skills for Claude Code
```

Why check: `git-ai await`, `git-ai blame payments/charge.py`, `git-ai show <commit>`, `git-ai show-prompt <session id>`, `git-ai blame <file> -L n,n --show-prompt | cat`.

## brain0 0.1.1

Needs glibc ≥ 2.39, so use `Dockerfile.trixie`.

```bash
mkdir -p ~/.npm-global && npm config set prefix ~/.npm-global
npm install -g brain0@0.1.1
```

brain0 is passive: it reads git and Claude Code transcripts after the fact. To give it its best shot at session B, [`harness/brain0-preb.sh`](harness/brain0-preb.sh) runs before B (via `PRE_B="bash /h/brain0-preb.sh"`): `brain0 ingest`, `brain0 observe`, `brain0 report --md`, then `claude mcp add brain0 -- brain0 mcp …` so B's agent can query it. No Ollama, so it used its documented offline fallbacks.

Why check: the MCP tools `brain0_blame` / `brain0_context` called directly over stdio (see `runs/brain0-haiku/mcp-direct.txt`), plus `brain0 query "why does charge() not retry after a ProviderTimeout"`.

## Agent Trace

Spec only (agent-trace.dev, v0.1.0 RFC). Its reference repo, github.com/cursor/agent-trace, returned 404 on 2026-10-21. Nothing to run.
