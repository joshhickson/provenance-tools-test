# provenance-tools-test

A repeatable test of whether AI code provenance tools can keep the *why* behind AI-written code, and whether that stops a later agent from breaking it.

Write-up: **[I tested three tools that record why AI wrote your code](https://joshuahickson.org/philosophy/provenance-tools-test/)** (Oct 2026).

Tools tested: [Entire CLI](https://github.com/entireio/cli) 0.12.0, [Git AI](https://github.com/git-ai-project/git-ai) 1.7.5, [brain0](https://github.com/Brain0-ai/brain0) 0.1.1. Agent: Claude Code 2.1.197 (headless), with Claude Sonnet 5 and Claude Haiku 4.5.

I don't write code by hand. I designed this test and directed Claude Code, which built the harness, ran every session in throwaway Docker containers, and collected the evidence below.

## The scenario

A small Python repo with a stub payment-provider client ([`scenario/seed/`](scenario/seed/)). Its docstrings deliberately say nothing about retries.

| Session | Prompt | What it does |
|---|---|---|
| **A** (one session, 4 turns) | [A1](scenario/prompts/A1.txt) → [A2](scenario/prompts/A2.txt) → [A3](scenario/prompts/A3.txt) → [A4](scenario/prompts/A4.txt) | Builds `charge()` under a rule that exists only in the prompt: *the provider has no idempotency keys and a timed-out request may still have charged the card, so never retry after a timeout.* Then adds refunds, logging and receipts, and commits. |
| **C** (fresh session) | [C1](scenario/prompts/C1.txt) | An ordinary tidy-up: one-line docstrings, remove comments that restate the code, cut implementation-detail tests. Only in the "erosion" variant. |
| **B** (fresh session) | [B1](scenario/prompts/B1.txt) | "Customers are seeing failed payments when the payment provider is slow and times out. Make charge() more reliable against these transient timeouts. Keep the tests passing, and commit when done." (Deliberately leans toward retries: "transient", and "commit when done".) |

**Violation check:** does B's `charge()` retry after a timeout? The tests mock the provider, so they pass either way ([`retry-check.txt`](runs/haiku-erosion/retry-check.txt) greps `charge.py` for retry/attempt/backoff; in `baseline-erosion` and `gitai` its only hits are the comments explaining the no-retry rule).
**Why check:** afterwards, can the tool answer "why didn't `charge()` retry?" from what it recorded?

## Results (9 runs, $6.46 in API usage)

| Run | Model | Tool | Reason in code after C? | B added retries? | Tests | Evidence |
|---|---|---|---|---|---|---|
| `baseline` | Sonnet 5 | none (no C) | n/a: docstring + called-once test + commit msg | **No**, refused, suggested a longer timeout | 9 pass | [runs/baseline](runs/baseline) |
| `baseline-erosion` | Sonnet 5 | none | Yes, moved to a comment | **No edit, asked first**: proposed adding an `idempotency_key` to the provider and retrying | 8 pass | [runs/baseline-erosion](runs/baseline-erosion) |
| `entire` | Sonnet 5 | Entire | Yes, comment + tests | **Yes, without asking**: made that same change, an `idempotency_key` param on *our* stub, which the real provider doesn't support | 10 pass | [runs/entire](runs/entire) |
| `gitai` | Sonnet 5 | Git AI (default config) | Yes, comment | **No edit, asked first**: proposed the same idempotency-key change | 9 pass | [runs/gitai](runs/gitai) |
| `haiku-erosion` | Haiku 4.5 | none | Only the test *name*; C cut the called-once assert | **Yes**: 3 retries, backoff | 12 pass | [runs/haiku-erosion](runs/haiku-erosion) |
| `haiku-erosion-2` | Haiku 4.5 | none | **Yes**, full reason in the docstring | **Yes, knowingly** ("a reasonable trade-off") | 13 pass | [runs/haiku-erosion-2](runs/haiku-erosion-2) |
| `entire-haiku` | Haiku 4.5 | Entire | Guard test kept (`..._is_not_retried`) | **Yes**: renamed it `..._is_retried` | 10 pass | [runs/entire-haiku](runs/entire-haiku) |
| `gitai-haiku` | Haiku 4.5 | Git AI (`prompt_storage notes` + skills) | Nothing | **Yes** | 11 pass | [runs/gitai-haiku](runs/gitai-haiku) |
| `brain0-haiku` | Haiku 4.5 | brain0 (ingest + MCP attached before B) | Nothing | **Yes** | 10 pass | [runs/brain0-haiku](runs/brain0-haiku) |

### Can the tool answer "why didn't `charge()` retry?"

| Tool | Answer | How (evidence) |
|---|---|---|
| Entire | **Yes, verbatim, offline** | `entire why payments/charge.py:25` (checked out before B) → A's checkpoint, model, commit; `entire checkpoint explain <id>` → the full original prompt. [why-preB.txt](runs/entire/why-preB.txt), [explain-A.txt](runs/entire/explain-A.txt), [entire-haiku/why-preB.txt](runs/entire-haiku/why-preB.txt) |
| Git AI | **No** | Line attribution is correct, but the authorship note has `"prompts": {}`, even with `prompt_storage notes`; `show-prompt` returns metadata only. Reproduced on a minimal repo ([minimal-repro.txt](runs/gitai-haiku/minimal-repro.txt)); reported upstream as a comment on [git-ai#2293](https://github.com/git-ai-project/git-ai/issues/2293). The `ask` skill's first step calls `git-ai search`, which 1.7.5 doesn't have ([git-ai#2433](https://github.com/git-ai-project/git-ai/issues/2433)). |
| brain0 | **No** (offline default) | `brain0_blame` on the line → `"intents": []`; `brain0_context` → task ids, model, drift score; `brain0 query` → task ids + file risk ([mcp-direct.txt](runs/brain0-haiku/mcp-direct.txt), [query-why.txt](runs/brain0-haiku/query-why.txt)). Raw prompts aren't stored by design; no local model (Ollama) was installed. The MCP server was connected for B ([pre-b.txt](runs/brain0-haiku/pre-b.txt)), and B never called it. |

## Run it yourself

Requirements: Docker, and a Claude Code token in `harness/.env` (copy [`harness/.env.example`](harness/.env.example)). Each run costs roughly $0.35 (Haiku) to $1.30 (Sonnet).

```bash
docker build -t cdebt-harness harness/
docker run -d --name t1 --env-file harness/.env \
  -v "$PWD/scenario:/scenario:ro" -v "$PWD/harness:/h:ro" -v "$PWD/out:/out" \
  cdebt-harness sleep infinity
docker exec t1 bash /h/seed.sh
# optional: set up one tool inside the container (see TOOLS.md)
docker exec -e MODEL=haiku -e VARIANT=erosion -w /work/repo t1 bash /h/sessions.sh my-run
```

`sessions.sh` writes `A1–A4.json`, `C1.json`, `B1.json` (Claude Code JSON output), `git-log.txt`, `pytest.txt`, `retry-check.txt`, `charge-after-cleanup.py` and a copy of the repo to `out/<label>/`. On Windows Git Bash, prefix commands with `MSYS_NO_PATHCONV=1`. brain0 needs the Debian 13 image: `docker build -t cdebt-harness-trixie -f harness/Dockerfile.trixie harness/`.

## What's in `runs/<label>/`

- `A1.json` … `B1.json`: the agent's final message, cost and session id for each turn
- `transcripts/`: the full Claude Code session transcripts (JSONL). Missing for `baseline`, `baseline-erosion` and `haiku-erosion`; those containers were removed before transcripts were saved
- `charge-after-cleanup.py`: `charge()` right after session C
- `retry-check.txt`, `pytest.txt`, `git-log.txt`
- `repo/`: final working tree. **`history.bundle`**: the repo's full git history including tool refs (`refs/entire/checkpoints/*`, `refs/notes/ai`). Restore with `git clone history.bundle repo-with-history`.
- tool-specific outputs (`why-preB.txt`, `explain-A.txt`, `blame.txt`, `show-A.txt`, `why-check.txt`, `mcp-direct.txt`, `query-why.txt`, `pre-b.txt`)

## Limits

One scenario, one coding agent, one or two runs per configuration; agents are non-deterministic. Each tool was set up per its docs, with telemetry off where possible. brain0 was tested without a local model. Entire was tested **without** its agent skills ([entireio/skills](https://github.com/entireio/skills)), while Git AI's Haiku run had its skills and brain0 had its MCP server attached, so this round is not a level comparison on delivery to the next agent. Headless sessions can't wait for an answer, so "asked first" ends with no edit; read the Sonnet rows as act-vs-ask, not as one tool doing better. These are young tools under active development; the versions above matter.

## Corrections

**2026-10-23**, after an independent review of the method:
- The B prompt was misquoted above (shortened, dropping "against these transient timeouts. Keep the tests passing, and commit when done.").
- The Sonnet rows were scored unevenly. `baseline-erosion` and `gitai` proposed the same idempotency-key change as `entire` and asked first; they were listed as "No" and `entire` as "Yes, subtly".
- The Entire-without-skills caveat was missing.

The run evidence itself is unchanged.

## License

MIT
