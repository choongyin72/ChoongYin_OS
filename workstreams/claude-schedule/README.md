# Claude Schedule — Scheduling Machinery

## How it works
1. A task spec is written to `drafts/<slug>.md` (by you or by a routine).
2. You review the spec and set `status: approved` (or rename the file to `approved-<slug>.md`).
3. The `auto-attach` script (runs every 10 min via Task Scheduler) detects approved specs and arms them via RemoteTrigger.
4. The scheduled agent runs at the specified time, does the work, and opens a PR.
5. You review and merge.

## Spec format
```yaml
slug: <short-id>
status: draft | approved | running | done | cancelled
schedule: "daily 08:00 AWST" | "2026-06-03T08:00+08:00" | "once"
permission_level: L1 | L2 | L3
prompt: |
  <what the agent should do>
```

## RemoteTrigger note
RemoteTrigger only works from an interactive, locally-OAuth'd Claude Code session (desktop app or IDE extension).
Mobile and headless CI cannot arm tasks — always arm from your local machine.
