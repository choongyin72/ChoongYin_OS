# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (IUD) Automation — State Lease
**Author:** Choong-Yin Lee / Claude
**Date:** 2026-06-12 (original build) — refreshed 2026-08-28 (lean-deliverable backfill, PR #440 provenance)
**Version:** 2.0 — Bank-pattern RF suite (PR #440, merged 2026-08-23); older Playwright reference retained for history

---

## 1. REQUIREMENT
Automate IUD on the **State Lease** screen with DB-level proof. Constraints: NEVER touch
existing data; fixed test code `AUTOTEST_STL`; local sandbox, user sysadmin.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT | AUTOTEST row in grid AND present in `OV_STATE_LEASE` | PASS |
| UPDATE | Name + Description change visible in grid row and form | PASS |
| FIND | Grid + form record match expected data | PASS |
| DELETE | End=Start -> gone from grid AND absent in `OV_STATE_LEASE` | PASS |

## 2. DESIGN
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Commercial Objects > State Lease |
| Screen type | Manage Object (OV), plain — no mandatory navigator/cascade dropdown (confirmed live) |
| Pattern | Bank pattern — label-driven, properties-file-driven, T2-consolidated (`docs/ec_screen_registry.md` row) |
| List/grid id | `manage_object_nav_nav:form:T_data` (`${OV_MANAGE_OBJECT_TABLE}` shared constant) |
| DB view | `OV_STATE_LEASE` |
| Delete semantics | End Date = Start Date (true delete) |
| Code label | "State Lease Code" (screen-prefixed, not generic "Code" — matches State's own precedent) |

### Mandatory fields (objectForm, live field-inventory scan 2026-08-23)
- State Lease Code* (mandatory, yellow)
- State Lease Name* (mandatory, yellow)
- Start Date* (mandatory, yellow, date)
- Description (optional)
- End Date (optional — present on objectForm too, unlike Bank/Customer)

`updateAttributes` only carries State Lease Code (read-only) / State Lease Name / Description —
Start Date and End Date are NOT present there; they only exist in `objectForm` and `objectdates`.

### Test data (from `testdata/state_lease_insert.properties` / `state_lease_update.properties`)
- Insert: Code `AUTOTEST_STL`, Name `AUTOTEST State Lease`, Start Date `2000-01-01`, Description
  `AUTOTEST State Lease Description`
- Update: Name `AUTOTEST State Lease UPDATED`, Description `AUTOTEST State Lease Description UPDATED`
- Delete: End Date = Start Date (`2000-01-01`)

## 3. DEVELOPMENT — dev story
Originally built (2026-06-12) as a standalone Playwright reference flow against the older
hardcoded-field-id pattern (`playwright/ec_iud_state_lease.py`, generated from the section recon
`investigation/commercial_objects_recon.py`). **PR #440** (merged 2026-08-23, Batch 4 of the
Bank-pattern conversion project) converted the RF suite (`state_lease_page.resource` +
`state_lease_iud.robot`) from that old hardcoded-field-id pattern to the label-driven,
properties-file-driven, T2-consolidated "Bank pattern," adding explicit grid-filter wiring
(`Find State Lease Row By Filter`) from day one. The conversion required a live recon of
`objectForm`/`updateAttributes` because State Lease uses its own screen-prefixed labels
("State Lease Code"/"State Lease Name") rather than Bank/Customer's generic "Code"/"Name" — the
same precedent already documented for State's own "State Code." No mandatory reference dropdowns
exist on this screen, so no `__FIRST__` value resolution was needed. A stray `RECON_STL` row left
by an earlier interrupted recon attempt was found and cleaned up (DB-reconfirmed absent) before
the final live run.

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF dryrun (full tree, PR #440) | headless | 740/740 PASS |
| RF live (PR #440, 2026-08-23) | headless | TC01–TC05 5/5 PASS, DB-verified (fresh oracledb connection) |
| RF live (this backfill, 2026-08-28) | headless | see `evidence/` and `CHECKLIST.md` for the re-run citation |
| Playwright reference run (2026-06-12, historical) | headless | see `evidence/state_lease_results.json` |

## 5. DELIVERABLES
RF suite + page object under `tests|pageobjects/.../Commercial_Objects/state_lease_*`,
this bundle (SOW/README/JOURNAL/CHECKLIST/evidence), registry row in `docs/ec_screen_registry.md`,
KB selector map `ec-ui-knowledge/screens/state_lease.md`.
