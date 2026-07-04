---
name: ec-deepdive-review
description: Use when running the PERIODIC review of the EC Screen Deep-Dive program — after the daily autopilot merges a new batch of screen notes to feature/ec-screen-deepdive, or when the user asks for a "deep dive review on the new screens / periodic review". Inventories the new batch, synthesizes EC-domain learnings + note-quality/improvement areas, and persists a dated review + a LEARNING-SCORECARD calibration row to the program branch. Read-only on screens/DB; isolated worktree; NEVER merges.
---

# EC Screen Deep-Dive — Periodic Review

Turn the recurring "what did the autopilot just learn, and how do we improve?" into a consistent,
fast, guarded routine. The autopilot (`tools/deep-dive-scheduler/run_ec_screen_learn.py`, daily ~1:30 PM)
writes `DeepDiveLearnings/ec-screens/notes/<BF_CODE>.md` for EC screens and pushes to the PERMANENT
branch `feature/ec-screen-deepdive`. This skill reviews each new batch. Program context lives in the
memory `project_ec_screen_deepdive_program` — read it first.

## When to use
- The user says "deep dive review on the new screens", "periodic review", or similar.
- A new batch merged to master / the program branch since the last `REVIEW-<date>.md`.
- A self-learning / never-idle slot where reviewing the latest batch is the top item.

## Inputs / where things live
- Notes: `DeepDiveLearnings/ec-screens/notes/<BF_CODE>.md` · tracker `CHECKLIST.md` · plan `MASTER-PLAN.md`
- Habit file: `DeepDiveLearnings/LEARNING-SCORECARD.md` (append a calibration row — see its own section 4)
- Prior reviews: `DeepDiveLearnings/ec-screens/REVIEW-<YYYY-MM-DD>.md`
- Reviewer-owned (READ-ONLY here, R23): `docs/lessons-learned.md`, `docs/review-log.md`,
  `docs/automation-scorecard.md`, `STATUS.md`
- Cross-reference shipped IUD bundles: `workstreams/master-plan/ec-automation/` + `docs/ec_screen_registry.md`

## Steps (execute in order)

**1. Inventory the new batch.** Find the base = the commit/date of the last review (from the newest
`REVIEW-*.md` or the program memory). Then:
`git diff --stat <base>..origin/master -- DeepDiveLearnings/ docs/` — list the new/changed `notes/*.md`,
plus changes to CHECKLIST / lessons-learned / review-log / scorecard. Note total coverage (N/1457 from CHECKLIST).

**2. Read (breadth + depth).**
- Delegate the breadth-read of the new `notes/*.md` to an **Explore subagent**: per screen return
  name, EC business purpose, screen type (OV/TV/N1/N3/PC/report), completeness tier, and any
  IUD-relevant facts (backing table/view, nav, delete semantics). Ask for a structured digest, not file dumps.
- Read the process docs YOURSELF (small, high-signal): the latest divergence analysis (if any),
  the new `docs/lessons-learned.md` lines, `docs/review-log.md` entry, and the CHECKLIST head.

**3. Synthesize (the actual review).**
- **EC domain learned:** group the batch's screens by subsystem; map the object hierarchy + recurring
  EC patterns (VERSIONED object + EVENT allocation/split data; copy-forward / sum-to-100%; Maintain-X
  cascade-copy; N1 time-gated grids). **CONNECT to shipped IUD work** — does any screen back a member /
  parent of an automated bundle? (e.g. Perf Interval = a well-bore interval).
- **Note-quality tiers:** classify each note strong / partial / stub; list concrete improvement areas
  (truncated help text, class-resolver gaps on Maintain-X screens, missing nav/grid-ids = not IUD-ready,
  missing delete semantics, missing cross-links). Note good patterns to KEEP (honest `[~]` partials, R23).
- **Highest-leverage recommendation:** which screens to prioritise next (usually the ones with the most
  reuse vs already-shipped patterns + the most domain leverage).

**4. Persist** (in an ISOLATED worktree off `origin/feature/ec-screen-deepdive`; see guardrails):
- Write `DeepDiveLearnings/ec-screens/REVIEW-<YYYY-MM-DD>.md` (sections: scope/coverage · domain learned ·
  note-quality assessment + improvements · highest-leverage rec · brief self-assessment).
- Append ONE calibration-log row to `DeepDiveLearnings/LEARNING-SCORECARD.md` per its section-4 protocol.
- Update the `project_ec_screen_deepdive_program` memory with a dated `PERIODIC REVIEW <date>` entry.
- Commit + `git push origin HEAD:refs/heads/feature/ec-screen-deepdive` (no force). This rides the
  standing draft PR — do NOT open a new PR and do NOT merge.

**5. Report** the review to the user (domain headline, top improvement, next-batch rec) + confirm pushed.

## Guardrails (non-negotiable)
- **Read-only** on screens + DB; no live writes, no Save.
- **Isolated worktree only.** Work in a fresh `git worktree add /c/tmp/wt-ec-review origin/feature/ec-screen-deepdive`
  (detached) + push `HEAD:refs/heads/...`. NEVER touch the autopilot checkout (`C:\tmp\wt-ec-learn`),
  the main checkout, or any sibling `wt-*` worktree. Remove the temp worktree when done.
- **Append-only / new-file only** — never edit the reviewer-owned docs (lessons-learned, review-log,
  automation-scorecard, STATUS) on this branch (R23 — keep 0 deletion lines on those four).
- **ASCII-clean** any `.py` touched (R20); `.md` may be natural prose.
- **NEVER merge** the standing draft PR (owner-merge-only) and **no force-push** to the branch.
- **Spot-verify** agent-supplied backing tables / classes against the live DB before they drive any
  future IUD build (the digest is breadth, not ground truth).
- **Honest tiering** — never inflate a stub note to "strong"; mark partials `[~]`, never faked `[x]`.

## Done = 
A dated `REVIEW-<date>.md` + a LEARNING-SCORECARD calibration row pushed to `feature/ec-screen-deepdive`
(standing draft PR, not merged) + the program memory updated + a concise report to the user.
Reference example: `DeepDiveLearnings/ec-screens/REVIEW-2026-06-27.md`.
