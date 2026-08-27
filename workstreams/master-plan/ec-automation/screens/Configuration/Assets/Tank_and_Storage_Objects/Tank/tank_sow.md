# EC Screen IUD — Statement of Work: **Tank**
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Built by:** `ec-area-pattern-new-screen` skill (autonomous run) — PR #553, merged 2026-08-26
**Backfilled:** `docs/lean-deliverable-backfill-workorder.md`, Batch 3 — 2026-08-27 (see §3, §5)
**Result:** COMPLETE — live **5/5 PASS** (Area-pattern, TC01-TC05), DB-verified, self-cleaning (0 residual)

---

## 1. REQUIREMENT / METADATA
| Property | Value | Source |
|---|---|---|
| Screen | **Tank** | input |
| Treeview path | **Configuration > Assets > Tank and Storage Objects > Tank** | confirmed live 2026-08-26 via treeview expand (direct sibling of Storage/Manage Tank/Maintain Tanks) |
| Class | `TANK` | `tank_page.resource` header |
| Class type | OV-GM (groupmodel manage-object) | live recon |
| Time scope | VERSIONED (date-effective) ⇒ **DELETE = End Date = Start Date** | live recon |
| Verify view | `OV_TANK` (versioned) | `docs/ec_screen_registry.md` row (line 357) |
| Family | OV-GM, same navigator shape as Well/Area/Storage | registry |
| Grid | `manageObject:form:T_data` | `tank_page.resource` |

