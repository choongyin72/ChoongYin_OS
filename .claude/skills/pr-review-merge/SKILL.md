---
name: pr-review-merge
description: Use when acting as the REVIEWER for this repo — the user says "review raised PRs and merge", "any raised PRs?", "code review and merge", or similar, in this or a fresh Claude Code session. Drives list PRs -> verify each against real diffs (never the PR body alone) -> fix-or-return -> merge (worktree technique for anything stacked/fixed) -> disclose -> file follow-up feedback, autonomously. The automated 06:00/14:00 AWST scheduled trigger is DISABLED (2026-08-01) — this is now the only way review happens, on-demand each time the owner asks.
---

# PR Review & Merge — the Reviewer role, end to end

> **INPUT CONTRACT: the owner just says "review raised PRs and merge" (or asks "any raised PRs?").**
> Do everything else yourself — list, verify, fix-or-return, merge, disclose, follow up — hands-off.
> Don't ask the owner to point you at a specific PR unless something genuinely needs their decision
> (a governance-file edit, an ambiguous MUST-FIX call, a destructive action).

This is the Worker-side `ec-object-iud-builder` skill's counterpart on the Reviewer side. That skill is
WHAT the Worker does to build a screen; this is WHAT the Reviewer does to review and merge it. The HOW —
every concrete technique referenced below — lives in `docs/PR-REVIEW-PROTOCOL.md`'s **"Reviewer merge
discipline"** and **"Reviewer per-PR checklist"** sections. Read those in full before the first PR of a
session; this skill is the orchestration, not a duplicate of the substance.

## Session-start (do this once per session, not per PR)
1. Read `docs/PR-REVIEW-PROTOCOL.md` in full — the two sections named above are the operational core.
2. Skim `docs/lessons-learned.md`'s changelog table (top of file) for any R# added since you last read it.
3. Read `docs/session-memory.md` for owner decisions / cross-session context.
4. `git fetch origin master` — confirm remote access before relying on it.

## Steps (execute in order, every time asked to review)

**1. Inventory.** List open PRs and open Issues in `choongyin72/ChoongYin_OS` (this repo only — never
search or act outside this scope). Note which PRs are stacked (`base` = another feature branch, or the
body says `depends on #N`) — these must be handled in dependency order, base-first.

**2. Verify each PR against real content, not its description.** For every PR:
   - Find the true fork point (`git merge-base origin/master <branch>`) and diff from there — comparing
     against current `origin/master` on a stacked PR shows an already-merged sibling's files as if they
     belonged to this PR.
   - Read the actual changed file contents for anything substantive — registry/scorecard/KB/JOURNAL rows,
     generator/template code, driver/T3/suite bundles. A file list or diff stat proves nothing.
   - EC Object IUD PRs: spot-check the real 21-item `docs/IUD-DELIVERABLE-CHECKLIST.md` substance behind
     each tick.
   - If a text-correctness fix touches the CHECKLIST/SOW/KB/registry/scorecard/JOURNAL layer, also grep
     the GENERATED driver `.py` / T3 `.resource` / suite `.robot` files for the same stale claim — this
     exact gap recurred three PRs running (#295/#297/#298) before it was named as a pattern.
   - Generator/template changed? Regenerate an UNRELATED already-shipped screen's config through both the
     old and new version and diff byte-for-byte before trusting a "no regression" claim.
   - `CLAUDE.md` or `ec-ui-knowledge/EC_BUG_TRACE_SOP.md` touched? **STOP.** Ask the owner explicitly
     (`AskUserQuestion`) before merging that part, no matter how reasonable it looks or how confident you
     are — this is the one hard line that never gets a judgment call.

**3. Decide: fix directly, or return to the Worker.**
   - Fix directly (with clear disclosure in the merge commit + PR comment) when the correct content is
     already known or mechanically reconstructable: a wording/placeholder error with an unambiguous
     substitution value already present elsewhere in the same PR, a generator-root fix for a defect class
     already fixed once in the same diff, restoring content that exists unchanged elsewhere in git history.
   - Return to the Worker (leave the PR open, post a `MUST-FIX` comment) when the gap needs genuinely new
     investigative or evidentiary content — JOURNAL narrative for work not actually done, DB evidence,
     screenshots, a root-cause claim not backed by anything already on record.

**4. Merge.**
   - Clean, independent, no-fix-needed PR → the normal GitHub merge path is fine.
   - Anything stacked, or anything needing a hand-fix → the worktree technique: `git worktree add --detach
     <path> origin/master`, real `git merge --no-ff --no-commit origin/<branch>`, resolve conflicts by hand
     (append-only docs: keep both sides if textually different, "ours" only if verified byte-identical),
     apply any disclosed fixes, `git commit`, `git push origin HEAD:refs/heads/master` (never a bare
     `push origin master` from a detached worktree — wrong ref).
   - Before pushing: conflict-marker sweep, `ast.parse` on every touched `.py`, non-ASCII scan on touched
     doc rows, and — if a shared vocabulary/hygiene validator exists (e.g. `check_row_vocab.py`) — re-run
     it across the WHOLE manifest, not just the screen this PR touches.
   - After pushing: confirm the PR flipped to `merged: true`. If its `base` was another feature branch and
     it didn't, verify `git merge-base --is-ancestor <branch> origin/master`, then try retargeting
     `base: master` — a "no new commits between base and head" error confirms zero diff remains — and
     close it manually with a comment explaining why, rather than leaving it looking unmerged.

**5. Disclose and follow up.**
   - Post a PR comment stating exactly what was verified and any fix folded in. A hand-fix must never look
     indistinguishable from what the Worker shipped.
   - A pattern worth remembering for next time → append a dated entry + the next R# to
     `docs/lessons-learned.md` (append-only — new section at the end, never rewrite existing lines).
   - Feedback for the Worker with no PR left open to carry it → file a GitHub Issue. The Worker's own
     session-start protocol only scans *open* Issues and *open* PRs; a comment on an already-closed PR
     will not resurface on its own.

## Hard boundaries (no judgment call, ever)
- Never push `--force`, skip hooks, or take a destructive git action without the owner's explicit go-ahead.
- Never edit `CLAUDE.md` or `ec-ui-knowledge/EC_BUG_TRACE_SOP.md` without an explicit owner decision first.
- Never fabricate JOURNAL narrative, DB evidence, or a root-cause explanation the Worker didn't establish.
- Never merge a `depends on #N` PR before #N, and never leave a stacked PR looking "unmerged" once its
  content is verified to already be an ancestor of `master`.
