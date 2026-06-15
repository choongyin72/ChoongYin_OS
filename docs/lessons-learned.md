# Lessons Learned — EC Automation
_Reviewed by Claude Code (reviewer session) and appended over time._
_Worker sessions: read this before starting any automation work._

> **Current rule version: v8** (R8 added 2026-06-15)
> If the version you last read is lower than this, **re-read from the changelog below** before starting work — do not scan the whole file hoping to spot the diff.

### Rules Changelog
| Version | Rule | One-line summary | Date added |
|---------|------|-----------------|------------|
| v1 | R1 | Unit conversion guard before any DB write (multiplicative units only) | 2026-06-14 |
| v2 | R2 | Read current DB value before any write — no null assumptions | 2026-06-14 |
| v3 | R3 | Document parked items with a one-line blocker | 2026-06-14 |
| v4 | R4 | Sub-daily patterns need datetime-keyed DbVerify | 2026-06-14 |
| v5 | R5 | ec-worker down = silent WAITING; ORA-06569 = worker ran, empty scope | 2026-06-14 (corrected 2026-06-15) |
| v6 | R6 | Check STAT_PROCESS_TASK.TABLE_ID + WHERE_FORMULA before claiming V→A testable | 2026-06-15 |
| v7 | R7 | Page-object class docstrings must match the Variables section | 2026-06-15 |
| v8 | R8 | Sync feature branch with master before every push (git merge origin/master) | 2026-06-15 |

---

## 2026-06-14 — Review by Reviewer Session

### Rules (apply immediately, no exceptions)

**R1 — Unit conversion guard before any DB write** ⚠️ _refined 2026-06-15 (worker validation below): the `expected = typed * DB_before/UI_before` ratio is valid ONLY for multiplicative/zero-offset units (pressure, rates); it is WRONG for offset units like temperature (°F↔°C). See validation §R1._
Before writing to any DB column and asserting `typed_value == DB_value`, check if the column has a unit conversion. Pressure and rate columns in EC store SI/base units in DB but display configured units in UI. Factor for pressure: ~14.5038 (psi ↔ bar). Never use a naive equality oracle on these columns — derive the expected DB value from the live ground truth: `expected = typed_display * DB_before / UI_before`.

**R2 — Read current value before any write (no null assumptions)**
Never assume a cell is null before checking. Always read the current DB value before performing a write-then-diff assertion. Assuming null and writing 0/null to a non-null cell caused a 192-cell data incident on 2026-06-14. Oracle Flashback saved it — but Flashback has a time window. Resolve OBJECT_ID and read current value upfront, every time.

**R3 — Document parked items with a one-line blocker**
When parking a test or pattern, always write a one-line reason in the commit message AND in the relevant design doc. "Parked" without a reason is unresumable and unhandable. Acceptable format: `PARKED: <screen> — <specific blocker> — next step: <action>`.

**R4 — Sub-daily patterns need datetime-keyed DbVerify**
PWEL_SUB_DAY_STATUS (and similar sub-daily tables) key on `(OBJECT_ID, DAYTIME[+time], SUMMER_TIME)` — not `TRUNC(date)`. The daily DbVerify helper will silently match wrong rows. Always create a datetime-keyed variant when the PK includes time.

**R5 — ec-worker must be confirmed running before N3 tests** ⚠️ _last sentence CORRECTED 2026-06-15 (worker validation below): ORA-06569 NEVER signals a down worker. See validation §R5._
Before running any status process (N3 pattern), verify ec-worker is up and its scheduler is in RUNNING state (not STANDBY). ORA-06569 with "no elements" = empty data scope, not an infra failure. ~~ORA-06569 on a date with real P data = ec-worker is down or scheduler is STANDBY.~~ (Incorrect — corrected below: ORA-06569 is raised by `PCK_STATUS` *while executing*, so the worker DID run; a down worker = silent WAITING with no error and no `STAT_PROCESS_STATUS` row.)

---

### Observations (good patterns to keep)

- **Self-cleaning oracle pattern in DbVerify**: re-executing the production rule's own `WHERE_FORMULA` to compute expected violations is the correct approach — prevents oracle drift from deployed logic. Keep this pattern for all new check-rule tests.
- **T1/T2/T3 layering**: working well. Do not collapse layers for convenience — isolation of screen-specific vs pattern-level vs universal concerns is paying off.
- **WR.0001 canary after each new suite**: good practice, keep it. Catches regressions in shared keywords before they propagate.
- **Timestamp-based test codes**: good. Never use fixed test codes — they cause state pollution across runs.

---

### Gaps still open (worker to address)

| Gap | Owner | Priority |
|-----|-------|----------|
| ~~3 Financial Objects parked — root causes not documented~~ ⚠️ NOT VERIFIED (2026-06-15): all 15 FO suites present, none parked — appears incorrect/stale | — | ✖ closed |
| N3 V→A daily suite — build-ready but not built | Worker | 🟡 Medium |
| N3 V→A monthly suite — separate screen, thin T3 needed | Worker | 🟡 Medium |
| Dispatching Pipeline slice — not started | Worker | 🟢 Low |
| Column unit-conversion registry — no central list of which columns need conversion | Worker | 🟡 Medium (build when 1st offset/temp write-verify lands — YAGNI) |

