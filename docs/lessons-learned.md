# Lessons Learned — EC Automation
_Reviewed by Claude Code (reviewer session) and appended over time._
_Worker sessions: read this before starting any automation work._

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
