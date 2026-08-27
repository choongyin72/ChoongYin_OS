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

---

## 7. ADDENDUM (2026-08-25/26) — Bank-pattern 5-TC structure conversion + shared navigator keyword

_Backfilled 2026-08-27 under `docs/lean-deliverable-backfill-workorder.md` — the RF suite work below
was already built and merged (PRs #521, #523); this addendum documents it, no automation changed here._

Sections 1-6 above describe the screen's ORIGINAL 2026-06-11 build (4 TCs, timestamp-generated test
code, inline navigator fill). On 2026-08-25 the owner directed a **one-off, deliberate exception**:
convert Area's RF suite STRUCTURE to the Bank-pattern shape used elsewhere in this project, while
explicitly KEEPING Area's genuine mandatory Production Unit navigator + GO gesture (Area stayed
OV-GM; this was not a reclassification). Landed as **PR #521** (merged 2026-08-25):

- 5 TCs (added **TC04 Find**, was 4), each with its own `Login To EC Application`/
  `Logout From EC Application` (Suite Setup still opens the browser once).
- **Fixed test code `AUTOTEST_AREA`** (owner-requested) replacing the previous
  `AUTOTEST_AREA_<timestamp>` generated code — confirmed absent from `OV_AREA` via a fresh DB query
  before being wired in.
- Properties-file-driven Insert/Update (`testdata/area_{insert,update,form_verify,grid_verify}.properties`)
  via the shared T2 `Insert/Update Object From Properties`.
- Explicit `Find/Clear Area Row By Filter` grid-filter wiring into Update/Find/Verify-Found/Delete.
- Screen-local DB-verify wrapper keywords (`Area Should Exist/Not Exist In DB`) **removed** —
  verification now delegates purely to shared T2 keywords (`Verify Object Insert Exists/Form
  Record/Found/Removed/Does Not Exist`).
- Real field labels reconfirmed live: screen-prefixed **"Area Code"/"Area Name"** (not the generic
  "Code"/"Name" Bank/Object List use).
- Evidence cited in the PR: live 5/5, full-tree dryrun 846/846, DB self-clean confirmed via fresh
  connection (0/0 before+after), robocop 7 issues (same DOC02/VAR02 categories as Bank's own
  baseline — parity, not a regression), grid-filter keyword confirmed firing (29 hits in output.xml).
- The pre-existing Playwright driver (`playwright/ec_iud_area.py`, described in Sections 1-6 above)
  was **left untouched** by this PR — the owner's directive was specifically for the RF `.robot`
  suite.

A same-day follow-up, **PR #523** (merged 2026-08-25, superseding a stale unmerged PR #522 that had
been built off pre-#521 master), extracted the inline `Select EC Dropdown Option` + `Apply Navigator`
fill logic out of Area's own page object and into a **new shared T2 keyword**,
`Apply Navigator From Properties` (`resources/manage_object.resource`), driven by the new
`testdata/area_navigator.properties`. **Area was the first screen this shared keyword was built
for** — per the PR body, "any OTHER OV-GM screen with a navigator can now reuse the same shared
keyword with its own properties file (proven shape: single-dropdown or same-row C:1..C:N cascades
only; per-field nav-group screens are a documented known limitation, not solved here)." Two other
OV-GM screens with their own bespoke navigator-fill logic (Well, Test Separator) were re-run live
UNCHANGED to prove zero regression from the shared-file edit (4/4 each). Evidence cited: live 5/5
re-confirmed on the new keyword, full-tree dryrun 846/846 (matched the post-#521 baseline exactly),
robocop +3 issues vs the 19-issue pre-existing baseline for the 3 touched files (1 LEN01 on the new
keyword's own name + 2 DEPR05 `Set Variable`, same categories as the sibling `Apply OV-GM Navigator
First Available` keyword — parity, no new issue type), DB self-clean re-confirmed via fresh
oracledb connection.

This shared keyword going on to be reused by 20+ further OV-GM navigator screens is why Area
subsequently became the **role-model / reference pattern for the whole navigator-screen family**
(owner's 2026-08-26 standing rule — see
`docs/navigator-screens-not-matching-area.md`). No real defect or flake was disclosed in either PR
body for Area itself; the only corrective action recorded there was PR #523 superseding the stale
#522 (a workflow correction, not a screen defect).

**Current (post-#521/#523) DOM/keyword facts**, superseding the stale Section 2.3 table above:
- Navigator dropdown id: `nav:form:G:0:R:1:C:1:dd` (not `R:0` as shown by an earlier recon revision).
- Insert Code/Name field IDs are no longer referenced directly by the T3 — Insert/Update/Verify all
  go through the shared T2's label-resolved `Insert/Update/Verify Object *` keywords with
  `code_label=Area Code`.
- Delete End Date field id: `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (unchanged).
- Grid id: `manageObject:form:T_data` (unchanged).
