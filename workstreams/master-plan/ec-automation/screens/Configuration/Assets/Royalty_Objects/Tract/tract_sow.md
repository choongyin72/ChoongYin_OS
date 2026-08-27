# EC Screen IUD Operation Test - Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS - EC Web App System Test
**Task:** EC Screen Insert/Update/Delete (IUD) Automation - Tract
**Screen:** Configuration > Assets > Royalty Objects > Tract (RC.0056)
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-26 (original build); updated 2026-08-26 (PR #555, Area-pattern conversion) and
2026-08-28 (this backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 4)
**Version:** 2.0

---

## 1. REQUIREMENT

### 1.1 Objective
Automate Insert, Update, Delete (IUD) on the Tract screen to validate creation, modification
and deletion of tract master records, with EC data integrity maintained and the sandbox left
exactly as found.

### 1.2 Scope
Single screen, one PR (Option 1). Tract is the 5th Royalty Objects screen built and the
**first OV-GM (gated)** one in the folder.

### 1.3 Constraints
- **NEVER modify existing production/configuration data.** Unit Agreement parents are READ-ONLY seed.
- Test code is now the FIXED `AUTOTEST_TRACT` (since PR #555, 2026-08-26 - replaces the original
  build's per-run `AUTOTEST_TR_<run>` timestamped code); confirmed free in `OV_TRACT` before each run.
- Target (this backfill, 2026-08-28): local sandbox web app, DB `localhost:1521/ORCL`
  (`ECKERNEL_EC`) - same DB target as the original build; the original build's sandbox web app URL
  (`ap-f0a7g341jn6d.corp.quorumsoftware.com`) is CLP-era and superseded.

### 1.4 Acceptance Criteria
| Operation | Pass Condition |
|---|---|
| INSERT | New `AUTOTEST_TR_*` code appears in the UA-filtered list AND in `ov_tract` |
| UPDATE | Tract Name changed and persisted (visible in the row) |
| DELETE | Record removed from `ov_tract` after End Date = Start Date + Save |
| CLEANUP | Environment returned to pre-test state (0 residual) |

---

## 2. DESIGN

### 2.1 Screen classification (recon: resolve_ec_screen.py + scan_ec_screen.py + tract_recon.py)
| Property | Value |
|---|---|
| Screen name | Tract |
| Treeview path | Configuration > Assets > Royalty Objects > Tract |
| Screen type | **OV-GM (Manage-Object, gated)** - NOT plain Bank family |
| CLASS_TYPE / TIME_SCOPE | OBJECT (OV) / VERSIONED (date-effective; DELETE = End=Start) |
| Base table / view | `TRACT` / `OV_TRACT` |
| App | EC_REVN |
| **Navigator (gated)** | date `nav:form:G:0:R:1:C:0:da_input` (already carries a non-empty default on load - confirmed live 2026-08-26, needs no fill) + **mandatory dd `nav:form:G:1:R:1:C:0:dd` = Unit Agreement** (the ONLY mandatory-and-empty nav field, confirmed live via its `{mandatory:true} MandatoryCellStyle` class) + GO `button:form:B`. Filled via the shared T2 `Apply Navigator From Properties` called with `group=1 start_col=0` (since PR #555) - structurally the same single-mandatory-dropdown shape as Area's own navigator, just at a different group/column index. |
| Nav options | Unit Agreement 1..4 (Unit Agreement 1 has existing data) |
| Grid tbody id | **`manageObject:form:T_data`** (OV-GM grid; lazy redraw) |
| Insert mandatory | Code R0, Name R1, Start Date R2, **Unit Agreement dd R3 (`objectForm…R:3:C:1:dd`, must = nav scope)** |
| Update / Delete | updateAttributes Code R0 / Name R1 ; objectdates End Date R0:C3 (EC-standard, shared with Transport System) |

### 2.2 IUD design (OV-GM, mirrors Transport System exemplar)
```
NAV:     pick Unit Agreement (e.g. 'Unit Agreement 1') in nav dd + GO -> grid loads.
INSERT:  Insert -> New Object -> objectForm: Code R0 / Name R1 / Start Date R2 +
         Unit Agreement dd R3 = same UA as nav (grid-visibility parent) -> Save -> refresh.
UPDATE:  select row -> updateAttributes Name R1 -> Save -> refresh.
DELETE:  objectdates End Date R0:C3 = Start Date (zero-length window) -> Save ->
         extra Apply Navigator (lazy GM redraw) -> gone from ov_tract (TRUE delete).
```
**Date:** `${TEST_START_DATE_REFDD}` - the Unit Agreement parent must be effective at the form
Start Date for the reference dropdown to offer it ([[reference_ec_object_start_date_version]]).

### 2.3 Test data (as of the 2026-08-26 Area-pattern conversion, PR #555)
| Field | Value |
|---|---|
| Code | fixed `AUTOTEST_TRACT` (confirmed free in `OV_TRACT` via a fresh oracledb connection before use; replaces the earlier per-run `AUTOTEST_TR_<run>` timestamped code) |
| Name (Insert/Update) | `testdata/tract_{insert,update}.properties`-driven Tract Name value |
| Nav + Insert parent (Unit Agreement) | `Unit Agreement 1` (IDENTICAL value in `testdata/tract_navigator.properties` and `testdata/tract_insert.properties`, per the owner's field-reuse rule) |
| Start/End Date | `2011-01-01` (reused from the prior driver; Unit Agreement parents confirmed live effective `2010-01-01`, so Start Date must be >= that) - End = Start -> true delete |

### 2.4 Technology + deliverables
RF suite layered T3 -> T2 (`resources/manage_object.resource`) + T1 (`resources/common.resource`) +
`libraries/DbVerify.py`. **RF-only** - never had a Playwright bundle (OV-GM exemplar precedent,
Transport System), and no new Playwright bundle is built for Area-pattern work regardless (owner
decision 2026-08-27, `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H - Universal Screen Engine
replaces that role). The live + DB-verified RF suite is the proof.
- T3: `pageobjects/Configuration/Assets/Royalty_Objects/tract_page.resource` (5-TC Area-pattern shape since PR #555)
- Suite: `tests/Configuration/Assets/Royalty_Objects/tract_iud.robot` (TC01 Clean State / TC02 Insert / TC03 Update / TC04 Find / TC05 Delete, per-TC Login/Logout)
- Test data: `testdata/tract_{navigator,insert,update,form_verify,grid_verify}.properties`
- Evidence: `evidence/` (RF step captures from the original 2026-06-26 live run) + `evidence/backfill_2026-08-28/` (this backfill's fresh dryrun + live re-run)

---

## 3. KNOWN RISKS
- **OV-GM lazy redraw** - grid redraws asynchronously after Save+GO; T3 delete adds an extra
  `Apply Navigator`, and `Row Should Exist` (T2) awaits the row (R17).
- Insert parent dd MUST equal the nav Unit Agreement or the row never lists under the filter.
- Reference dropdown only offers Unit Agreements effective at the form Start Date -> use the
  proven `2011-01-01` (Unit Agreement parents effective `2010-01-01`).

---

## 4. DEV STORY

**Original build (2026-06-26):** built as the 5th Royalty Objects screen and the folder's 1st
OV-GM (gated) screen, following the Transport System exemplar. Live 4/4, RF-only (no Playwright
bundle, per the OV-GM exemplar precedent). Target was the CLP-era sandbox web app
(`ap-f0a7g341jn6d.corp.quorumsoftware.com`), not this repo's current plutodev environment - the
screen/DB facts below were re-confirmed live against the current environment during the PR #555
conversion and this backfill, not merely carried over from 2026-06-26.

**Area-pattern conversion (PR #555, merged 2026-08-26) - the real, important story:** this PR's
OWN FIRST COMMIT WRONGLY DECLINED the Area-pattern conversion for Tract, reasoning that its
navigator's two separate DOM groups (`nav:form:G:0` for Date, `nav:form:G:1` for Unit Agreement)
didn't fit Area's single-group cascade shape - and logged that wrong conclusion to
`docs/navigator-screens-not-matching-area.md`. The owner corrected this, and a fresh live DOM
recon the same day found the real shape: `G:0`'s Date field already carries a non-empty default
on load and needs no fill at all, so it was never a genuine second mandatory group in practice;
`G:1`'s Unit Agreement dropdown (confirmed live via its `{mandatory:true} MandatoryCellStyle`
class) is the ONLY mandatory-and-empty navigator field. Tract's REAL navigator requirement is
therefore exactly ONE mandatory dropdown - structurally the SAME shape as Area's own
single-dropdown navigator, just living at group 1 / column 0 instead of group 0 / column 1. The
wrongly-added row was removed from `docs/navigator-screens-not-matching-area.md` with an explicit
correction-log entry (not silently deleted), and Tract was converted to the full Area pattern in
the same PR (commit added on top, same branch/PR number - not a new PR).

To make the conversion possible, the shared T2 `Apply Navigator From Properties` keyword
(`resources/manage_object.resource`) was extended with two new OPTIONAL, backward-compatible
arguments: `${group}=0` and `${start_col}=1` (defaults preserve every existing caller unchanged -
Area/Well Hookup/Contract/Meter/etc. all still target `nav:form:G:0:...C:1..C:N`). Tract calls it
as `group=1 start_col=0`. This was proven backward-compatible via a full-tree dryrun (874/874
unchanged before/after the edit) plus live 5/5 regression canaries on 2 existing callers of the
keyword's old 2-arg form (Area, Meter).

The owner's field-reuse rule was applied here: the navigator's Unit Agreement value
(`testdata/tract_navigator.properties`) is reused identically in the insert form's own Unit
Agreement field (`testdata/tract_insert.properties`) - the inserted row is otherwise invisible
under the OV-GM filtered grid.

Full rebuild delivered: 5 TCs (added TC04 Find), per-TC Login/Logout
(`TRACT_EC_USER`/`TRACT_EC_PASS`), fixed test code `AUTOTEST_TRACT` (confirmed free live via a
fresh oracledb connection), properties-file-driven insert/update/verify, explicit `Find/Clear
Tract Row By Filter` (15 hits confirmed via output.xml grep), zero inline DB-verify calls in the
`.robot` file. Live 5/5, full-tree dryrun 875/875, robocop 7 issues on the changed screen files =
exact parity with Area's own 7-issue baseline, DB self-clean confirmed 0 residual `AUTOTEST_TRACT`
via a fresh connection.

**This backfill (2026-08-28, Batch 4, `docs/lean-deliverable-backfill-workorder.md`):** added the
retroactive JOURNAL/CHECKLIST/KB-map artifacts the 2026-08-23/26 lean waiver had skipped, refreshed
this pre-existing (2026-06-26) SOW/README to reflect PR #555's Area-pattern conversion and
wrong-then-corrected story, and captured fresh dryrun + live evidence of the already-proven suite
in `evidence/backfill_2026-08-28/` - no automation code touched, rebuilt, or re-verified from
scratch.
