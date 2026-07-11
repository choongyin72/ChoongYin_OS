# Lessons Learned — EC Automation
_Reviewed by Claude Code (reviewer session) and appended over time._
_Worker sessions: read this before starting any automation work._

> **Current rule version: v29** (R29 added 2026-07-06)
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
| v23 | R23 | A long-lived/permanent Worker branch must keep reviewer-owned append-only docs in sync — `git diff origin/master...HEAD` must show NO `-` lines on lessons-learned.md / review-log.md / automation-scorecard.md / STATUS.md | 2026-06-23 |
| v24 | R24 | Pushing from a detached/throwaway worktree MUST use `push origin HEAD:refs/heads/<branch>` -- a bare `push origin <branch>` resolves to the shared local branch ref (another worktree's tip), NOT the detached HEAD | 2026-06-25 |
| v25 | R25 | When any tool/MCP/connection breaks, OWN the troubleshooting -- diagnose, give actionable fix steps, keep moving; never say "I can't" without following up with "here is how to fix it" | 2026-06-25 |
| v26 | R26 | Every EC Object IUD PR is gated against the 19-item `docs/IUD-DELIVERABLE-CHECKLIST.md`; the bundle MUST carry a ticked `CHECKLIST.md`; reviewer spot-checks SUBSTANCE not just ticks; a missing/failing deliverable ⇒ MUST-FIX | 2026-06-28 |
| v27 | R27 | A squash-style milestone merge of a permanent standing-draft branch breaks shared history; rebase the continuation onto master (or use `git merge --no-ff`) before the branch's next milestone push, or expect real file conflicts | 2026-07-03 |
| v28 | R28 | `CLAUDE.md` is auto-injected into every session's context (unlike other mandatory-read docs) — every review run checks `wc -l CLAUDE.md`; >200 lines = NICE-TO-HAVE (name pruning candidates), >400 lines = MUST-FIX | 2026-07-02 |
| v29 | R29 | A scheduled/unattended runner MUST be sync/hash-verified against the branch tip before every run — a stale executing copy silently mass-produces artifacts in a superseded format while the commit history claims the fix is live | 2026-07-06 |

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

## 2026-06-23 — Automated Review (14:00 AWST, 1 open PR #103 — STANDING/DRAFT)

_Open PR triggers a full review (R14). The only open PR is the re-opened **STANDING/DRAFT** EC Screen Deep-Dive PR (#103) on the Worker's permanent branch — #100 (the prior draft) was owner-milestone-merged (`661e90b`) and the 06:00 review merged via #101 (`56c58c1`). Reviewed #103 at branch tip: **NOT merged** (owner-merge-only by design). **1 MUST-FIX** (stale reviewer-owned docs — clobber risk). **One new rule (R23).** R1–R22 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #103 | **MUST-FIX** — the branch is behind master on reviewer-owned append-only docs. The only new commit since 06:00 is `2cc15cf` (merge-log + re-open standing draft), and its re-sync was taken from a master state *before* #101 (06:00 review) landed, so `git diff --stat origin/master...HEAD` shows `docs/lessons-learned.md \| 32 ---` and `docs/review-log.md \| 1 -`. Those `-` lines are the entire **2026-06-23 06:00 review (#101)** entry — merging #103 as-is would clobber it. Deep-dive *content* (read-only metadata recon + Help capture, ASCII notes, honest `[~]` partials) was already reviewed CLEAR at 06:00; no new content findings. NICE-TO-HAVE carry-overs: R9 header drift (harmless for a never-auto-merged draft); runner-source non-ASCII (R20, `tools/**`); `"{done_partial} DB-only"` label → `"partial"`. | ⛔ MUST-FIX open — **left open (owner-merge-only)** |

### Rules (apply immediately, no exceptions)

**R23 — A long-lived/permanent Worker branch must keep reviewer-owned append-only docs in sync** ✅ _live-validated (PR #103 diff vs master)_
The reviewer owns four append-only files: `docs/lessons-learned.md`, `docs/review-log.md`, `docs/automation-scorecard.md`, and `STATUS.md`. On a normal short-lived feature branch R8 (sync before push) is enough, but a **permanent / long-lived** branch (e.g. `feature/ec-screen-deepdive`, which is never deleted and is re-opened as a fresh draft after each milestone merge) silently drifts behind master on these files every time the reviewer appends an entry. If the branch is then milestone-merged, the squash **reverts** the reviewer entries it never re-absorbed. Therefore: before any milestone push/merge of a permanent branch, `git fetch origin master && git merge origin/master`, and verify `git diff --stat origin/master...HEAD` shows **NO `-` (deletion) lines** on any of the four reviewer-owned files — a `-` line on them is a clobber-on-merge defect, not a real change. **Better still:** do not track local edits to these four files on a permanent Worker branch at all — let the reviewer own them on master so they can never drift.
_Live-validated: #103's `2cc15cf` re-sync (taken pre-#101) presented `lessons-learned.md -32` + `review-log.md -1` = the full 06:00 review entry; merging as-is would have deleted #101's record._

### Observations (good patterns to keep)

- **The standing-draft model is working as intended, with one sharp edge.** Keeping the permanent branch behind a never-auto-merged DRAFT (owner merges at milestones) correctly stops the reviewer from auto-merging accumulating learning notes. The one edge — reviewer-owned docs drifting on the long-lived branch (R23) — is structural, not a one-off; the durable fix is to keep those four files off the permanent branch entirely.
- **Reviewer self-isolation held again.** This run created `review/feedback-2026-06-23-1400` in an isolated `C:/tmp/wt-review-2026-06-23-1400` worktree off `origin/master`; the Worker's dirty permanent checkout (and its `wt-ec-learn` runner worktree) were never touched. The `wt-ec-learn` worktree is the Worker's runner workspace — NOT a `wt-review-*` reviewer worktree — so step 17 cleanup correctly left it alone.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| **#103 MUST-FIX:** re-sync the permanent branch with master (`git merge origin/master`) before the owner milestone-merges, OR stop carrying the four reviewer-owned docs on it (R23) | Worker | 🔴 High |
| Runner source `run_ec_screen_learn.py` non-ASCII (R20) + outside the hygiene glob (`tools/**` not scanned); `"{done_partial} DB-only"` commit label should read `"partial"` | Worker | 🟢 Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` → `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

---


## 2026-06-24 - Automated Review (06:00 AWST, 1 open PR #103, STANDING/DRAFT)

_Open PR triggers a full review (R14). #103's head (`c32cec2`) is unchanged since the 2026-06-23 14:00 re-verify that cleared it - no new pushed content this run. **Re-confirmed CLEAR; NOT merged** (owner-merge-only standing draft, still DRAFT). **No new executable rules - version stays v23.** R1-R23 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #103 | Clear (re-confirmation). Head `c32cec2` is byte-identical to the commit cleared at the 2026-06-23 14:00 re-verify - no new pushed content (`git log c32cec2..origin/feature/ec-screen-deepdive` empty; PR `headRefOid` = `c32cec2`). **R23 stays satisfied:** `git diff --stat origin/master...origin/feature/ec-screen-deepdive` lists only the 8 deep-dive note/doc files, with ZERO `-` (deletion) lines on any of the four reviewer-owned files - the 14:00 MUST-FIX remains resolved. Two prior NICE-TO-HAVEs are now CLOSED in-PR (commit `1312bcc`, which is an ancestor of `c32cec2`): the runner `run_ec_screen_learn.py` is ASCII-clean (`rg [^\x00-\x7F]` -> 0 matches), and the `"DB-only"` commit label now reads `"partial"` (`run_ec_screen_learn.py:198`). **NOT merged** (owner-merge-only standing draft, still DRAFT). | OK Clear (NICE-TO-HAVE) - left open (owner-merge-only) |

### Observations (good patterns to keep)

- **An unchanged open-PR head is a re-confirmation, not a re-review of the same diff.** #103's head has not moved since the 14:00 re-verify, so the deep-dive *content* (already CLEAR twice) was not re-litigated; the run instead verified (a) the never-auto-merge invariant still holds, (b) R23 is still satisfied vs the now-further-advanced master, and (c) prior NICE-TO-HAVEs actually landed. This is the correct shape for a standing-draft PR that the reviewer is forbidden to merge: confirm the safety invariants, don't re-score frozen content.
- **NICE-TO-HAVE -> next-commit loop closed for the runner.** The 06:00/14:00 runs flagged the runner source's functional non-ASCII (R20) and the inaccurate `"DB-only"` commit label; commit `1312bcc` ("runner source ASCII-clean (R20) + 'DB-only' -> 'partial' wording [reviewer NICE-TO-HAVE #100]") fixed both, and the fix is in the PR. The advisory-comment -> Worker-fix loop is working even for a never-merged draft.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `DeepDiveLearnings/ec-screens/gen_checklist.py:33` `print("wrote CHECKLIST.md -...",...)` emits a U+2014 em-dash to stdout (R18/R20 - `UnicodeEncodeError` on a cp1252 redirected/captured console). Pre-existing on master (merged via #100), outside the hygiene-guard glob, non-gating. The markdown `out`-list lines (23-30) are written via `.write_text(...,encoding="utf-8")` and are exempt; only the `print` on line 33 needs ASCII. | Worker | 🟢 Low |
| ~~#103 MUST-FIX (R23 clobber risk)~~ - **RESOLVED** at the 2026-06-23 14:00 re-verify (`df45d58` re-absorbed #101/#104); re-confirmed still zero `-` lines on reviewer docs this run (MR3 staleness sweep). | - | OK Closed |
| ~~Runner `run_ec_screen_learn.py` non-ASCII (R20) + `"{done_partial} DB-only"` label~~ - **RESOLVED** in-PR via `1312bcc` (runner ASCII-clean; label now `"partial"`). The hygiene guard still does not scan `tools/**` (or `.claude/skills/**` / `workstreams/**/scripts/*.py`) - that broadening remains open below. | Worker | 🟢 Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (would catch `gen_checklist.py:33`); fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

---

## 2026-06-24 - Automated Review (14:00 AWST, 1 open PR #107)

_Open PR triggers a full review (R14). #107 CLEAR - no MUST-FIX - squash-merged (`903b719`). The standing deep-dive draft (#103) was owner-milestone-MERGED since the 06:00 run, so it is no longer open. **No new executable rules - version stays v23.** R1-R23 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #107 | Clear (HIGH effort - client SQL logic + Oracle/Playwright capture scripts). ECSR-35263 (per-message report-date fix for `ZWP_P_MAIL_UTIL.getReportDate`, resolving via `REPORT_SEND_LOG`->`TV_REPORT_GENERATED` with an NVL fallback to the old by-type logic) + ECSR-35264 (split the shared Burrup Daily Production email config into dedicated `_PLUTO` / `_SCA` ACTOR-Maintenance sets). Both forward `.sql`: idempotent upsert (`UPDATE; IF SQL%ROWCOUNT=0 INSERT`, no MERGE); **0 `DELETE`** (new objects CREATED + message-def/connection RE-POINTED, old shared objects left intact - correctly avoids ORA-02292 since Oracle can't UPDATE a child-referenced CODE; the `ROLLBACK__...PLUTO.sql` DELETEs are intentional baseline-restore); **R22 clean** (`REV_TEXT='ECSR-35264'` real ticket, no `ECPR-XXXX`/`ECSR-XXXX` placeholder); **R18/R20 clean** (`rg [^\x00-\x7F]` over all `.py`+`.sql` -> 0 matches; non-ASCII only in `ANALYSIS.md`/`README.md` pure-MD docs, exempt; SQL uses `chr(123)/chr(64)/chr(38)/chr(91)` to keep braces/@/&/[] sqlplus-encoding-safe); **R16 clean** (web `EC_USER`/`EC_PASS` + DB `EC_DB_USER`/`EC_DB_PASS` all env-var with empty-string defaults, zero hardcoded secrets); **R8/R23** (924 ins / 0 del, isolated `workstreams/ecsr-35263-35264-sca-email/` tree, no reviewer-owned/shared file touched, GitHub MERGEABLE). ECSR-35263 `.sql` is honestly a delivery NOTE (commented patch spec for the repeatable `R__0400/R__0500_ZWP_P_MAIL_UTIL` package files, not standalone Flyway) - correctly disclosed, not over-claimed. DB ground-truth (MESSAGE_OUT 414 Pluto / 410 Scarborough = TEXT, REV_TEXT=ECSR-35264, Status=ERROR by-design no-SMTP on COPSDEV) taken as worker-attested (COPSDEV read-only policy, not reviewer-re-run). | OK Clear (NICE-TO-HAVE) - merged |

### Rules (apply immediately, no exceptions)

_None this run. Every finding is covered by the existing R1-R23 - notably R22 (real `REV_TEXT`), R18/R20 (ASCII in console/parse-bound files), R16 (env-var creds), R8/R23 (sync + no `-` on reviewer docs). Version stays v23._

### Observations (good patterns to keep)

- **Non-destructive live-config change done right (second client SQL since R22 minted).** The `_PLUTO`/`_SCA` split CREATES new consistently-named objects and RE-POINTS the message-def `COMPANY_CONTACT_CODE` + distribution connection, leaving the old shared objects intact (historical messages still reference them). The header explicitly reasons why a CODE rename would fail (ORA-02292, no ON-UPDATE-CASCADE) - this is the correct, reversible, idempotent shape for a client-config migration, and it shipped with a matching ROLLBACK baseline-restore script (cf. R3 / [[feedback_db_script_rerunnable_revtext]]).
- **R22 now reflexive on every client SQL delivery.** Both #96 (NOPTA) and now #107 set the real governing ticket via a single `lv_rev_text` constant on every DML - no `ECPR-XXXX` placeholder has appeared in a client SQL since R22 was extracted from #93's demo SQL.
- **R20 carried into a non-`screens/` tree unprompted.** All four `.py` capture/build scripts (outside the hygiene-guard glob) are ASCII-clean by authoring - the Worker applied the ASCII-at-authoring discipline to a workstream tree the static guard doesn't even scan. This is exactly the gap the standing "extend the guard to `workstreams/**`" item exists to backstop; the Worker pre-empted it.
- **Credential hygiene beyond R16's letter.** R16 mandates env-var creds in Playwright bundles; #107's capture scripts go further - empty-string defaults (not a baked-in `sysadmin` default), so a misconfigured run fails closed rather than silently using a default login. Good pattern for any net-new EC-touching script.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| #107 NICE-TO-HAVE (R21): "Files touched" lists 7 of 14 diff files - omits `ANALYSIS.md`, `UT/.gitignore`, and the whole `UT/capture/` toolchain (`README.md`, `build_ut_docs.py`, `capture_ut_screens.py`, `fetch_message_content.py`). Body under-claims a correct change; reconcile via `git diff --stat origin/master...HEAD` before pushing. Non-gating (already merged). | Worker | 🟢 Low |
| #107 `ROLLBACK__...PLUTO.sql` mixes `_PLU` (30-char truncated) and `_PLUTO` CODEs in its defensive cleanup list - harmless (forward run committed nothing; the DELETEd codes were never inserted) but align if the rollback is ever exercised. | Worker | 🟢 Low |
| ECSR-35263: the SCA Upstream Daily Partner email config was NOT found on plutodev (only `R_PLU_DAILY_PARTNER` reference exists) - per the PR's own ANALYSIS.md the 18/12-Jun date bug repro lives on ECaaS TEST; the `getReportDate(p_message_no)` overload is the code fix but needs an ECaaS TEST repro to confirm. Worker-disclosed open question, not a defect in this PR. | Worker (when resumed) | 🟡 Medium |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (would catch `gen_checklist.py:33`); fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

---

## 2026-06-25 01:00 AWST — Automated Review (off-schedule early run, 3 open PRs #109/#110/#111)

_Open PRs trigger a full review (R14) even at an off-schedule hour (run fired 01:22 AWST). 0 new master commits since #108/`a092ac6` but 3 open PRs. **All 3 CLEAR — zero MUST-FIX — all 3 squash-merged**; 0 PRs left open afterward. **No new executable rules** — R1–R23 cover every finding; version stays **v23**._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #109 | Clear (low effort — config-only, +10/-1). Promotes 9 allow-list MCP/tool permission entries into the shared `.claude/settings.json` (Atlassian/playwright/ec-mcp read tools + `openspec status/config/instructions`). Independently verified on the PR head: `py -m json.tool` parses clean; ASCII-clean (R18); Files-touched maps 1:1 to the diff (only `settings.json`); `settings.local.json` (carries creds) and 25 regenerated screenshots correctly excluded from the stage (stage-own-files-by-path). No security-sensitive grants. | ✅ Clear — squash-merged (`b9ab709`) |
| #110 | Clear (HIGH effort — runner logic, +71/-18). Three EC-screen-runner improvements: (1) best-effort full-page Help-popup screenshot per screen; (2) **layered HIGH-confidence DB-class resolution** — URL `CLASS_NAME` → URL last-path-token *only if it is a real class* (`_class_exists` vs `class_cnfg`) → case-insensitive EXACT `LABEL` *only when unique*; ambiguous/none stays an honest `[~]` partial (never guesses a binding); a `_Resolved by:` provenance line is added per note; (3) `_clip` trims Help text on a sentence/paragraph boundary instead of a hard `[:900]`. Independently verified: `py_compile` OK; **ASCII-clean (R20)** — 0 non-ASCII bytes over the whole file; `help_text` now returns a 2-tuple `(text, shot_ok)` with all three return paths and the `main` unpack consistent (no arity bug); queries are metadata-read-only; screenshot is nested-try/except so it never fails a screen; full/partial threshold unchanged (full = DB + Help text). DB-recovery claims (CO.0018→EQUITY_SHARE, CO.0038→TANK_USAGE, PO.0008→OBJECT_ITEM_COMMENT recovered; known-good screens unregressed) taken as worker-attested (sandbox not reviewer-re-run). 3 NICE-TO-HAVE. | ✅ Clear (NICE-TO-HAVE) — squash-merged (`0a5aa42`) |
| #111 | Clear (low effort — reviewer-prompt process, +4/-1). Adds a new step 18 to `.claude/review-prompt.txt` so the reviewer auto-merges master **INTO** `feature/ec-screen-deepdive` after each run (`git merge origin/master --no-edit` — **not** force-push), then renumbers the old step 18→19. Sound structural fix for the R23 drift problem (keeps the permanent branch synced with master each run, including reviewer-owned docs). Body matches the diff (R21). The diff is ASCII; the only non-ASCII byte in the file is a pre-existing em-dash on line 14 (the step-6 format string) — outside this diff and outside R18 scope (the prompt is read by Claude, not console/PS-parsed). 1 NICE-TO-HAVE. | ✅ Clear (NICE-TO-HAVE) — squash-merged (`9ce47bd`) |

### Observations (good patterns to keep)

- **Accuracy-first DB resolution is the right shape for an unattended coverage runner (#110).** Each new fallback either binds a *verified-real* class or refuses and leaves an honest `[~]` partial with a `_Resolved by:` provenance line — it never fabricates a binding to make a screen look "full." This is the same discipline R19/R3 reward (honest partials over plausible-but-wrong data) carried into the runner's own resolution logic.
- **Best-effort enrichment must never gate the core capture.** The Help screenshot is wrapped so a screenshot failure degrades to "no screenshot this run" rather than failing the whole screen, and it explicitly does not move the full/partial threshold. Correct severity split — the bonus data can't regress the proven metadata+Help baseline.
- **Reviewer-owned-doc drift on the permanent branch is being fixed structurally, not by reminder (#111).** R23 (2026-06-23) flagged the drift as structural; #111 turns the "merge master before milestone" guidance into an automatic per-run reviewer step. The remaining edge is purely operational (see gap) — the *intent* and the no-force-push safety are correct.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| #110: committing a full-page Help PNG per screen (~735 KB each per the PR body) across ~1457 screens is ~1 GB of binaries into git history — repo-health risk (cf. standing maintainability concern). Consider downscale/JPEG-quality, a max-dimension cap, or storing screenshots out-of-repo (LFS/external) with only the `.md` reference committed. | Worker | 🟡 Medium |
| #110 (minor): strategy-(2) URL token `url.rstrip('/').split('/')[-1].upper()` does not strip a trailing query/fragment — harmless (the `_class_exists` gate just won't match → falls through to label) but a `split('?')[0].split('#')[0]` first would let path-token resolution fire on more screens. Also `notes_dir.mkdir` is now redundantly done in both `main()` and `write_note()`. | Worker | 🟢 Low |
| #111: the new step 18 cannot run as written in this environment — `git checkout feature/ec-screen-deepdive` fails when that branch is already checked out (dirty) in the Worker's main checkout, and forcing it would disrupt the Worker. Harden: do the merge in a dedicated throwaway worktree (`git worktree add <tmp> feature/ec-screen-deepdive && git merge origin/master --no-edit && git push && git worktree remove <tmp>`), or guard/skip when the branch is checked out elsewhere or its tree is dirty. **This run deferred the deep-dive sync for exactly this reason** (Worker's permanent checkout dirty — 493 files). | Reviewer/Worker | 🟡 Medium |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (would catch `gen_checklist.py:33`); fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

### Reviewer process note (deep-dive sync deferred; isolated worktree)

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's **permanent** branch `feature/ec-screen-deepdive` with a dirty tree (493 files) plus two Worker runner worktrees (`wt-ec-learn`, `wt-ecsr`). All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-25-0100` worktree off `origin/master`; the Worker's checkout and runner worktrees were never touched. The newly-merged step 18 (deep-dive auto-sync) was **not executed** — branch-checkout collision + dirty Worker tree make it unsafe this run (logged as the #111 gap above).

---

## 2026-06-25 14:00 AWST — Automated Review (2 open PRs #113/#114)

_Open PRs trigger a full review (R14); run fired ~16:00 AWST (late 14:00 slot). 0 new master commits since the 01:00 run (#112/`dcc77b3`) but 2 open PRs. **#114 CLEAR — squash-merged (`5e1649a`); #113 MUST-FIX — left open.** Both PRs directly action the 01:00 run's #110/#111 gaps. **One new executable rule (R24).** R1–R23 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #114 | Clear (HIGH effort — runner control-flow, +16/-6). Wraps the two uncaught crash points in `run_ec_screen_learn.py` — `oracledb.connect()`+`cur`, and the Playwright `launch`/`new_context`/`goto`/login block — in `try/except` that log `ABORTED: DB connect failed (...)` / `ABORTED: browser/login failed (...)` to `session_log.txt` and `return 1`, so the 2026-06-25 13:30 silent-truncation crash is diagnosable next time. Verified: resource cleanup correct (`br=None` guard + `if br: br.close()` then `con.close()` on the browser-failure path; `con` opened before the `with sync_playwright()` block so closing it there is right); **ASCII-clean** (full-file byte scan → 0 non-ASCII, R18/R20); `str(e)[:120]` is runtime-dynamic (out of R18's authored-char scope) and `log()` writes the file `encoding='utf-8'`. R9 (6 fields), R21 (Files-touched = the one diff file), R16 (creds untouched). | ✅ Clear — squash-merged (`5e1649a`) |
| #113 | **MUST-FIX** (HIGH effort — reviewer-process change that runs `git push` unattended, +8/-3). Rewrites step 18 to do the deep-dive sync in a `--detach` throwaway worktree instead of `git checkout feature/ec-screen-deepdive` — **correctly fixes the dirty-checkout collision** flagged in the 01:00 #111 gap. But the push command `git push origin feature/ec-screen-deepdive` from the detached worktree pushes the **local branch ref** (`refs/heads/feature/ec-screen-deepdive` = the Worker's dirty main-checkout tip), **NOT** the detached merge HEAD — so the merge result is discarded and the sync silently fails (or non-fast-forward-rejects). **Empirically proven** this run (see R24). Fix is one line: `git -C C:/tmp/wt-review-deepdive-sync push origin HEAD:refs/heads/feature/ec-screen-deepdive`. Otherwise clean (R9/R18/R21). NICE-TO-HAVE: worktree named `wt-review-deepdive-sync` matches step 17's `wt-review-*` sweep but step 17 runs before step 18 same-run, so only the *next* run cleans it. | ⛔ MUST-FIX open — left open for Worker |

### Rules (apply immediately, no exceptions)

**R24 — Pushing from a detached/throwaway worktree MUST use an explicit `HEAD:refs/heads/<branch>` refspec** ✅ _live-validated this run (dry-run reproduction)_
When you `git worktree add --detach <tmp> origin/<branch>`, do work on the detached HEAD, then push, a bare `git push origin <branch>` does **not** push the detached HEAD. The positional refspec `<branch>` resolves its *source* to the shared local ref `refs/heads/<branch>` — i.e. whatever tip another worktree (e.g. the Worker's main checkout) has that branch checked out at — not the current worktree's `HEAD`. So a "merge-in-a-throwaway-worktree then push" flow silently pushes the wrong commit (or fails non-fast-forward) while the merge you just made is thrown away. **Always push the detached HEAD explicitly:** `git -C <tmp> push origin HEAD:refs/heads/<branch>`. This applies to the reviewer's own step-18 deep-dive sync and to any Worker flow that builds a commit in a throwaway/detached worktree.
_Live-validated: reproduced PR #113's exact step 18 in a detached worktree off `origin/feature/ec-screen-deepdive`, merged `origin/master`, then `git push --dry-run origin feature/ec-screen-deepdive` reported source `feature/ec-screen-deepdive` (local `a7a0a3d`) → `! [rejected] (non-fast-forward)` against origin `cb5bdbf` — i.e. it tried to push the stale local branch ref, not the detached merge HEAD (`cb5bdbf`, which would have reported "Everything up-to-date")._

### Observations (good patterns to keep)

- **Gap → next-PR loop closed in one cycle, again.** The 01:00 run logged two gaps: the runner needs error logging on its crash points (implied by #110's "silent truncation" risk) and step 18's checkout-collision (#111 gap). #114 and #113 are the Worker's direct response the same day. #114 lands clean; #113 is the right *approach* with one wrong refspec — the advisory→fix loop is working, the MUST-FIX just sharpens the last 5%.
- **Diagnosability-first error handling (#114).** Wrapping the connect + browser-launch in try/except that writes a precise `ABORTED:` line to the runner's own log (not just Task Scheduler's stdout capture) is the correct fix for a silently-truncated session log — the next failure self-documents its root cause. Returning `1` (not raising) keeps the scheduler's exit-code contract.
- **A reviewer-process change that runs `git push` unattended deserves the same rigor as code.** #113's defect would never surface in a green run (it only bites when the local branch diverges from origin) — exactly the FAIL-only-branch class R20 warns about, but for git plumbing. Verifying it required reproducing the command, not reading it. Reach for empirical reproduction on any unattended git-mutation step.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| **#113 MUST-FIX:** step 18 push pushes the local branch ref, not the detached HEAD — change to `git -C C:/tmp/wt-review-deepdive-sync push origin HEAD:refs/heads/feature/ec-screen-deepdive` (R24). Re-push the one-line fix to clear. | Worker | 🔴 High |
| #113 NICE-TO-HAVE: throwaway worktree `wt-review-deepdive-sync` matches step 17's `wt-review-*` glob but step 17 runs before step 18 in the same run — rename outside the glob (e.g. `wt-deepdive-sync`) or accept the cross-run cleanup as the backstop. | Worker | 🟢 Low |
| Carry-over from 01:00 (#110): ~1 GB of per-screen Help PNGs into git history over ~1457 screens — downscale/JPEG/LFS/out-of-repo. | Worker | 🟡 Medium |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (would catch `gen_checklist.py:33`); fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

### Reviewer process note (isolated worktree; deep-dive sync deferred)

- Main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's **permanent** dirty `feature/ec-screen-deepdive` (493 files) plus Worker runner worktrees (`wt-ec-learn`, `wt-ecsr`, `wt-ecsr35236`). All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-25-1400` worktree off `origin/master`; the Worker's checkout and runner worktrees were never touched. The deep-dive auto-sync (step 18) is **not in this run's review prompt** (the prompt predates #111's step-18) and, regardless, is the very flow #113 fixes — left for the corrected #113 to land. The empirical push test used a throwaway `wt-test-push-refspec` worktree, removed immediately after.

---

## 2026-06-25 06:00 AWST -- Automated Review (6 open PRs #116-#122)

_1 new master commit since the 14:00 run (`5b47ce5` review #115); 6 open non-draft PRs (#116, #117, #119, #120, #121, #122) + 1 standing draft (#118). Open PRs trigger a full review (R14). **All 6 CLEAR -- zero MUST-FIX.** One new rule (R25). R1-R24 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #116 | Clear (runner DB retry loop, +31/-2). `EC_LEARN_DB_RETRIES`/`EC_LEARN_DB_RETRY_WAIT` env-configurable; `tcp_connect_timeout=15` prevents hang; abort log names DSN+retry count; `return 1` propagates non-zero exit to Task Scheduler; R16/R20 clean. **Merge before #117.** | OK -- CLEAR |
| #117 | Clear (6 robustness fixes, +61/-18). `git fetch` warning non-fatal; XPath quote-switching handles names containing double-quotes; ASCII hyphen in checklist line (_ascii(), R20); no-op detection warns rather than silently skipping; empty-commit guard; push retry via rebase then re-push using `HEAD:refs/heads/<branch>` (R24). **Depends on #116.** | OK -- CLEAR |
| #119 | Clear (Royalty Owner IUD, T3 + robot + Playwright bundle). TC02/TC04 use `ov_royalty_owner`; End-Date=Start-Date delete pattern; R16/R20 clean. **Base of 4-deep stack.** | OK -- CLEAR |
| #120 | Clear (Royalty Depositor IUD). TC02/TC04 use `ov_royalty_depositor`; same pattern. Depends on #119. | OK -- CLEAR |
| #121 | Clear (Product Group IUD). TC02/TC04 use `ov_product_group`; same pattern. Depends on #120. | OK -- CLEAR |
| #122 | Clear (Unit Agreement IUD + `gen_ov_iud_bundle.py` generator). TC02/TC04 use `ov_unit_agreement`; same pattern. NICE-TO-HAVE: move `gen_ov_iud_bundle.py` from `tmp/scripts/` to `tools/generators/`. Depends on #121. | OK -- CLEAR (NICE-TO-HAVE) |

### Merge order constraint

`#116` then `#117` (conflict if out of order), then `#119` -> `#120` -> `#121` -> `#122` (stacked -- scorecard append conflict if out of order).

### Rules (apply immediately, no exceptions)

**R25 -- When a tool or connection breaks, OWN the troubleshooting -- never treat it as someone else's problem**
When any tool, MCP server, or external connection fails mid-session (GitHub MCP disconnect, DB connection lost, browser not launching, etc.), the correct response is:
1. Diagnose immediately -- what broke, why, and what state we are in
2. Give the user clear actionable steps to fix it -- even if the fix requires action on their machine/browser/phone
3. Keep moving -- do not stall, wait, or redirect the user to figure it out alone
It does not matter whether the reviewer/assistant set up the connection. If it is broken and the user needs it to work, it is the reviewer's problem to guide through resolution. Saying "I can't access it" without following up with "here is how to fix it" is a bad attitude and a failure to serve the user.
_Added 2026-06-25 after reviewer failed to guide user through GitHub MCP reconnection -- treated it as outside scope instead of taking ownership of the troubleshooting._

### Observations (good patterns to keep)

- **Bank-family IUD pattern is now well-established.** PRs #119-#122 are the 3rd-through-6th applications of the End-Date=Start-Date delete + `ov_<class>` view assertion pattern (R1-R2-Bank family). The pattern is copy-stable -- all 4 PRs are clean without intervention.
- **Generator scripts accelerate the stack (#122).** `gen_ov_iud_bundle.py` scaffolded the #122 bundle directly, cutting authoring time for the 4th-in-stack. Moving it to `tools/generators/` makes it first-class tooling (NICE-TO-HAVE).
- **DB retry loop addresses the real root cause (#116).** The Oracle Docker sandbox goes down after laptop restarts; the retry loop + configurable wait (default 3 tries, 20s apart) makes the runner self-healing for transient Docker startup delays -- a correct fix at the right layer.

### Gaps (verified against PRs)

| Gap | Owner | Priority |
|-----|-------|----------|
| `gen_ov_iud_bundle.py` lives in `tmp/scripts/` -- move to `tools/generators/` for permanence and hygiene-guard coverage (NICE-TO-HAVE from #122) | Worker | Low |
| Remaining 4 Royalty Object screens (RC.0054, RC.0056, RC.0057, RC.0058) -- not yet started; blocked on Oracle sandbox restart + IUD stack merge | Worker | Medium |
| Carry-over (still open): #113 MUST-FIX (step 18 push refspec) | Worker | High |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS upload flakiness | Worker | Medium |

### Reviewer process note

- All 6 PR comment postings used `mcp__github__add_issue_comment` (plain comment) after APPROVE was rejected with "Cannot approve your own pull request." This is the correct workaround -- use COMMENT not APPROVE when reviewer == author.
- Review-doc edits committed on `claude/repo-review-f21x0s` and will be raised as a PR targeting master.

---

## 2026-06-26 -- Automated Review (06:00 AWST, 7 worker PRs + 1 orphan review PR)

_1 new master commit (#113/`f80b2b4`) since the 06-25 14:00 run; 8 open PRs (7 worker + the orphan review #123) + 1 standing draft (#118). Open PRs trigger a full review (R14). **All 7 worker PRs CLEAR -- zero MUST-FIX.** One live reviewer-process MUST-FIX found and fixed in this PR (step-18 push refspec). **No new executable rule -- R1-R25 cover every finding; version stays v25.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #123 | Orphan review PR from the 06-25 06:00 session (created `claude/repo-review-f21x0s` but never self-merged -- the session crashed before its merge step, stranding 6 cleared worker PRs). Content sound: bumps v24->v25 + R25 (own the troubleshooting), clears #116-#122, appends the 06:00 review-log entry. Docs-only/append-only. **Squash-merged FIRST** to preserve R25 + the review record before merging the workers it cleared. | OK -- merged |
| #116 | Clear (runner DB pre-flight retry +31/-2). `con=None` sentinel + `EC_LEARN_DB_RETRIES`/`_WAIT` env knobs + `tcp_connect_timeout=15`; abort log names DSN+count; `return 1` propagates to Task Scheduler. ASCII (R18/R20), env creds (R16). | OK -- merged (before #117) |
| #117 | Clear (6 runner robustness fixes +61/-18). fetch-warn non-fatal; XPath quote-switch for names with `"`; ASCII hyphen via `_ascii()`; no-op `re.sub` warns; empty-commit guard; push retry via fetch+rebase+re-push using `HEAD:refs/heads/<branch>` (R24-compliant). Disjoint `main()` hunks vs #116 -> merged clean. | OK -- merged |
| #119-#122 | Clear (Royalty Owner / Depositor / Product Group / Unit Agreement -- Bank-family OV clones). `ov_<class>` view asserts, End=Start delete, env-var creds, R9 6-field bodies, **no shared T1/T2 edits** (reuse `manage_object.resource`), append-only scorecard/registry rows. #122's `gen_ov_iud_bundle.py` is already under `tools/generators/` (the #123 NICE-TO-HAVE was actioned in-stack). | OK -- merged (stack, in order) |
| #124 | Clear (Tract -- 1st OV-GM in Royalty Objects). Gated by Unit Agreement nav dd + GO; insert parent dd R3 = nav scope; **R17 lazy-redraw** extra `Apply Navigator` after insert/delete; **date-effective parent gotcha solved** (UA parents effective 2010-01-01 -> form date 2011-01-01); cloned the Transport System OV-GM exemplar (not Bank); RF-only per OV-GM precedent; no shared-file edits. 1 NICE-TO-HAVE (R21 doc drift: SOW says `${TEST_START_DATE_REFDD}`, suite hardcodes 2011-01-01). | OK -- merged (top of stack) |

### Rules (apply immediately, no exceptions)

_None new this cycle. R1-R25 cover every finding. Version stays **v25**._

### Observations (good patterns to keep)

- **The Bank-family OV IUD pattern is fully copy-stable, and the OV-GM variant is now a clean clone too.** #119-#122 are 4 textbook Bank clones with zero intervention; #124 extended the same folder into its first OV-GM (gated) screen and reused the Transport System exemplar's two well-known gotchas (R17 lazy redraw + date-effective parent) *pre-emptively* -- the gotchas were in the T3 from the first run, not rediscovered after a false-fail. The exemplar-clone + registry feedback loop is working as designed.
- **Reviewer must apply its own ratified rules to its own tooling.** R24 (extracted from #113's detached-worktree push bug) was still being violated by the *merged* step 18 itself: line 42 pushed the bare `push origin feature/ec-screen-deepdive` from a `--detach` worktree. #113 fixed the worktree-isolation half but shipped the refspec half still broken, and the merge masked it (the merge log shows the fix commit title, not that the body was only half-applied). Caught by reading the live prompt during step-18 prep rather than trusting the #113 merge title (MR3 staleness sweep + verify-before-trust). Fixed in this PR; step 18 executed with the correct `HEAD:refs/heads/...` refspec.
- **Orphan-review-PR recovery.** A prior session that creates its review PR but crashes before the self-merge leaves a docs-only PR plus all the worker PRs it cleared, unmerged. The correct recovery is to independently re-verify the workers (don't blind-trust the orphan's verdicts), then merge the orphan FIRST (so its R25 + review-log entry land before the workers it references), then merge the workers. This preserves attribution + rule numbering and avoids a duplicate R25.

### Reviewer process note (stacked-squash append-conflict resolution)

- **Every PR in a content-stack that appends to the same shared doc add/add-conflicts at squash-merge time, by construction.** Once the parent is squash-merged, master holds the parent's rows as a *new* commit that is not in the child's ancestry; the child branch still carries the parent's *original* commits, so the merge-base is pre-stack master and git flags the adjacent row insertions as a conflict. For these four PRs the child branch is always a **strict superset** of master on `automation-scorecard.md` + `ec_screen_registry.md` (it has every prior row plus its own), so the deterministic resolution is `git checkout --ours <both files>` -> verify the expected N rows are present -> commit -> `push origin HEAD:refs/heads/<branch>` (R24). Done in a throwaway `C:/tmp/wt-stack` detached worktree because the stack branches are checked out in the Worker's own worktrees and must not be touched. (Future option: have the Worker base the stack so only the top PR carries the doc rows, or rebase children onto the squashed parent before merge -- but the `--ours` superset resolution is safe and fast as-is.)

### Gaps (verified against filesystem / PRs)

| Gap | Owner | Priority |
|-----|-------|----------|
| ~~#113 MUST-FIX (step 18 push refspec)~~ -- **RESOLVED this run** (`.claude/review-prompt.txt:42` now pushes `HEAD:refs/heads/feature/ec-screen-deepdive`, R24) | Reviewer | OK Closed |
| #124 SOW date wording (`${TEST_START_DATE_REFDD}`) does not match the suite's hardcoded `2011-01-01` (R21 doc drift) -- align the SOW to the actual value | Worker | Low |
| Remaining 3 Royalty Object screens (RC.0054/0057/0058) not yet started (Tract RC.0056 now done) | Worker | Medium |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (would catch `gen_ov_iud_bundle.py`/`gen_checklist.py`); fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload->RUN NOW` flakiness root cause | Worker | Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | Low |

---

## 2026-06-26 -- Automated Review (14:00 AWST, 1 worker PR + 1 standing draft)

_No new master commits since the 06:00 run (#125/`327e769`) other than what this run merges; 2 open PRs -- #126 (ECSR-35236 PHD check-rule scoping SQL, NOT draft) and #118 (the standing deep-dive draft). Open PRs trigger a full review (R14). **#126 CLEAR -- zero MUST-FIX -- squash-merged (`b991897`).** #118 left open (owner-merge-only standing draft). **No new executable rule -- R1-R25 cover every finding; version stays v25.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #126 | Clear (HIGH effort -- client check-rule config SQL + paired rollback). Scopes 8 PHD validation rules (tank GRS_MASS/STD_DENS = MEASURED; stream DENSITY/GCV = COMP_ANALYSIS; 4x PWEL no-data temp/press = ON_STREAM_HRS > 0) by appending a method/on-stream criterion to each WHERE_FORMULA + an ATTRIBUTE method var, mirroring the live `PHD_STREAM_LIQUID_MEAS_VAL2` rule. Apply SQL: idempotent upsert (`UPDATE; IF SQL%ROWCOUNT=0 THEN INSERT`, no MERGE), **targets by CHECK_NAME** (CHECK_ID env-local, resolved at runtime), `REV_TEXT='ECSR-35236'` real ticket (**R22 clean -- no `ECPR-XXXX`**), **0 DELETE** (non-destructive), per-rule `check_id` keying so shared var names (`ConstMEASURED`/`ConstCOMP`/`OnStrmHrs`) never collide across rules. Rollback SQL: restores original value-only formulas, DELETE precisely guarded by `rev_text='ECSR-35236'` + the 7 net-new var names + the 8 target check_ids; net-new status cross-checked vs pristine ECAASTEST (the key safety proof for a stamp-guarded delete). Full apply->rollback->re-apply cycle is clean. R8 satisfied (branch merged origin/master `306d2f55`/`0c15c32`). DB ground-truth (round-trip S0==S2, behavioural before/after counts, Validation Overview screen 20->12 Errors) + self-clean taken as worker-attested (plutodev read-write-with-rollback, not reviewer-re-run). **1 NICE-TO-HAVE (R18/R20):** `investigation/compare_check_rules.py` has em-dashes in its docstring/comments (lines 3/5/13) -- only in docstring/comments (not `print()` strings) so no cp1252 runtime crash, and the file is outside the `check_bundle_hygiene.py` glob (`workstreams/**` not scanned) so the static gate misses it. Exactly the still-open "broaden the hygiene glob to `workstreams/**`" carry-over. | OK Clear (NICE-TO-HAVE) -- merged |
| #118 | STANDING/DRAFT EC Screen Deep-Dive (draft=true). Reviewer leaves it alone by design (draft = skip; owner milestone-merges). Not reviewed for content this run. | -- left open (owner-merge-only) |

### Rules (apply immediately, no exceptions)

_None new this cycle. R1-R25 cover every finding. Version stays **v25**._

### Observations (good patterns to keep)

- **Paired apply/rollback with asymmetric audit stamps is the right shape.** #126's rollback audit-stamps the rule rows with a distinct `'ECSR-35236-ROLLBACK'` REV_TEXT while keying the variable DELETE off the apply's `'ECSR-35236'` stamp -- so the currently-applied-vs-rolled-back state is legible straight from REV_TEXT, and the deletion still targets exactly what apply wrote. The stamp-guarded delete is only safe because the worker proved the 7 vars are net-new via a pristine-ECAASTEST cross-check ([[feedback_clone_full_row_diff]] / R2 verify-before-assume) -- that cross-check is what turns "DELETE WHERE rev_text=mine" from risky into precise.
- **R22 is now reflexive on client SQL.** Every SQL delivery since R22 was minted (#96 NOPTA, #107 SCA-email, now #126) has set the real governing ticket on every DML via a single `lv_rev_text` constant with zero `ECPR-XXXX`/`ECSR-XXXX` placeholder. The standing re-runnable+REV_TEXT directive needs no reminder.
- **Per-branch JOURNAL.md habit landed.** #126's `a757ba5` adds a committed `JOURNAL.md` (built / done-wrong / done-well / improve / blockers+resolution / decisions) -- the first instance of the standing per-feature-branch journal habit. Good for handover/resumability; keep it.

### Gaps (verified against filesystem / PRs)

| Gap | Owner | Priority |
|-----|-------|----------|
| `workstreams/ecsr-35236-phd-validations/investigation/compare_check_rules.py` em-dashes (lines 3/5/13) -- ASCII-normalise (R18/R20). Reinforces the open carry-over to broaden `check_bundle_hygiene.py` to `workstreams/**/**.py` so these are machine-caught | Worker | Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/**.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload->RUN NOW` flakiness root cause | Worker | Medium |
| Carry-over (still open): #124 SOW date wording vs hardcoded `2011-01-01` (R21); remaining 3 Royalty Object screens (RC.0054/0057/0058); Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | Low |

### Reviewer process note

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent `feature/ec-screen-deepdive` branch with a dirty working tree (and many active sibling IUD worktrees: `wt-royalty*`/`wt-tract`/`wt-prodgrp`/`wt-unitagr`/`wt-ecsr*`/`wt-ec-learn`). That branch was behind master at **v23** while master is **v25** -- the exact R23/MR4 drift. All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-26-1400` worktree off `origin/master`; the Worker's checkout and every sibling worktree were never touched. The current `lessons-learned.md` state (v25, R24/R25) was re-read from the master copy in the worktree, not the stale v23 main-checkout copy (MR4).

---

## 2026-06-27 06:00 AWST -- Automated Review (1 worker PR #128 + 1 standing draft #118)

_0 new master commits since #127/`1aa08e0` (the 06-26 14:00 review); 1 non-draft worker PR (#128) + the standing deep-dive draft (#118). Open PRs trigger a full review (R14). **#128 content CLEAR but has 1 MUST-FIX (R9 body header drift) -- left OPEN.** #118 = owner-merge-only standing draft, **NOT merged**, R23 satisfied. **No new executable rules** -- R1-R25 cover every finding; version stays **v25**._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #128 | **MUST-FIX (R9)** -- ECSR-35333 RAU report read-only fact-finding (Issue 1 root cause proven, no fix, awaiting client re-test). The diff is clean and high quality, independently verified: 8 `investigation/*.py` are **read-only** (0 INSERT/UPDATE/DELETE/MERGE/commit, grep-verified), env-var creds `EC_DB_USER`/`EC_DB_PWD`/`EC_DB_DSN` (R16), ASCII-clean `.py` (R18/R20 -- `[^\x00-\x7F]` -> 0 matches; em-dash only in pure-MD `FINDINGS.md`/`JOURNAL.md`, exempt), isolated `workstreams/ecsr-35333-rau-report/` tree, **0 deletions** anywhere (R8/R23 trivially clean), root cause proven four independent ways (As-Built DDS 4.1.6 + `ZWP_P_DEF_RAU_CALC` gate code + live 120/150 `P` unverified + the calc's own revision text). DB ground-truth taken as worker-attested (ECAASDEV read-only, not reviewer-re-run). **But the PR body is missing 4 of the 6 literal R9 headers:** "What was built" (present only as "What this is"), "DB ground-truth evidence", "Self-clean confirmed", and "Rules applied" (entirely absent). Format-only fix -- no code change needed. | MUST-FIX open -- left for Worker |
| #118 | Clear (re-confirmation) -- standing DRAFT EC Screen Deep-Dive; reviewer never auto-merges (owner milestone-merges). Increment since the last cleared head `c32cec2` = `39fb078` (CO.0018/CO.0038/PO.0008) + `12eaad8` (CO.0039/0040/0042/0044/0045/0049/0050/0051) = 11 new screen notes, all **full** (DB binding + Help both present). Bindings spot-checked real (CO.0049 Well->`WELL`/OBJECT/VERSIONED->`OV_WELL`; CO.0039 Tank Strapping->`TANK_STRAPPING`/DATA/EVENT->`DV_TANK_STRAPPING`), genuine EC config-manual Help text, ASCII-clean, honest marking. **R23 satisfied:** `git diff --stat origin/master...origin/feature/ec-screen-deepdive` shows ZERO `-` lines on the four reviewer-owned docs (the 21 deletions are CHECKLIST `[ ]`->`[x]` flips + note re-enrichment). | OK Clear -- left open (owner-merge-only) |

### Observations (good patterns to keep)

- **A content-clean PR can still earn a MUST-FIX purely on body discipline -- and should.** #128's *change* is exemplary (read-only, env creds, ASCII, isolated tree, 4-way-proven root cause), yet the body is missing 4 of the 6 literal R9 headers. R9 exists precisely so the body is a trustworthy parse surface; "What this is" is not "What was built", and "Rules applied" being absent means the reviewer cannot see which rules the worker claims to have honoured. Holding the line here is consistent (cf. #19 missing-fields MUST-FIX) and the fix is format-only -- low cost to the worker, high value to the merge gate.
- **R23 holds on the permanent branch this run without intervention.** The deep-dive branch has re-absorbed master (now v25) via its own `git merge origin/master` commits (`3d9aa78`), so the four reviewer-owned docs show zero `-` lines vs master -- a milestone-merge will not clobber any review record. The standing-draft + branch-self-syncs model is working as designed (cf. R23 + the step-18 sync).
- **Read-only fact-finding is the correct deliverable shape for a critical client bug awaiting re-test.** #128 proves the root cause and stops (no fix, no client-repo touch, no DB write) -- the operational fix (verify the outstanding June deferment events, re-run `ZWP_RAU_CALC_PLUSCA`) is handed back for the client to action. This is exactly R3-style "prove what works, park what requires the other party, never over-claim" applied to investigation work.

### Gaps (verified against filesystem / PRs)

| Gap | Owner | Priority |
|-----|-------|----------|
| **#128 MUST-FIX:** add the 4 missing literal R9 headers to the PR body ("What was built" / "DB ground-truth evidence" / "Self-clean confirmed" / "Rules applied"); push the body fix to clear (format-only, no code change) | Worker | High |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/**.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload->RUN NOW` flakiness root cause | Worker | Medium |
| Carry-over (still open): #124 SOW date wording vs hardcoded `2011-01-01` (R21); remaining 3 Royalty Object screens (RC.0054/0057/0058); Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | Low |

### Reviewer process note

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent `feature/ec-screen-deepdive` branch with a dirty working tree (sibling IUD worktrees `wt-royalty*`/`wt-tract`/`wt-prodgrp`/`wt-unitagr`/`wt-uws2`/`wt-ecsr*`/`wt-ec-learn` all present). The main checkout sits at `a7a0a3d` (v23) while master is `1aa08e0` (v25) -- the R23/MR4 drift; the *committed* deep-dive branch tip (`origin/feature/ec-screen-deepdive` = `12eaad8`) has re-absorbed master, so R23 is green at the branch tip even though the dirty checkout is behind. All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-27-0600` worktree off `origin/master`; the Worker's checkout and every sibling worktree were never touched. Current v25 state (R24/R25) re-read from the master copy in the worktree, not the stale v23 main-checkout copy (MR4).

---

## 2026-06-27 — Automated Review (14:00 AWST, 3 new worker PRs #130/#131/#132 + #128 re-check + standing draft #118)

_Open PRs trigger a full review (R14); run fired ~16:00 AWST (late 14:00 slot). **3 of 4 worker PRs CLEAR — squash-merged; 1 MUST-FIX left open.** **No new executable rules** — R1–R25 cover every finding; version stays **v25**. The MUST-FIX on #130 is a pure R13/R21 re-application, not a new rule._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #128 | **CLEAR (06:00 MUST-FIX resolved).** The 06:00 R9-body MUST-FIX is fixed — the body now carries all 6 literal headers (What was built / Files touched / DB ground-truth evidence / Self-clean confirmed / Rules applied / Base branch). Content (ECSR-35333 RAU read-only fact-finding) was already verified CLEAR at 06:00 (8 read-only `investigation/*.py`, env creds, ASCII, isolated tree, 0 deletions). | ✅ Clear — merged |
| #131 | **CLEAR.** Tract - Well Setup (RC.0057, PC cascade), full I-U-D. 4 TCs = title/body/scorecard all `4/4` (R13). DB ground-truth real via T3 wrappers over `DbVerify.py` (`View Count Where Should Be DV_TRACT_WELL_SETUP` count-delta 0→1→0 + `Code Should Be Present/Absent In View` COMMENTS sentinel). Env creds (R16), 5 `.py` ASCII-clean (R18/R20), no shared T1/T2/DbVerify edits (R12), 0 deletion lines on append-only scorecard+registry (R23). Self-clean: baseline-0 member under existing Unit 3 Tract 01, pre-existing PI-5/PI-6 verified intact. | ✅ Clear — merged |
| #132 | **CLEAR.** Product Group Setup (RC.0054), 3-tier master→detail→sub-detail, tab-gated, no nav — most complex of the batch. 10 TCs = `10/10` everywhere (R13). Per-entity COMMENTS-sentinel oracle over `DV_PRODUCT_GROUP_SETUP`/`DV_PRODUCT_GROUP_COST`/`PRODUCT_STRM_BAL_CAT` (label≠table handled). 11 `.py` ASCII-clean, R12/R16/R23 clean. Royalty Objects batch **COMPLETE 8/8**. (Resolved the expected stacked add/add conflict on `automation-scorecard.md` + `ec_screen_registry.md` after #131's squash — see process note.) | ✅ Clear — merged |
| #130 | **MUST-FIX (R13/R21 — body/title only, no code change).** Unit - Well Setup (RC.0050, PC) suite is **4 TCs full I-U-D** (TC01 Clean / TC02 Insert / TC03 Update / TC04 Delete; results.json `"update":"PASS"`) and the scorecard, README, and SOW all say **4/4 full I-U-D** — but the PR **title** still says `live 3/3` and the **body** says `RF 3/3 PASS` + `insert/delete` (omitting the UPDATE added after user feedback). Stale title/body contradicting the 4-TC suite = the same defect class that was a MUST-FIX on PR #24. | ⛔ MUST-FIX open — left for Worker |
| #118 | **CLEAR — NOT merged** (owner-merge-only standing deep-dive draft, still DRAFT). Only new content since the 06:00 run (`12eaad8`) is `1910222` (CO.0054–0069: 7 full + 1 honest `[~]` partial — CO.0060 "missing DB binding", not fabricated to `[x]`). Real bindings spot-checked (`WELL_BORE`→`OV_WELL_BORE`, `WELL_BORE_SPLIT_FACTOR`→`DV_WELL_BORE_SPLIT_FACTOR`, `CARGO_ACTIVITY`→`TV_CARGO_ACTIVITY`), ASCII-clean, CHECKLIST flips only. **R23 satisfied** — `git diff --stat origin/master...origin/feature/ec-screen-deepdive` shows 0 `-` lines on the four reviewer-owned docs. | ✅ Clear (NICE-TO-HAVE) — left open (owner-merge-only) |

### Observations (good patterns to keep)

- **Reviewer-flagged MUST-FIX closed in one cycle (#128).** The 06:00 run posted a format-only R9-body MUST-FIX; the Worker fixed the body (no code change) and the 14:00 run merged it. The post-comment → Worker-fix → next-run-merge loop works for body-only defects too.
- **The "3/3 → 4/4 after adding UPDATE" trap recurs, and the suite-side artifacts caught it (#130).** When a suite grows from I/D to full I-U-D after feedback, the count must be re-stated in EVERY surface. Here the scorecard/README/SOW were all updated to 4/4 but the PR title/body were missed — the same R13 failure mode as PR #24. The fix is mechanical; the lesson is that the *PR title and body* are part of the "everywhere" in R13, not just the in-repo docs.
- **Stacked-PR append-only conflict resolved by union, not `--ours`.** Unlike the 2026-06-26 stack (where the child branch was a strict superset of master for the two append-only files, so `--ours` was correct), here #132's branch was cut **before** #131 merged, so `--ours` would have dropped #131's Tract-Well-Setup row. Correct resolution = a real merge keeping the **union** of rows (master's 7/8 row + the branch's 8/8 row), committed in a throwaway `--detach` worktree and pushed `HEAD:refs/heads/feature/product-group-setup-iud` (R24). Reaffirms: choose `--ours`/`--theirs` only after confirming superset direction; default to a hand-merged union for append-only files.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| **#130 MUST-FIX:** update title `3/3`→`4/4`, body `RF 3/3 PASS`→`RF 4/4 PASS`, and "What was built" `insert/delete`→`insert/update/delete` to match the 4-TC suite + scorecard/README/SOW (R13/R21; body/title only, no code) | Worker | High |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/**.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` → `'ECPR-DEMO'` (R22); ECIS `upload->RUN NOW` flakiness root cause | Worker | Medium |
| Carry-over (still open): #124 SOW date wording vs hardcoded `2011-01-01` (R21); Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | Low |

### Reviewer process note

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent `feature/ec-screen-deepdive` branch with a dirty working tree (sibling IUD/runner worktrees `wt-ec-learn`/`wt-ecsr*`/`wt-pgs`/`wt-prodgrp`/`wt-royalty*`/`wt-tract`/`wt-tws`/`wt-unitagr`/`wt-uws2` all present); it sits at `a7a0a3d` (v23) while master advanced to v25 — the standing R23/MR4 drift. **The reviewer's v23 cached read at session start was the stale main-checkout copy; the live v25 state (R24/R25) was re-read from the master copy in the worktree (MR4).** All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-27-1400` worktree off `origin/master`; the #132 stacked-conflict resolution used a throwaway `C:/tmp/wt-pgs-merge` detached worktree (removed after push). The Worker's checkout and every `wt-*` sibling worktree were never touched.

---

## 2026-06-28 - Automated Review (06:00 AWST, 3 worker PRs #130/#134/#136 + 1 standing draft #135)

_Open PRs trigger a full review (R14). All 3 worker PRs CLEAR -- zero MUST-FIX -- all squash-merged; #135 left open (owner-merge-only draft). **No new executable rules** -- R1-R25 cover every finding; version stays **v25**. R1-R25 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #130 | Clear (HIGH effort -- full I-U-D RF suite, PC pattern). Unit - Well Setup IUD (RC.0050, 6th of 8 Royalty Objects, 2nd PC). The **06-27 14:00 R13/R21 MUST-FIX is RESOLVED**: title `live 4/4`, body `RF 4/4 PASS` + insert/update/delete, count consistent across title/body/scorecard (`Live 4/4 full I-U-D`)/README (TC01-TC04)/SOW. Re-verified: 4 TCs (clean / insert +1 / update COMMENTS `C3_in` present-in-view / delete count-delta to baseline) over `DV_UNIT_WELL_SETUP`; `investigation/*.py`+`playwright/*.py` ASCII-clean (R20, em-dash only in .md prose -- exempt); scorecard+registry append-only (R23, 0 deletion lines); no shared T1/T2/DbVerify (R12 N/A); env creds (R16). | OK Clear -- merged |
| #134 | Clear (low effort -- single SKILL.md, doc-only). New `ec-deepdive-review` skill codifying the periodic deep-dive-program review (inventory batch -> Explore breadth-read + read process docs -> synthesize domain learnings + note-quality + next-batch rec -> persist `REVIEW-<date>.md` + LEARNING-SCORECARD row to the program branch). All 6 body fields; correctly encodes the program guardrails (read-only screens/DB, isolated worktree, R23 append-only, never-merge the standing draft, ASCII .py, spot-verify agent claims, honest `[~]` tiering). 1 NICE-TO-HAVE (R21): the skill's "Reference example: REVIEW-2026-06-27.md" lives only on the program branch, not master (verified `git cat-file -e origin/master:...` absent). | OK Clear (NICE-TO-HAVE) -- merged |
| #136 | Clear (HIGH effort -- CI workflow logic). `reopen-deepdive-draft-pr.yml` auto-reopens a fresh DRAFT standing PR after the owner milestone-merges the deep-dive branch. Trigger correctly gated (`merged==true && head.ref=='feature/ec-screen-deepdive'` -- fires only on the program branch's own merges); double-open + not-ahead guards; creates a DRAFT (owner-merge-only); least-privilege perms (`contents: read`, `pull-requests: write`) + `github.token`. 1 NICE-TO-HAVE (R20 consistency): em-dash in the `--title` line vs the file's own ASCII hyphens. | OK Clear (NICE-TO-HAVE) -- merged |
| #135 | Clear -- standing deep-dive DRAFT (re-opened post-milestone-merge of #118). **NOT merged** (owner-merge-only by design). R23 satisfied: `git diff --stat origin/master...origin/feature/ec-screen-deepdive` = ZERO changes on the four reviewer-owned docs; diff vs master = 2 files / 86 ins / 0 del (new `REVIEW-2026-06-27.md` + 1 append-only LEARNING-SCORECARD row). Still DRAFT, MERGEABLE. | OK Clear -- left open (owner-merge-only) |

### Observations (good patterns to keep)

- **NICE-TO-HAVE -> next-PR fix loop closed for #130.** The 06-27 14:00 run left #130 open on a single R13/R21 body/title defect (suite was 4-TC full I-U-D but title/body said `3/3` + insert/delete only, the UPDATE silently dropped). This run confirmed the Worker fixed both the title (`live 4/4`) and the body (added the UPDATE TC + the "MUST-FIX addressed" rules line) -- the suite code never changed, only the parse surface. Exactly the R13/R21 advisory-comment -> worker-fix -> re-verify loop working as intended (cf. PR #24).
- **Re-introducing GH Actions is policy-compatible when it is a no-LLM `gh`-only job on a public repo (#136).** PR #44 (2026-06-17) dropped GH Actions on a company-spend concern, but that concern was specifically the *paid LLM-driven reviewer* on Actions. #136 is a few-second `gh pr list/api compare/pr create` job that fires only at a milestone merge on a PUBLIC repo (free minutes), uses the built-in `github.token` (no extra API spend), and runs no model -- so it does not re-trip the #44 policy. The lesson: a prior "we removed X for policy reason Y" is scoped to Y; re-introducing a narrow, Y-free variant of X is fine, but say so explicitly so the audit trail shows the policy was considered, not forgotten.
- **The deep-dive program's manual step is being automated end-to-end (#134 + #136).** #136 removes the manual re-open of the standing draft after a milestone merge; #134 turns the periodic review into a repeatable skill. Together they harden the standing-draft model (never-auto-merge draft + auto-reopen + codified review) so the program runs unattended without the reviewer ever auto-merging accumulating learning notes.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| #134 skill references `DeepDiveLearnings/ec-screens/REVIEW-2026-06-27.md` as its reference example, but that file is program-branch-only (not on master where the skill lives) -- note it is program-branch-only or seed an on-master example (R21-adjacent) | Worker | Low |
| #136 `--title` line carries a U+2014 em-dash vs the file's own ASCII hyphens -- swap to ` - ` for consistency (no crash risk on ubuntu-latest; cosmetic R20) | Worker | Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/**.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload->RUN NOW` flakiness root cause | Worker | Medium |
| Carry-over (still open): #124 SOW date wording vs hardcoded `2011-01-01` (R21); Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | Low |

### Reviewer process note

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent `feature/ec-screen-deepdive` branch with a dirty working tree (sibling IUD/runner worktrees `wt-ec-learn`/`wt-ecsr*`/`wt-ghaction`/`wt-pgs`/`wt-prodgrp`/`wt-royalty*`/`wt-tract`/`wt-tws`/`wt-unitagr`/`wt-uws2` all present); it sits at `a7a0a3d` (v23) while master is at v25 -- the standing R23/MR4 drift. **The session-start cached read was the stale v23 main-checkout copy; the live v25 state (R24/R25) was re-read from the master copy in the worktree (MR4).** All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-28-0600` worktree off `origin/master`; the Worker's checkout and every `wt-*` sibling worktree were never touched. Two CLEAR merges (#130 head branch in `wt-uws2`, #136 head branch in `wt-ghaction`) succeeded on the remote but `gh --delete-branch` could not delete the local branch (checked out in a Worker worktree) -- the remote merge is unaffected (verified `state=MERGED` via `gh pr view`), and the worktrees were correctly left untouched.

---

## 2026-06-28 - Automated Review (14:00 AWST, 8 worker PRs #139/#140/#141/#142/#143/#144/#145/#146 + 1 standing draft #135)

_Open PRs trigger a full review (R14); run fired ~16:00 AWST (late 14:00 slot). All 8 worker PRs **CLEAR -- zero MUST-FIX -- all squash-merged**; #135 left open (owner-merge-only draft). **One new executable rule (R26)** formalises the owner-directed IUD deliverable gate that PR #140 introduced. R1-R25 remain current; version -> v26._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #139 | Clear (low effort, config). Adds Worker session-start step 5 (check open GitHub Issues), renumbers old 5 -> 6 in `CLAUDE.md`. Diff 1:1 to body (R21); 6 R9 fields; ASCII; single-purpose. | OK Clear -- merged |
| #140 | Clear (process/docs). New `docs/IUD-DELIVERABLE-CHECKLIST.md` (19 hard gates, owner-locked) + `ec-object-iud-builder` SKILL.md "Done =" rewrite + `PR-REVIEW-PROTOCOL.md` "IUD PR gate" append -- all additive/append-only; **R23 respected** (`lessons-learned.md` untouched -- left for the reviewer to formalise); 6 R9 fields; Files-touched 1:1 to diff (R21). Per the PR's own note, formalised as **R26** this run. Merged FIRST so the gate doc is on master before the IUD stack. | OK Clear -- merged |
| #141 | Clear (HIGH effort, new RF suite). **Pilot** for the 19-item standard (Document Date Term CD.0107, OV Bank-family, METHOD dd R:6 + numeric OFFSET R:7 filled-last). Internally consistent -- it IS Document Date Term, so `OV_DOC_DATE_TERM`/`AUTOTEST_DDT` are correct throughout. Live 4/4 = title/body/scorecard/README (R13); scorecard+registry append-only (R23); env creds (R16), ASCII (R20); CHECKLIST.md carries all 19. | OK Clear -- merged |
| #142 | Clear (HIGH effort). Document Received Term (CD.0108), clone of #141. Suite + PR body name the correct view (`ov_doc_received_term`); R23/R16/R20 clean. **1 NICE-TO-HAVE** (clone copy-paste, doc-only): CHECKLIST item 15 + README "DB ground truth" still cite the pilot's `OV_DOC_DATE_TERM` instead of `OV_DOC_RECEIVED_TERM`. | OK Clear (NICE-TO-HAVE) -- merged |
| #143 | Clear (HIGH effort). Payment Term (CD.0023). Good recon -- caught shifted field rows (Method R:7, mandatory DAY_VALUE R:8) instead of trusting the exemplar's R:6/R:7. Correct view in suite + body (`ov_payment_term`). **1 NICE-TO-HAVE**: same item-15/README `OV_DOC_DATE_TERM` copy-paste (-> `OV_PAYMENT_TERM`). | OK Clear (NICE-TO-HAVE) -- merged |
| #144 | Clear (HIGH effort). Calendar (CD.0024), **custom-URL OV** (grid `nav:form:T_data`, no GO). Good diagnose-before-retry: first run's `Row Should Exist` failure diagnosed vs DB (insert had PERSISTED -- a UI-read bug not an insert bug), grid id fixed, 3 diagnostic residuals cleaned, re-run 4/4. Correct view in suite + body. **1 NICE-TO-HAVE**: item-15/README `OV_DOC_DATE_TERM` (-> `OV_CALENDAR`) + README recon list vs CHECKLIST item-5 mismatch. | OK Clear (NICE-TO-HAVE) -- merged |
| #145 | Clear (HIGH effort). Calendar Collection (CD.0105), custom-URL OV; recon-first -> 4/4 first run. **Completes Date Objects 5/5.** T3+suite+playwright all use the correct `ov_calendar_collection`/`nav:form:T_data`; JOURNAL names the right view; R23/R16 clean. **1 NICE-TO-HAVE**: item-15 cites `AUTOTEST_CAL%` in `OV_DOC_DATE_TERM` (-> `AUTOTEST_CC%` in `OV_CALENDAR_COLLECTION`); item-1 `calendar_sow.md` (-> `calendar_collection_sow.md`); README "DB ground truth" `OV_DOC_DATE_TERM` (-> `OV_CALENDAR_COLLECTION`); README run-cmd path uses a space not underscore. | OK Clear (NICE-TO-HAVE) -- merged |
| #146 | Clear. Read-only grid-locator pre-flight guard (`tmp/scripts/preflight_grid_locator.py`): opens the screen, asserts the T3's declared `GRID_ID` resolves in the live DOM + GO presence matches, FAILS LOUD (exit 1) printing the actual grid ids when a sibling id was assumed -- no Save/no DB mutation, env creds (R16), ASCII (R20). Validated both ways vs live Calendar. SKILL.md trust-boundary #4 + Step-5 mandatory pre-flight + custom-URL OV cheat-sheet row turn the CD.0024 lesson into an enforced gate (section-disjoint from #140's "Done =" edit -- merged cleanly after #140). **1 NICE-TO-HAVE** (R9): body header "Evidence (guard validated both ways)" instead of the literal "DB ground-truth evidence". | OK Clear (NICE-TO-HAVE) -- merged |
| #135 | Clear -- standing deep-dive DRAFT, **NOT merged** (owner-merge-only). Increment since the 06:00 run: 7 new notes (CO.0070/0072/0074/0076/0077/0078/0079) + CO.0060 re-enrichment + `REVIEW-2026-06-27.md` + 1 LEARNING-SCORECARD row + CHECKLIST flips. Spot-checked bindings real & honest (CO.0070 `CHEM_TANK`->`OV_CHEM_TANK` OBJECT/VERSIONED; CO.0060 honestly "(no class resolved)" for generic `manage_copy_equipment`). **R23 satisfied** -- ZERO changes on the four reviewer-owned docs. | OK Clear -- left open (owner-merge-only) |

### Rules (apply immediately, no exceptions)

**R26 -- Every EC Object IUD PR is gated against the 19-item `docs/IUD-DELIVERABLE-CHECKLIST.md`** OK _live-validated (PR #140 introduced the gate; first applied to the #141-#145 batch this run)_
Owner-locked 2026-06-28: an EC Object IUD screen is "covered" ONLY when all 19 deliverables are green -- artifacts (SOW/README/JOURNAL/playwright/investigation/evidence/`CHECKLIST.md`), RF (T3 + suite), gates (robocop/dryrun/**live N/N**/**DB ground-truth**/**full I-U-D**/self-clean/hygiene), delivery (registry row + scorecard row + R9 PR). The Worker MUST copy the canonical list into the bundle as `CHECKLIST.md` with every item ticked + evidence. **Reviewer: verify each item against the PR and spot-check the SUBSTANCE, not just the tick** -- item 12 has a real N/N, item 13's DbVerify assertion is real, items 17/18 are 0-deletion appends (R23). A genuinely missing or failing deliverable is a MUST-FIX (do not merge, leave open, post the note-back in the checklist doc, re-review next run). _Nuance from this run's application: a copy-paste error in the bundle's EVIDENCE PROSE (e.g. CHECKLIST item-15 / README naming the wrong `OV_*` view) where the underlying deliverable is independently proven correct (suite + PR body name the right view, live N/N DB-verified) is a NICE-TO-HAVE doc-accuracy fix, NOT a failing gate -- the gate tests whether the deliverable exists and is real, and here it does/is. Reserve MUST-FIX for an ABSENT or FALSE deliverable._

### Observations (good patterns to keep)

- **Recon-first paid off across the batch -- two genuine trust-boundary catches.** #143 (Payment Term) re-derived the shifted form rows from live DOM instead of cloning the exemplar's R:6/R:7; #144 (Calendar) caught the custom-URL OV (grid `nav:form:T_data`, no GO) and diagnosed the resulting UI-read failure against the DB (the insert had persisted) rather than assuming an insert bug. These are exactly the template-trust-boundary points the `ec-object-iud-builder` skill warns about. #146 then turned the #144 lesson into an enforced pre-flight guard, closing the loop the same day.
- **Stacked-PR append-only conflicts resolved deterministically (R24).** The 4 children (#142-#145) each add/add-conflicted on `automation-scorecard.md` + `ec_screen_registry.md` after the parent's squash-merge (branch carries the parent's real commits; master has the squash). Each was resolved in a throwaway `--detach` worktree: retarget base->master, `git merge origin/master`, `git checkout --ours` on the two append-only docs (the branch is a strict superset = all prior rows + the new row), then `push origin HEAD:refs/heads/<branch>` (R24) -- never touching the Worker's worktrees. Verified post-merge: master's scorecard carries all 5 Date Objects rows (no row lost).
- **Recurring clone-substitution gap worth a generator.** The same wrong-view (`OV_DOC_DATE_TERM`) crept into the item-15 self-clean line + README "DB ground truth" of all four clones (#142-#145) because the clone substitutes the code/screen name but not every embedded `OV_*`/base-table token in the evidence prose. Non-blocking here (R26 substance met), but a clone helper that takes a full token map (code + short label + view + base table + tag) -- which the Worker flagged in #145's own JOURNAL -- would eliminate this class of doc drift. Reinforces R7/R13/R21 (docs must match reality).

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| Batch-wide clone copy-paste (doc-only, R26-NICE-TO-HAVE): CHECKLIST item 15 + README "DB ground truth" cite the pilot view `OV_DOC_DATE_TERM` instead of this screen's view in #142 (`OV_DOC_RECEIVED_TERM`), #143 (`OV_PAYMENT_TERM`), #144 (`OV_CALENDAR`), #145 (`OV_CALENDAR_COLLECTION` + prefix `AUTOTEST_CC%` + `calendar_sow.md`->`calendar_collection_sow.md`). Suite + PR body are correct; fix the bundle docs in a follow-up (a token-map clone helper would prevent recurrence). | Worker | Low |
| #146 PR body uses "Evidence (...)" not the literal R9 header "DB ground-truth evidence"; harmless (read-only work, evidence present) but drifts the 6-field gate -- write "DB ground-truth evidence -- N/A (read-only guard, validated live)". | Worker | Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/**.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload->RUN NOW` flakiness root cause; #134 skill REVIEW reference is program-branch-only; #136 `--title` em-dash. | Worker | Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp. | Worker | Low |

### Reviewer process note

- Main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent `feature/ec-screen-deepdive` branch, dirty, sitting at `a7a0a3d` (v23) while master is at v25 -- the standing R23/MR4 drift. The session-start cached read was the stale v23 copy; the live state (v25, R24/R25) was re-read from the master copy in the worktree (MR4) before extracting R26. All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-28-1400` worktree off `origin/master`; the stacked-PR conflict resolution used a throwaway `C:/tmp/wt-stack-0628` detached worktree (removed). The Worker's checkout and every `wt-*` sibling worktree were never touched.

## 2026-06-29 -- Automated Review (06:00 AWST, 2 worker PRs #148/#149 + standing draft #135)

_Open PRs trigger a full review (R14) despite 0 new master commits since #147/`c8c1fa5` (= master HEAD). Both worker PRs CLEAR -- zero MUST-FIX -- both squash-merged. #135 left open (owner-merge-only draft). **No new executable rules -- R1-R26 cover every finding; version stays v26.** R1-R26 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #148 | Clear (doc-only, low effort) -- closes the 06-28 14:00 (#147) batch-wide clone doc-drift NICE-TO-HAVE. All 4 Date Objects clones now cite their OWN OV view in CHECKLIST item-15 + README "DB ground truth" (`OV_CALENDAR`/`OV_CALENDAR_COLLECTION`/`OV_DOC_RECEIVED_TERM`/`OV_PAYMENT_TERM`), each cross-checked vs `ec_screen_registry.md:120-123`; SOW filename fix applied; `git grep OV_DOC_DATE_TERM` over the 4 clone dirs -> NONE. 6 body fields (R9); R23 trivially clean. **1 NICE-TO-HAVE (R7/R26-nuance):** the same README sentence's trailing `Base \`DOC_DATE_TERM\`` base-table clause was NOT corrected per-screen (each screen has its own base table per the registry) -- same drift class, automation DB-verified-correct, non-gating. | OK Clear (NICE-TO-HAVE) -- merged `15ead59` |
| #149 | Clear (HIGH effort -- changes the reviewer's own operating contract). Adds step-8d SME review dimensions + REVIEWER MINDSET + mandatory `ec-domain-reference.md` read to `.claude/review-prompt.txt` (+71); new 245-line `docs/ec-domain-reference.md`; scorecard +`Coverage Strategy (Phased Rollout)` section. SME-verified the new reference vs live/merged ground truth -- §1.1-1.6 patterns match R17/R19/R26 + merged evidence; §2's worked example `OV_UNIT_AGR` (not `OV_UNIT_AGREEMENT`) confirmed correct against the merged live-4/4 #122 suite + registry (NOT a stale guess). 6 body fields (R9); R23 OK on scorecard (only `-` line = date bump). **1 NICE-TO-HAVE (R21):** body "Files touched" lists ONLY `review-prompt.txt`, omitting the new 245-line `ec-domain-reference.md` + the scorecard edit -- under-claim not over-claim, non-gating. | OK Clear (NICE-TO-HAVE) -- merged `8885201` |
| #135 | Clear (re-confirmation) -- STANDING/DRAFT EC Screen Deep-Dive program. Head `48b8fa0` unchanged since the 06-28 14:00 review; increment is the already-reviewed CO.0070-0079 + CO.0060 fix + `REVIEW-2026-06-27.md`. R23 satisfied (0 changes on the four reviewer-owned docs); CO.0070 binding spot-checked real (`CHEM_TANK`->`OV_CHEM_TANK`), ASCII-clean. **NOT merged** (owner-merge-only, still DRAFT). | OK Clear -- left open (owner-merge-only) |

### Observations (good patterns to keep)

- **The reviewer SME-upgrade (#149) is sound, and verifying its own reference doc paid off immediately.** A mandatory-read knowledge base can propagate wrong domain claims if it ships an unverified "fact", so every concrete assertion in `ec-domain-reference.md` was checked against merged/live evidence before accepting -- the §2 worked example `OV_UNIT_AGR` looked like it might contradict the 06-25 review-log's loose paraphrase ("ov_unit_agreement"), but the actual merged #122 code/registry assert `ov_unit_agr`, so the doc is right and the review-log summary was the loose one. Lesson reaffirmed (MR1): verify the live artifact, not the prose summary of it -- in both directions.
- **SME review caught a residual drift the doc-fix PR itself missed (#148).** #148 corrected the OV-view clause but left the adjacent `Base DOC_DATE_TERM` clause in the same README sentence pointing at the pilot across all 4 clones. A line-level clone substitution that fixes one token in a sentence and not its neighbour is exactly the failure mode a **token-map clone helper** (code + label + view + base table + tag) would eliminate -- now flagged for the 3rd time (#145 JOURNAL, #147 reviewer note, here). This is the strongest argument yet for building it before the next sibling batch.
- **0-new-master-commit + open-PRs => still a full review (R14 working as designed).** Master HEAD was the previous review commit, yet two substantive PRs (created after the 14:00 run) needed review. The skip logic correctly did not fire.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| Build a **token-map clone helper** (code + short label + OV/DV view + base table + AUTOTEST prefix + SOW filename + grid id + registry code) so sibling-batch evidence prose is fully substituted in one pass -- would have prevented BOTH the #147 OV-view drift and the #148 residual base-table drift. 3rd recurrence. | Worker | Medium |
| #148 residual (doc-only): the 4 Date Objects clone READMEs still read `Base \`DOC_DATE_TERM\`` instead of each screen's own base table (`DOC_RECEIVED_TERM`/`PAYMENT_TERM`/`CALENDAR`/`CALENDAR_COLLECTION`). | Worker | Low |
| #149 body under-claim (R21): future reviewer-prompt PRs must list every touched file (it added a 245-line `ec-domain-reference.md` + a scorecard edit not in "Files touched"). | Worker | Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/**.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload->RUN NOW` flakiness root cause; ~1 GB Help-PNG history (downscale/JPEG/LFS). | Worker | Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp. | Worker | Low |

### Reviewer process note

- Main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent dirty `feature/ec-screen-deepdive` branch, behind master on the reviewer-owned docs (R23/MR4 drift -- the session-start cached read was a stale v23 copy; live v26 + R24/R25/R26 were re-read from the master copy in the worktree per MR4 before any review judgement). All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-29-0600` worktree off `origin/master`; the Worker's checkout and every `wt-*` sibling/runner worktree (`wt-ec-learn`, `wt-ecsr*`, `wt-royalty*`, `wt-tract`, `wt-tws`, `wt-uws2`, `wt-pgs`, `wt-prodgrp`, `wt-unitagr`, `wt-iudchk`, `wt-ghaction`, `wt-calclab`, `wt-docdateterm`) were never touched. No reviewer worktree from this run (`wt-review-2026-06-29-0600`) is left behind after step 17.

---

## 2026-06-29 -- Automated Review (14:00 AWST, 1 worker PR #152 + standing draft #135)

_Open PRs trigger a full review (R14); run fired ~16:00 AWST (late 14:00 slot). 0 new master commits since #151/`e4cb4d4` (the 06:00 review = master HEAD). **#152 CLEAR -- zero MUST-FIX -- squash-merged**; #135 standing draft re-confirmed CLEAR, NOT merged (owner-merge-only). **No new executable rules -- R1-R26 cover every finding; version stays v26.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #152 | Clear (low/medium effort -- a 1-line runner config change + a 1-line scorecard note). Raises the EC screen deep-dive runner's per-run batch cap **8 -> 25** (default), overridable via **`EC_LEARN_MAX_SCREENS`**; verified `MAXN = int(os.environ.get('EC_LEARN_MAX_SCREENS', os.environ.get('EC_LEARN_MAX', '25')))` meets all 4 acceptance criteria (no-env->25; `EC_LEARN_MAX_SCREENS=50`->50; legacy `EC_LEARN_MAX=8` alone->8 back-compat; both set->primary wins). Recon-first name reconciliation (issue/scorecard assumed `EC_LEARN_MAX_SCREENS`; real knob was `EC_LEARN_MAX`) handled by honouring the new name + keeping the legacy alias. R9 (6 fields), R21 (Files-touched 1:1 to the 2-file diff), R18/R20 (both added `.py` lines ASCII; runner is `tools/**`, outside the hygiene glob, noted), R8 (base = master HEAD). The single `-` line on `automation-scorecard.md` is a legitimate factual update of the runner-default note -- not a reviewer-entry clobber, so R23 not implicated. **2 NICE-TO-HAVE** (R21/doc): scorecard `_Last updated_` not bumped on the edited line; "increase up to 50" wording implies a hard cap the code does not enforce. | OK Clear (NICE-TO-HAVE) -- squash-merged (`b1370fe`) |
| #135 | Clear re-confirmation -- standing deep-dive draft, **NOT merged** (owner-merge-only, still DRAFT). Head `48b8fa0`->`4081edb` (1 new commit: CO.0080/0081/0082 + 5 note re-touches, "1 full, 7 partial"). **R23 satisfied** -- `git diff --stat origin/master...origin/feature/ec-screen-deepdive` on the four reviewer-owned docs = EMPTY (the 8 deletions are CHECKLIST `[ ]`->`[x]` flips + note re-enrichment). Spot-checked CO.0081 (Stream Formula Editor) + CO.0080 (Rule Group Combination): real captured Help, honest `(no class resolved from URL/LABEL)` partial marking (R3, not fabricated), pure-MD notes ASCII-clean. | OK Clear -- left open (owner-merge-only) |

### Observations (good patterns to keep)

- **Recon-first beat the issue's assumption.** #150 (and the scorecard) named the knob `EC_LEARN_MAX_SCREENS`, but the runner's existing env var was `EC_LEARN_MAX`; the worker located the real constant before editing rather than adding a second, dead knob. The fix honours the new name AND keeps the legacy one as a quiet alias -- the correct way to reconcile a doc/code name mismatch without breaking an existing caller. Reinforces the standing "REFER/recon before guessing" discipline.
- **The standing-draft invariants held again.** #135's only safety obligations for a never-auto-merged draft -- (a) never merge it, (b) R23 zero `-` lines on the four reviewer-owned docs, (c) partials marked honestly not fabricated -- all held. An unchanged-content draft is a re-confirmation; here the head DID move (CO.0080-0082) so the increment's substance was spot-checked, not just the invariants.

### Gaps (verified against filesystem / live diff)

| Gap | Owner | Priority |
|-----|-------|----------|
| #152 scorecard edit did not bump `_Last updated_`; "increase up to 50" wording implies a hard cap the runner does not enforce (env accepts any int) -- doc-only, non-gating | Worker | Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (would catch the runner + `gen_checklist.py:33`); `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | Low |

### Reviewer process note

- Main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent dirty `feature/ec-screen-deepdive` branch, behind master on the reviewer-owned docs (R23/MR4 drift -- the session-start cached read was a stale v23 copy; live v26 + R24/R25/R26 were re-read from the master copy in the worktree per MR4 before any review judgement). All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-29-1400` worktree off `origin/master`; the Worker's checkout and every `wt-*` sibling/runner worktree (`wt-ec-learn`, `wt-ecsr*`, `wt-royalty*`, `wt-tract`, `wt-tws`, `wt-uws2`, `wt-pgs`, `wt-prodgrp`, `wt-unitagr`, `wt-iudchk`, `wt-ghaction`, `wt-calclab`, `wt-docdateterm`, `wt-runner`) were never touched. No reviewer worktree from this run (`wt-review-2026-06-29-1400`) is left behind after step 17.

---

## 2026-06-30 - Automated Review (06:00 AWST, 1 open PR #135, STANDING/DRAFT)

_Open PR triggers a full review (R14). The only open PR is the standing **EC Screen Deep-Dive** draft (#135) on the Worker's permanent branch. Its head `4081edb` is unchanged since the 2026-06-29 14:00 re-verify that cleared it - no new pushed content (0 new master commits since #153/`92a0302`). **Re-confirmed CLEAR; NOT merged** (owner-merge-only standing draft, still DRAFT). **No new executable rules - version stays v26.** R1-R26 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #135 | Clear (re-confirmation). Head `4081edb` is byte-identical to the commit cleared at the 2026-06-29 14:00 review (`gh pr view 135 --json headRefOid` = `4081edb...`; 0 new master commits since #153). Per the unchanged-head pattern the already-cleared content is NOT re-litigated; the run instead verified the safety invariants: (a) the never-auto-merge invariant holds (still `DRAFT`); (b) **R23 satisfied vs the now-further-advanced master** - `git diff --stat origin/master...origin/feature/ec-screen-deepdive` over the FIVE reviewer-owned docs (`lessons-learned.md`/`review-log.md`/`automation-scorecard.md`/`STATUS.md`/`ec-domain-reference.md`) is EMPTY = ZERO `-` (deletion) lines; the 11 deletions in the full diff are all CHECKLIST `[ ]`->`[x]` flips + the CO.0060 note re-enrichment, none on reviewer docs; (c) substance spot-check - newest note CO.0082 (Sub Area) carries a real metadata binding `SUB_AREA -> OV_SUB_AREA` (OBJECT/VERSIONED, base `GEOGRAPHICAL_AREA`), correct OV typing, genuine captured Help, and all new notes (CO.0072/0074/0076/0077/0078/0079/0080/0081/0082) are ASCII-clean (R18/R20, `[^\x00-\x7F]` -> 0). **NOT merged** (owner-merge-only standing draft, still DRAFT). | OK Clear - left open (owner-merge-only) |

### Observations (good patterns to keep)

- **An unchanged open-PR head is a re-confirmation, not a re-review of the same diff (4th consecutive standing-draft re-confirm).** #135's head has not moved since the 14:00 re-verify, so the deep-dive *content* (already CLEAR) was not re-scored; the run verified (a) the never-auto-merge invariant, (b) R23 still holds against a master that has advanced further (now +`ec-domain-reference.md` as a fifth reviewer-owned doc since #149), and (c) the prior pass's content is unchanged. This is the correct, low-cost shape for a standing-draft PR the reviewer is forbidden to merge: confirm invariants, don't re-litigate frozen content.
- **The fifth reviewer-owned doc is now in the R23 check.** Since #149 added `docs/ec-domain-reference.md` as reviewer-owned, the R23 deletion-line sweep was run over all FIVE files (not the original four). The branch shows zero `-` lines on every one - the standing-draft "don't track reviewer-owned docs on the permanent branch" discipline (R23 better-still clause) is holding even as the reviewer-owned set grows.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `DeepDiveLearnings/ec-screens/gen_checklist.py:33` `print("wrote CHECKLIST.md -...",...)` emits a U+2014 em-dash to stdout (R18/R20 - `UnicodeEncodeError` on a cp1252 redirected/captured console). Pre-existing on master, outside the hygiene-guard glob, non-gating. Still open. | Worker | 🟢 Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (would catch `gen_checklist.py:33` and the runner); fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | 🟢 Low |

### Reviewer process note (standing-draft on a permanent Worker branch)

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's **permanent** branch `feature/ec-screen-deepdive` with a dirty working tree, and is itself behind master on the reviewer-owned docs (R23/MR4 drift - it was at an older rule version locally; the live v26 + R23-R26 were re-read from the master copy in the isolated worktree per MR4 before any review judgement). All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-30-0600` worktree off `origin/master`; the Worker's checkout and every `wt-*` sibling/runner worktree were never touched. The reviewer worktree from this run is removed at step 17.

---

## 2026-06-30 - Automated Review (06:00 re-verify, late morning slot, 1 open PR #135 STANDING/DRAFT)

_Re-fire of the morning slot (clock ~08:00 AWST). The 06:00 run (#154/`cd9ebe4`) already cleared #135 at head `4081edb`; this run fired with 1 genuinely new worker commit on the standing draft (`4081edb`->`e63237e`), so it is a distinct **re-verify** (per the 2026-06-23 precedent), not a crash-restart duplicate. Open PR triggers a full review (R14). #135 **re-confirmed CLEAR; NOT merged** (owner-merge-only standing draft, still DRAFT). **No new executable rules - version stays v26.** R1-R26 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #135 | Clear (re-confirmation). New commit `e63237e` ("CO.0060, CO.0074, CO.0076, CO.0077, CO.0078, CO.0080, CO.0081, CO.0086 - 0 full, 8 partial") adds one new note (CO.0086 Stream Reference Values) + re-touches 7 existing notes (date-stamp bump) + a CHECKLIST flip. **R23 satisfied** - `git diff --stat origin/master...origin/feature/ec-screen-deepdive` on the FIVE reviewer-owned docs is EMPTY (zero `-` lines); the 8 deletions in `4081edb..e63237e` are date bumps + the CO.0086 CHECKLIST `[ ]`->`[~]` flip, none on reviewer docs. **Content spot-check:** CO.0086 honestly marked `[~]` partial with `(no class resolved from URL/LABEL)` (R3) - correct for a generic-maintain/calc-type screen with no resolvable class; the "0 full, 8 partial" label is accurate; all 8 touched notes ASCII-clean (R18/R20, `[^\x00-\x7F]` -> 0). **NOT merged** (owner-merge-only standing draft, still DRAFT). | OK Clear - left open (owner-merge-only) |

### Observations (good patterns to keep)

- **A re-fire with a genuinely-new head is a re-verify, not a duplicate skip.** #154 cleared head `4081edb`; this run saw `e63237e` (1 new commit), so it correctly logged a distinct re-verify row rather than skipping as a same-hour duplicate. The dedup guard (step 6) only suppresses a row when the date AND hour match AND there is no new content - new pushed content on the open PR is exactly what justifies a fresh review pass.
- **Honest `[~]` partial marking continues to be the right shape.** A "0 full, 8 partial" batch (all missing DB binding) is a transparent, resumable outcome for calc/formula-editor/generic-maintain screens that have no resolvable class - far better than fabricating a binding to flip the box to `[x]`. CO.0086's `(no class resolved from URL/LABEL)` is the model (R3).

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (would catch `gen_checklist.py:33`); fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | 🟢 Low |

### Reviewer process note (standing-draft on a permanent Worker branch)

- Same posture as the 06:00 run: the main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's **permanent** branch `feature/ec-screen-deepdive` with a dirty working tree, locally behind master on the reviewer-owned docs (R23/MR4 drift - the live v26 + R23-R26 were re-read from the master copy per MR4 before any review judgement). All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-06-30-0600r` worktree off `origin/master`; the Worker's checkout and every `wt-*` sibling/runner worktree were never touched. The reviewer worktree from this run is removed at step 17.

---

## 2026-07-01 — Automated Review (14:00 AWST, 1 open PR #135 — STANDING/DRAFT)

_Open PR triggers a full review (R14). The only open PR is the long-lived **STANDING/DRAFT** EC Screen Deep-Dive program PR (#135) on the Worker's permanent branch. Its head `e63237e` is byte-identical to the commit cleared at the 2026-06-30 06:00 re-verify (0 new master commits since #155/`77f2abd`; no 2026-06-30 14:00 run was logged, so this is the next scheduled slot). **Re-confirmed CLEAR; NOT merged** (owner-merge-only standing draft). **No new executable rules — version stays v26.** R1–R26 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #135 | Clear (re-confirmation). Head `e63237e` unchanged since the 06-30 06:00 re-verify — no new pushed content. Per the unchanged-head standing-draft pattern, confirmed the safety invariants rather than re-litigating frozen content: (a) **never-auto-merge invariant holds** (still `draft: true`); (b) **R23 satisfied vs the further-advanced master** — `git diff --stat origin/master...origin/feature/ec-screen-deepdive` on the FIVE reviewer-owned docs (`docs/lessons-learned.md`/`docs/review-log.md`/`docs/automation-scorecard.md`/`STATUS.md`/`docs/ec-domain-reference.md`) is EMPTY = ZERO `-` lines; the 12 deletions in the full diff are all CHECKLIST `[ ]`->`[x]`/`[~]` flips + note date-stamp/enrichment, none on reviewer docs; (c) **content spot-check** — newest notes (CO.0079/0080/0081/0082/0086) unchanged since the re-verify; CO.0086 (Stream Reference Values) remains an honest `[~]` partial (`no class resolved from URL/LABEL`, not fabricated — R3); new CO.* notes ASCII-clean. | OK Clear — left open (owner-merge-only) |

### Observations (good patterns to keep)

- **An unchanged open-PR head is a re-confirmation, not a re-review of the same diff.** #135's head has not moved since the 06-30 06:00 re-verify, so the deep-dive *content* (already CLEAR repeatedly) was not re-litigated; the run instead verified (a) the never-auto-merge invariant still holds, (b) R23 is still satisfied vs the now-further-advanced master, and (c) the newest notes remain ASCII-clean and honestly partial-marked. This is the correct shape for a standing-draft PR the reviewer is forbidden to merge: confirm the safety invariants, don't re-score frozen content.
- **R18-exemption for markdown notes held under scrutiny.** An ASCII scan over all branch notes flagged PO.0001/0002/0003/0005 as containing non-ASCII bytes — but they are **pre-existing on master, identical, and NOT in this PR's diff**, and markdown notes are R18-exempt regardless (R18/R20 scope only to console-printed / PowerShell-parsed `.py` files, never `.write_text(encoding="utf-8")` notes). Verified before flagging (MR1) — not a finding.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| `DeepDiveLearnings/ec-screens/gen_checklist.py:33` `print(...)` em-dash to stdout (R18/R20, cp1252 crash risk); pre-existing on master, outside the hygiene glob, non-gating | Worker | 🟢 Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | 🟡 Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

### Reviewer process note (standing-draft on a permanent Worker branch)

- Same posture as every recent run: the main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's **permanent** branch `feature/ec-screen-deepdive` with a dirty working tree, locally **55 commits behind master** on the reviewer-owned docs (R23/MR4 drift — the live v26 + R23–R26 were re-read from the master copy per MR4 before any review judgement; the local stale copy showed only v23). All review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-01-1400` worktree off `origin/master`; the Worker's checkout and every `wt-*` sibling/runner worktree were never touched. The reviewer worktree from this run is removed at step 17.

---

## 2026-07-01 - Automated Review (14:00 re-verify, 1 open PR #135 - STANDING/DRAFT)

_Re-fire of the 14:00 slot (clock ~16:00 AWST). The morning 14:00 run merged as #156 (`5107e44`, now master HEAD); since then the Worker pushed ONE new commit (`e63237e`->`e902713`) to the permanent branch, so this is a distinct follow-up row (not a crash-restart, not a duplicate) per the 2026-06-30 re-verify precedent. Open PR triggers a full review (R14). **#135 re-confirmed CLEAR; NOT merged** (owner-merge-only standing draft). **No new executable rules - R1-R26 cover all findings; version stays v26.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #135 | Clear (re-confirmation). Head advanced `e63237e`->`e902713` since #156; the sole new commit is labelled "0 full, 8 partial" and is accurate - it adds NO new DB bindings, only re-touches the deep-dive date-stamp (`2026-06-30`->`2026-07-01`) on 8 already-partial notes (CO.0060/0074/0076/0077/0078/0080/0081/0086). **R23 stays satisfied:** `git diff --stat origin/master...origin/feature/ec-screen-deepdive` on the FIVE reviewer-owned docs (`docs/lessons-learned.md`/`docs/review-log.md`/`docs/automation-scorecard.md`/`STATUS.md`/`docs/ec-domain-reference.md`) is EMPTY = ZERO `-` lines; the 8 deletions in the new commit are all date-stamp single-line flips, none on reviewer docs. Content spot-check: CO.0086 (Stream Reference Values) + CO.0081 (Stream Formula Editor) remain honest `(no class resolved from URL/LABEL)` partials with genuine captured Help, not fabricated bindings (R3) - correct for generic-maintain/calc-editor screens with no OV/TV class. All 8 touched notes ASCII-clean (R18/R20, ripgrep `[^\x00-\x7F]` -> 0 matches). **NOT merged** (owner-merge-only standing draft, still DRAFT). | OK Clear - left open (owner-merge-only) |

### Observations (good patterns to keep)

- **A re-touch-only advance is a re-confirmation, not a re-review.** The new commit changes nothing but the deep-dive date stamp on 8 partial notes, so the deep-dive content (already CLEAR across many prior runs) was not re-litigated; the run instead verified the three standing-draft safety invariants: (a) never-auto-merge holds (still DRAFT); (b) R23 satisfied vs the now-further-advanced master; (c) the "0 full, 8 partial" commit label is truthful and no partial was silently promoted to a fabricated binding. This is the correct shape for a standing-draft PR the reviewer is forbidden to merge.
- **Honest partial marking still holding at re-visit.** CO.0086 and CO.0081 were re-visited by the runner and kept their `[~]`/`(no class resolved)` marking rather than being back-filled with a guessed class - the runner does not invent bindings on a second pass (R3).

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**` (would catch `gen_checklist.py:33`); fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause | Worker | Medium |
| Carry-over (still open): Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD (Transport System / Contract Type); WR.0010.02 Well Oil Comp | Worker | Medium |

### Reviewer process note

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent, dirty `feature/ec-screen-deepdive`. Following the standing precedent, ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-01-1400r` worktree off `origin/master`; the main checkout and every `wt-*` sibling worktree (incl. the runner's `wt-ec-learn`) were never touched. `lessons-learned.md` was re-read live from the master copy at session start per MR4 (the Worker's branch copy is behind master = R23/MR4 drift, which is expected on the permanent branch and is why the four/five reviewer-owned docs are best kept off it entirely).

---

## 2026-07-03 — Automated Review (06:00 AWST, 6 new master commits since #157, 1 open PR #159 STANDING/DRAFT)

_Open PR triggers a full review (R14); also 6 new master commits since the 2026-07-01 14:00 re-verify (`5107e44`) clear the >=3-commit threshold independently. Reviewed #159 (the reopened standing draft, following #135's milestone merge via `e9ad812`) at head `406b989`. **CLEAR, no MUST-FIX, NOT merged** (owner-merge-only by design). **One new rule (R27).** R1-R26 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #159 | Clear — 8 new commits since the 2026-07-01 14:00 re-verify's head (`e902713`): CO.0060/0074/0076-0082/0086 upgraded from partial to full via a runner rework that sources Help from the local offline online-help corpus instead of live-scraping the sandbox web app, plus 17 newly captured screens (CO.0087/0088/0089/0091/0093/0094x2/0096/0096.01/0098/0100/0102/0103/0105/0108/0118). Spot-checked bindings (CO.0118 `REGION -> OV_REGION`/`GEOGRAPHICAL_AREA`; CO.0060 `EQUIPMENT` interface w/o view) are real, not fabricated. Runner refactor (+145/-76) removes the Playwright/browser/login dependency entirely, fixes the perpetual-partial re-pick loop (full = structure resolved, not Help-gated), and adds a NO-PROGRESS ALARM that loudly flags a stalled run. `py_compile` OK, 0 non-ASCII bytes (R18/R20). **R23 clean** — `git diff --stat origin/master...origin/feature/ec-screen-deepdive` on the five reviewer-owned docs is empty. 2 NICE-TO-HAVE posted (dead code left by the corpus-switch refactor; new `mergeable: CONFLICTING` status against master — see R27). | ✅ Clear (NICE-TO-HAVE) — left open (owner-merge-only) |

### Rules (apply immediately, no exceptions)

**R27 — A squash-style milestone merge of a permanent standing-draft branch breaks shared history for files both sides keep touching** ✅ _live-validated via `git merge-tree` against PR #159_
Standing-draft branches like `feature/ec-screen-deepdive` are milestone-merged into master periodically (e.g. `e9ad812`, "milestone merge (post-#118 batch)"). When that merge is a **squash** (or any merge that doesn't preserve the branch's own commit ancestry as a real parent), `git merge-base origin/master origin/feature/ec-screen-deepdive` resolves to an OLD commit from *before* the milestone (`1910222`, not `e9ad812`) — because master's squash commit and the branch's continuing commits share no direct lineage. Any file both sides go on to touch after that point (`CHECKLIST.md`, and any revisited note like `notes/CO.0060.md`) then presents as "changed in both" with real conflict markers, even though there is no genuine content contradiction — it is a false conflict manufactured by the squash. First observed live on PR #159 (`mergeable: CONFLICTING`); confirmed via `git merge-tree $(git merge-base ...) origin/master origin/feature/ec-screen-deepdive`. This is NOT reviewer-fixable (the reviewer never merges this draft) — it is the **owner's** responsibility at the next milestone merge: either (a) `git rebase origin/master` the standing-draft branch immediately after any squash milestone merge, before further commits land on it, or (b) perform future milestone merges as a true `git merge --no-ff` (not squash) so the branch's ancestry is preserved and no false conflict can arise. Distinguish this from R23 (which governs the four/five *reviewer-owned* docs specifically) — R27 covers the branch's *own* content files.

### Observations (good patterns to keep)

- **Runner evolution is converging on a robust, dependency-light design.** Across this cycle the runner went from live-browser Help scraping (fragile: login/timeout/DOM-drift risk) to an offline local corpus lookup (`docs/EC/EC Calculation/online-help-14.2.5/`) — faster, deterministic, and removes an entire class of flakiness (browser/login failures) that previously caused silent stalls. Combined with the redefined completeness gate (structure-resolved, not Help-gated) and the new NO-PROGRESS ALARM, three real operational failure modes from the last two weeks (perpetual-partial loop, silent 06-30->07-01 stall, browser-login ABORTED runs) are now each independently guarded against.
- **R23 holding steady across an owner milestone-merge cycle.** Despite the PR base moving (old #135 -> merged -> new #159 reopened), the five reviewer-owned docs still show zero deletion risk — the append-only discipline survives across milestone boundaries, which is exactly what R23 was designed to guarantee.
- **NICE-TO-HAVE -> next-commit loop still open, not yet exercised this cycle**: the dead `EC_URL`/`EC_USER`/`EC_PASS`/`help_text()` leftovers are a natural target for the runner's next touch.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| PR #159 is `mergeable: CONFLICTING` against master (R27) — real conflicts on `CHECKLIST.md` + `notes/CO.0060.md` will surface at the next milestone merge; rebase onto master or switch to `--no-ff` merges going forward | Owner | 🔴 High |
| `run_ec_screen_learn.py` dead code from the corpus-switch refactor: unused `EC_URL`/`EC_USER`/`EC_PASS` constants + unused `help_text(page, ...)` Playwright function | Worker (next runner touch) | 🟢 Low |
| Carry-over (still open, unchanged this cycle): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

Review-doc edits made in isolated `C:/tmp/wt-review-2026-07-03-0600` worktree off `origin/master`; the Worker's dirty permanent-branch checkout (`C:\Projects\ChoongYin_OS`, still on `feature/ec-screen-deepdive`) and all sibling `wt-*` worktrees were never touched. A stale, never-pushed `C:/tmp/wt-review-2026-07-02-0600` worktree (0 commits, crashed before any doc edit) was found and removed per step 17.

---

## 2026-07-04 - Automated Review (06:00 AWST, 1 open PR #159, STANDING/DRAFT)

_Open PR triggers a full review (R14) despite 0 new master commits since #164/`ccfd603`. #159's head advanced `20d41a8` -> `d7e0c8d` (1 new Worker commit). **Re-confirmed CLEAR - zero MUST-FIX - NOT merged** (owner-merge-only standing draft, still DRAFT). **No new executable rules - version stays v27.** R1-R27 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #159 | Clear. 1 new commit `d7e0c8d`: raise runner default batch size 8 -> 100 screens/run (`EC_LEARN_MAX` default + matching docstring line - a 2-line, ASCII-clean change with no R7 doc/code drift). Rationale sound: the already-reviewed 2026-07-03 corpus-Help refactor removed the browser bottleneck (~0.5s/screen), so the 8/day throttle was pacing the remaining ~1,377 screens at ~172 days; 100/day finishes in ~14. Per-screen try/except + hard timeout + NO-PROGRESS alarm unchanged, so a 100-screen batch cannot hang or flail any more than an 8-screen one. Safety invariants re-confirmed: never-auto-merge holds (still DRAFT); **R23 clean** (`git diff --stat origin/master...origin/feature/ec-screen-deepdive` on the five reviewer-owned docs = EMPTY, zero `-` lines). 2 NICE-TO-HAVE posted (repo-growth pacing; R27 carry-over). | OK Clear (NICE-TO-HAVE) - left open (owner-merge-only) |

### Observations (good patterns to keep)

- **Throttle removal follows the bottleneck, not the other way round.** The 8/day cap existed to bound a slow, fragile browser loop; once the corpus refactor made the loop fast and deterministic, the Worker raised the cap in a separate, minimal, well-argued commit (with the arithmetic in the commit message) rather than bundling it into the refactor. Change-one-thing discipline keeps each commit independently reviewable.
- **Repo-growth math got cheaper than feared - measured, not assumed (MR1).** The notes tree measures ~140KB/screen actual (6.6MB over the current 138 note files, `git cat-file -s` summed), so full 1,457-screen coverage projects to roughly +190MB of committed corpus images - well under the earlier ~1GB live-capture projection. Acceptable as-is; but at 100/day the bulk lands within ~2 weeks, so if LFS/out-of-repo storage (open #110 carry-over) is ever going to happen, the economical moment is BEFORE the sweep completes, not after.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| PR #159 still `mergeable_state: dirty` (CONFLICTING) against master (R27, unchanged since 2026-07-03 06:00) - rebase onto master or `--no-ff` at the next milestone. At 100 screens/day the next milestone arrives fast; resolving NOW avoids a much larger conflict surface | Owner | 🔴 High |
| Decide LFS/out-of-repo for corpus Help images BEFORE the 100/day sweep completes (~2 weeks); after that the ~190MB is permanently in history (revised down from the ~1GB #110 projection - measured ~140KB/screen) | Owner/Worker | 🟡 Medium |
| `run_ec_screen_learn.py` dead code from the corpus-switch refactor (unused `EC_URL`/`EC_USER`/`EC_PASS` + `help_text()`) - untouched by `d7e0c8d`, still open | Worker (next runner touch) | 🟢 Low |
| Carry-over (still open, unchanged this cycle): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

Review-doc edits made in isolated `C:/tmp/wt-review-2026-07-04-0600` worktree off `origin/master`; the Worker's dirty permanent-branch checkout (`C:\Projects\ChoongYin_OS`, on `feature/ec-screen-deepdive`) and all sibling `wt-*` worktrees were never touched.

---

## 2026-07-04 - Automated Review (14:00 AWST, 1 open PR #159, STANDING/DRAFT)

_Open PR triggers a full review (R14) despite 0 new master commits since #165/`405c30f`. #159's head advanced `d7e0c8d` -> `076f420` (1 new Worker commit). **Re-confirmed CLEAR - zero MUST-FIX - NOT merged** (owner-merge-only standing draft, still DRAFT). **No new executable rules - version stays v27.** R1-R27 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #159 | Clear. 1 new commit `076f420`: the FIRST run at the raised 100-screen batch cap - 100 new full screens (CO.0133..CO.1003, 0 partial), 259 files +2360/-100. **Pure-data commit** verified against the diff: zero `.py`/`.ps1`/`.robot`/`.resource`/`.sql` changes; only 100 new `notes/*.md` + corpus screenshots + CHECKLIST flips (200 changed lines = exactly 100 `[ ]`->`[x]`; new-note file count = 100 = commit-message claim, R21 holds). CHECKLIST now 181 `[x]` / 1 `[~]`. **R23 clean** (diff vs master on the reviewer-owned docs = EMPTY). **R18/R20 clean** (zero non-ASCII bytes on ADDED lines; the 103 context-line em-dashes are pre-existing exempt markdown). **Honest classification:** CO.0500 (Keycloak account) / CO.1000-1003 (User Maintenance family) record "(no class resolved from URL/LABEL)" and are typed process/config - a valid terminal type per the runner logic cleared 2026-07-03; no fabricated bindings. 1 NICE-TO-HAVE posted (dead `PARTIAL` branch, below). | OK Clear (NICE-TO-HAVE) - left open (owner-merge-only) |

### Observations (good patterns to keep)

- **The 100-screen cap raise performed exactly as argued.** The 06:00 review cleared the 8->100 cap raise on the arithmetic that the corpus refactor removed the browser bottleneck; this run is the empirical confirmation - 100 screens captured in one run, all with notes + flips consistent, zero code drift, zero partials fabricated to full (the no-class screens carry their honest "(no class resolved)" marker inside the note). Predict-then-confirm across two review cycles is the right cadence for a throughput change.
- **"0 partial" is now structurally guaranteed, which weakens it as an audit signal.** `full = has_db or bool(info['classes']) or is_process` is tautologically True (`is_process = not info['classes']`), so `done_partial` and the `PARTIAL[...]` log branch are dead code. That is the documented intent (no perpetual-partial re-picks), but a reader of "(100 full, 0 partial)" may wrongly infer every binding resolved. NICE-TO-HAVE posted: simplify to `full = True` and log flag counts (e.g. "100 screens, N flagged no-corpus-Help / no-class") so the commit message keeps informational content.

### Gaps (verified against filesystem / GitHub API)

| Gap | Owner | Priority |
|-----|-------|----------|
| PR #159 still `mergeable_state: dirty` (CONFLICTING) against master (R27, unchanged since 2026-07-03 06:00) - re-confirmed via the GitHub API this run. At 100 screens/day the conflict surface compounds every run; rebase onto master or switch to `--no-ff` milestone merges NOW, before the next milestone | Owner | 🔴 High |
| Runner `full` flag is tautologically True - dead `done_partial`/`PARTIAL` branch; replace "(N full, 0 partial)" with flag-count logging | Worker (next runner touch) | 🟢 Low |
| Decide LFS/out-of-repo for corpus Help images BEFORE the 100/day sweep completes (~2 weeks at current pace; 181/1457 done) | Owner/Worker | 🟡 Medium |
| Carry-over (still open, unchanged this cycle): `run_ec_screen_learn.py` dead corpus-switch code (`EC_URL`/`EC_USER`/`EC_PASS` + `help_text()`); extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

Review-doc edits made in isolated `C:/tmp/wt-review-2026-07-04-1400` worktree off `origin/master`; the Worker's dirty permanent-branch checkout (`C:\Projects\ChoongYin_OS`, on `feature/ec-screen-deepdive`) and all sibling `wt-*` worktrees were never touched.

---

## 2026-07-02 (Owner-directed — CLAUDE.md context-budget gate; branch-synced into master 2026-07-04)

_Authored 2026-07-02 on the Worker's `claude/session-memory-resume-ljdyun` branch, which was not yet merged when the 2026-07-03/07-04 automated reviews above (independently) claimed v27/R27 for the squash-merge-conflict rule. Renumbered R27→**R28** on merge to preserve both rules under the append-only discipline (R23) — no content from either side was dropped._

### Rule (apply immediately, no exceptions)

**R28 — `CLAUDE.md` size gate (auto-injected context budget)**
`CLAUDE.md` is auto-injected in full into every session's context on session start — unlike
`lessons-learned.md`/`session-memory.md`/`automation-scorecard.md`, which are only loaded when a
session explicitly reads them. This makes `CLAUDE.md` the highest-leverage place for standing
behavioral rules (see the 2026-07-02 status-update-routine fix, backfilled in `session-memory.md`),
but it also means uncontrolled growth there has a real, permanent cost paid on every single session
regardless of whether that session needs the content.

Every reviewer run (06:00/14:00 AWST, step 3a) MUST check `wc -l CLAUDE.md`:
- **> 200 lines** → post a NICE-TO-HAVE in the review PR body naming the specific section(s) that
  are pruning/relocation candidates (move to a read-on-demand doc: `lessons-learned.md`,
  `session-memory.md`, `PR-REVIEW-PROTOCOL.md`, `automation-scorecard.md`).
- **> 400 lines** → escalate to MUST-FIX. Do not let it grow unchecked just because no open PR
  happens to touch it directly — this is a standing gate, not a diff-triggered one.
- Record the current line count in the `docs/review-log.md` row each run so growth is trackable
  over time (e.g. "CLAUDE.md: 124 lines").

**Guiding principle:** `CLAUDE.md` = always-true, rarely-changing rules only (session-start reading
order, git workflow, standing behavioral definitions). Narrative, historical, or occasionally-needed
content belongs in a mandatory-read doc instead, where volume is cheap because it's read on demand,
not injected on every turn.

### Context
Raised by the owner after observing a cross-session knowledge gap (the "status update" routine —
meetings/email/Teams pull — lived only in `tools/morning-briefing/run_briefing.py`, undiscoverable by
a fresh session) get fixed by adding it directly to `CLAUDE.md`. The owner then asked what happens if
that pattern repeats indefinitely and `CLAUDE.md` grows unbounded. This rule is the standing answer:
a periodic size check wired into the existing daily reviewer cadence, so growth is caught early
without requiring the owner to notice and flag it manually. Current baseline: 124 lines (well under
the 200-line NICE-TO-HAVE threshold).

---

## 2026-07-05 - Automated Review (06:00 AWST, 4 new master commits, 1 open PR #167)

_Open PR triggers a full review (R14); the 4 new master commits since #166 also clear the threshold independently. Reviewed #167 (owner-session docs/config PR): **CLEAR - zero MUST-FIX - squash-merged (`954e3a0`)**, bringing master to **v28** (R28 authored by the owner session, not this review). **No new executable rules from this run - version stays v28.** R1-R28 current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #167 | Clear - (1) "Status update" standing routine baked into `CLAUDE.md` (GitHub + Outlook calendar/email + Teams, emoji-sectioned format) so a fresh session never needs re-teaching; (2) **R28** (CLAUDE.md size gate: >200 lines NICE-TO-HAVE, >400 MUST-FIX, count recorded each review run) + review-prompt step 3a wiring; (3) undisclosed-but-sound fix to `.github/workflows/reopen-deepdive-draft-pr.yml` adding a `push` trigger for the program branch. R23 append-only verified on the lessons-learned edit (zero deletions; the R27/R28 version-collision renumber preserved both rules). 2 NICE-TO-HAVE (R21 body drift in BOTH directions - workflow file omitted from "Files touched"/"What was built"; `review-log.md`+`STATUS.md` listed but absent from the final 5-file diff). First R28 gate run: **CLAUDE.md = 124 lines, PASS**. | OK Clear (NICE-TO-HAVE) - merged |

### Observations (good patterns to keep)

- **R27 closed the loop: the owner performed the `18a87c4` milestone merge as a true `--no-ff` merge.** Verified: the commit has two parents (2nd = branch tip `e680ed3`) and `git merge-base origin/master origin/feature/ec-screen-deepdive` now resolves to the milestone point itself - no more false conflicts, the 🔴 High R27 gap (open since 2026-07-03) is RESOLVED. Rule -> owner-action -> verified-fix in two days; this is the extract-a-rule loop working at the owner level, not just the Worker level.
- **The auto-reopen workflow had a real blind spot, now fixed by #167.** The `closed`-event run at the milestone fired while the branch was ahead_by=0 (correct no-op), but when the next autopilot commit (`02a2041`, 200 screens) landed there was no open PR and no event to re-trigger the check - so the standing-draft PR silently did not exist this run. #167's `push` trigger on `feature/ec-screen-deepdive` self-heals exactly this. Until the next autopilot push fires it, `02a2041` was reviewed directly against the branch (pure-data, 200 CHECKLIST flips = claim, 0 non-ASCII added, spot-checked binding real, R23 clean on all five reviewer-owned docs).
- **Reviewer self-correction (MR1):** this run's #167 review comment asserted "PR-head CLAUDE.md = 158 lines" without measuring; the actual count is 124. Corrected publicly via follow-up comment. Reminder: any number published in a review comment must come from a command actually run, not an estimate - the same discipline demanded of Worker PR bodies (R13/R21) applies to reviewer comments.

### Gaps (verified against filesystem / GitHub API)

| Gap | Owner | Priority |
|-----|-------|----------|
| Standing-draft PR for `feature/ec-screen-deepdive` currently MISSING (post-milestone, pre-next-push). Expected to auto-reopen on the next autopilot push via #167's new trigger - next review run MUST verify it exists again; if not, the push trigger needs debugging | Reviewer (verify next run) | 🔴 High |
| ~~PR #159/#166 R27 CONFLICTING carry-over~~ - **RESOLVED**: `18a87c4` was a true `--no-ff` merge; merge-base = milestone point; branch conflict-free | - | OK Closed |
| Decide LFS/out-of-repo for corpus Help images BEFORE the sweep completes - now MORE urgent: cap raised again 100 -> 200/run (`841019a`) and 381+/1457 done; at 200/day the remaining ~1,076 screens land in ~5-6 days | Owner/Worker | 🟡 Medium |
| Carry-over (still open, unchanged this cycle): `run_ec_screen_learn.py` dead corpus-switch code (`EC_URL`/`EC_USER`/`EC_PASS` + `help_text()`) + tautological `full` flag/dead `PARTIAL` branch; extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; fix `sql_idempotency_check.py` em-dashes; `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'` -> `'ECPR-DEMO'` (R22); ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

Review-doc edits made in isolated `C:/tmp/wt-review-2026-07-05-0600` worktree off `origin/master`; the Worker's dirty permanent-branch checkout (`C:\Projects\ChoongYin_OS`, on `feature/ec-screen-deepdive`) and all sibling `wt-*` worktrees were never touched.

---

## 2026-07-05 - Automated Review (14:00 AWST, 1 open PR #170, STANDING/DRAFT)

_Open PR triggers a full review (R14). #170 is the auto-reopened standing draft (the push-trigger fix from #167 worked - the draft reopened at 06:19Z after the milestone merge). Reviewed at head `0432659`: **CLEAR - zero MUST-FIX - NOT merged** (owner-merge-only standing draft). **No new executable rules - version stays v28.** R1-R28 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #170 | Clear. PR stats inflated by the squash milestone (1,501 files / +14,483 shown); **real net delta vs master (`c3ce9d5..0432659`) = 7 files / +47 lines**: the new `EXECUTION-PLAN-completion.md` (sound completion sequencing; Tier-3 pilot correctly behind a separate owner gate) + removal of 6 orphaned pre-corpus `PO.000x_help.png` (orphan claim grep-verified, zero references). Milestone content already on master (`c3ce9d5`, 776/1457 + resolver v3) spot-checked post-hoc: bindings real (`WELL_GAS_INJ_COMPONENT` -> `TV_WELL_GAS_INJ_COMPONENT`, base `FLUID_ANALYSIS_COMPONENT`, resolved-by label exact/unique), runner 0 non-ASCII bytes (R18/R20), honest `no class resolved` flag now rendered into notes. **R23 clean** (diff vs master on all five reviewer-owned docs = EMPTY). `mergeable_state: clean`. CLAUDE.md 124 lines (R28 gate PASS). 3 NICE-TO-HAVE posted (see below). | OK Clear (NICE-TO-HAVE) - left open (owner-merge-only) |

### Observations (good patterns to keep)

- **The #167 auto-reopen push trigger closed the standing-PR gap on its first live firing.** The 06:00 review noted the prior `closed`-event trigger failed at ahead_by=0; today the milestone merge (`c3ce9d5`) was followed within a minute by the workflow reopening #170. The reviewer always has a PR surface to review now.
- **R27 recurred the same day it was credited as fixed.** The 06:00 review recorded "R27 High gap RESOLVED - `18a87c4` is a true two-parent merge"; the very next milestone (`c3ce9d5`, ~06:18) was a single-parent SQUASH again (merged via the GitHub UI squash button by the look of the bot authorship). Current effect is cosmetic (merge-base stuck at `317bbdb` -> inflated PR stats; `mergeable_state` still clean because content is identical), but divergent edits to the same files on both sides will now produce R27's false conflicts. Sharper edge: **the Worker's own `EXECUTION-PLAN-completion.md` Phase 4 step 2 prescribes "squash" for the next milestone** - the recurrence is baked into the plan doc. Advisory posted: change Phase 4 to `--no-ff` (or rebase the branch right after any squash).
- **Verify-the-claim before clearing a deletion commit:** `c8941a8` claims the 6 deleted `_help.png` are unreferenced orphans; grep over the branch's notes tree confirmed zero references before clearing. Deletion commits get the same ground-truth treatment as insertions (MR1).

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| Resolver v3 dead candidate (`run_ec_screen_learn.py:104`, on master via `c3ce9d5`): combined prefix+suffix strip uses replacement `r''` (verified: always yields `''`, dropped by the `if c` filter) - intended `r'\2'`; URL tokens needing BOTH strips (e.g. `DAILY_TANK_STATUS` -> `TANK`) silently never resolve via this path. Fold into the planned resolver v4 (Phase 2 of the completion plan). | Worker | 🟡 Medium |
| `EXECUTION-PLAN-completion.md` Phase 4 step 2 prescribes a squash milestone merge - R27 recurrence baked into the plan; change to `--no-ff`/rebase | Worker | 🟡 Medium |
| R9 header drift in the standing-draft body (carry-over; harmless for a never-auto-merged draft) | Worker | 🟢 Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD; WR.0010.02 Well Oil Comp automation | Worker | 🟡 Medium |

---

## 2026-07-06 - Automated Review (06:00 AWST, 1 open PR #170, STANDING/DRAFT)

_Open PR triggers a full review (R14; 0 new master commits since #171). Reviewed #170 at head `ea1da6b`: **CLEAR - zero MUST-FIX - NOT merged** (owner-merge-only standing draft). **One new rule (R29).** R1-R28 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #170 | Clear. ~444 new screens since the 07-05 14:00 review (WR/SA/CP 200 via `ea1da6b`, PO/GD/CD/WR 200 via `405eeb4`, 44 corpus regens via `d2efc31`) + completion execution plan (`0432659`) + note resets/orphan-png cleanup (Worker-owned files) + runner resolver/labeling fix (`f2ddb71`). Spot-checks: WR.0091 dual-class binding real; SA.0084 honest "(no class resolved from URL/LABEL)" (R3). **R23 clean** (diff vs master on all four reviewer-owned docs = EMPTY); **R28 PASS** (CLAUDE.md 124 lines). 4 NICE-TO-HAVE posted: stale executing runner (-> R29); resolver dead 7th candidate (`r''` replacement, carry-over from #171, still present at tip); R27 pre-milestone-sync reminder; R9 header drift (carry-over). | OK Clear (NICE-TO-HAVE) - left open (owner-merge-only) |

### Rules (apply immediately, no exceptions)

**R29 - A scheduled/unattended runner MUST be verified against the branch tip before every run** ⚠️ _code-derived - the artifact mismatch is confirmed in committed content; the exact execution path (which stale copy ran) is inferred, not live-observed_
When an unattended autopilot commits artifacts to a branch, the copy of the runner it EXECUTES must be the same version that is COMMITTED on that branch tip. Before each run, sync the executing workspace (`git -C <runner-worktree> pull` / detach to the branch tip) or hash-compare the executing script against `git show <branch>:<path>`; abort the run on mismatch. Otherwise a runner fix lands on the branch but never takes effect, and the autopilot mass-produces artifacts in the superseded format while the commit history claims the fix is live.
_Precedent: `f2ddb71` (2026-07-05, honest "no class resolved" screen-type wording) is an ancestor of `ea1da6b` (2026-07-06, 200 screens), yet notes ADDED by `ea1da6b` (e.g. `SA.0084.md`) still emit the pre-fix wording "process/config (no data class ...)" - verified by diffing the note against the branch-tip runner (line 131). ~400 notes were generated with the superseded labeling; they are content-correct but will need the enrichment pass anyway (execution-plan Phase 2), so no reset was demanded._

### Observations (good patterns to keep)

- **The honest-partial design keeps holding at scale:** all 3 batches report "N full, 0 partial" and the spot-checked no-class screen (SA.0084) records the unresolved binding transparently instead of fabricating one. The corpus-format note shape (Identity / DB binding / Screen type / Help images) is uniform across modules (WR, SA, CP, GD, CD checked by sample).
- **Worker-owned deletions are fine when they are regeneration resets:** `7182f9c`/`d075025` (reset pre-corpus notes) and `c8941a8` (6 orphaned `_help.png`, unreferenced - claim verified by grep at the 07-05 14:00 review) account for the -1,246 lines; none touch reviewer-owned docs.
- **The completion execution plan (`0432659`) is a good unattended-program artifact:** phased, each phase with a Done-condition, Tier-3 pilot behind a separate owner gate. One standing advisory remains: Phase 4 step 2 still says "squash" for the milestone merge (R27 recurrence baked in - change to `--no-ff`/rebase).

### Gaps (verified against filesystem / GitHub API)

| Gap | Owner | Priority |
|-----|-------|----------|
| Autopilot executes a stale runner copy (R29): sync `wt-ec-learn` (and any scheduled-task runner path) to the branch tip before each run; the main checkout also holds a STAGED-modified `run_ec_screen_learn.py` that may be the drift source | Worker | 🔴 High |
| Resolver dead 7th candidate (`r''` -> intended `r'\2'`) still present at `ea1da6b` (carry-over from #171); fold into resolver v4 (completion-plan Phase 2) | Worker | 🟡 Medium |
| `EXECUTION-PLAN-completion.md` Phase 4 step 2 still prescribes a squash milestone merge (R27) - change to `--no-ff`/rebase | Worker | 🟡 Medium |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; next OV-GM IUD; WR.0010.02 Well Oil Comp automation | Worker | 🟡 Medium |

---

## 2026-07-06 - Automated Review (14:00 AWST, 1 open PR #170, STANDING/DRAFT)

_Open PR triggers a full review (R14). 0 new master commits since #172/`3789fa6` (the 06:00 review). The only open PR is the **STANDING/DRAFT** EC Screen Deep-Dive PR #170, head advanced `ea1da6b` -> `a8f58bf` -> `2d3a255` (400 new full screens across 2 autopilot batches). **CLEAR; NOT merged** (owner-merge-only). **No new executable rules - version stays v29.** R1-R29 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #170 | Clear - 400 new full screens (`a8f58bf` CP/PP/SP/VO/PR + `2d3a255` SD/FC/TO/IN/PT/MHM/PD/RP/PA), 0 partial. Pure-data (0 `.py`/`.robot`/`.sql`/`.resource` touched), exactly 400 CHECKLIST `[ ]`->`[x]` flips = commit claims (R21). **R23 clean** (diff vs master on all five reviewer-owned docs = EMPTY). **R18/R20 clean** (0 non-ASCII on added lines). **R28 PASS** (CLAUDE.md 124 lines). Bindings spot-checked real (`TERM_OPERATION_NAVIGATOR`->`TV_TERM_OPERATION_NAVIGATOR`, TABLE/EVENT); honest `(no class resolved)` w/ stated reason for SD.0001/FC.0003/MHM.0001 (R3). **NOT merged** (owner-merge-only standing draft). 4 NICE-TO-HAVE carry-overs below. | OK Clear (NICE-TO-HAVE) - left open (owner-merge-only) |

### Observations (good patterns to keep)

- **R29 is a real, recurring defect - confirmed a second time.** The stale-runner symptom extracted at 06:00 recurs verbatim in the 14:00 batch: the runner committed at branch tip carries the `f2ddb71` screen-type-wording fix (`run_ec_screen_learn.py:131`), yet notes ADDED by `2d3a255` (same day) still emit the PRE-`f2ddb71` wording. This is not a one-off timing artifact - the unattended autopilot is executing a runner copy that predates the fix, so every committed runner improvement (resolver v3/v4, wording, batch caps) silently never reaches the notes until the autopilot's own copy is re-synced. The durable fix is a `git pull`/re-checkout of the runner at each autopilot run start (or pointing the scheduler directly at the branch-tip file), not another runner edit.
- **Pure-data batch discipline holding at 200/run.** Two consecutive 200-screen commits touched zero code files and flipped exactly 200 CHECKLIST boxes each - the append-only, no-code-in-a-data-commit shape that keeps R23/R21 trivially verifiable and the reviewer's job to invariant-confirmation rather than content re-litigation.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| **R29 stale-runner** - autopilot emits PRE-`f2ddb71` note wording though the branch-tip runner is fixed; re-sync the autopilot's runner copy at each run start (verified: notes at `2d3a255` still carry the old `process/config (no data class -- e.g. ...)` string) | Worker | 🟡 Medium |
| Resolver dead 7th candidate `run_ec_screen_learn.py:104` - `re.sub(...,r'',base)` is always empty (intended `r'\2'`); carry-over from #171/#172, still at tip | Worker | 🟢 Low |
| **R27 conflict** - #170 still `mergeable_state: dirty` (base `c3ce9d5` vs master `3789fa6`, single-parent squash lineage); rebase onto master or `--no-ff` at the next milestone merge | Owner | 🔴 High |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; `gen_checklist.py:33` em-dash `print`; ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

### Reviewer process note

- Main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent branch `feature/ec-screen-deepdive` at a stale tip (`a7a0a3d`, 2026-06-24) far behind master (`3789fa6`, 2026-07-06). ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-06-1400` worktree off `origin/master`; the Worker's checkout and all sibling `wt-*` worktrees were never touched. Steps 4b/18's `git checkout master` in the main checkout would disrupt the parallel Worker session and were deliberately NOT run there.

---

## 2026-07-07 — Automated Review (06:00 AWST, 1 open PR #170 — STANDING/DRAFT)

_Open PR triggers a full review (R14). The only open PR is the standing-draft EC Screen Deep-Dive PR #170 on the Worker's permanent branch. Reviewed at branch tip: **CLEAR, zero MUST-FIX, NOT merged** (owner-merge-only). **No new executable rules — R1–R29 cover every finding; version stays v29.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #170 | Clear — 1 new commit since 07-06 14:00 (`91c8864`): **76 new full screens, 0 partial** (PA/RC/LM/HA/CM/IS/FI/CA/LA/WL). Pure-data commit (0 `.py`/`.robot`/`.sql`/`.resource`); 76 new notes = 76 CHECKLIST `[ ]`->`[x]` flips = commit claim (R21). **R23 clean** (diff vs master on all five reviewer-owned docs = EMPTY). **R18/R20 clean** (added notes ASCII, markdown-exempt regardless). **R28 PASS** (CLAUDE.md 124 lines). Bindings spot-checked real: `CARGO`->`TV_CARGO`, `STREAM_ITEM`->`OV_STREAM_ITEM`, `TASK_LIST`->`TV_TASK_LIST`. **NOT merged** (owner-merge-only standing draft, still DRAFT). 4 NICE-TO-HAVE carry-overs (see below). | ✅ Clear — left open (owner-merge-only) |

### Observations (good patterns to keep)

- **R29 stale-runner is now a 3-run recurrence — a persistently-unactioned NICE-TO-HAVE, not a flake.** Extracted 07-06 06:00, re-observed 07-06 14:00, re-observed again 07-07 06:00: the branch-tip runner carries the `f2ddb71` wording fix (`run_ec_screen_learn.py:131` → `no class resolved -- process/config screen OR a data screen...`) yet note `HA.0001` ADDED today by `91c8864` still emits the PRE-`f2ddb71` `process/config (no data class -- e.g. ...)` wording. The autopilot is executing a stale runner copy, so the resolver improvements never take effect — screens that *could* resolve a class remain mislabeled process/config. This is a genuine quality degradation (not merely cosmetic), but it does not gate a never-auto-merged draft, so it stays NICE-TO-HAVE while the recurrence count is flagged to raise urgency. The durable fix is a `git pull`/re-checkout (or hash-verify) of the runner at each autopilot run start, per R29 — a runner *edit* cannot fix a runner that is not being re-read.
- **Unchanged-master, single-new-commit re-confirmation shape held.** Master did not advance since #173; the run confirmed the safety invariants (never-auto-merge, R23 clean, R21/R18/R20/R28) and spot-checked substance on the one new commit, rather than re-litigating already-cleared content — the correct shape for a standing-draft PR the reviewer is forbidden to merge.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| **R29 stale-runner (3rd consecutive recurrence)** — autopilot emits PRE-`f2ddb71` note wording though the branch-tip runner is fixed; re-sync/hash-verify the autopilot's runner copy at each run start (verified: `HA.0001` added by `91c8864` still carries the old `process/config (no data class -- e.g. ...)` string) | Worker | 🟡 Medium (escalating) |
| Resolver dead 7th candidate `run_ec_screen_learn.py:104` — `re.sub(...,r'',base)` is always empty (intended `r'\2'`); carry-over from #170/#171/#172, still at tip | Worker | 🟢 Low |
| **R27 conflict** — #170 still `mergeable_state: dirty` (CONFLICTING on `CHECKLIST.md` + overlapping `notes/*.md` from the `c3ce9d5` squash lineage vs master `a4ba2a8`; NOT a reviewer-doc clobber — R23 clean); rebase onto master or `--no-ff` before the next milestone merge | Owner | 🔴 High |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; `gen_checklist.py:33` em-dash `print`; ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

### Reviewer process note (MR4/R23 — stale mandatory-read docs)

- Session start read the mandatory `docs/lessons-learned.md` (v23) and `docs/review-log.md` (ending 2026-06-24) from the **main checkout** — but that checkout is the Worker's permanent branch at a stale tip (`a7a0a3d`), **90 commits behind master**, so those were the STALE copies. The live docs on master are at **v29** (R1–R29), review-log through 2026-07-06 14:00. The worktree HEAD (`a4ba2a8` = #173) surfaced the discrepancy; the live v29 versions were re-read from the master copy in the worktree **before** any rule/version decision — MR4 working exactly as intended. Lesson reinforced: on this repo, always re-read the reviewer-owned docs from `origin/master` (worktree), never trust the main-checkout copies, because the main checkout is a long-lived branch that lags master.
- ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-07-0600` worktree off `origin/master`; the Worker's dirty permanent-branch checkout and all sibling `wt-*` worktrees were never touched. Steps 4b/18's `git checkout master` in the main checkout would disrupt the parallel Worker session and were deliberately NOT run there.

---

## 2026-07-07 — Automated Review (14:00 AWST, 1 open PR #170 — STANDING/DRAFT)

_Open PR triggers a full review (R14). The only open PR is the standing-draft EC Screen Deep-Dive PR #170; its head (`91c8864`) is **byte-identical** to the commit cleared ~8h earlier at the 06:00 review (#174) and master did not advance (0 new commits). **Re-confirmed CLEAR, zero MUST-FIX, NOT merged** (owner-merge-only). **No new executable rules — R1–R29 cover every finding; version stays v29.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #170 | Clear (re-confirmation). Head `91c8864` unchanged since the 06:00 review (#174); 0 new master commits. Content already CLEAR at 06:00 — not re-litigated. Safety invariants re-verified at the tip: **R23 clean** (diff vs master on all five reviewer-owned docs = EMPTY, zero `-` lines), **R28 PASS** (CLAUDE.md 124 lines), R18/R20 unaffected (no new content). **R27** still `mergeable_state: DIRTY`/CONFLICTING (squash-lineage vs master; NOT a reviewer-doc clobber). **NOT merged** (owner-merge-only standing draft, still DRAFT). 4 NICE-TO-HAVE carry-overs re-verified present (see below). | ✅ Clear — left open (owner-merge-only) |

### Observations (good patterns to keep)

- **An unchanged open-PR head is a re-confirmation, not a re-review.** With #170's head byte-identical to the 06:00 commit and master static, the run confirmed the never-auto-merge invariant + R23/R28/R27 status and re-verified the carry-over findings still hold at the tip (MR1 — spot-checked, not inferred), rather than re-scoring frozen content. This is the correct shape for a standing-draft PR the reviewer is forbidden to merge.
- **R29 stale-runner is now a 4-run recurrence — the durable fix is a Worker action R29 already prescribes.** 07-06 06:00 (extracted) → 07-06 14:00 → 07-07 06:00 → 07-07 14:00: the branch-tip runner carries the `f2ddb71` wording fix, yet notes added on the Worker's permanent branch (`HA.0001` via `91c8864`) still emit the PRE-`f2ddb71` `process/config (no data class -- e.g. ...)` string. The unattended autopilot executes a stale runner copy, so resolver/wording fixes never take effect and screens that *could* resolve a class stay mislabeled. It is a genuine quality degradation but does not gate a never-auto-merged draft, so it remains NICE-TO-HAVE with the recurrence count flagged. A runner *edit* cannot fix a runner that is never re-read — the fix is a `git pull`/re-checkout or hash-verify of the autopilot's runner at each run start (R29).

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| **R29 stale-runner (4th consecutive recurrence)** — autopilot emits PRE-`f2ddb71` note wording though the branch-tip runner is fixed; re-sync/hash-verify the autopilot's runner copy at each run start (verified: `HA.0001.md` added by `91c8864` still carries `process/config (no data class -- e.g. ...)`; runner tip `run_ec_screen_learn.py:131` has the fixed wording) | Worker | 🟡 Medium (escalating) |
| Resolver dead 7th candidate `run_ec_screen_learn.py:104` — `re.sub(...,r'',base)` always empty (intended `r'\2'`); carry-over from #170/#171/#172/#174, still at tip | Worker | 🟢 Low |
| **R27 conflict** — #170 still `mergeable_state: DIRTY`/CONFLICTING (squash lineage from `c3ce9d5` vs master; NOT a reviewer-doc clobber — R23 clean); rebase onto master or `--no-ff` before the next milestone merge | Owner | 🔴 High |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; `gen_checklist.py:33` em-dash `print`; ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

### Reviewer process note (isolated worktree; stale main-checkout docs)

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent branch `feature/ec-screen-deepdive` at a stale tip (`a7a0a3d`, **90 commits behind master**), so the session-start mandatory-read `docs/lessons-learned.md`/`docs/review-log.md` there were the STALE v23 copies; the live v29 docs were re-read from the master copy in the worktree before any rule/version decision (MR4). ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-07-1400` worktree off `origin/master`; the Worker's dirty permanent-branch checkout and all sibling `wt-*` worktrees were never touched. Steps 4b/18's `git checkout master` in the main checkout would disrupt the parallel Worker session and were deliberately NOT run there.

---

## 2026-07-08 — Automated Review (06:00 AWST, 1 open PR #170 — STANDING/DRAFT)

_Open PR triggers a full review (R14). The only open PR is the standing-draft EC Screen Deep-Dive PR #170; its head (`91c8864`) is **byte-identical** to the commit cleared at both the 2026-07-07 06:00 (#174) and 14:00 (#175) reviews, and master did not advance (0 new commits since #175). This is the **5th consecutive run on the same head**. **Re-confirmed CLEAR, zero MUST-FIX, NOT merged** (owner-merge-only). **No new executable rules — R1–R29 cover every finding; version stays v29.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #170 | Clear (re-confirmation). Head `91c8864` unchanged since #174/#175; 0 new master commits. Content already CLEAR — not re-litigated. Safety invariants re-verified at the tip (MR1 — checked, not inferred): **R23 clean** (diff vs master on all five reviewer-owned docs = EMPTY, zero `-` lines), **R28 PASS** (CLAUDE.md 124 lines), R18/R20 unaffected (no new content). **R27** still `mergeable_state: DIRTY`/CONFLICTING (squash-lineage vs master; NOT a reviewer-doc clobber). **NOT merged** (owner-merge-only standing draft, still DRAFT). 4 NICE-TO-HAVE carry-overs re-verified present (see below). | ✅ Clear — left open (owner-merge-only) |

### Observations (good patterns to keep)

- **An unchanged open-PR head is a re-confirmation, not a re-review.** With #170's head byte-identical across three consecutive reviews (#174/#175 and now) and master static, the run confirmed the never-auto-merge invariant + R23/R28/R27 status and re-verified the carry-over findings still hold at the tip (MR1 — spot-checked `HA.0001.md` and `run_ec_screen_learn.py:104` directly, not inferred), rather than re-scoring frozen content. Correct shape for a standing-draft PR the reviewer is forbidden to merge.
- **R29 stale-runner is now a 5-run recurrence — durable fix is a Worker action R29 already prescribes.** 07-06 06:00 (extracted) → 07-06 14:00 → 07-07 06:00 → 07-07 14:00 → 07-08 06:00: the branch-tip runner carries the `f2ddb71` wording fix, yet the note added on the Worker's permanent branch (`HA.0001` via `91c8864`) still emits the PRE-`f2ddb71` `process/config (no data class -- e.g. ...)` string. The unattended autopilot executes a stale runner copy, so resolver/wording fixes never take effect. A genuine quality degradation, but it does not gate a never-auto-merged draft, so it stays NICE-TO-HAVE with the escalating recurrence count flagged. A runner *edit* cannot fix a runner that is never re-read — the fix is a `git pull`/re-checkout or hash-verify of the autopilot's runner at each run start (R29).

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| **R29 stale-runner (5th consecutive recurrence)** — autopilot emits PRE-`f2ddb71` note wording though the branch-tip runner is fixed; re-sync/hash-verify the autopilot's runner copy at each run start (verified: `notes/HA.0001.md` added by `91c8864` still carries `process/config (no data class -- e.g. ...)`; runner tip has the fixed wording) | Worker | 🟡 Medium (escalating) |
| Resolver dead 7th candidate `run_ec_screen_learn.py:104` — `re.sub(...,r'',base)` always empty (intended `r'\2'`); carry-over from #171/#172/#174/#175, verified still at tip | Worker | 🟢 Low |
| **R27 conflict** — #170 still `mergeable_state: DIRTY`/CONFLICTING (squash lineage from `c3ce9d5` vs master; NOT a reviewer-doc clobber — R23 clean); rebase onto master or `--no-ff` before the next milestone merge | Owner | 🔴 High |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; `gen_checklist.py:33` em-dash `print`; ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |

### Reviewer process note (isolated worktree; stale main-checkout docs)

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent branch `feature/ec-screen-deepdive` at a stale tip (`a7a0a3d`, **91 commits behind master**), so the session-start mandatory-read `docs/lessons-learned.md`/`docs/review-log.md` there were the STALE v23 copies; the live v29 docs were re-read from the master copy in the worktree before any rule/version decision (MR4). ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-08-0600` worktree off `origin/master`; the Worker's dirty permanent-branch checkout and all sibling `wt-*` worktrees were never touched. Steps 4b/18's `git checkout master` in the main checkout would disrupt the parallel Worker session and were deliberately NOT run there.

---

## 2026-07-09 — Automated Review (16:00 AWST, milestone-completion run, 1 open PR #178 — STANDING/DRAFT)

_Off-schedule milestone-completion run (the 14:00 slot was #177 on the frozen `91c8864` head). Since #177 the owner **squash-milestone-merged the prior standing draft #170** — `d3cd8eb` "EC Screen Deep-Dive: milestone COMPLETE **1457/1457** + underscore BF-code parser fix" landed on master — and CI auto-reopened a fresh standing shell **#178**. Open PR triggers a full review (R14). **#178 CLEAR — zero MUST-FIX — NOT merged** (owner-merge-only standing draft). **No new executable rules — R1–R29 cover every finding; version stays v29.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #178 | Clear — auto-reopened standing shell, **content byte-identical to master**. Direct tip-vs-tip `git diff --stat origin/master origin/feature/ec-screen-deepdive` = **EMPTY**: the whole 1457-note corpus is on master via the milestone squash, so #178 carries **zero real content divergence** (the ~1924-file `origin/master...branch` three-dot diff is purely the R27 squash-history artifact — the squash `d3cd8eb` is not a true ancestor of the branch, so all branch notes read as "added" vs the merge-base though the trees match). **R23 clean** (`git diff --numstat origin/master...origin/feature/ec-screen-deepdive` on all four reviewer-owned docs = EMPTY, zero `-` lines). **R28 PASS** (CLAUDE.md 124 lines). **mergeStateStatus = CLEAN/MERGEABLE** — the prior R27 DIRTY/CONFLICTING state is **RESOLVED**: branch tip `52d4436` is a fresh `Merge origin/master into HEAD` re-absorbing the squash. Newest note (`c6404e9` SA.0019.DS_PC) spot-checked: real binding `SCTR_ACC_DAY_DS_PC_ALLOC` (DATA/DAY) → `DV_SCTR_ACC_DAY_DS_PC_ALLOC`, honest "no field-description images in corpus", ASCII-clean. 3 NICE-TO-HAVE carry-overs. **NOT merged** (owner-merge-only standing draft). | ✅ Clear (NICE-TO-HAVE) — left open (owner-merge-only) |

### Observations (good patterns to keep)

- **1457/1457 milestone complete — the deterministic-runner deep-dive program landed in full.** The whole corpus is now on master via `d3cd8eb`. The design that got it there is worth restating: a deterministic (no-LLM) runner executing a proven recon→metadata-resolve→corpus-Help→note recipe, honest `[~]`/no-class partials (R3), read-only-by-construction against the live EC, and a never-auto-merged standing-draft PR the reviewer confirms-but-never-merges. It scaled from ~8 screens/run to 200/run without a MUST-FIX on content.
- **R27's remedy was applied correctly this time.** The milestone was squash-merged (single-parent `d3cd8eb`) — R27 recurrence, as the execution plan's Phase 4 still bakes in — but the Worker then `Merge origin/master into HEAD` on the branch (`52d4436`), which re-absorbed the squash and returned #178 to CLEAN/MERGEABLE with a byte-identical tree. A squash milestone is survivable if the continuation immediately merges master back; the durable fix remains `--no-ff`/rebase to avoid the transient DIRTY window (still owed in `EXECUTION-PLAN-completion.md`).
- **R29 stale-runner resolved by worktree convergence.** The Worker's autopilot runner worktree `wt-ec-learn` is now at `52d4436` (= branch tip), so the executing runner copy finally matches the committed one — the 6-run recurrence chain ends here. The lesson (R29) still stands for any future unattended program: hash/sync-verify the executing copy at each run start rather than trusting that a committed fix is live.
- **A byte-identical open head is a re-confirmation, not a re-review.** With the branch tree == master tree, the review's job was to confirm the never-auto-merge invariant, R23/R28 safety, the R27 conflict-resolution, and content quality of the single new commit — not to re-score 1457 frozen notes.

### Gaps (verified against filesystem / GitHub API)

| Gap | Owner | Priority |
|-----|-------|----------|
| `DeepDiveLearnings/ec-screens/EXECUTION-PLAN-completion.md` Phase 4 step 2 still prescribes a **squash** milestone merge (R27) — change to `--no-ff`/rebase so any future milestone push does not re-enter the DIRTY window | Worker | 🟡 Medium |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; `gen_checklist.py:33` em-dash `print` (R18/R20); resolver dead 7th candidate `run_ec_screen_learn.py:104` (`re.sub(...,r'',base)` → intended `r'\2'`); ECIS `upload -> RUN NOW` flakiness root cause; Reported Alarms EVENT_LOG clone; #84 base-table count into the suite; WR.0010.02 Well Oil Comp | Worker | 🟡 Medium |
| R9 header drift on the auto-generated #178 draft body (no exact 6 field headers) — harmless for a never-auto-merged draft; the reopen-PR workflow template could adopt the 6 headers | Worker | 🟢 Low |

### Reviewer process note (isolated worktree; stale main-checkout docs)

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent branch `feature/ec-screen-deepdive` at a stale tip (`a7a0a3d`, **90+ commits behind master**), so the session-start mandatory-read `docs/lessons-learned.md`/`docs/review-log.md` there were the STALE **v23** copies; the live **v29** docs were re-read from the master copy in the worktree before any rule/version decision (MR4). ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-09-1600` worktree off `origin/master`; the Worker's dirty permanent-branch checkout and all sibling `wt-*` worktrees (incl. the runner's `wt-ec-learn` at `52d4436`) were never touched. Steps 4b/18's `git checkout master` in the main checkout would disrupt the parallel Worker session and were deliberately NOT run there.

---

## 2026-07-10 06:00 AWST — Automated Review (0 new master commits since #179; 1 open PR #178, STANDING/DRAFT)

_Open PR triggers a full review (R14). #178 (the post-completion standing-draft shell) had REAL new work this run — 3 branch commits since #179, one a runner code change — so it was reviewed HIGH effort, not treated as an unchanged-head re-confirmation. **CLEAR — zero MUST-FIX — NOT merged** (owner-merge-only standing draft). **No new executable rules — R1–R29 cover every finding; version stays v29.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #178 | Clear — 3 new commits since #179 (`04044c5` reset 5 INTERFACE screens for re-resolution + `f6dcd21` re-learn 5 + `56ed452` runner fix). **Runner fix** (`run_ec_screen_learn.py`, +2/-2): `pick_screens` BF-code regex `[A-Z0-9.]+`→`[A-Z0-9._]+` (matches underscore BF-codes) and `db_resolve` adds `'RV_'` to the `OV_/TV_/DV_` view-prefix search (INTERFACE-class read-views now resolve) — both correct, ASCII-clean (em-dash is `chr(0x2014)` code-point, R18/R20-safe), diff↔commit-message match (R21). **5 INTERFACE re-resolutions** (CO.0060/CO.0237→`EQUIPMENT`→`RV_EQUIPMENT`; CD.0157/VO.0039/VO.0040→`STREAM_ITEM_SPLIT`→`RV_STREAM_ITEM_SPLIT`): honest DoD-backfill — verified before→after on CD.0157 (`(none)`→`RV_STREAM_ITEM_SPLIT`), consistent with INTERFACE/VERSIONED typing, not fabricated. **R23 clean** (three-dot diff on the four reviewer-owned docs = EMPTY). **R28 PASS** (CLAUDE.md 124 lines). **R18/R20 clean** (0 non-ASCII on added lines). **NOT merged** (owner-merge-only draft). 3 NICE-TO-HAVE (carry-overs) — see below. | ✅ Clear (NICE-TO-HAVE) — **left open (owner-merge-only)** |

### Observations (good patterns to keep)

- **RV_ read-view resolution is the right fix, and it landed honestly.** The old runner only searched `OV_/TV_/DV_` prefixes, so INTERFACE-class screens (EQUIPMENT, STREAM_ITEM_SPLIT) recorded `(none)` for their View — an honest gap, not a fabrication. Adding `RV_` (EC's read-view prefix for INTERFACE classes) closes the gap for real: each of the 5 reset screens now binds to an existing `RV_*` view. The worker reset the 5 notes to a clean baseline (`04044c5`) THEN re-resolved with the improved runner (`f6dcd21`/`56ed452`) rather than hand-patching the View column — the correct, reproducible shape for a post-completion resolver improvement.
- **A moved standing-draft head is not automatically a re-confirmation.** The last five runs were unchanged-head re-confirmations of a frozen `91c8864`; this run's head genuinely moved (`52d4436`→`56ed452`) with a `.py` change, so it earned a full HIGH-effort review of the actual 3-commit delta (isolated via `git diff 04044c5^..56ed452`, NOT the 1927-file three-dot artifact). Reviewing the real commit range — not the squash-lineage-inflated three-dot diff — is what keeps the R27 noise from drowning a genuine 7-file change.

### Gaps (verified against filesystem / git at tip)

| Gap | Owner | Priority |
|-----|-------|----------|
| **R27 pre-milestone re-absorb (now a live clobber-latent).** The 3 new commits were built on `52d4436` (pre-#179) without re-absorbing master, so the DIRECT two-dot `git diff origin/master origin/feature/ec-screen-deepdive` shows `docs/lessons-learned.md -31` + `docs/review-log.md -1` + `STATUS.md` (= #179's review entry the branch is now behind on). The literal R23 test is the THREE-dot form and it is CLEAN (branch made no edit to those files) → NOT an R23 MUST-FIX; but the owner MUST `git merge origin/master` (or `--no-ff`) before the next milestone push/merge or a squash would clobber #179's record. | Worker/owner | 🟡 Medium |
| Resolver dead 7th candidate at `run_ec_screen_learn.py:104` — `re.sub('^(DAILY\|SUB_DAILY\|MONTHLY\|MTH\|YEARLY)_(.*?)(_STATUS\|_OVERVIEW)?$', r'', base)` uses replacement `r''` (always empty → filtered out by `if c`); intended `r'\2'`. Carry-over from #170–#179, still at tip. | Worker | 🟢 Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; `gen_checklist.py:33` `print(... em-dash ...)` (R18/R20); `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'`→`'ECPR-DEMO'` (R22). | Worker | 🟡 Medium |
| Carry-over (still open): R27 squash still prescribed in `EXECUTION-PLAN-completion.md` Phase 4 (switch to `--no-ff`/rebase for any future milestone); R9 header drift on the bot-generated draft body (harmless for a never-auto-merged draft). | Worker | 🟢 Low |

### Reviewer process note (isolated worktree; stale main-checkout docs)

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent branch `feature/ec-screen-deepdive` at a stale tip (`a7a0a3d`, ~90 commits behind master), so the session-start mandatory-read `docs/lessons-learned.md`/`docs/review-log.md` there were the STALE **v23** copies; the live **v29** docs were re-read from the `origin/master` copy in the worktree before any rule/version decision (MR4). ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-10-0600` worktree off `origin/master`; the Worker's dirty permanent-branch checkout and all sibling `wt-*` worktrees were never touched. Steps 4b/18's `git checkout master` in the main checkout would disrupt the parallel Worker session and were deliberately NOT run there.

---

## 2026-07-11 06:00 AWST — Automated Review (0 new master commits since #181; 1 open PR #178, STANDING/DRAFT)

_Open PR triggers a full review (R14). #178's head `56ed452` is byte-identical to the commit cleared ~16h/~8h ago at the 07-10 06:00 (#180) and 14:00 (#181) reviews and master did not advance (0 new commits since `e533162`) — an unchanged-head RE-CONFIRMATION (2nd consecutive on `56ed452`), NOT a re-review of already-cleared content. **Re-confirmed CLEAR; NOT merged** (owner-merge-only standing draft, still `draft:true`). **No new executable rules — R1–R29 cover every finding; version stays v29.**_

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #178 | Clear (re-confirmation). Head `56ed452` byte-identical to the commit cleared at #180/#181 (PR `headRefOid` = `56ed452`, `updated_at` 2026-07-10T08:02:51Z — no new push). Safety invariants re-verified at the tip (checked, not inferred — MR1): **R23 CLEAN** (`git diff --numstat origin/master...origin/feature/ec-screen-deepdive` on all four reviewer-owned docs = EMPTY, zero `-` lines — the branch does not edit those files); **R28 PASS** (CLAUDE.md 124 lines); never-auto-merge invariant holds (`draft:true`, `merged:false`). The 1928 `changed_files` / +16366/-692 the GitHub API reports is the R27 squash-lineage three-dot artifact (`d3cd8eb` milestone squash is not a true ancestor of the branch), NOT real content divergence. **NOT merged** (owner-merge-only standing draft). 3 NICE-TO-HAVE carry-overs. | ✅ Clear (NICE-TO-HAVE) — left open (owner-merge-only) |

### Observations (good patterns to keep)

- **An unchanged open-PR head is a re-confirmation, not a re-review.** #178's head has not moved since #180 (the last run with real work — the RV_ runner fix + 5 INTERFACE re-resolutions), so the 1457-note corpus (already CLEAR many times) was not re-litigated. The run instead confirmed (a) the never-auto-merge invariant still holds, (b) R23 is still satisfied vs the now-further-advanced master, and (c) R28 still passes — the correct shape for a standing-draft PR the reviewer is forbidden to merge.
- **The R23 (three-dot) vs R27 (two-dot) distinction remains the crux of this branch.** The literal R23 test — the branch's OWN edits since merge-base — stays EMPTY every run, because the deep-dive branch never edits the four reviewer-owned docs. What grows every review is the two-dot gap (branch behind master), now `lessons-learned.md -61` + `review-log.md -3` + `STATUS.md`, purely because each review APPENDS to those files on master and the permanent branch has not re-absorbed. That is an R27 pre-milestone-re-absorb obligation on the owner, not an R23 clobber the reviewer must block. Conflating the two would either falsely MUST-FIX a clean branch or falsely clear a real clobber — keep testing both forms explicitly.

### Gaps (verified against filesystem / GitHub API)

| Gap | Owner | Priority |
|-----|-------|----------|
| **R27 pre-milestone re-absorb (clobber-latent, NICE-TO-HAVE not MUST-FIX).** The branch is behind master on the reviewer-owned docs (two-dot: `lessons-learned.md -61` + `review-log.md -3` + `STATUS.md`) — the #179/#180/#181 review entries it has not re-absorbed. R23 three-dot is CLEAN so this is not a reviewer-blocking clobber, but the owner MUST `git merge origin/master` (or `--no-ff`) before the next milestone push/merge or a squash would delete those review records. | Worker/owner | 🟡 Medium |
| Resolver dead 7th candidate at `run_ec_screen_learn.py:104` — `re.sub('^(DAILY\|SUB_DAILY\|MONTHLY\|MTH\|YEARLY)_(.*?)(_STATUS\|_OVERVIEW)?$', r'', base)` uses replacement `r''` (always empty → filtered out by `if c`); intended `r'\2'`. Carry-over from #170–#181, still at tip. | Worker | 🟢 Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; `DeepDiveLearnings/ec-screens/gen_checklist.py:33` em-dash `print` (R18/R20); `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'`→`'ECPR-DEMO'` (R22); `EXECUTION-PLAN-completion.md` Phase 4 still prescribes squash (R27 — switch to `--no-ff`/rebase); R9 header drift on the bot-generated draft body (harmless for a never-auto-merged draft). | Worker | 🟡 Medium |

### Reviewer process note (isolated worktree; stale main-checkout docs)

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent branch `feature/ec-screen-deepdive` at a stale tip (`a7a0a3d`, ~97 commits behind master), so the session-start mandatory-read `docs/lessons-learned.md`/`docs/review-log.md` there were the STALE **v23** copies; the live **v29** docs were re-read from the `origin/master` copy in the worktree before any rule/version decision (MR4). ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-11-0600` worktree off `origin/master`; the Worker's dirty permanent-branch checkout and all sibling `wt-*` worktrees (incl. the runner's `wt-ec-learn`) were never touched. Steps 4b/18's `git checkout master` in the main checkout would disrupt the parallel Worker session and were deliberately NOT run there.

---

## 2026-07-11 — Automated Review (14:00 AWST, 1 open PR #178 — STANDING/DRAFT)

_Open PR triggers a full review (R14). #178's head `56ed452` is byte-identical to the commit cleared at the 07-10 06:00 (#180), 07-10 14:00 (#181) and 07-11 06:00 (#182) reviews and master did not advance (0 new commits since `84ab6c2`) — an unchanged-head **RE-CONFIRMATION** (4th consecutive on `56ed452`). **Re-confirmed CLEAR; NOT merged** (owner-merge-only standing draft). **No new executable rules — version stays v29.** R1–R29 remain current._

### PR Status after this review pass

| PR | Finding | Status |
|----|---------|--------|
| #178 | Clear (re-confirmation). Head `56ed452` unchanged since #180/#181/#182; master unchanged (`84ab6c2`). Safety invariants re-verified at the tip (MR1, checked not inferred): **R23 CLEAN** (`git diff --numstat origin/master...origin/feature/ec-screen-deepdive` on all four reviewer-owned docs = EMPTY, zero `-` lines — the branch does not edit those files); **R28 PASS** (CLAUDE.md 124 lines); never-auto-merge invariant holds (`draft:true`). Content spot-re-verified fresh this run: runner 0 non-ASCII bytes; all 1457 `notes/*.md` ASCII-clean; WR.0091 dual-class binding real (`WELL_FLUID_ANALYSIS`+`WELL_FLUID_COMPONENT` → `DV_*`); honest `[~]`/no-class partials (R3). **NOT merged** (owner-merge-only standing draft). 3 NICE-TO-HAVE carry-overs (below). | OK Clear (NICE-TO-HAVE) — left open (owner-merge-only) |

### Observations (good patterns to keep)

- **An unchanged open-PR head is a re-confirmation, not a re-review of the same diff.** #178's head has not moved for four consecutive runs; the deep-dive content (cleared repeatedly since the milestone) was not re-litigated. The run instead verified the safety invariants that CAN change out from under a frozen head — the never-auto-merge flag, R23 three-dot cleanliness vs an ever-advancing master, and R28 line count. Correct shape for a standing-draft PR the reviewer is forbidden to merge.
- **Verify carry-overs against ground truth each run (MR1), don't inherit the prior text.** The `gen_checklist.py:33` em-dash carry-over was re-confirmed present via a Python `ord()>127` scan — a Windows `grep -P "[^\x00-\x7F]"` returned empty (its byte-class did not match the U+2014), which would have produced a false "resolved" claim had it been trusted. The Python scan is authoritative on this platform.

### Gaps (verified against filesystem)

| Gap | Owner | Priority |
|-----|-------|----------|
| **R27 pre-milestone re-absorb (clobber-latent, NICE-TO-HAVE not MUST-FIX).** Branch is behind master on the reviewer-owned docs (two-dot: `lessons-learned.md` + `review-log.md` + `STATUS.md` = the #179–#182 review entries not re-absorbed). R23 three-dot is CLEAN so this is not a reviewer-blocking clobber, but the owner MUST `git merge origin/master` (or `--no-ff`) before the next milestone push/merge or a squash would delete those review records. | Worker/owner | 🟡 Medium |
| Resolver dead 7th candidate at `run_ec_screen_learn.py:104` — replacement `r''` (always empty → filtered out); intended `r'\2'`. Carry-over from #170–#182, still at tip. | Worker | 🟢 Low |
| Carry-over (still open): extend `check_bundle_hygiene.py` ASCII gate to `.claude/skills/**/*.py` + `workstreams/**/scripts/*.py` + `tools/**`; `DeepDiveLearnings/ec-screens/gen_checklist.py:33` em-dash `print` (R18/R20, re-confirmed present via Python ord-scan); `ec-sql-script-builder` demo SQL `REV_TEXT='ECPR-XXXX'`→`'ECPR-DEMO'` (R22); `EXECUTION-PLAN-completion.md` Phase 4 still prescribes squash (R27 — switch to `--no-ff`/rebase); R9 header drift on the bot-generated draft body (harmless for a never-auto-merged draft). | Worker | 🟡 Medium |

### Reviewer process note (isolated worktree; stale main-checkout docs)

- The main checkout (`C:\Projects\ChoongYin_OS`) is the Worker's permanent branch `feature/ec-screen-deepdive` at a stale tip (`a7a0a3d`, ~100 commits behind master), so the session-start mandatory-read `docs/lessons-learned.md`/`docs/review-log.md` there were the STALE **v23** copies; the live **v29** docs were re-read from the `origin/master` copy in the worktree before any rule/version decision (MR4). ALL review-doc edits were made in an isolated `C:/tmp/wt-review-2026-07-11-1400` worktree off `origin/master`; the Worker's dirty permanent-branch checkout and all sibling `wt-*` worktrees (incl. the runner's `wt-ec-learn`) were never touched. Steps 4b/18's `git checkout master` in the main checkout would disrupt the parallel Worker session and were deliberately NOT run there.

---
