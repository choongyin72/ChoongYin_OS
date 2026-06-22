# Lessons Learned — EC Automation
_Reviewed by Claude Code (reviewer session) and appended over time._
_Worker sessions: read this before starting any automation work._

> **Current rule version: v22** (R22 added 2026-06-22)
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
| v9 | R9 | PR body MUST use the EXACT 6 field headers; non-DB work → "DB ground-truth evidence: N/A (reason)" | 2026-06-15 |
| v10 | R10 | Check toolbar New/Delete enabled-state BEFORE claiming Insert/Delete; disabled = UPDATE-ONLY screen | 2026-06-15 |
| v11 | R11 | Declare CONTENT dependencies (`depends on #N`) even when the PR merges without a git conflict | 2026-06-15 |
| v12 | R12 | Shared T1/T2 edit ⇒ run canary + 1 random sibling suite and cite it; never claim "no shared-file changes" | 2026-06-15 |
| v13 | R13 | State ONE live N/N equal to the test-case count, identical across title/body/scorecard/README/SOW | 2026-06-15 |
| v14 | R14 | Skip-day check must verify BOTH < 3 new commits AND 0 open PRs; open PRs alone trigger a full review | 2026-06-17 |
| v15 | R15 | PowerShell backtick line-continuation must be the LAST character on the line — no trailing space, comment, or text | 2026-06-17 |
| v16 | R16 | Playwright bundle credentials MUST use env vars (`EC_USER`/`EC_PASS`) — never hardcode strings | 2026-06-18 |
| v17 | R17 | OV-GM T3 MUST define `<Screen> Row Should Exist` with `Wait For Elements State visible 20s` before T1 assert (lazy redraw) | 2026-06-18 |
| v18 | R18 | Files printed to a Windows console or parsed by PowerShell MUST be ASCII-only — no em-dash/smart-quotes/non-breaking-space | 2026-06-19 |
| v19 | R19 | Code-less event-log screens: use a unique per-run marker oracle via `view_count_where_should_be`; prove PHYSICAL delete = marker count 0 in BOTH the OV view AND the base table | 2026-06-20 |
| v20 | R20 | Author every bundle/recon `.py` ASCII at authoring time — a green run never catches an em-dash in a FAIL-only branch; extend the hygiene guard to flag non-ASCII statically | 2026-06-20 |
| v21 | R21 | PR-body content must match the final diff: list EVERY touched file under "Files touched", and never leave a stale "blocked/not done/pending" note for work the PR actually includes | 2026-06-20 |
| v22 | R22 | Never ship the literal `REV_TEXT='ECPR-XXXX'` placeholder; set the governing ticket, or `'ECPR-DEMO'` for demo/sandbox objects with no client ECPR | 2026-06-22 |

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

## 2026-06-16 — Automated Review (06:00 AWST, 14 open PRs #15–#28)

_No new executable rules this run. R9–R13 are documented in PR #28 (open, not yet on master) — merge PR #28 to activate them for workers._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #15 | Clear (doc/SME — no MUST-FIX from concurrent reviewer) | ✅ Clear |
| #16 | **MUST-FIX open** — body claims "not stacked on #15" but references `ec-mhm-sme.md` (only on #15's branch, not master). Worker must update body to `depends on #15`. | ⛔ Blocked |
| #17 | Clear (doc/SME) | ✅ Clear |
| #18 | Clear (doc/SME) | ✅ Clear |
| #19 | Clear (MUST-FIX from prior run resolved: all 6 body fields now present) | ✅ Clear |
| #20 | Clear (doc/SME) | ✅ Clear |
| #21 | Clear (SME capstone) | ✅ Clear |
| #22 | Clear, gated (N3 Monthly, LIVE_OK gate in place) | ✅ Clear (gated) |
| #23 | Clear (doc correction) | ✅ Clear |
| #24 | Both MUST-FIX **resolved**: body drops false "no shared-file" claim (R12); worker pushed commit `aa9306f` fixing SOW 3/3→4/4 (R13). Clearing comment posted. | ✅ Clear |
| #25 | Clear. NICE-TO-HAVE posted: skill doc says `backup_keyword_file.py` is missing — **file EXISTS** at `tmp/scripts/backup_keyword_file.py` (filesystem-verified). | ✅ Clear (NICE-TO-HAVE) |
| #26 | Clear (EC_SLOWMO infra) | ✅ Clear |
| #27 | Clear, stacked on #24 | ✅ Clear (merge after #24) |
| #28 | Concurrent reviewer PR — contains R9–R13 + review-log entry + STATUS. For user to decide which review PR to merge. | Human gate |

### Gap correction (MR1 — verify before publishing)

