# EC Screen IUD — Statement of Work: **Pipeline Segment**
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Original build:** pre-existing RF automation, live-verified 2026-06-12 (4-TC/suite-login/timestamped-code shape)
**Converted:** `ec-area-pattern-converter` skill — PR #558 (`feature/pipeline-segment-area-pattern`), merged 2026-08-26
**Backfilled:** `docs/lean-deliverable-backfill-workorder.md`, Batch 3 — 2026-08-27 (see §3.2, §5)
**Result:** ✅ COMPLETE — live **5/5 PASS** (Area-pattern, TC01-TC05), DB-verified, self-cleaning (0 residue)

---

## 1. REQUIREMENT / METADATA
| Property | Value | Source |
|---|---|---|
| Screen | **Pipeline Segment** | input |
| Treeview path | **Configuration > Assets > Dispatching Objects > Pipeline Segment** | `docs/ec_screen_registry.md` |
| Class type | OV-GM (Business-Unit-gated manage-object) | registry + `pipeline_segment_page.resource` Documentation |
| Time scope | date-effective ⇒ **DELETE = End Date = Start Date** | registry, PR #558 body |
| Verify view | `OV_PIPELINE_SEGMENT` | `libraries/DbVerify.py` usage in the suite |
| Family | **OV-GM, single-mandatory-Business-Unit-dropdown** — same shape as Area's own Production Unit navigator / Meter's own Business Unit navigator | registry row |

## 2. LIVE RECON (as re-confirmed live 2026-08-26, per PR #558)
**Navigator** — the grid stays empty until a Business Unit is chosen + GO:
| Element | Locator | Mandatory |
|---|---|---|
| Nav date | `nav:form:G:0:R:1:C:0:da_input` | pre-filled, not empty-mandatory |
| **Nav Business Unit** (dd) | `nav:form:G:0:R:1:C:1:dd` | **yes** |
| Nav Pipeline (dd, filter) | `nav:form:G:0:R:1:C:2:dd` | no — `mandatory:false`, confirmed live; GO succeeds with only C:1 filled |
| Grid | `manageObject:form:T_data` | — |

**Insert (`objectForm`) — fields, screen-prefixed labels confirmed live:**
| Field | Mandatory |
|---|---|
| Pipeline Segment Code | **yes** |
| Pipeline Segment Name | **yes** |
| Start Date | **yes** |
| Pipeline Name (dd) | **yes** — no popup on this screen's insert form, so fill order is not load-bearing |

