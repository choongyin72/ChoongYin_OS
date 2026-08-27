---
name: ec-bank-pattern-converter
description: Use when upgrading an EC (Energy Components) screen's EXISTING RF automation to the full "Bank pattern" — e.g. "convert <screen> to the Bank pattern", "bring <screen> up to full Bank-pattern shape", "add grid-filter wiring to <screen>". The screen already has SOME RF automation (old hardcoded field-ids, or partial label-driven) and needs upgrading to the properties-file-driven, T2-consolidated, explicit-grid-filter shape used by `bank_page.resource`/`berth_page.resource`. Also covers running this as a batch of N screens via parallel subagents. Distinct from `ec-object-iud-builder`, which builds a screen's IUD automation from scratch.
---

# EC Bank-Pattern Converter — upgrade existing RF automation to the consolidated shape

> **INPUT CONTRACT: the user gives one or more EC screen names (or "recon the remaining
> screens and batch them").** You determine each screen's current pattern, convert it if
> eligible, and raise a PR — hands-off. Only come back to the user for: a genuine blocker
> (environment/access/shared-file need), or a batch/merge-authorization decision.

Distilled from the Bank-pattern conversion project (Batches 2-11, 34+ EC screens converted,
2026-08-23). This is the WHAT-and-HOW for taking a screen from "has some RF automation" to
"matches Bank/Berth exactly" — reusable for any future round, and safe to hand to a fresh
Claude Code session or dispatch as a batch of parallel subagents.

## The three starting patterns (classify BEFORE touching anything)

Grep the screen's existing `pageobjects/.../<screen>_page.resource`:

| Pattern | Signal | What's needed |
|---|---|---|
| **FULL Bank pattern (already done)** | Has BOTH `Insert Object From Properties` AND `Find <Screen> Row By Filter` | Nothing — skip it |
| **PARTIAL label-driven** | Has `Fill OV Field By Label` / `Update Object From Properties`, but NOT the above | Add properties-file-driven insert/update/verify + explicit grid-filter wiring |
| **OLD hardcoded** | Has `Fill New Object Form` with raw field-id args | Full rebuild to label-driven + properties-file-driven + filter wiring (bigger lift) |

Never trust a name, a category label from an old survey, or "it already has automation" as a
reason to skip — **the sole eligibility criterion is screen LAYOUT similarity to Bank**, not
prior automation history. A screen with existing Playwright/generator automation still
qualifies for RF Bank-pattern conversion if its layout matches; the goal is ONE consolidated
RF implementation per layout type, not defect-fixing or deduplication of effort.

## Eligibility: is this screen Bank-shaped?

Bank-shaped = plain manage-object OV or custom-URL OV, single Date(+GO) navigator (or no
navigator at all), no mandatory dropdown/cascade gating the grid. Confirm via:
1. The screen's row in `docs/ec_screen_registry.md` (navigator column) — but if it says
   "unclear" or isn't listed, do NOT assume nav-free; recon live before batching.
2. The screen's own already-proven Playwright/RF driver (`py/<screen>_iud.py` or
   `screens/.../playwright/ec_iud_<slug>.py`) — read it fully; it usually already encodes the
   real mandatory-field set and nav shape from prior work.

**Not Bank-shaped → mark EXCLUDED, do not force it**: mandatory Business Unit/Area dropdown +
GO, cascading multi-level navigator, multi-object junction table, event-log/status-grid,
PC-style parent-child. Skip and move to the next screen — never force-fit.

## Recon-first, no guessing

- Read the screen's OWN existing page object and OWN existing driver before writing any new
  config. Never extrapolate field labels, mandatory sets, or grid ids from a sibling screen —
  two similar-looking screens can differ (screen-prefixed vs generic Code/Name labels,
  different extra mandatory fields, different grid ids, paginated vs single-page grids).
- A field that looks optional in a static CSS/mandatory-class scan can still be **de-facto
  mandatory** at the business-rule level — Save clicks fine but the row never persists, and
  EC's own unsaved-changes confirmation modal is left open, stalling the suite. If Save
  silently fails to persist, re-run the screen's own unmodified, already-proven driver before
  assuming the field is optional — trust the proven driver's field set over a fresh guess.
- Confirm the fixed `AUTOTEST_<SCREEN>` test code is free in the DB (fresh oracledb
  connection: dsn `localhost:1521/ORCL`, user `ECKERNEL_EC`, password `energy`) before using
  it.

