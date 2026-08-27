# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Field
**Author:** Choong-Yin Lee / Claude
**Date:** 2026-08-27 (backfilled — retroactive documentation per
`docs/lean-deliverable-backfill-workorder.md`, owner decision 2026-08-27)
**Version:** 2.0 — FULL Area-pattern conversion (RF suite), superseding v1.0's original
Playwright-era build (2026-06-12)

---

## 1. REQUIREMENT
Automate IUD on the **Field** screen with DB-level proof. Constraints: NEVER touch
existing data; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_FIELD` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| FIND | Grid + form record match expected data | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_FIELD` | PASS |

## 2. CLASSIFICATION
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > Field |
| Screen type | Manage Object (OV-GM groupmodel) — navigator matches Area's layout (single-dropdown cascade) |
| Pattern | FULL Area-pattern conversion (owner standing rule 2026-08-26: any navigator screen matching Area's layout follows Area's full pattern, not just the navigator-fill piece) |
| List/grid id | `manageObject:form:T_data` |
| DB view | `OV_FIELD` |
| Delete semantics | End Date = Start Date (true delete) |
| Navigator (mandatory before grid loads) | Single Area dropdown (`nav:form:G:0:R:1:C:1:dd`) + GO, value `Offshore area` |
| Grid headers (confirmed live) | Field Code / Field Name / Start Date / End Date |
| Mandatory fields (confirmed live via ECCell/MandatoryCellStyle dump) | Field Code, Field Name, Start Date (screen-prefixed labels, not generic "Code"/"Name") — Sort Order/Description/Master System Code+Name/Commercial Entity/Parent field/Operator/Country/State/Comments/Full field name/Non equity Indicator all confirmed NOT mandatory |
| Business-rule field (not statically mandatory, but required for grid visibility) | Geo Area = navigator Area value (`Offshore area`) — the groupmodel link |

## 3. TEST DATA
| Field | Value |
|---|---|
| Test code (fixed, not generated) | `AUTOTEST_FIELD` |
| Field Name (insert) | `Automation Test Field` |
| Field Name (update) | `Automation Test Field UPDATED` |
| Start Date | `2003-01-01` |
| End Date (delete) | `2003-01-01` (= Start Date) |
| Geo Area | `Offshore area` |

Fixed test code confirmed free in `OV_FIELD` via a fresh `oracledb` connection before each
live run (`SELECT COUNT(*) FROM OV_FIELD WHERE CODE LIKE 'AUTOTEST%'` → 0).

## 4. DEV STORY (real history, from PR #525 and PR #529)
Field's RF automation was originally built 2026-06-12 as part of the Commercial Objects
11-screen batch (generated code, hardcoded field-ids, generated `AUTOTEST_FLD_<timestamp>`
codes, 4-TC structure with inline DB-verify calls).

**PR #525 (merged 2026-08-26)** converted only the navigator-fill piece: Field's inline
`Select EC Dropdown Option` + `Apply Navigator` sequence was replaced with the new shared
T2 keyword `Apply Navigator From Properties` (`resources/manage_object.resource`, built for
Area), driven by a new `testdata/field_navigator.properties`. This was a deliberate
reusability test of the shared keyword on a screen it was not originally built for. Field's
navigator is a genuine single-dropdown cascade (`nav:form:G:0:R:1:C:1:dd`), the exact shape
the keyword's documented known limitation covers, so it fit with no design changes to the
shared keyword. **One real defect was caught, not assumed:** `field_page.resource` had never
imported `libraries/PropertiesReader.py` (no properties-file mechanism existed on this screen
before), so the shared keyword's `Read Properties` call failed at suite setup. The mandatory
full-tree dryrun caught this — the count regressed to 842/846 immediately after the page-object
edit, before the import fix restored it to 846/846. This is the honest "done wrong" of the
build: a missing-import defect shipped in a first pass and was caught by process (the mandatory
dryrun gate), not by review.

**PR #529 (closed but content merged to master via commit `a5104dea`)** was the owner's
follow-up standing rule from 2026-08-26: any EC screen with a navigator matching Area's layout
must follow Area's FULL pattern, not just the navigator-fill piece. This PR converted the rest
of Field's suite structure to match `area_page.resource`/`area_iud.robot` exactly: 5 TCs
(Verify Clean State/Insert/Update/Find/Delete), per-TC `Login To EC Application`/
`Logout From EC Application` on one browser opened once in Suite Setup, a dedicated
`FIELD_EC_USER`/`FIELD_EC_PASS` credential pair, a fixed test code (`AUTOTEST_FIELD`,
replacing the generated `AUTOTEST_FLD_<timestamp>`), properties-file-driven Insert/Update/
Verify via 4 new `testdata/field_*.properties` files, explicit `Find/Clear Field Row By
Filter` grid-filter wiring, and pure-screen verification (zero inline DB-verify calls left in
`field_iud.robot` — the DB check now lives only inside the shared T2 `Verify Object Removed`).
No shared T1/T2 file changes were needed beyond what Area already added; Field's navigator
shape already fit the existing keyword.

## 5. LESSONS
- A screen can appear to "already work" (Field's pre-existing navigator fill was live-tested
  and passing) while still missing plumbing (the `PropertiesReader` import) that only a
  structural change exposes — the mandatory full-tree dryrun is what caught it, reinforcing
  why that gate is non-negotiable even on a "just navigator delegation" change.
- Converting only part of a screen (navigator-fill only, in #525) left it inconsistent with
  the rest of the batch until the owner's standing rule (2026-08-26) closed the gap in #529 —
  confirms the value of the "full pattern, not partial" rule once a screen's layout is
  confirmed to match Area's.

## 6. TEST EXECUTION (backfill re-run, 2026-08-27)
| Run | Mode | Result |
|---|---|---|
| Full-tree `robot --dryrun tests/` | headless | 883/883 PASS |
| `field_iud.robot` live | `EC_HEADLESS=true` | 5/5 PASS (TC01–TC05) |
| DB self-clean (fresh `oracledb` connection, `localhost:1521/ORCL`, `ECKERNEL_EC`) | `SELECT COUNT(*) FROM OV_FIELD WHERE CODE LIKE 'AUTOTEST%'` | 0 |
| Filter-keyword wiring | `grep` on live `output.xml` | 14 `Find Field Row By Filter` + 5 `Clear Field Row Filter` hits |
| `py scripts/check_bundle_hygiene.py` | repo root | RESULT: PASS |

## 7. DELIVERABLES
- RF suite + page object: `pageobjects/Configuration/Assets/Commercial_Objects/field_page.resource`,
  `tests/Configuration/Assets/Commercial_Objects/field_iud.robot` (already merged, NOT modified
  by this backfill task).
- This documentation bundle (SOW, README, JOURNAL, evidence, CHECKLIST) — backfilled 2026-08-27.
- Registry row: `docs/ec_screen_registry.md` (already present, describes the full conversion).
- KB selector map: `ec-ui-knowledge/screens/field.md` (added by this backfill).
- Legacy artifacts kept unchanged: `playwright/ec_iud_field.py`, `investigation/*.py`,
  `evidence/field_0*.png` + `field_results.json` from the original 2026-06-12 build — these
  predate the Area-pattern conversion and describe the OLD 4-TC/generated-code shape; kept as
  historical reference only, not updated (items 4/5 of the deliverable checklist stay waived
  per Section H — the Universal Screen Engine replaces the Playwright-driver role going
  forward, so no new Playwright work is done here).