---

## 2026-06-15 — Worker Validation (of the 2026-06-14 review)

First peer-review cycle. Worker validated each reviewer rule against the actual code/DB. Verdicts:

### Confirmed correct
- **R2 / R3 / R4** hold. R4 nuance: `sub_day_status_value` makes `SUMMER_TIME` an OPTIONAL filter (off by default), so on a DST-boundary day one HH:MI maps to two rows — pass `summer_time` on those days. R2 factual tweak: the 192-cell incident was a destructive *cleanup* on a null-assumption, not "writing 0/null to a non-null cell" — the rule (read full state before any destructive write/cleanup) is right.

### §R1 — refined (correct but unsafe as a general rule)
The live factor derivation `expected = typed_display × DB_before ÷ UI_before` (implemented at `pageobjects/Production/subdaily_well_status_page.resource`, WHP=AVG_WH_PRESS) is mathematically valid **only for zero-offset / multiplicative units** (pressure psi↔bar, rates). It is **WRONG for offset units** — temperature (°F = °C×1.8+32) is not a ratio, so the formula would silently mis-assert. No live failure yet (only pressure write-verify exists), but the guard is unsafe for temp/offset columns. **Action taken:** added an explicit multiplicative-only warning to the WHP keyword doc so the ratio approach is never reused for an offset column. **Deferred (YAGNI):** the full typed unit-conversion registry — build it (recording per-column conversion *type*: multiplicative factor vs offset formula) when the first offset/temperature write-verify is actually needed, not before.

### §R5 — corrected (reviewer's last clause is technically wrong)
"ORA-06569 on a date with real P data = ec-worker down/STANDBY" is **incorrect**. ORA-06569 is raised by `PCK_STATUS` *during execution* → the worker **ran** and found an empty matching scope. The signatures are opposite:
- **ORA-06569** ⇒ worker executed; empty/unmatched data scope (a config/scope problem).
- **silent WAITING, no error, no new `STAT_PROCESS_STATUS` row** ⇒ worker down or scheduler STANDBY.
Also: the N3 suite does not currently pre-check ec-worker; it relies on a poll timeout (25×3s) that fails with a clear message. An explicit ec-worker pre-flight in Suite Setup is a reasonable future add (not yet built).

### Gap correction
"3 Financial Objects parked — root causes not documented" (was 🔴 High) is **not substantiated**: all 15 Financial_Objects IUD suites are present and none are parked (the only `_parked` dir is `Commercial_Objects/_parked` → one `sub_field_iud.robot`). Closed as stale/incorrect.

### Process note
Reviewer correctly re-derived the unit-conversion + data-safety lessons independently — high-value. Two factual errors (R5 clause, FO gap) caught by validating against ground truth rather than accepting the review verbatim. Practice working as intended: review → independent worker validation → corrected shared record.

---

## 2026-06-15 — Automated Review (06:00 AWST)

### Rules (apply immediately, no exceptions)

**R6 — Check STAT_PROCESS_TASK.TABLE_ID + WHERE_FORMULA before claiming a V→A process is testable**
Before building a N3 V→A suite, always do two checks on `STAT_PROCESS_TASK` for the target process:
1. `TABLE_ID` — the physical table the process lifts (not in `STATUS_PROCESS` itself). Verify it has data rows in the sandbox scope before proceeding.
2. `WHERE_FORMULA` — if set, resolve the variable types (`FUNC_VAR` vs `SUBQ_VAR` vs `STATUS_PROCESS_VARIABLE`) to determine if scope is fixed or dynamic. Unresolved WHERE vars = process scope unknown = not testable.
Both conditions must be satisfied before the build is started. If either fails, park with a one-line blocker (R3) and stop.

### Observations (good patterns to keep)

- **No-loop discipline**: Worker correctly parked N3 V→A daily when the sandbox data blocker was confirmed rather than grinding an unreachable test. Correct behaviour — never retry a hard blocker loop; park and document.
- **Recon scripts as design documentation**: The `n3_va_daily_recon*.py` scripts serve as reproducible evidence of the blocker (anyone can re-run them). Good practice — keep this for all parked items where the blocker is data/config dependent.

### Gaps (new)

| Gap | Owner | Priority |
|-----|-------|----------|
| N3 V→A Daily — STIM_DAY_VALUE empty; WELL_FLUID_ANALYSIS needs WHERE vars + data | Worker (when data available / SME confirms) | 🟡 Medium |
| N3 V→A Monthly — build-ready but not built | Worker | 🟡 Medium |
| `docs/automation-scorecard.md` credential pattern — recon scripts use `password='energy'` hardcoded; apply `os.environ.get('EC_DB_PWD', 'energy')` to new scripts going forward | Worker | 🟢 Low |

---

## 2026-06-15 — Catch-up Review (PRs #10, #11, #12 missed by 06:00 run)