**Distinct from:** Chemical Tank (a different sibling screen with its own `OV_CHEM_TANK` view and
`chemical_tank_page.resource`/`chemical_tank_iud.robot` files) — confirmed by name via
`grep -ril "tank_page.resource"` excluding any `chemical` match, and by the registry row text
which explicitly separates Tank from Chemical Tank/Chemical Transport Tank/Storage/Storage
Flow/`daily_tank_status_vcf` as unrelated siblings (PR #553 body, "What was built").

## 2. LIVE RECON (as documented by the original build, PR #553 + `tank_page.resource`)
**Navigator** — single row, increasing-column cascade `nav:form:G:0:R:1:C:0..3`:
| Element | Locator | Mandatory |
|---|---|---|
| Nav Date (C:0) | `nav:form:G:0:R:1:C:0:da_input` | has a working default — left untouched, GO succeeds without filling it |
| Nav Op Production Unit (C:1, dd) | `nav:form:G:0:R:1:C:1:dd` | **yes** |
| Nav Op Area (C:2, dd) | `nav:form:G:0:R:1:C:2:dd` | **yes** |
| Nav Op Facility Class 1 (C:3, dd) | `nav:form:G:0:R:1:C:3:dd` | **yes** |
| GO | `button:form:B` | — |
| Grid | `manageObject:form:T_data` | first column = Tank Code |

Same shape as Well's own navigator (`well_page.resource` "Apply Well Navigator") and same "P1
Production Unit"/"P1 Area"/"P1 Facility 1" values Well already uses.

**Insert — `objectForm` (New Object), labels SCREEN-PREFIXED ("Tank Code"/"Tank Name", like
Area's "Area Code"/"Area Name"):**
| Field | Mandatory (yellow+empty, confirmed live) |
|---|---|
| Tank Code | **yes** |
| Tank Name | **yes** |
| Start Date | **yes** |
| Tank Meter Freq. | **yes** — filled `__FIRST__` |
| Use in BF | **yes** — filled `__FIRST__` |
| Op Production Unit / Op Area / Op Facility Class 1 | NOT mandatory (white bg), but NOT
  auto-populated from the navigator scope — confirmed live via a self-cleaning probe
  insert/delete (`AUTOTEST_TANK_RECON`, never the real fixed test code); must be filled explicitly
  to match the nav scope or the new row is invisible under this OV-GM navigator scope |

**Update — `updateAttributes`:** only Tank Name is edited (Tank Code read-only; Start Date lives
only in `objectdates`, same pattern as Bank/Area/Storage Flow).

**Delete — `objectdates`:** End Date `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` = Start
Date ⇒ true delete from `OV_TANK` (same framework-invariant layout as Area/Bank).

**Test data:** fixed test code `AUTOTEST_TANK` (confirmed absent from `OV_TANK` before the
original build), Start Date `2003-01-01`, navigator scope P1 Production Unit / P1 Area / P1
Facility 1.

## 3. DEV STORY — brand-new build, NOT a conversion (PR #553, merged 2026-08-26)
Unlike most of this backfill batch, Tank never had ANY prior automation — no legacy Playwright
driver, no old-style RF suite, no pre-existing `screens/` bundle before PR #553 (confirmed via a
fresh repo grep at build time). It was built from scratch via the `ec-area-pattern-new-screen`
skill directly to the current Area-pattern shape, after a live DOM scan confirmed the navigator is
Area-pattern-shaped: a single row, increasing-column cascade (`nav:form:G:0:R:1:C:0..3`) where C:0
is a Date field with a working default (left untouched) and C:1/C:2/C:3 are a genuine Production
Unit -> Area -> Facility Class 1 cascade — the SAME shape and SAME "P1 Production Unit"/"P1
Area"/"P1 Facility 1" values already proven on Well's navigator. Built as a 5-TC/per-TC-login/
pure-screen-verify structure, properties-file-driven, T2-consolidated, mirroring
`area_page.resource`/`area_iud.robot` exactly. No gotcha or defect was disclosed in PR #553's own
body — the recon (navigator shape, mandatory-field scan, the Op Production Unit/Op Area/Op
Facility Class 1 scope-matching requirement, and the objectdates Delete field id) was all
confirmed live via a self-cleaning probe (`AUTOTEST_TANK_RECON`) before any locator was written,
and the build passed live 5/5 on the first attempt cited in the PR.

Because this was a lean RF-only new-screen build (owner decision 2026-08-23/26, since retired by
Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` on 2026-08-27), the SOW/README/JOURNAL/evidence/
CHECKLIST/KB map this file is part of were not produced at build time — this is that retroactive
backfill (see §5).

## 4. ISSUES FOUND
None disclosed in PR #553's body for the original build. No issues found during this backfill's
re-run either, once an unrelated environment/process-leak flake (see §5) was diagnosed and cleared
— it was not a Tank suite defect.

## 5. EVIDENCE

### Original build (PR #553, 2026-08-26)
- Live suite run: `EC_HEADLESS=true robot tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot`
  -> **5 tests, 5 passed, 0 failed** (TC01-TC05).
- Fresh independent `oracledb` connection after the live run: `SELECT CODE, NAME FROM OV_TANK
  WHERE UPPER(CODE) LIKE 'AUTOTEST%' OR UPPER(NAME) LIKE 'AUTOTEST%'` -> **0 residual rows**.
- `grep -c "Find Object Row By Filter" results/tank_live/output.xml` -> **15**.
- Full-tree dryrun: **854 tests, 854 passed, 0 failed**.
- Robocop: **7 issues**, exact parity with `area_page.resource`/`area_iud.robot`'s own 7-issue
  baseline (2x VAR02 + 5x DOC02).
- `AUTOTEST_TANK` confirmed free in `OV_TANK` before the build.

### This backfill (2026-08-27, `evidence/backfill_2026-08-27/`)
- Fresh dryrun re-run of the already-proven suite alone: **5/5 PASS** (`dryrun/`).
- Live headless re-run: **5/5 PASS** (`live/`), reached on the 5th attempt this session — the
  first 4 attempts failed with page/connection errors caused by an accumulating pile of stray
  `chrome-headless-shell.exe`/`node.exe`/`robot.exe` processes left behind by earlier failed
  attempts, confirmed via `tasklist`, and NOT a Tank suite defect (dryrun stayed 5/5 throughout;
  an isolated TC01+TC02-only run passed cleanly mid-investigation). One of those partial live
  attempts left a residual `AUTOTEST_TANK` row (insert completed, delete never reached) — cleaned
  up by running TC05 alone before the final clean 5/5 attempt. See `evidence/backfill_2026-08-27/
  summary.json` for the full timeline.
- Fresh `oracledb` connection self-clean check, before and after the final live run: `OV_TANK`
  `AUTOTEST%` -> **0 residual rows** both times.
- `grep -c "Find Object Row By Filter" evidence/backfill_2026-08-27/live/output.xml` -> **15**
  (matches PR #553's cited count).
- `robocop check` re-run on the 2 unmodified files: **7 issues**, cross-checked against
  `area_page.resource`/`area_iud.robot` (also 7) — parity re-confirmed independently.
- `py scripts/check_bundle_hygiene.py` -> `RESULT: PASS`.
- **No RF automation file was modified, rebuilt, or re-verified from scratch by this backfill** —
  confirmed via `git diff --stat` against `pageobjects/`, `tests/`, `testdata/`,
  `resources/credentials.py`, `docs/ec_screen_registry.md`, `docs/automation-scorecard.md`
  (empty diff) before committing.

## 6. DELIVERABLES
| Deliverable | Path |
|---|---|
| T3 page object | `pageobjects/Configuration/Assets/Tank_and_Storage_Objects/tank_page.resource` (Area-pattern shape, PR #553) |
| RF suite | `tests/Configuration/Assets/Tank_and_Storage_Objects/tank_iud.robot` (5 TCs, PR #553) |
| Testdata | `testdata/tank_{insert,update,form_verify,grid_verify,navigator}.properties` (PR #553) |
| Playwright bundle | N/A — waived (Section H); no hand-written Playwright driver was ever built for this screen (owner decision, Universal Screen Engine replaces this role) |
| Recon scripts | `investigation/{recon.py,dbcheck_selfclean.py}` (PR #553, consolidated live-recon evidence — original build, unchanged by this backfill) |
| Evidence | `evidence/backfill_2026-08-27/` (this backfill's dryrun + live re-run; no original-build evidence/ folder existed since this was a lean new-screen build) |
| JOURNAL / CHECKLIST | `JOURNAL.md`, `CHECKLIST.md` (added 2026-08-27 backfill) |
| KB selector map | `ec-ui-knowledge/screens/tank.md` (added 2026-08-27 backfill) |
| Reuse | T2 `resources/manage_object.resource` (incl. `Apply Navigator From Properties`) + T1 `common`/`table`/`navigator` — no shared-file changes by PR #553 or this backfill |
