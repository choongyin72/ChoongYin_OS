# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Sub Area
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11 (original build); updated 2026-08-27 (backfill after PR #538 Area-pattern conversion)
**Version:** 2.0 — COMPLETE (RF suite converted to the Area-pattern 5-TC structure via PR #538, 2026-08-26; original Playwright reference kept unchanged; live + DB-verified)

---

## 1. REQUIREMENT
Automate Insert / Update / Delete on the **Sub Area** screen and prove, at DB level,
that EC creates, modifies and truly deletes the record. Constraints: NEVER touch
existing data; all test data prefixed `AUTOTEST_SUBAREA_`; environment = local EC
sandbox (`ap-f0a7g341jn6d`), user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_SUB_AREA` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End Date = Start Date -> gone from grid AND absent in `OV_SUB_AREA` | PASS |
| CLEANUP | zero leftover test data | PASS |

## 2. DESIGN

### 2.1 Screen classification
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Basic Objects > Sub Area |
| Screen type | Manage Object (OV-GM groupmodel) |
| List/grid id | `manageObject:form:T_data` |
| DB view (ground truth) | `OV_SUB_AREA` |
| Delete semantics | End Date = Start Date (true delete) |
| Navigator (mandatory before grid loads) | `Production Unit` then `Offshore area` + GO |

### 2.2 Screen-specific notes
OV-GM with a CASCADING navigator: Production Unit first, then Area (its options only load after the PU is picked). LEADING-SPACE QUIRK: the sandbox area names are stored as ' Offshore area' (leading space, invisible in every trimmed display) - option matching must use normalize-space on data-item-label.

### 2.3 DOM reference (from recon)
```
INSERT objectForm : Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
                    Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
                    Start tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
                    Op Production Unit:tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd (MANDATORY dropdown)
                    Op Area:tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd (MANDATORY dropdown)
UPDATE            : Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
                    Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE objectdates: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### 2.4 Test data
| Field | Value |
|---|---|
| Code | `AUTOTEST_SUBAREA_<timestamp>` (fresh per run — deleted codes linger in the base table) |
| Name / Name (update) | `Sub Area <code>` / `Sub Area <code> UPD` |
| Start = End (delete) | `2003-01-01` |
| Op Production Unit | `Production Unit` (user-approved 2026-06-11) |
| Op Area | `Offshore area` (user-approved 2026-06-11) |

## 3. DEVELOPMENT — what it took

### 3.1 Original build (2026-06-11 session)
The screen was recon'd with the scripts preserved in `investigation/` (full-section
recon + label/mandatory mapping; per-screen probes where the first live run failed).
Key phase findings that shaped this screen's automation:
- The cascading Area dropdown only populates after the PU pick, and the stored names carry a LEADING SPACE (' Offshore area') -> normalize-space matching in the shared keyword; cascade retry via Escape+reopen.

### 3.2 Area-pattern conversion (PR #538, merged 2026-08-26)
One-paragraph dev story pulled from the real PR #538 body (not invented): the RF suite was
converted from the OLD bespoke-navigator/4-TC/suite-level-login pattern to the full Area-pattern
structure — properties-file-driven navigator via the shared `Apply Navigator From Properties` T2
keyword (`resources/manage_object.resource`), per-TC login/logout (each TC opens its own
Login/Logout pair on the one Suite-Setup browser, matching Area/Facility Class 1), a new TC04
Find test case (4 TC -> 5 TC), a fixed test code (`AUTOTEST_SUB_AREA`, confirmed absent from
`OV_SUB_AREA` before the conversion via a fresh oracledb connection) replacing the old
timestamped code, a dedicated credentials pair (`SUB_AREA_EC_USER`/`SUB_AREA_EC_PASS` in
`resources/credentials.py`), and zero inline DB-verify calls in the `.robot` file (the suite is
now pure-screen-verification; the one DB check that remains — TC05's absence check — lives in
the shared T2 `Verify Object Removed`). The screen's genuine 2-level Production Unit -> Area
navigator cascade was kept exactly as the prior build proved it (same values: `Production Unit` /
`Offshore area`) — this was a STRUCTURAL conversion, not a reclassification of the screen. Five
new `testdata/sub_area_*.properties` files were added (navigator/insert/update/form_verify/
grid_verify); `resources/manage_object.resource` (the shared T2) was NOT modified — Sub Area's
cascade fit the already-proven shape with no gap found. Live run at conversion time: `5 tests, 5
passed, 0 failed` (TC01-TC05), fresh-connection DB self-clean confirmed both before and after
(`OV_SUB_AREA` 0 rows for `AUTOTEST_SUB_AREA`, 0 residual `AUTOTEST%`).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun (structure, original 4-TC) | headless | PASS |
| RF live batch (original 4-TC) | headless | TC01–TC04 4/4 PASS, DB-verified |
| RF demo (original 4-TC) | HEADED (watched) | 4/4 PASS |
| Playwright reference run | headless | see `evidence/sub_area_results.json` |
| RF dryrun (Area-pattern 5-TC, PR #538) | headless | 5 tests, 5 passed, 0 failed |
| RF live (Area-pattern 5-TC, PR #538) | headless | 5 tests, 5 passed, 0 failed, DB-verified |
| RF dryrun (backfill re-run, 2026-08-27) | headless | 5 tests, 5 passed, 0 failed |
| RF live (backfill re-run, 2026-08-27) | headless | 5 tests, 5 passed, 0 failed; `OV_SUB_AREA` self-clean re-confirmed (0 rows `AUTOTEST_SUB_AREA`, 0 residual `AUTOTEST%`) |

Evidence screenshots in `evidence/` (loaded / clean / insert / update / delete steps, original
build). The backfill re-run's log/report/output are in `evidence/backfill_2026-08-27/`.

## 5. DELIVERABLES
| Deliverable | Where |
|---|---|
| RF suite (maintained test, Area-pattern 5-TC) | `tests/Configuration/Assets/Basic_Objects/sub_area_iud.robot` |
| RF page object (Area-pattern) | `pageobjects/Configuration/Assets/Basic_Objects/sub_area_page.resource` |
| RF navigator/data files | `testdata/sub_area_navigator.properties`, `sub_area_insert.properties`, `sub_area_update.properties`, `sub_area_form_verify.properties`, `sub_area_grid_verify.properties` |
| Playwright reference (unmodified by PR #538) | `playwright/ec_iud_sub_area.py` (+ `_shared/iud_engine.py`) |
| Recon trail (original build) | `investigation/` |
| Registry row | `docs/ec_screen_registry.md` |
| Conversion PR | [#538](https://github.com/choongyin72/ChoongYin_OS/pull/538) |
| Work journal | `JOURNAL.md` |
| KB selector map | `../../../../../ec-ui-knowledge/screens/sub_area.md` |

## 6. LESSONS LEARNED (section-wide, applied here)
1. **Silent reject = mandatory field**: a Save that produces no row + the banner
   "Required fields are empty: <field>" — fill the named dropdown.
2. **Code/Name rows are NOT always R0/R1** — recon the `:C:0:la` labels first
   (State/County have Master System rows above them).
3. **Form dropdowns are effective-date-filtered** — only objects valid at the form's
   Start Date are offered.
4. **Dropdown labels may carry leading/double spaces** in seed data — match with
   normalize-space.
5. **The UI can lie**: groupmodel grids redraw lazily; ALWAYS verify at the DB.
