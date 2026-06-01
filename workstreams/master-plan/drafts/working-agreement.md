# Working Agreement

## The Three Gates
1. **Approve the spec** — before any unattended work runs, you read the task spec in `drafts/<slug>.md` and rename it (or set `status: approved`).
2. **Merge the PR** — the agent opens a PR; you review and merge.
3. **Strategic calls** — anything involving tone, sensitive wording, or external comms comes back to you.

## Permission Contract

### L1 — Always allowed (no gate)
- Read any file in this repo
- Write/update files in this repo
- Run read-only git commands
- Look up docs and search the web

### L2 — Allowed unattended (auto-approve)
- Push commits to feature branches in this repo
- Open PRs against `master`
- Read files in `C:/DEV/GIT/woodside_impl_pluto_12839`

### L3 — Requires explicit approval
- Write to `C:/DEV/GIT/woodside_impl_pluto_12839` (code changes)
- Any external service calls (EC Web App, DB)
- Sending any message or notification on your behalf
- Merging PRs

## Norms
- Specs live in `workstreams/claude-schedule/drafts/` until approved
- Run logs live in `workstreams/claude-schedule/runs/`
- Candidates for the next day are proposed in `workstreams/master-plan/drafts/candidates/YYYY-MM-DD.md`
- Never commit credentials — reference DATA_SOURCES.MD locally only