## Build

- Per-TC `Login To EC Application`/`Logout From EC Application`, 5-TC business narrative
  (TC01 Verify Clean State / TC02 Insert / TC03 Update / TC04 Find / TC05 Delete), fixed test
  code, dedicated `<SCREEN>_EC_USER`/`<SCREEN>_EC_PASS` pair appended (additive only) to
  `resources/credentials.py`.
- Reuse shared T2 (`resources/manage_object.resource`) keywords as-is:
  `Insert/Update Object From Properties`, `Verify Object Insert Exists/Form Record/Found/
  Removed/Does Not Exist`, `Find/Clear Object Row By Filter`.
- Add a thin T3 wrapper `Find/Clear <Screen> Row By Filter` delegating to the shared T2
  filter keywords, wired into **Update/Find/Verify-Found/Delete only** — NOT into
  Verify-Removed/Does-Not-Exist (those already get a filter-based absence check for free).
- 4 properties files per screen under `testdata/`: `<screen>_{insert,update,form_verify,
  grid_verify}.properties`.
- Dropdown fields filled with `__FIRST__` (or any resolved-reference value): exclude from the
  round-trip form-label compare list — a resolved value can re-render different display text
  (e.g. Description instead of code) after reload, causing a false mismatch.

## Hard rule: never touch shared files this round

**Do NOT edit `resources/manage_object.resource` or `resources/common.resource`.** If the
screen genuinely needs a new/modified shared keyword to reach full completion, STOP — do not
add it. Log the screen as a SCOPE MISMATCH and skip it instead. (If a shared-file change is
ever genuinely authorized in a future round, follow the `ec-screen-automation` skill's
shared-file safety protocol: backup first, additive-only, canary + random-sibling regression.)

## Verification — every step must actually run, cite real output

1. `py -m robocop check <changed files>` — compare issue count/category against an already-
   merged sibling suite (e.g. `berth_iud.robot`); parity = not a regression, don't chase
   pre-existing DOC02/VAR02 style noise to zero.
2. `robot --dryrun` on the FULL `tests/` tree — must stay 100% pass (proves no collision with
   any other screen's suite).
3. Live run, `EC_HEADLESS=true`, of the screen's own suite — must be 5/5.
4. Independent DB self-clean: a FRESH oracledb connection (not the RF library's own), querying
   for `AUTOTEST%` rows — 0 residual, checked AFTER the live run.
5. Confirm the filter keyword actually fired: `grep -c "Find Object Row By Filter" output.xml`
   (or the screen-specific wrapper name) — non-zero.

Never report "done" without having actually run all five and citing the real numbers.

## Blocker / scope-mismatch protocol

- A verification step fails: retry ONCE with a genuine evidence-based fix (not a random
  selector change). Fails a second time: STOP, log a BLOCKED entry with the exact failure and
  evidence — do not grind further attempts.
- Screen turns out not Bank-shaped, or needs a shared-file change: STOP, log a SCOPE MISMATCH
  entry, do not force it.
- **Genuine environment/access blocker** (e.g. a role-permission gate makes the screen
  unreachable, not a code defect): do NOT attempt any sandbox security-config write yourself.
  STOP after confirming it's reproducible (e.g. re-run a working sibling suite in the same
  session to rule out a transient/session issue), log it BLOCKED with the exact evidence, and
  leave any already-built work sitting uncommitted in its isolated clone — it doesn't need to
  be rebuilt once the owner resolves the blocker, only re-verified.

## Git / PR

- Isolated clone per screen: `git clone --no-checkout <remote> Workplaces/<screen_slug>/`,
  then `git sparse-checkout init --cone && git sparse-checkout set <the relevant subdirs>`,
  then `git checkout -b feature/<screen>-bank-pattern origin/master`. This avoids Windows
  long-path failures a plain full checkout can hit, and keeps parallel agents from stepping on
  each other's working trees.
- Commit only the screen's own files by explicit path — never `git add -A`.
- Sync with `origin/master` before pushing (other batches may have merged since you cloned).
- Raise a PR with a 6-field body: What was built / Files touched / DB ground-truth evidence /
  Self-clean confirmed / Rules applied / Base branch. **Never merge your own PR** — even a
  standing "proceed autonomously" instruction does not imply merge authorization; that needs
  its own fresh, explicit grant each round.
- If the screen already has an existing row in `docs/ec_screen_registry.md` /
  `docs/automation-scorecard.md` (from an earlier build), you are MODIFYING that row, not
  adding a new one — say so explicitly in the PR body, and make the row a clean, complete
  replacement (don't leave the old row's stale text sitting nearby).

## Running this as a batch of N parallel screens

1. **Classify candidates first** (see table above) by grepping each screen's page object
   directly — don't trust a stale survey/category label. Group into batches of ~5.
2. **Write `tmp/batchN_shared_findings.md`** before dispatching: the batch's screen list with
   per-screen notes (labels confirmed screen-prefixed or generic, any extra mandatory fields,
   sibling screens to avoid touching), the hard rules above, and an "Entries" section for
   agents to append their findings to (gotchas compound batch-over-batch: LEN32 robocop
   variable-length limits, cascade dropdowns, conditional-mandatory business rules, etc.).
3. **Pre-create the batch's section header** in `docs/bank-pattern-conversion-checklist.md`
   and `docs/grid-filter-standardization-checklist.md` in ONE commit/PR, BEFORE dispatching
   subagents — an empty "## Batch N additions (pending)" section + table header. Each screen's
   PR then appends only its own row, avoiding checklist fragmentation from N parallel PRs each
   creating their own header.
4. **Wait for that header PR to actually MERGE** (confirm via a PR-status check —
   `merged: true`, not just pushed) before dispatching the batch's subagents. Subagents clone
   fresh off `origin/master`; if the header is only pushed to its own unmerged branch, every
   subagent either fabricates its own header or hand-copies the unmerged one, and the
   resulting duplicate-row/duplicate-header mess needs a manual consolidation fix. This was
   the single biggest process defect across the whole project — it is fully avoidable by
   waiting for the merge.
5. **Dispatch one subagent per screen in parallel**, each with the full context above plus its
   specific screen name, folder, confirmed label style, and any sibling-screen warnings. Each
   agent works in its own isolated clone, does the work in the same turn (no further nested
   subagent delegation), and raises its own PR without merging.
6. **Independently re-verify every subagent's PR** via a PR-read tool (e.g.
   `mcp__github__pull_request_read`) before counting it done — check the diff is real,
   independent of siblings, and `mergeable_state: clean`. Never trust a subagent's own summary
   alone.
