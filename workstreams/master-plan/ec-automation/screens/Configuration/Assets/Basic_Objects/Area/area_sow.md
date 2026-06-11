# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — Area
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate Insert / Update / Delete on the **Area** screen and prove, at DB level,
that EC creates, modifies and truly deletes the record. Constraints: NEVER touch
existing data; all test data prefixed `AUTOTEST_AREA_`; environment = local EC
sandbox (`ap-f0a7g341jn6d`), user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_AREA` | PASS |
| UPDATE | Name change visible in grid row | PASS |
| DELETE | End Date = Start Date -> gone from grid AND absent in `OV_AREA` | PASS |
| CLEANUP | zero leftover test data | PASS |

## 2. DESIGN

### 2.1 Screen classification
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Basic Objects > Area |
| Screen type | Manage Object (OV-GM groupmodel) |
| List/grid id | `manageObject:form:T_data` |
| DB view (ground truth) | `OV_AREA` |
| Delete semantics | End Date = Start Date (true delete) |
| Navigator (mandatory before grid loads) | `Production Unit` + GO |

### 2.2 Screen-specific notes
OV-GM (groupmodel): grid loads ONLY after a Production Unit is picked in the navigator + GO. The inserted area must set Op Production Unit = the navigator PU or it never shows in the filtered grid. Form dropdowns are EFFECTIVE-DATE-FILTERED: with Start Date 2000-01-01 the Op PU list excludes 'Production Unit' (starts 2002-01-01) -> test dates are 2003-01-01. Versioned grid redraws lazily after delete -> one extra GO.

### 2.3 DOM reference (from recon)
```
INSERT objectForm : Code  tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
                    Name  tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
                    Start tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
                    Op Production Unit:tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd (MANDATORY dropdown)
UPDATE            : Code  tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in (guard)
                    Name  tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
DELETE objectdates: End   tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
```

### 2.4 Test data
| Field | Value |
|---|---|
| Code | `AUTOTEST_AREA_<timestamp>` (fresh per run — deleted codes linger in the base table) |
| Name / Name (update) | `Area <code>` / `Area <code> UPD` |
| Start = End (delete) | `2003-01-01` |
| Op Production Unit | `Production Unit` (user-approved 2026-06-11) |

## 3. DEVELOPMENT — what it took (2026-06-11 session)
The screen was recon'd with the scripts preserved in `investigation/` (full-section
recon + label/mandatory mapping; per-screen probes where the first live run failed).
Key phase findings that shaped this screen's automation:
- Three failures before green: (1) form dropdown options are effective-date-filtered (dates moved to 2003-01-01); (2) dropdown panel structure differs between navigator and form (tr[data-item-label]); (3) the versioned grid redrew lazily after delete (extra GO before asserting).

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun (structure) | headless | PASS |
| RF live batch | headless | TC01–TC04 4/4 PASS, DB-verified |
| RF demo | HEADED (watched) | 4/4 PASS |
| Playwright reference run | headless | see `evidence/area_results.json` |

Evidence screenshots in `evidence/` (loaded / clean / insert / update / delete steps).

## 5. DELIVERABLES
| Deliverable | Where |
|---|---|
| RF suite (maintained test) | `tests/Configuration/Assets/Basic_Objects/area_iud.robot` |
| RF page object | `pageobjects/Configuration/Assets/Basic_Objects/area_page.resource` |
| Playwright reference | `playwright/ec_iud_area.py` (+ `_shared/iud_engine.py`) |
| Recon trail | `investigation/` |
| Registry row | `docs/ec_screen_registry.md` |

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