### Rules (apply immediately, no exceptions)

**R7 — Class docstrings in page objects must match the Variables section, not contradict it**
In Robot Framework resource files, the class-level `Documentation` block is the first thing a future adapter reads. If it names a different cell/column than `${CELL_COLUMN}` / `${TARGET_DB_COLUMN}` in the Variables section, the adapter will target the wrong cell. Rule: after every per-screen edit→diff that changes the target cell, update the class docstring AND the test file docstring to match the Variables. Verify: the column name in the class doc = the column name in `${TARGET_DB_COLUMN}`. Precedent: PR #12 class doc said "C1 = ON_STREAM_HRS" but the suite correctly edited C2 = GRS_VOL (MUST-FIX).

### Observations

- **Edit→diff per screen reaffirmed (PR #12)**: Worker independently caught the derived-cell trap (C1 On Strm[hr] non-persisting on STRM sub-daily) — same trap as sub-daily PWEL. The pattern is working: never assume the first editable-looking column persists; always verify by DB diff before building the suite. Keep this as a mandatory step.
- **Systematic recon scripts as blocker evidence (PRs #10, #11)**: Both PRs include recon scripts that prove exactly why the blocker is real (co-present query + member sums for N2; nav crack sequence for PFLW). Reproducible evidence beats "I checked and it's blocked." Keep this practice.

### Gaps (updated)

| Gap | Owner | Priority |
|-----|-------|----------|
| PR #12 MUST-FIX: fix doc errors in `subdaily_gas_stream_status_page.resource` and `sub_daily_gas_stream_status_edit.robot` — class doc says C1/ON_STREAM_HRS, code correctly uses C2/GRS_VOL | Worker (next session) | ✅ Resolved — PR #12 merged 2026-06-15 |

---

## 2026-06-15 — Post-merge Rule (PR #12 conflict incident)

### Rules (apply immediately, no exceptions)

**R8 — Sync feature branch with master before every push/PR update**
Before pushing any commit to a feature branch (whether raising a new PR or pushing fixes to an existing one), always run:
```
git fetch origin master && git merge origin/master
```
Resolve any conflicts, then push. Reason: other PRs may have merged into master while your branch was open, touching the same files. Not syncing = guaranteed conflict at merge time, which blocks the merge and forces the reviewer to do manual conflict resolution. Precedent: PR #12's feature branch missed PFLW changes (merged via PRs #11 + #14) to `ec_screen_registry.md` and `pattern_n1_daily_status_grid_design.md`, causing a blocked merge and reviewer-side manual fix.

---

## 2026-06-15 — Reviewer Self-Assessment (after ~6 PRs)

_Honest record of reviewer failures and process improvements. Worker: read this to calibrate how much to trust vs independently validate reviewer findings._

### Reviewer errors this cycle (confirmed)

| Error | Impact | Root cause |
|-------|--------|-----------|
| Phantom "3 Financial Objects parked" gap posted (R) | Worker spent time validating a stale claim | Reviewer derived from doc text without checking actual filesystem — accepted stale state |
| ORA-06569 rule (R5, last clause) backwards — "ORA-06569 on real P data = worker down" | Incorrect mental model published as a rule | Reviewer inferred from first principles, didn't validate against actual error-raising code path |
| Automated 06:00 run missed PRs #10, #11, #12 | 3 PRs reviewed late; 1 had MUST-FIX that sat unmerged | Step 6 of scheduled task was ambiguous — didn't require listing ALL open PRs before starting |

### What this means for worker
- Treat reviewer rules as **high-confidence proposals**, not ground truth. When a rule feels wrong against what you see in the DB/code, validate and push back — the process is designed for this (two-way reflection).
- If you validate a reviewer claim and it's wrong, document the correction in a dated section. The worker-validated §R1 and §R5 corrections are the right model.
- Reviewer's valid-catch rate across ~6 PRs: 1 genuine MUST-FIX (PR #12 docstring), 1 stale phantom gap, 1 backwards rule. Good-but-not-100% — human merge gate stays.

### Improvements made as a result

| Improvement | Where |
|------------|-------|
| Scheduled task step 6: explicit `list_pull_requests` + confirm ALL PRs listed before starting review | `.claude/scheduled_tasks.json` |
| Version changelog added to this file | Top of this file |
| R8 (sync before push) added to CLAUDE.md as a mandatory step | `CLAUDE.md` step 2a |

### Reviewer process rules (for reviewer's own conduct)

**MR1 — Validate gaps against ground truth before publishing**
Before adding a gap entry ("X is parked / missing"), check the actual filesystem or DB — don't infer from stale doc text. If you can't verify, say "unverified" in the gap entry.

**MR2 — Flag confidence level on new rules**
When a rule is derived from code-reading only (not validated against live system), mark it `⚠️ code-derived, not live-validated`. Worker should independently verify before treating it as final.

**MR3 — Check own past entries for staleness when reviewing**
Before the PR review loop, scan open gaps in the table and mark any that are now closed. A gap that was resolved mid-session should be closed before posting new ones.

---
