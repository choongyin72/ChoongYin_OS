# RF Task Board — EC Bank-Pattern Conversion

Small local Flask dashboard tracking EC screens moving through the Bank-pattern
conversion workflow (`ec-bank-pattern-converter` / `ec-bank-pattern-new-screen`
skills for the worker side, `pr-review-merge` for the reviewer side).

## Run it

```
py -m pip install -r requirements.txt
py app.py
```

Then open http://localhost:5057/ in a browser.

No cron, no webhooks in this version — it's a shared state board that
independent Claude Code sessions (or you, by hand) read from and write to via
its HTTP API. Nothing auto-triggers; a worker session claims + updates a task
itself, a reviewer session queries `pr_raised` tasks itself.

## Data

Everything lives in `tasks.db` (SQLite, created automatically on first run).
Two tables: `tasks` (current state) and `task_history` (every status
transition, with an optional note — used for blocker/rejection reasons).

## API (for a Claude Code worker/reviewer session to call)

| Method | Path | Body | Purpose |
|---|---|---|---|
| GET | `/api/tasks` | — | list all tasks (optional `?status=` filter) |
| GET | `/api/tasks/<id>` | — | one task + its full history |
| POST | `/api/tasks` | `{screen_name, pattern}` | add a new screen to the queue |
| POST | `/api/tasks/<id>/claim` | `{claimed_by}` | unclaimed -> in_progress; fails (409) if not currently unclaimed |
| POST | `/api/tasks/<id>/status` | `{status, note?, pr_number?}` | move to any valid status; `blocked` requires/sets `note` as the blocker reason |
| GET | `/api/summary` | — | counts per status |

Valid `status` values: `unclaimed`, `in_progress`, `pr_raised`,
`changes_requested`, `merged`, `blocked`.

### Typical worker sequence
```
POST /api/tasks/7/claim         {"claimed_by": "worker-session-A"}
... do the actual EC/RF conversion work, raise the PR ...
POST /api/tasks/7/status        {"status": "pr_raised", "pr_number": 482}
```

### Typical reviewer sequence
```
GET  /api/tasks?status=pr_raised
... review PR #482 ...
POST /api/tasks/7/status        {"status": "merged"}
   # or, if it needs rework:
POST /api/tasks/7/status        {"status": "changes_requested", "note": "add DB self-clean evidence"}
```

## Scope (v1)

Single local user, no auth, no notifications/push, no cron/webhooks — the
board is a shared source of truth that any number of independent Claude Code
sessions can poll and update, but nothing here automatically dispatches or
notifies anyone. See the design discussion in this project's session history
for the v2/v3 ideas (webhook-driven auto-update, auto-dispatch) if this proves
useful and warrants expanding.