**`backup_keyword_file.py` EXISTS (corrects PR #28 gap entry)**
PR #28 (concurrent reviewer) has a gap entry "backup_keyword_file.py MISSING (verified absent)." This is **incorrect** — the file exists at `tmp/scripts/backup_keyword_file.py` (verified via filesystem Glob on 2026-06-16). The skill doc (PR #25) should reference it as available. The concurrent reviewer likely searched a different path. This is a case of MR1 failing in a concurrent session — corroborates the need for independent cross-check.

### Observations

- **Independent second-pass value confirmed (again):** The concurrent reviewer's run cleared PR #24 initially, then self-corrected; this run confirmed the resolution. Two passes caught the SOW 4/4 fix commit.
- **PR #16 is the only blocking MUST-FIX**: The fix is trivial (add "depends on #15" to body). Worker should resolve before next merge cycle.
- **R9–R13 in PR #28**: No conflict to create here — just note they are pending. Do NOT increment version in this file until PR #28 merges (to avoid conflict).

### Recommended merge sequence

```
#15 → #16 (after worker fixes body) → #17 → #18 → #19 → #20 → #21 → #23
→ #28 (after user approves — activates R9–R13 on master)
→ #24 → #25 → #26 → #27 (retarget to master after #24 merges)
→ #22 (user-observed live run required before merge due to LIVE_OK gate)
```

_Note: All PRs above have now been merged (2026-06-16). #22 merged with LIVE_OK gate intact. R9–R13 backfilled in this section below._

---

## 2026-06-15 — Rules R9–R13 (backfilled 2026-06-16)

_These rules were validated during the 2026-06-15 afternoon review sessions (PRs #15–#27) but were only on the PR #28 branch, which was closed rather than merged. Backfilled directly to master 2026-06-16 to unblock the worker who was already applying them._

### Rules (apply immediately, no exceptions)

**R9 — PR body MUST use the EXACT 6 field headers**
The headers must read literally: **What was built / Files touched / DB ground-truth evidence / Self-clean confirmed / Rules applied / Base branch**. Variant wording (`## What`, `## Files (GI-only delta)`, `## Verification`) fails the automated 6-field gate. For non-DB work (infra/docs), write `DB ground-truth evidence: N/A (<reason + the proof you do have>)`.
_Live-validated: #19 missing 4 fields caught and fixed; #26 and #27 had header drift._

**R10 — Check the toolbar New/Delete enabled-state BEFORE claiming or building Insert/Delete**
If New and Delete are disabled, the screen is **UPDATE-ONLY** — the (object×day) row is pre-instantiated by EC batch processes. Never relabel value set/clear as record insert/delete. Build only the edit gestures; name test cases Set/Change/Clear, not Insert/Update/Delete.
_Live-validated: IFLW (#24) was first built as "IUD" then corrected to update-only after user verified the disabled toolbar on-screen._

**R11 — Declare CONTENT dependencies, not only git-conflict ones**
If your doc/suite references a file (or keyword/table) that another OPEN PR introduces and that is not yet on master, mark **`depends on #N — merge after`** in the title/body — even when the two PRs merge without a git conflict. Verify by checking the referenced path exists on master; if it only exists on a sibling branch, the dependency is real.
_Live-validated: #16 referenced `ec-mhm-sme.md` (introduced by #15) while explicitly claiming "not stacked."_

**R12 — A shared-resource edit forces a canary + sibling run; never claim "no shared-file changes"**
Run `git diff --stat` before writing the PR body. If it lists a shared T1/T2 file (`resources/*.resource`, `libraries/DbVerify.py`), you may **not** write "no shared-file changes / no canary needed" — even for a purely additive keyword. Run the canary pack PLUS one randomly chosen sibling suite live and cite both results.
_Live-validated: #24 added `Clear Daily Status Cell` to `daily_status_grid.resource` while claiming the file was reused verbatim._

**R13 — One consistent live N/N, equal to the test-case count, everywhere**
The live pass count in the PR title, PR body, scorecard row, README, and SOW must be identical and must equal the number of test cases in the suite. Reconcile before raising the PR.
_Live-validated: #24 said "3/3" in title/body over a 4-test suite that scorecard/README/SOW called "4/4". Fixed by worker via commit `aa9306f`._

---

## 2026-06-17 — Automated Review (06:00 AWST, 4 open PRs #34–#37)

_Initially skipped by the scheduled task due to 0 new master commits — blind spot in the skip logic (see R14). Caught and reviewed manually in-session._

### Rules (apply immediately, no exceptions)

**R14 — Skip-day check must verify BOTH < 3 new commits AND 0 open PRs**
Before issuing a skip (step 5 of the scheduled task), call `list_pull_requests(state=open)`. Skip only if BOTH conditions hold: fewer than 3 new master commits AND zero open PRs. If there are open PRs, proceed to step 6 regardless of commit count — the review exists to catch PRs, not just master commits.
_Live-validated: 4 PRs (#34–#37, N1 stream siblings + gap audit) were missed by today's 06:00 run because the skip check only counted master commits (0) without checking open PRs (4)._

### Observations

- **N1 T2 reuse confirmed across ALL stream types:** PRs #35/#36/#37 prove the `daily_status_grid` T2 reuses verbatim for Oil/Water/Electrical stream siblings. The only per-screen change is in the T3 Variables section (column index, DB column, scope date, target stream name). This is the N1 pattern working as designed.
- **First non-GRS_VOL column (POWER_CONSUMPTION):** Electrical streams have no volume — PO.0066 correctly uses `POWER_CONSUMPTION` as the DB oracle column. Worker identified this from recon before building, did not assume GRS_VOL. Good recon-first discipline.
- **Stacked PR chain properly declared (R11):** #35 (base=master) → #36 (base=#35) → #37 (base=#36). Each PR explicitly declares its dependency. Clean chain.
- **Gap audit (PR #34) led directly to 3 built suites:** The audit on Jun 16 correctly prioritised PO.0001/0003/0066; all 3 were live-proven and submitted the same day. Audit-to-build turnaround = same session. High efficiency.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| N1 Tank Status (PO.0005.02 VCF) — scope/table verified (PR #34); not yet built | Worker | 🟡 Medium |
| Scheduled task step 5 — skip logic now fixed (R14 + task update this PR) | Reviewer | ✅ Fixed |
| Monthly stream/well N1 variants — not attempted | Worker | 🟢 Low |
| Folder-split (legacy flat `Production/` vs menu-mirrored `EC_Production/`) — #35/#36/#37 use flat `Production/` (consistent with existing siblings, not new menu convention) | Worker (follow-up migration) | 🟢 Low |

---

## 2026-06-18 — Automated Review (06:00 AWST, 7 open PRs #48–#54)

_No new executable rules this run. All 7 PRs clear — no MUST-FIX. R1–R15 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #48 | Clear — PO.0019 Stream Oil Comp SME doc. Oil uses WT_PCT (`C2_in`); `C1_in` (MOL_PCT) exists but is empty/read-only for oil. | ✅ Clear |
| #49 | Clear — PO.0019 Phase 1 recon. Editable cell = `C2_in` (WT_PCT). Facility = "P1 Facility Allocation". Two dirty-cell incidents transparently documented + cleaned (restore scripts committed). | ✅ Clear |
| #50 | Clear — PO.0019 live 3/3 suite. T3 correctly substitutes WT_PCT/C2_in/P1 Facility Allocation vs gas. TC03 reload-before-revert guard present. R12 N/A cited (no shared-file changes). | ✅ Clear |
| #51 | Clear — WR.0010.01 Well Gas Comp SME doc. MOL_PCT (same unit as stream gas). 9-field navigator. New interaction: analysis header row select before component grid loads. | ✅ Clear |
| #52 | Clear — WR.0010.01 Phase 1 recon. Mandatory = yellow (`rgb(252,249,192)`) fields only (Date+PU+Area+Facility). Well field optional — filling it FIRST causes 0-row result. TC03 reload + RE-SELECT documented. `WELL_SOURCE=WELL_VERSION`. | ✅ Clear |
| #53 | Clear — WR.0010.01 live 3/3 suite. `Select Analysis Row` uses JS to find header row by well name, clicks `C0_in`. TC03 `Reload And Find Target Component` = re-nav + RE-SELECT + re-cache. R12 N/A. | ✅ Clear |
| #54 | Clear — EC Object IUD spec template + `ec-object-iud-builder` skill. Read-only scripts (`resolve_ec_screen.py`, `scan_ec_screen.py`). Binary screenshots in `tmp/` acceptable. No shared resources modified. | ✅ Clear |

### Observations

- **Oil comp cell column is WT_PCT, not MOL_PCT (PO.0019):** Stream gas and well gas use MOL_PCT (`C0_in`). Oil uses WT_PCT (`C2_in`) — the MOL_PCT column exists on the oil grid but is empty/read-only. Future workers: don't probe `C1_in` for oil comp; go directly to `C2_in`.
- **Well comp has an extra interaction step (WR.0010.01):** After GO, a list of analyses loads in a header grid. The component grid only appears AFTER clicking a header row. This means TC03 (revert) must reload + RE-SELECT the analysis header row before re-caching the component cell — stream/oil don't have this step.
- **Dirty-cell transparency is working (R7):** Worker documented two recon dirty-cell incidents in #49 with cleanup restore scripts. No attempt to hide the misfires. Pattern is embedded.
- **IUD skill scaffolding (PR #54):** `ec-object-iud-builder` provides a reusable recon→build→live→bundle→PR workflow. `resolve_ec_screen.py` derives IUD metadata from DB config tables. `scan_ec_screen.py` scans live DOM read-only. Together they reduce per-screen effort for OV/TV screens.
- **Merge chains clear:** #48→#49→#50 (oil comp) and #51→#52→#53 (well gas comp) are fully independent of each other. #54 is independent. No cross-chain dependencies.

### Gaps (updated)

| Gap | Owner | Priority |
|-----|-------|----------|
| PO.0019 Stream Oil Comp — ✅ Built and merged (3/3 live) | — | ✅ Closed |
| WR.0010.01 Well Gas Comp — ✅ Built and merged (3/3 live) | — | ✅ Closed |
| WR.0010.02 Well Oil Comp — not yet attempted (similar pattern to WR.0010.01 with WT_PCT) | Worker | 🟢 Low |
| EC Object IUD (OV/TV screens) — skill + spec template now in place; first application pending | Worker | 🟡 Medium |
| N1 Tank VCF (PO.0005.02) monthly variant — not yet attempted | Worker | 🟢 Low |
| Windows Task Scheduler — one-time setup run and confirmed firing at 06:00 AWST | ✅ Confirmed | ✅ Done |

### Recommended merge sequence

```
#48 → #49 → #50  (oil comp chain — merge in order)
#51 → #52 → #53  (well gas comp chain — merge in order; independent of oil comp chain)
#54              (independent — can merge any time)
```

---

## 2026-06-18 — Automated Review (second run, 1 open PR #57)

_No new executable rules this run. Single open PR (#57) reviewed under R14 (open PR ⇒ full review regardless of commit count). R1–R15 remain current; no version bump._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #57 | Clear — ChoongYin_OS `check_scheduler.py` + `session_checkpoint.py` diagnostic tools. All 6 body fields present. Both scripts read-only (git/gh/schtasks/CSV/JSON reads); UTC→AWST `+8h` correct; self-clean holds. **NICE-TO-HAVE:** `check_scheduler.py` reads a hardcoded `tmp/schtasks_dump.csv` that is neither committed nor produced by the script (filesystem-verified: `git ls-files tmp/schtasks_dump.csv` → empty) — `FileNotFoundError` on a fresh checkout. Suggested fix: put the producing command in the docstring or generate the dump in-script. | ✅ Clear (NICE-TO-HAVE) |

### Observations

- **Diagnostic-tool reproducibility gap (MR1-style, verified):** A read-only diagnostic that depends on an out-of-band artifact (`schtasks_dump.csv`) is only reproducible if the artifact-producing step is documented in the script itself. Confirmed against the filesystem rather than inferred — the CSV is genuinely untracked. Worth folding into the canonical resume/checkpoint tooling as it matures.
- **Context-loss insurance tooling (item #3):** `session_checkpoint.py` emits a paste-ready CHECKPOINT block (git branch/ahead/sync + recent commits + tracked-dirty + open PRs) so a post-`/clear` session can fast-forward. Complements the live resume-log discipline; the canonical resume-log structure + reviewer-freshness validation are a declared follow-up.
- **Body discipline holding:** PR #57 used the exact 6 field headers including `DB ground-truth evidence — N/A (read-only, ...)` per R9. No header drift.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `check_scheduler.py` — document or in-script-generate `tmp/schtasks_dump.csv` (currently untracked; FileNotFoundError on fresh checkout) | Worker (follow-up) | 🟢 Low |
| Canonical resume-log structure + reviewer-freshness validation (declared follow-up to #57) | Worker | 🟡 Medium |
| WR.0010.02 Well Oil Comp — not yet attempted (WT_PCT variant of WR.0010.01) | Worker | 🟢 Low |
| N1 Tank VCF (PO.0005.02) monthly variant — not yet attempted | Worker | 🟢 Low |

---

## 2026-06-17 — Manual Review (7 open PRs #39–#45)

_User-triggered manual review mid-session (Windows Task Scheduler alternative being discussed). Reviewed 7 open PRs: #39 N1 Tank VCF, #40 Comp SME doc, #41 SME troubleshooting matrix, #42 Comp Phase 1 recon, #43 Comp suite (PO.0020), #44 remove GH Actions, #45 Lab lineage. One MUST-FIX found and fixed (PR #44)._

### Rules (apply immediately, no exceptions)

**R15 — PowerShell backtick line-continuation must be the LAST character on the line** ⚠️ _code-derived — caught in PR #44 diff review; not live-tested on Windows_
In PowerShell, the backtick `` ` `` only acts as a line-continuation when it is followed immediately by a newline — no trailing space, no inline comment (`# ...`), nothing. Any character after the backtick makes it a literal character, silently breaking the continuation. The `New-ScheduledTaskSettingsSet` call in `install-daily-review-task.ps1` had `-StartWhenAvailable \`   # comment` which broke the parameter chain; fixed by moving the comment to its own line above the command.

### Observations

- **N1 Tank variant (PR #39):** Tank Name is an INPUT (not textContent) so `Get Table Rows` counts 0 falsely. Two new T3-only keywords (`Tank Row Index By Name`, `Tank Grid Row Count`) solve it using JS against C1 input values. Pattern: when the row-identifier column is an editable input, resolve by input VALUE not textContent.
- **Composition is a new pattern grain (PR #43):** Per-COMPONENT rows (not object×day). Requires a component-keyed DbVerify keyword (`component_value_should_be`). The navigator has 8 fields; the grid only loads when Analysis Status + Sampling Method MATCH the analysis. Pattern is now live-proven; PO.0019 / WR.0010.01 are near-turnkey T3 reuse.
- **Ethane guard pattern (PR #43):** Asserting a SECOND untouched component after Save proves the screen did NOT silently run Normalize-on-save. Use this guard for any composition edit suite.
- **SME troubleshooting matrix (PR #41):** 22-row matrix added to ec-screen-automation skill. Every previously re-discovered EC problem now has a one-line proven fix + source citation. Reach for it before re-deriving.
- **Lab/sample lineage (PR #45):** The composition screens are the consuming end; `SAMPLE_REGISTRATION` is the upstream hub (all `LAB_*` FK→ it). P→V→A lifecycle here = same lifecycle as N3 status-process suites.
- **GH Actions reviewer dropped (PR #44):** Company policy disallows extra API spend. Daily reviews continue via `.claude/scheduled_tasks.json` (subscription-based) + Windows Task Scheduler script as an unattended alternative.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| PO.0019 Stream Oil Component Analysis — near-turnkey T3 reuse from #43 | Worker | 🟡 Medium |
| WR.0010.01 Well Gas Component Analysis — same composition pattern | Worker | 🟡 Medium |
| N1 Tank VCF (PO.0005.02) monthly variant — not yet attempted | Worker | 🟢 Low |
| Scorecard `_Last updated_` header (stale at 2026-06-15) — pre-existing | Worker | 🟢 Low |
| Windows Task Scheduler one-time setup not yet run (pending tomorrow morning) | User | 🟡 Medium |

---

## 2026-06-18 — Manual Review (PR #68, Contract Area IUD — ec-object-iud-builder first application)

_User-triggered review: PR #68 (Contract Area IUD, skill stress-test, live 4/4). Two new rules extracted from retrospective (R16, R17). Skill template (PR #69) updated to embed both. R1–R15 remain current._

### Rules (apply immediately, no exceptions)

**R16 — Playwright bundle credentials MUST use env vars — never hardcode strings**
`ec_iud_<slug>.py` (and any other Playwright bundle) must read credentials from environment variables:
`os.environ.get("EC_USER", "sysadmin")` and `os.environ.get("EC_PASS", "Sysadmin@01")`.
Never use `page.fill('#username', 'sysadmin')` or any hardcoded string — investigation scripts already follow this pattern and the bundle must match. Hardcoded credentials are unsafe to commit and break portability across environments.
_Live-validated: PR #68 Playwright bundle had hardcoded `sysadmin`; investigation scripts in the same PR used `os.environ.get`. Inconsistency caught in retrospective._

**R17 — OV-GM T3 MUST define `<Screen> Row Should Exist` with a grid-redraw wait**
On any OV-GM screen (Business Unit / PU navigator required), the OV grid redraws lazily after Save+GO. The T1 `Row Should Exist` keyword fires instantly and false-fails before the row renders — the insert actually persisted. Fix: define a T3-level wrapper keyword `<Screen> Row Should Exist` that calls `Wait For Elements State    css=<row locator>    visible    20s` before delegating to T1. Keep this wrapper in T3 only — do not modify shared T1/T2. This pattern is now embedded in the `ec-object-iud-builder` skill (PR #69).
_Live-validated: PR #68 TC02 false-failed on fresh run; OV-GM lazy redraw diagnosed and fixed in T3. Applicable to all OV-GM siblings (Transport System, Contract Type, etc.)._

### Observations

- **ec-object-iud-builder skill: first real application (Contract Area, PR #68):** Skill autonomously derived VERSIONED time scope (End Date = Start Date delete) from DB config tables, identified OV-GM as the screen type, built all 5 recon scripts + T3 + RF suite + Playwright bundle + SOW. 4/4 live PASS. Only post-hoc finding: credentials not env-var'd in the bundle (R16) and OV-GM wait wrapper not pre-known to the skill (R17). Both now embedded in skill v2 (PR #69).
- **OV-GM lazy redraw is a class-wide bug:** The wait-wrapper pattern will be needed on every OV-GM screen with a BU navigator. Worker should not rediscover it — the skill template now flags it pre-build (SOW Known Risks section) and the RF step prescribes the T3 wrapper.
- **Skill retrospective → skill update loop working:** Three N-items from PR #68 retrospective were immediately embedded in the skill file (PR #69) and in this lessons-learned entry. Future IUD builds inherit the fixes without needing a human to rediscover them. This is the intended feedback loop.

### Gaps (updated)

| Gap | Owner | Priority |
|-----|-------|----------|
| EC Object IUD — Contract Area: ✅ live 4/4, merged PR #68 | — | ✅ Closed |
| ec-object-iud-builder skill improvements (R16/R17/SOW) — ✅ embedded in skill via PR #69 | — | ✅ Closed |
| Next OV-GM IUD screen (Transport System, Contract Type, or similar) — apply updated skill | Worker | 🟡 Medium |
| WR.0010.02 Well Oil Comp — not yet attempted (WT_PCT variant of WR.0010.01) | Worker | 🟢 Low |
| `check_scheduler.py` — document or in-script-generate `tmp/schtasks_dump.csv` | Worker | 🟢 Low |
| Canonical resume-log structure + reviewer-freshness validation | Worker | 🟡 Medium |

---

## 2026-06-19 — Automated Review (06:00 AWST, 7 open PRs #71/#72/#74/#75/#76/#77/#78)

_Open PRs trigger a full review (R14) despite only 1 new master commit (#73). All 7 PRs CLEAR — zero MUST-FIX — and all 7 merged (squash). One new rule extracted (R18). R1–R17 remain current._

### Rules (apply immediately, no exceptions)

**R18 — Files printed to a Windows console or parsed by PowerShell MUST be ASCII-only** ✅ _live-validated this cycle (merge conflict) + prior precedent (#59 PowerShell parse error)_
Any file whose content is `print()`ed to a Windows `cp1252` console (Python recon/resolver tools), embedded in a console string, or parsed by PowerShell (Task Scheduler scripts) must use plain ASCII: hyphen `-` not em-dash `—`, straight quotes `'`/`"` not smart quotes, regular space not non-breaking space. Non-ASCII renders as mojibake on `cp1252` and an em-dash inside a PowerShell here-string/comment already broke the daily-review script (#59). It also creates avoidable merge friction: #76's only conflict this cycle was em-dash (#75) vs ASCII hyphen (#76) on the SAME `ec_screen_registry.json` labels. **Reserve non-ASCII for pure-Markdown docs that are never printed or parsed** (this lessons-learned file is fine). When a JSON/Python/PS1 file will be consoled or parsed, write ASCII at authoring time — don't rely on a later "tidy" pass.
_Live-validated: #76 add/add conflict resolved by keeping the ASCII-hyphen version; the worker had already converted the labels to ASCII precisely because em-dash printed as mojibake on the cp1252 console._

### Observations (good patterns to keep)

- **R16 went from prose to a machine gate (#77):** `scripts/check_bundle_hygiene.py` scans `screens/**/playwright/*.py`, FAILS (exit 1) on any bundle credential not resolved from env, and WARNs (non-gating) on `investigation/` recon scripts — the correct severity split for R16's bundle scope. `main()` returns 1 and `sys.exit(main())` propagates it, so it genuinely gates. The `ENV_OK` skip-list prevents false positives on `os.environ.get('EC_USER','sysadmin')` default lines (verified: PASS on all bundles). #78 then wired it into the skill's Step-5 verify chain — a rule is now enforced, not just documented. This is the model: when a rule can be mechanically checked, build the checker and wire it into the build loop.
- **R16 fully remediated (#72):** all 5 canonical bundles (Contract Area / Equipment / Bank / Language / MIME) now read `EC_USER`/`EC_PASS` from env. Sandbox default `sysadmin`/`sysadmin` is the verified working login for the `ap-f0a7g341jn6d.corp.quorumsoftware.com` env (distinct from plutodev's `Sysadmin@01`) — live re-run ALL PASS, 0 AUTOTEST residue.
- **Registry made machine-queryable (#75/#76):** `ec_screen_registry.json` curates 7 IUD families (OV / OV-custom-URL / OV-GM-groupmodel / OV-GM-BU-gated / OV-GM-popup / TV / PC) with class_type/time_scope/discriminator/golden_exemplar/page_object/t2/members. `resolve_ec_screen.py` now prints a CLONE suggestion (REGISTRY MATCH → exact exemplar; else candidate families by CLASS_TYPE for the live scan to disambiguate). Read-only, degrades quietly if the JSON is absent. Turns "which screen do I clone?" from a manual scan into an automatic hint.
- **Recon scanner now handles gated screens (#74):** `scan_ec_screen.py` fills ONLY yellow/mandatory nav dropdowns (over-filling white fields empties the grid — finder-first rule), in group order, + GO, so OV-GM/BU-gated grids actually load before capture. Each dd fill is try/except-guarded; still read-only (never Saves). Closes the gap that forced a hand-written recon on Contract Area.

### Reviewer process note (stacked-PR add/add conflict)

- **Content-stacked PRs that both ADD the same new file will add/add-conflict after the parent squash-merges.** #76 was stacked on #75 and carried its own copy of `ec_screen_registry.json`; once #75 squash-merged to master, #76's identical-but-for-em-dash copy conflicted. Resolution that worked: `git checkout --ours` on the child branch (the child's version was the intended final), re-validate the JSON, commit the merge, push, retry the squash. For future stacks, prefer a `git rebase` of the child onto the merged parent, or have the child only ADD files that the parent does not.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `scan_ec_screen.py` still hardcodes `sysadmin` login (`tmp/scripts/`, outside R16 bundle scope + outside the hygiene-guard glob) — could import `tmp/scripts/ec_session.py` | Worker | 🟢 Low |
| `check_bundle_hygiene.py` docstring says it scans `ec_iud_*.py` but the glob is `**/playwright/*.py` (broader) — align docstring to glob | Worker | 🟢 Low |
| Next OV-GM IUD screen (Transport System / Contract Type) — apply skill + new resolver/scan tooling | Worker | 🟡 Medium |
| WR.0010.02 Well Oil Comp — not yet attempted (WT_PCT variant of WR.0010.01) | Worker | 🟢 Low |

---

## 2026-06-20 — Automated Review (06:00 AWST, 3 open PRs #83/#84/#85)

_Open PRs trigger a full review (R14). All 3 CLEAR — zero MUST-FIX — all 3 squash-merged. Two new rules (R19, R20). R1–R18 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #83 | Clear — Carrier IUD, plain OV (Cargo Objects). 1st Cargo Objects screen. Toolbar New/Delete enabled → full IUD. R17 correctly N/A (plain-OV family, no groupmodel). Live 4/4; `OV_CARRIER` residue 0 ×2. NICE-TO-HAVE: R18 em-dash in bundle FAIL-branch print string + recon-script docstrings. | ✅ Clear (NICE-TO-HAVE) |
| #84 | Clear — Alarms IUD, **NEW EVENT-LOG pattern** (code-less event rows, marker oracle, physical delete). `view_count_where_should_be` confirmed pre-existing on master (not a shared-file edit → R12 N/A holds). Live 4/4; residue 0 in both `DV_ALARMS` and base `FCTY_DAY_ALARM`. NICE-TO-HAVE: R18 em-dash in bundle FAIL string; base-table assertion is recon-only (not in-suite). | ✅ Clear (NICE-TO-HAVE) |
| #85 | Clear — Analysis Point IUD, OV-GM 3-level cascade (Laboratory Objects). 1st Laboratory Objects screen. **R17 wrapper present and correct** (`Analysis Point Row Should Exist` waits `visible 20s` before T1 assert). Live 4/4; `OV_ANALYSIS_POINT` residue 0 ×2. add/add conflict on `automation-scorecard.md` (vs #83, same insert region) resolved keeping BOTH rows. NICE-TO-HAVE: R18 em-dash in bundle FAIL string. | ✅ Clear (NICE-TO-HAVE) |

### Rules (apply immediately, no exceptions)

**R19 — Code-less event-log screens use a marker oracle + dual-location physical-delete proof** ✅ _live-validated (PR #84, Alarms, 4/4)_
For event-log / inline-grid screens that render a `DATA`/DAY class as addable rows with **no object code** (rows identified only by a free-text cell — e.g. Alarms `FCTY_DAY_ALARM`, REASON), the DB oracle MUST be a unique per-run marker value (`AUTOTEST_<screen>_<timestamp>` written into that free-text column) asserted via `view_count_where_should_be <view> <column> <marker> <n>`. This makes INSERT/UPDATE/DELETE count-delta-safe against shared seed data (never rely on absolute row counts). For screens whose delete is **PHYSICAL** (not date-effective End=Start), prove deletion two ways: marker count = 0 in the OV **view** AND in the **base table** — a view can mask base-table residue. Distinguish at recon time: PHYSICAL-delete screens have no End Date column; do not relabel them as End-Date deletes (cf. R10). Golden exemplar registered as the `EVENT_LOG` family (`ec_screen_registry.json`); next clone = Reported Alarms (`SR_MD_REPORTED_ALARMS`, same base table).

**R20 — Author bundle/recon `.py` ASCII at authoring time; a green run cannot enforce R18** ✅ _live-validated (3-for-3 recurrence this cycle)_ ⚠️ _the static-guard extension is code-derived — not yet built_
R18 (ASCII-only for console-printed/PowerShell-parsed files) cannot be left to a passing test run, because the most common violation hides where a green run never executes: the **em-dash in the FAIL-only branch** of a bundle's delete-result string (`results['delete'] = 'PASS' if ... else 'FAIL — still present'`, then `print()`ed). It ships silently and raises `UnicodeEncodeError` on a cp1252 (redirected/captured) stream the first time a regression actually trips the FAIL path — i.e. the proof bundle crashes instead of reporting the failure, exactly when the diagnostic matters. All three IUD bundles this cycle (#83/#84/#85) shipped the identical em-dash because the `ec-object-iud-builder` bundle template emits it by default. Therefore: (1) **never** write a non-ASCII char in any `screens/**/playwright/*.py` or `investigation/*.py` file, including docstrings/comments and untaken branches — these files are not "pure-Markdown docs" and are out of R18's exemption; (2) sanitise the skill's bundle/recon templates so future files are born ASCII-clean; (3) extend `scripts/check_bundle_hygiene.py` to FAIL on any non-ASCII byte in those globs — a static scan, not a runtime check — and wire it into the skill Step-5 verify next to the existing R16 credential gate.

### Observations (good patterns to keep)

- **First-of-kind coverage, three sections in one cycle:** Carrier (1st Cargo Objects), Alarms (1st event-log), Analysis Point (1st Laboratory Objects) — all built autonomously via `ec-object-iud-builder`, all live 4/4 first try. The skill's recon→build→live→DB-verify→bundle→PR loop is generalising cleanly across screen types.
- **R17 wrapper now applied pre-emptively (PR #85):** the OV-GM lazy-redraw wrapper was present in the T3 from the first run (not rediscovered after a false-fail) — the R17 → skill-template feedback loop from the Contract Area retrospective worked as intended.
- **Append-only discipline held under a real cross-PR collision:** #83 and #85 independently added a Section-Coverage row at the same scorecard line; the merge kept both rows with no data loss. This is exactly the append-only conflict R18's reviewer note (last cycle) anticipated for content-stacked PRs.
- **OV-GM 3-level cascade nav gotcha (PR #85, worth remembering):** cascade nav dds sit at C:1–C:3 (Date at C:0) so they need `Select EC Dropdown Option`, not `Set Navigator Filter`; and the groupmodel **link fields (Op PU/Area/Facility) are required for grid visibility even when not yellow** — set them = nav scope or the inserted row never lists. This is the line between a "clean" settable OV-GM and a parked one (cf. Pipeline).

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `ec-object-iud-builder` bundle/recon templates emit em-dashes by default — sanitise to ASCII (R20 root cause) | Worker | 🟡 Medium |
| Extend `check_bundle_hygiene.py` to statically FAIL on non-ASCII in `screens/**/playwright/*.py` + `investigation/*.py` (R20) | Worker | 🟡 Medium |
| Reported Alarms (`SR_MD_REPORTED_ALARMS`) — clone the new EVENT_LOG family (same base table as Alarms) | Worker | 🟢 Low |
| #84 base-table (`FCTY_DAY_ALARM`) zero-residue check is recon-only — fold a base-table count assertion into the suite | Worker | 🟢 Low |
| Next OV-GM IUD screen (Transport System / Contract Type) — apply skill + new tooling | Worker | 🟡 Medium |
| WR.0010.02 Well Oil Comp — not yet attempted (WT_PCT variant of WR.0010.01) | Worker | 🟢 Low |

---

## 2026-06-20 — Automated Review (14:00 AWST, 1 open PR #87)

_Open PR triggers a full review (R14). #87 CLEAR — no MUST-FIX — squash-merged (1ae4960). One new rule (R21). R1–R20 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #87 | Clear — worker actioning #86's two R20 Medium gaps: ASCII-normalised 40 bundle/recon `.py` + extended `check_bundle_hygiene.py` with a static non-ASCII gate over `playwright/*.py` + `investigation/*.py`. Verified on the PR head tree (worktree off `pr87`, merge-base = master so R8 holds): guard → `RESULT: PASS (R16 + R20)`, exit 0, scanned 48 bundles + 121 recon; ripgrep `[^\x00-\x7F]` over both globs → 0 matches. **R20's static-guard is now built and live-validated** (was code-derived/"not yet built" at #86) — the two #86 Medium gaps are closed. NICE-TO-HAVE: PR-body content drift (see R21). | ✅ Clear (NICE-TO-HAVE) |

### Rules (apply immediately, no exceptions)

**R21 — PR-body content must match the final diff (not just carry the 6 headers)** ✅ _live-validated (PR #87, verified against the actual diff)_
R9 mandates the six field *headers* exist; R21 mandates their *content* is true to the diff that's being merged. Two concrete failure modes, both seen in #87 (the change was correct — the body was not): (1) **"Files touched" must enumerate every file in the diff** — #87 edited `.claude/skills/ec-object-iud-builder/SKILL.md` but omitted it from the list, so a reviewer parsing the body alone would miss a skill-definition change; (2) **never leave a stale "blocked / not done / pending" note for work the PR actually includes** — #87's "Not done (blocked)" claimed the SKILL.md Step-5 wiring was still pending due to the auto-mode self-modification classifier, yet that exact edit was present and complete in the diff. Before pushing, re-diff (`git diff --stat origin/master...HEAD`) and reconcile the body against it: add any missing file, and delete or correct any "blocked/pending" line that the final diff has since resolved. A body that *under-claims* is still a defect — it erodes the reviewer's ability to trust the body as the parse surface.

### Observations (good patterns to keep)

- **Reviewer-flagged gaps closed in one cycle:** #86 logged two Medium gaps (sanitise the builder templates' em-dashes; extend the hygiene guard to a static non-ASCII scan) and marked R20's guard "code-derived — not yet built." #87 closed both the next cycle and the guard is now live-validated (PASS over 48+121 files). The gaps-table → next-PR loop is working.
- **Hygiene guard now enforces R16 + R20 together:** `check_bundle_hygiene.py` is a single static gate (no live env needed) wired into skill Step-5; reviewer reproduced PASS independently. This is the right shape for a CI-style guard — deterministic, offline, fast.
- **The em-dash root cause is fixed at the source:** normalising the 40 already-merged exemplars (not just the guard) means future clones from Bank/Language/etc. are born ASCII-clean, so the guard stays green rather than red against legacy debt.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `tmp/scripts/ascii_sanitise_bundles.py` and `tmp/scripts/ec_session.py` sit outside the hygiene-guard glob (`tmp/scripts/`, not `screens/**`) — one-off/shared tooling not ASCII-gated; acceptable but note if promoted into `scripts/` | Worker | 🟢 Low |
| PR-body content fidelity (R21) is reviewer-caught, not machine-checked — a pre-push `git diff --stat` reconcile step in the worker routine would catch it earlier | Worker | 🟢 Low |
| Carry-over from #86 (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

---

## 2026-06-20 — Manual Review (PR #89, grid-menu deep-dive)

_1 open PR (#89) reviewed after the scheduled 14:00 AWST run did not fire. PR CLEAR — squash-merged. One reviewer error self-corrected (see MR4 below). No new executable rules._

### PR Status

| PR | Finding | Status |
|----|---------|--------|
| #89 | Clear — NEW additive `grid_menu.resource` (8 T2 keywords: filtering + reset-personalisation), `grid_menu_smoke.robot` (live 4/4 read-only, self-cleaning teardown), `ec-table-column-menu.md` (all 8 [V]). R12 N/A correct (brand-new file, nothing imports it). DB ground-truth N/A justified (view-only). 6 body fields present. NICE-TO-HAVE posted then immediately self-corrected (reviewer error — see MR4). | ✅ Clear — merged |

### Reviewer process rules (added)

**MR4 — Re-read `lessons-learned.md` after any context compaction; never trust a pre-compaction cached read**
After context compression the reviewer's in-memory version of `lessons-learned.md` may be stale: new rules added by earlier sessions in the same day will be absent from the cached summary. In this session the reviewer saw v18 (pre-compaction) while the file was at v21 (R19/R20/R21 added by the 06:00 and 14:00 AWST runs today). This caused the reviewer to flag R20/R21 in PR #89 as "phantom rules" — a false NICE-TO-HAVE that had to be publicly corrected with a follow-up comment. Fix: after resuming from compaction, ALWAYS open `docs/lessons-learned.md` explicitly with the Read tool before writing any review comment that references rule numbers. Do not infer the current version from the compaction summary.

### Gaps (updated)

| Gap | Owner | Priority |
|-----|-------|----------|
| grid_menu.resource is brand-new and not yet imported by any suite — first real use will be the next filtering-heavy screen | Worker | 🟢 Low |
| Carry-over from #88 (still open): Reported Alarms EVENT_LOG clone; #84 base-table count; next OV-GM IUD; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

---

## 2026-06-22 — Automated Review (06:00 AWST, 2 open PRs #93/#94)

_Open PRs trigger a full review (R14). Both CLEAR — zero MUST-FIX — both squash-merged. One new rule (R22). R1–R21 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #94 | Clear (low effort — single-line, non-logic). Adds Step 15 to `.claude/review-prompt.txt`: the reviewer must remove its own `C:/tmp/wt-review-*` worktrees at session end (even on skip runs) so a stale worktree holding `master` no longer blocks the Worker's `git checkout master`. ASCII-only (R18), Files-touched maps 1:1 to the diff (R21), 6 body fields present. Real reproducible blocker fixed. | ✅ Clear — merged |
| #93 | Clear (HIGH effort — SQL logic + 2 skills + 30+ scripts). ECIS Excel-upload: re-runnable config/scheduler SQL, manually-verified live DB demo, page-broken evidence doc, `ec-sql-script-builder` + `ecis-excel-upload-builder` skills. Idempotency pattern correct (`UPDATE; IF SQL%ROWCOUNT=0 THEN INSERT`, no MERGE). R12 N/A correct (no shared T1/T2/DbVerify edits). R18/R20 clean across all 30+ workstream scripts. Known automation gap (`upload -> RUN NOW` timing flakiness) transparently disclosed, root cause unconfirmed — does NOT gate (deliverable is the SQL+skills+manual-verified demo, no over-claim of full automation; correct R3-style blocker handling). **2 NICE-TO-HAVE** (R18 em-dash in the skill's `sql_idempotency_check.py` print strings — one on the happy path; `REV_TEXT='ECPR-XXXX'` placeholder → R22). | ✅ Clear (NICE-TO-HAVE) — merged |

### Rules (apply immediately, no exceptions)

**R22 — Never ship the literal `REV_TEXT='ECPR-XXXX'` placeholder** ⚠️ _code-derived — caught in PR #93 diff review; not live-validated_
Every DB script sets `REV_TEXT` for audit ([[feedback_db_script_rerunnable_revtext]] / the standing user directive). The value MUST be a real, meaningful ticket — the **governing ECPR** for client work, or `'ECPR-DEMO'` for demo/sandbox objects that have no client ECPR. Never leave the template placeholder `'ECPR-XXXX'` in a script that will actually run: a run then writes a non-meaningful audit value, which is worse than no audit because it looks intentional. PR #93's create SQL shipped `v_rev constant varchar2(30) := 'ECPR-XXXX'` for the demo objects `CLAUDE_WELL_TEST`/`ClaudeExcelImport`; the skill's own checklist already prescribes the real-ticket-or-`ECPR-DEMO` rule — follow it before raising the PR. Before pushing any `.sql`, grep for `ECPR-XXXX` and replace it.

### Observations (good patterns to keep)

- **R18/R20 applied to net-new workstream scripts:** all 30+ `workstreams/ecis-excel-upload/scripts/*.py` are ASCII-clean — the worker carried the ASCII-at-authoring discipline (R20) into a non-`screens/` tree without being told. Only the skill utility slipped (see gap below).
- **Idempotency proven the right way:** `delete -> create -> create-again = identical counts, no dups` is the correct re-runnability proof for a config-build script, and the `sql_idempotency_check.py` harness re-runs the block twice and diffs counts — exactly the standing re-runnable directive made mechanical. (Fix its 2 em-dashes and it is a clean reusable template.)
- **Transparent automation-gap disclosure:** #93 explicitly told the reviewer "do not treat as fully-automated" and documented the `upload -> RUN NOW` flakiness as a KNOWN OPEN ISSUE with an *unconfirmed* root cause (no fabricated cause — honest reporting). This is the correct way to ship a partially-working capability: prove what works (manual + DB-verified), park what doesn't (R3), never over-claim.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `scripts/check_bundle_hygiene.py` ASCII gate globs only `screens/**/playwright/*.py` + `screens/**/investigation/*.py` — console-printed Python OUTSIDE the screens tree (`.claude/skills/**/*.py`, `workstreams/**/scripts/*.py`) is NOT machine-checked. This is exactly how the R18 em-dash in `sql_idempotency_check.py` slipped through. Extend the static non-ASCII scan to cover those globs (verified: guard source has no `skills`/`workstreams` glob). | Worker | 🟡 Medium |
| `sql_idempotency_check.py` — 2 em-dashes (U+2014) in `print()` strings (R18); one on the PASS/happy path | Worker | 🟢 Low |
| `ec-sql-script-builder` create-SQL ships `REV_TEXT='ECPR-XXXX'` placeholder for demo objects — change to `'ECPR-DEMO'` (R22) | Worker | 🟢 Low |
| ECIS `upload -> RUN NOW` automation timing flakiness — root cause unconfirmed; documented as KNOWN OPEN ISSUE in README + skill | Worker (when resumed) | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

---

## 2026-06-22 — Automated Review (14:00 AWST, 2 open PRs #96/#97)

_Open PRs trigger a full review (R14). Both CLEAR — zero MUST-FIX — both squash-merged. **No new executable rules** — R1–R22 cover every finding; version stays v22._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #97 | Clear (low effort — `.claude/review-prompt.txt` process reorder, no executable logic). The change is sound: it moves the reviewer's branch creation ahead of all doc edits and adds a MANDATORY MR4 re-read, a pre-flight discard of stale reviewer-owned files, a review-log dedup guard, a post-merge review-branch sync, and a final master clean-up (step 18) — directly fixing the dirty-working-tree blocker that stops the Worker's `git checkout master`. Adopted the ordering for this run. **NICE-TO-HAVE (R21):** title/"Files touched" say *"moved branch creation from step 12 to step 9; renumbered steps 10–14"* but the diff moves it to **step 5** and renumbers through **18**, adding the four steps above — body materially under-claims the change. | ✅ Clear (NICE-TO-HAVE) — merged |
| #96 | Clear (HIGH effort — SQL config logic, ECPR-31089 R_PLU_NOPTA + ECPR-31090 R_SCA_NOPTA email-send enablement). Both `.sql` files: idempotent upsert (`UPDATE; IF SQL%ROWCOUNT=0 THEN INSERT`), **non-destructive (0 `DELETE` statements, grep-verified)**, `REV_TEXT` driven by `lv_rev_text := 'ECPR-31089'`/`'ECPR-31090'` — real governing tickets, **no `ECPR-XXXX` placeholder anywhere (R22 clean)**, ASCII-clean (R18/R20, Grep `[^\x00-\x7F]` → no matches). R8 merge deferred per body but every file is a NEW addition in an isolated `workstreams/ecsr-35329-35330-nopta-email/` tree → GitHub `MERGEABLE`, conflict-free. DB ground-truth (MESSAGE_OUT 407/408 = TEXT, recipient `prodreporting@woodside.com`, `TRANSMIT_STATUS='ERROR'` by-design no-SMTP) taken as worker-attested, not reviewer-re-run on the live DB. | ✅ Clear — merged |

### Observations (good patterns to keep)

- **R22 honoured on first client SQL since it was minted:** R22 (no `ECPR-XXXX` placeholder) was extracted only this morning from PR #93's demo SQL; PR #96 — the next SQL delivery — set the real governing tickets (`ECPR-31089`/`ECPR-31090`) on every DML via a single `lv_rev_text` constant. The standing re-runnable+REV_TEXT directive is now reflexive, not reminded.
- **Non-destructive format conversion done right:** the Pluto NOPTA SQL converts REPORT/XML → TEXT by *demoting* the old format and adding the TEXT default in place (0 `DELETE`s), so the migration is reversible and idempotent on re-run — the correct shape for a live client-config change (cf. R3 blocker handling / [[feedback_db_script_rerunnable_revtext]]).
- **Reviewer self-isolation via worktree (R-process):** this run consumed PR #97's own fix — created the review-doc branch in a clean `C:/tmp/wt-review-2026-06-22-1400` worktree off `origin/master` and left the Worker's dirty main checkout (27 unrelated uncommitted files) entirely untouched. The merged review-prompt now mandates this branch-before-edits ordering; this is the first run to follow it.

### Reviewer process note (local-checkout-on-merge)

- **`gh pr merge --delete-branch` while standing on the merged branch fails locally, not remotely.** Merging #96 (whose head branch was the current checkout) succeeded on the remote (`218eb97`) but `gh` then aborted the local `git checkout master` because the shared working tree was dirty (`STATUS.md`, `docs/lessons-learned.md`, `docs/automation-scorecard.md`, `docs/review-log.md` modified). The remote merge is unaffected — verify with `gh pr view <n> --json state,mergedAt` rather than trusting the CLI's non-zero exit. PR #97's new step 18 (final master clean-up) is the durable fix; until then, do reviewer doc work in an isolated worktree (as this run did).

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `.claude/review-prompt.txt` step-6 format string still embeds an em-dash (`skipped — no new work`) and the title carried one — harmless (the prompt file is read by Claude, not console-printed/PS-parsed, so outside R18 scope) but worth normalising on the next prompt edit for consistency | Reviewer | 🟢 Low |
| Carry-over from #93/#95 (still open): extend the `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py`; fix `sql_idempotency_check.py` em-dashes; change `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` → `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

---

## 2026-06-23 — Automated Review (06:00 AWST, 1 open PR #100 — STANDING/DRAFT)

_Open PR triggers a full review (R14). The only open PR is the long-lived **STANDING/DRAFT** EC Screen Deep-Dive PR (#100) on the Worker's permanent branch. Reviewed at the branch tip — **CLEAR, no MUST-FIX, NOT merged** (owner-merge-only at milestones by design). **No new executable rules** — R1–R22 cover every finding; version stays **v22**._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #100 | Clear — STANDING/DRAFT EC Screen Deep-Dive program (12/1457 screens; +2260/-21; 32 files). The deterministic runner `tools/deep-dive-scheduler/run_ec_screen_learn.py` is read-only on the live EC (recon + in-session `openOnlineHelp()` only — no Save, no DB mutation), no-LLM/no-improvising, hard-timeout-guarded so it cannot hang, env-var credentials (R16), and `_ascii()`-sanitises Help text so committed notes are ASCII-clean (R18/R20 — verified). Partials honestly marked `[~]` with the missing component named (R3 — e.g. CO.0018 records "(no class resolved from URL/LABEL)" rather than fabricating a binding). Metadata-only DB queries → no ORA-06569. **NOT merged** — it is a draft the owner merges at milestones; the reviewer never auto-merges it. 3 NICE-TO-HAVE posted (see below). | ✅ Clear (NICE-TO-HAVE) — **left open (owner-merge-only)** |

### Observations (good patterns to keep)

- **Deterministic runner beats an LLM-improvising one for an unattended program.** The rewrite runs the *proven* recipe directly in Python (read CHECKLIST → metadata DB resolve → best-effort Help → write note → commit/push on an isolated worktree) with a per-screen try/except and timeouts, so it can never flail (the prior LLM version logged ORA-06569 ×24, timeouts, 30 min, 0 commits). For repeatable unattended capture, hard-code the verified gestures; reserve the model for genuinely novel screens.
- **Honest partial marking is the right shape for a coverage program.** `[~]` + the named missing component (DB binding and/or Help) + a note that still records whatever WAS captured is far more useful than skipping the screen or fabricating a binding. CO.0018 (Help captured, class unresolved) is the model — transparent and resumable (R3).
- **Read-only by construction.** The runner has no Save/write path against the live EC and queries only metadata tables (`business_function`, `class_cnfg`, `class_property_cnfg`, `all_views`) — so it cannot dirty shared sandbox state, the recurring risk on write-capable recon (cf. the probe-write self-clean lessons).

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `tools/deep-dive-scheduler/run_ec_screen_learn.py` has functional non-ASCII source bytes (verified lines 60, 120-121, 160 — em-dash in the `pick_screens` regex + `_ascii` map keys + em-dash written to CHECKLIST). Never `print()`ed → no cp1252 crash, but R20 asks for ASCII-at-authoring: express the map keys + regex alternation as `\uXXXX` escapes. File is OUTSIDE the `check_bundle_hygiene.py` glob → not machine-checked | Worker | 🟢 Low |
| Commit-message label "{done_partial} DB-only" is inaccurate — `done_partial` counts ANY partial (missing DB **or** Help; e.g. CO.0018 is Help-present/DB-missing). Use the neutral word "partial" to avoid a misleading audit trail | Worker | 🟢 Low |
| PR #100 body header drift from the exact R9 headers ("What this is/Files/Evidence" vs "What was built/Files touched/DB ground-truth evidence/Self-clean confirmed") — harmless for a never-auto-merged draft; align at the next milestone edit | Worker | 🟢 Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (this run adds `tools/**` to the list); fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` → `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

### Reviewer process note (dirty main checkout on a permanent Worker branch)

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's **permanent** branch `feature/ec-screen-deepdive` with an active, dirty working tree (the deep-dive autopilot runs there). Steps 4b/5/18 of the review prompt assume operating on `master` in the main checkout — that is **unsafe here** (it would stash/disrupt the parallel Worker session). Following the 2026-06-22 14:00 precedent, ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-23-0600` worktree off `origin/master`; the main checkout was never touched. Final master clean-up (step 18) was scoped to verifying the main checkout was left exactly as the Worker had it, NOT forcing `git checkout master`.

---
