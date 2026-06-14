# PR & Review Protocol — Worker ↔ Reviewer

**Status: v0.1 (DRAFT — proposed by the worker session 2026-06-15).** The "Open questions" at the
bottom need the reviewer's / user's confirmation; everything else is what the worker commits to now.
This doc is the shared contract for the feature-branch + PR workflow. Both sessions should read it at
session start. It evolves only via PR (append-only edits — see §Shared-file discipline).

## Roles
- **Worker** (builds EC automation): creates feature branches, opens PRs, never merges.
- **Reviewer** (daily 06:00 AWST): runs `/code-review --comment` on open worker PRs, posts inline
  findings, extracts actionable rules into `docs/lessons-learned.md` (via its own `review/` PR).
- **Human** (Choong-Yin): reviews; the merge is performed by the reviewer session / human, never the worker.

## Branch & PR conventions
- **Branch naming:** `feature/<short-task-name>` (worker), `review/feedback-YYYY-MM-DD` (reviewer).
- **Base:** branch INDEPENDENT tasks off `master`; branch DEPENDENT tasks off the parent branch.
- **Stacking:** stacked/parallel PRs are allowed (don't idle waiting for a merge). If a PR builds on
  another, put **`depends on #N — merge after`** in the title/body; the merger must respect that order.
- **PR title prefix:** `feat:` / `fix:` / `recon:` / `chore:` / `review:`.
- **The worker never merges and never commits to `master` directly.**

## Worker guarantees (every PR)
1. **Standard PR body** (see template below) — same shape every time, so review is fast to parse.
2. **Small, single-purpose PRs** — one screen/pattern each.
3. **Evidence-first** — a PASS is claimed only with DB ground truth (live run + the exact DbVerify
   assertion), never a green UI log alone; the evidence is linked in the PR.
4. **Self-cleaning** — any test that writes data restores the sandbox exactly as found (DB-verified);
   the PR states the self-clean result.
5. **Engage comments with rigor** — verify each finding against code/DB, then fix or push back with
   technical reasoning (no performative agreement, no blind implementation).

## Reviewer asks (to make findings actionable)
1. **Tag each comment `MUST-FIX` vs `NICE-TO-HAVE`** so the worker knows what gates the merge.
2. **Cite `file:line` + the concrete failure mode + a suggested fix** — "always do X / never do Y",
   not "consider X" (the same bar `lessons-learned.md` rules are held to).
3. **Verify claims against the actual code/DB before posting** — especially DB/runtime claims not
   visible in the diff. (Precedent: a "3 Financial Objects parked" gap and a backwards ORA-06569 rule
   did not hold up on validation 2026-06-15.) The worker will validate feedback the same way — to
   anchor on ground truth, not to dismiss it.
4. **Append-only when writing to shared docs** (`lessons-learned.md`, `automation-scorecard.md`) —
   new dated sections / rows, never rewriting existing lines — so review PRs don't collide with open
   work PRs.
5. **Respect stack order** — never merge a `depends on #N` PR before #N.

## PR body template (worker)
```
## What
<one-line: what was built/fixed>

## Scope
- files: <list>
- base: <master | feature/parent>   depends on: <#N | none>

## Evidence (DB ground truth)
- suite: <path>   result: <live N/N>
- DB-verify: <the exact assertion, e.g. PWEL_SUB_DAY_STATUS.AVG_WH_PRESS 210->206.84 unit-robust>
- self-clean: <restored to baseline, 0 residual — verified>

## Lessons-learned rules applied
- R# <which rules from docs/lessons-learned.md this honoured>

## Notes / risks
<anything the reviewer should know>
```

## Shared-file discipline (both sessions)
These files are edited almost every task and are conflict-magnets:
`libraries/DbVerify.py`, `docs/ec_screen_registry.md`, `docs/automation-scorecard.md`,
`DeepDiveLearnings/SELF-LEARNING-BACKLOG.md`, `docs/lessons-learned.md`.
**Rule: APPEND-ONLY** — add new functions / table rows / dated sections at the end; never rewrite
existing lines. This keeps parallel PRs auto-mergeable and safe for an automated merger.

## Handling review comments (worker routine)
1. At **session start**, check my open PRs for new review comments before opening new branches.
2. For each comment: restate it, verify against code/DB, then **fix** (`MUST-FIX`) or **reply with
   technical reasoning** if I believe it's wrong (cite the test/DB that proves it).
3. Reply in the PR comment thread, not as a new top-level comment.
4. Re-run the affected suite + the canary after addressing comments; note the result in the thread.

## Open questions — TO BE CONFIRMED by reviewer / human
1. **Merge gate:** does the reviewer merge only after `MUST-FIX` comments are resolved, or
   merge-then-comment (advisory)? (Worker's assumption: **MUST-FIX gates the merge**.)
2. **Notification:** is "check open PRs for review comments at session start" the agreed worker
   routine? (Worker will adopt it unless told otherwise.)
3. **Turnaround:** confirm the reviewer does **not** merge an un-addressed worker PR within the
   ~20h window between PR-open and the next 06:00 review run.

## Recommended wiring (not done in this PR)
Add this file to `CLAUDE.md`'s "On session start (mandatory)" reading list so both sessions load it.
(Left to the reviewer/human who own `CLAUDE.md`, to keep this PR single-purpose.)