7. **After the batch merges**: sync local master, personally spot-check 1-2 of the batch's
   screens yourself (checkout, run the live suite) rather than relying solely on subagent
   self-reports — this is cheap insurance against a subagent's evidence being subtly wrong.
8. **Clean up** the batch's `Workplaces/<slug>/` clones once merged, then move to the next
   batch (repeat steps 3-7).

## Bundle deliverables (owner decision 2026-08-27 — restored from `ec-object-iud-builder`)

Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` retired the 2026-08-23 lean waiver: every
Bank-pattern conversion now also produces, under `screens/<menu path>/<Screen>/`:
- **`<screen>_sow.md`** — classification, grid/cell shape, test data, dev story.
- **`README.md`** — bundle overview + exact run commands.
- **`JOURNAL.md`** — per-branch work journal (built / done-wrong / done-well / improve /
  blockers→resolution / decisions / evidence).
- **`evidence/`** — step screenshots + a results record from the real live run.
- **`CHECKLIST.md`** — a copy of `docs/IUD-DELIVERABLE-CHECKLIST.md` (Steps 0, A minus 4/5, B, C, D,
  E), ticked with evidence.
- **KB selector map** `ec-ui-knowledge/screens/<screen>.md`.

**Still NOT required** (superseded by the Universal Screen Engine, per the same owner decision):
a hand-written Playwright driver (item 4) or its `investigation/` recon scripts (item 5) — a
throwaway scratch script in `Workplaces/<screen>/` (gitignored) is fine for ad-hoc recon and does
not need to become a permanent deliverable.

Raising a PR without these bundle artifacts is no longer "done" for this skill — the RF-suite
verification gates below are necessary but not sufficient.

## What "done" looks like for a screen

Properties-file-driven insert/update/verify + explicit `Find/Clear <Screen> Row By Filter`
grid-filter wiring, matching `bank_page.resource`/`berth_page.resource` exactly. Live 5/5,
dryrun 100% on the full tree, DB self-clean confirmed via a fresh connection, filter keyword
confirmed fired, no shared T1/T2 file changes, registry/scorecard/checklist docs updated, the
bundle deliverables above produced, PR raised (not self-merged).