**Update (`updateAttributes`):** Pipeline Segment Name only (Code IS an editable `<input>` here, unlike Meter's read-only one, but the conversion deliberately keeps the "only Name changes" scope every other converted screen uses).
**Delete (`objectdates`):** End Date `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` = Start Date ⇒ true delete from `OV_PIPELINE_SEGMENT`.

**Test data used (unchanged from the pre-existing 2026-06-12 build, reused not reinvented):**
- Fixed test code `AUTOTEST_PIPELINE_SEGMENT`.
- Business Unit navigator scope: `TS5 BU`.
- Insert Pipeline Name dropdown value: `TS5 Gas Pipeline` (the same value the pre-existing driver already proved live and DB-verified under the TS5 BU scope).
- Start Date `2020-01-01`.

## 3. IUD DESIGN (pre-existing, structurally converted by PR #558)
```
SETUP : Open EC Screen -> Apply Navigator From Properties (Business Unit = TS5 BU) -> GO
INSERT: New Object -> Code/Name/Start Date + Pipeline Name = TS5 Gas Pipeline -> Save -> GO
UPDATE: select row by code -> updateAttributes Pipeline Segment Name -> Save -> GO
FIND  : filter grid by code -> compare grid + form record
DELETE: select row -> objectdates End Date = Start Date -> Save -> GO
```

## 3.2 AREA-PATTERN CONVERSION (PR #558, merged 2026-08-26)
Converted the RF automation from the OLD 4-TC/suite-login/generated-timestamp-code/inline-DB-verify
shape to the full Area-pattern structure (real PR #558 body):
- Live read-only DOM recon (2026-08-26, temp recon `.robot` files, deleted before commit)
  re-confirmed the navigator is a single mandatory Business Unit dropdown at
  `nav:form:G:0:R:1:C:1:dd` — the SAME single-dropdown shape as Area's own Production Unit
  navigator (`G:0` only; row 1 has Date pre-filled/non-empty at `C:0`, Business Unit genuinely
  mandatory+empty at `C:1`, an optional "Pipeline" filter at `C:2`). This confirms the fit for
  Area's pattern — no scope mismatch found, so no entry was needed in
  `docs/navigator-screens-not-matching-area.md`.
- 5 TCs (added TC04 Find), per-TC Login/Logout (`PIPELINE_SEGMENT_EC_USER`/`PIPELINE_SEGMENT_EC_PASS`
  added to `resources/credentials.py`, additive only).
- Navigator filled via the shared T2 `Apply Navigator From Properties` (zero shared-file changes)
  driven by `testdata/pipeline_segment_navigator.properties`.
- Properties-file-driven insert/update/verify
  (`testdata/pipeline_segment_{insert,update,form_verify,grid_verify}.properties`).
- Fixed test code `AUTOTEST_PIPELINE_SEGMENT` (confirmed free in `OV_PIPELINE_SEGMENT` via a fresh
  independent oracledb connection before the build).
- Explicit `Find/Clear Pipeline Segment Row By Filter` wired into Update/Find/Verify-Found/Delete.
- Zero inline DB-verify calls in the `.robot` file (pure-screen verification; DB checks live only
  inside the shared T2 `Verify Object Removed`).
- Field labels confirmed screen-prefixed live: "Pipeline Segment Code"/"Pipeline Segment Name".
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  MODIFIED in place, plus new R38 sections added to
  `docs/bank-pattern-conversion-checklist.md` and `docs/grid-filter-standardization-checklist.md`.

**Real incident disclosed at merge (shared-checkout collision, resolved via isolated git plumbing):**
this session's shared repo checkout had its HEAD moved to a detached state by concurrent agents
working other screens (Contract Inventory/Property/Pilot mid-conversion at the same time). Rather
than risk cross-contaminating Pipeline Segment's commit with another in-flight agent's uncommitted
state on the same shared branch, PR #558's own commit was built via **isolated git plumbing**
(`read-tree`/`hash-object`/`commit-tree` against the shared branch's fork point) — producing a
commit containing ONLY the 12 Pipeline Segment files, independent of whatever else the shared
working tree held at that moment. The PR body notes `check_bundle_hygiene.py`'s live overall exit
code at the time reflected the OTHER agents' in-flight state too (not a Pipeline Segment defect);
Pipeline Segment's own R38 four-doc-set requirement was satisfied within this diff regardless.

## 4. ISSUE FOUND & FIXED
No new issue found or fixed by PR #558 itself — the conversion was structural (navigator/insert/
update/delete gestures were re-confirmed to behave exactly as the pre-existing 2026-06-12 driver
already documented; no new/extrapolated fields were added).

This backfill (2026-08-27) hit one real live-run flake on the FIRST evidence-capture attempt:
`EC_HEADLESS=true robot ...` failed all 5 TCs with `Could not find active page` / `Target page,
context or browser has been closed` — the browser context died mid-suite. `tasklist | grep -i
chrome` immediately after showed 0 chrome processes (they had already been torn down), consistent
with resource contention from other agents' concurrent live runs in this shared environment, not a
Pipeline Segment code defect. An immediate retry of the same unmodified command passed clean
(5/5 PASS) — see §5.

## 5. EVIDENCE (DB ground truth)

### Original 2026-06-12 build / PR #558 conversion (2026-08-26)
- Live run: `EC_HEADLESS=true robot tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot` → **5/5 PASS**.
- Fresh independent oracledb connection (dsn `localhost:1521/ORCL`) confirmed `AUTOTEST_PIPELINE_SEGMENT` was 0 rows in `OV_PIPELINE_SEGMENT` before the build.
- Filter keyword fired: `grep -c "Find Object Row By Filter" output.xml` → 15.
- Self-clean: fresh independent oracledb connection AFTER the run confirmed 0 residual `AUTOTEST%` rows.
- Full `tests/` tree `robot --dryrun` → 878/878 pass, 0 collisions.
- `py -m robocop check` on the 2 changed screen files → 7 issues (2 VAR02 + 5 DOC02), exact parity with `area_page.resource`/`area_iud.robot`'s own 7-issue baseline.

### This backfill (2026-08-27, `evidence/backfill_2026-08-27/`)
- Dryrun re-run of the already-proven suite alone: **5/5 PASS** (`evidence/backfill_2026-08-27/dryrun/`).
- Live headless re-run, FIRST attempt: **5 tests, 0 passed, 5 failed** — real browser-context-closed
  flake, disclosed in §4, not smoothed over. RETRY (same unmodified command): **5/5 PASS**
  (`evidence/backfill_2026-08-27/live/`, the retry's artifacts).
- `grep -c "Find Object Row By Filter"` on the retry's `output.xml` → 15 (matches PR #558's cited count).
- `robocop check` on the 2 files re-run: 7 issues (2x VAR02 + 5x DOC02), cross-checked against
  `area_page.resource`/`area_iud.robot` (also 7) — parity confirmed independently.
- Fresh independent oracledb connection, run AFTER the passing retry:
  `SELECT COUNT(*) FROM OV_PIPELINE_SEGMENT WHERE CODE = 'AUTOTEST_PIPELINE_SEGMENT'` → 0;
  `SELECT CODE FROM OV_PIPELINE_SEGMENT WHERE CODE LIKE 'AUTOTEST%'` → no rows.
- `py scripts/check_bundle_hygiene.py` (repo root) → `RESULT: PASS` (one unrelated pre-existing WARN
  on Contract Area's `investigation/` selector-string false positive, not a Pipeline Segment issue).
- **No RF automation file was modified, rebuilt, or re-verified from scratch by this backfill** —
  confirmed via `git diff --stat` against `pageobjects/`, `tests/`, `testdata/`,
  `resources/credentials.py`, `docs/ec_screen_registry.md` (empty diff) before committing.

## 6. DELIVERABLES
| Deliverable | Path |
|---|---|
| T3 page object | `pageobjects/Configuration/Assets/Dispatching_Objects/pipeline_segment_page.resource` (Area-pattern shape, PR #558) |
| RF suite | `tests/Configuration/Assets/Dispatching_Objects/pipeline_segment_iud.robot` (5 TCs, PR #558) |
| Testdata | `testdata/pipeline_segment_{navigator,insert,update,form_verify,grid_verify}.properties` (PR #558) |
| Playwright bundle | N/A — permanently waived for Area-pattern work (Section H); none built by this backfill |
| Evidence | `screens/.../Pipeline_Segment/evidence/backfill_2026-08-27/` (this backfill's dryrun + live re-run, including the disclosed flake+retry) |
| JOURNAL / CHECKLIST | `JOURNAL.md`, `CHECKLIST.md` (added 2026-08-27 backfill) |
| KB selector map | `ec-ui-knowledge/screens/pipeline_segment.md` (added 2026-08-27 backfill) |
| Reuse | T2 `manage_object.resource` (incl. `Apply Navigator From Properties`) + T1 `common`/`table`/`navigator` (no shared-file changes by PR #558 or this backfill) |
