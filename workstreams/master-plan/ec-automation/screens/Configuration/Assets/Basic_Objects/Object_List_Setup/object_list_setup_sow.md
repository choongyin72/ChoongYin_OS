# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Delete (item IUD) Automation — Object List Setup
**Author:** Choong-Yin Lee / Claude Fable 5
**Date:** 2026-06-11
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate adding and removing a MEMBER ITEM of an existing Object List and prove it
at DB level. Constraints: NEVER modify existing data — the member account is only
referenced; the membership row created by the test is physically deleted again.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT item | row in item grid AND `OBJECT_LIST_SETUP` count = baseline+1 | PASS |
| DELETE item | row gone AND count back to baseline | PASS |
| CLEANUP | zero leftover rows (delta oracle proves it) | PASS |

## 2. DESIGN

### 2.1 Screen classification — NEW pattern "PC" (parent-child setup)
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Basic Objects > Object List Setup |
| Screen URL | `com.ec.revn.cd/manage_object_list` |
| Navigator (mandatory) | Daytime + List Class + Object List + GO |
| Item grid | `tab:tabPanel:object_list_table:form:T_data` (inline TV-style cells) |
| Toolbar | Insert > "Object List Item" / Delete > "Object List Item" (both submenus) |
| Item delete semantics | PHYSICAL row delete |
| DB oracle | count-delta on `OBJECT_LIST_SETUP.GENERIC_OBJECT_CODE` |

### 2.2 Item-row DOM (from recon)
```
row cells: tab:tabPanel:object_list_table:form:T:{row}:C{col}...
  C0  start date  (existing rows: C0_in text; NEW rows render C0_da_input calendar)
  C1  end date    (C1_da_input)
  C2  member OBJECT dropdown (C2_dd_input value = object code; pick via C2_dd panel)
  C5  SORT ORDER  (C5_in) — MANDATORY (yellow) on a new row
  C6  checkbox, C3/C4/C7 optional texts
Blank-row detection: row whose C2_dd_input value is empty.
RE-FIND the row after the dropdown selection — the grid can re-index.
```

### 2.3 Test data (user-approved 2026-06-11)
| Field | Value |
|---|---|
| List Class | `FIN_ACCOUNT` |
| Object List | `OPEX GL Equipment Rental` (existing list `LST_GL_EQ_RENT`) |
| Member item | account `6931250` (label = its own code → unambiguous DB matching) |
| Item start date / sort order | `2003-01-01` / `999` |

## 3. DEVELOPMENT — what it took (2026-06-11 session)
- First live run: UI showed the new row but the DB count stayed at baseline — the
  classic EC SILENT REJECT, caught only by the DB oracle.
- Save-reject probe (`investigation/probe_ols_save_reject.py`) revealed the cause:
  the new row's **Sort Order (C5) cell renders MANDATORY (yellow)** and was empty.
- Second finding: the new row's start-date cell is a **calendar (C0_da_input)**, not
  the text cell (C0_in) existing rows show; and the row **re-indexes** after the
  object dropdown selection (re-find by C2 value before filling).
- Count-delta oracle design: `6931250` already sits in one other list — baseline
  recorded at start makes pre-existing rows irrelevant.

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| RF live (3 rounds to green) | headless | TC01–TC03 3/3 PASS, count-delta verified |
| RF demo | HEADED (watched) | 3/3 PASS |
| RF regression after shared-keyword hardening | headless | PASS |
| Playwright reference run | headless | see `evidence/object_list_setup_results.json` |

## 5. DELIVERABLES
| Deliverable | Where |
|---|---|
| RF suite (maintained test) | `tests/Configuration/Assets/Basic_Objects/object_list_setup_iud.robot` |
| RF page object | `pageobjects/Configuration/Assets/Basic_Objects/object_list_setup_page.resource` |
| Playwright reference | `playwright/ec_iud_object_list_setup.py` |
| Shared keywords gained | `Insert New Grid Row By Label`, `Find Grid Row By Cell Input Value` (T2), `View Count Where` (DbVerify) |
| Registry | "PC — parent-child setup" pattern section in `docs/ec_screen_registry.md` |

## 6. LESSONS LEARNED
1. **The UI can lie on parent-child grids too** — the unsaved row renders exactly like
   a saved one; only the DB count exposed the silent reject.
2. **New rows ≠ existing rows** — cell types differ (calendar vs text) and the row
   index moves after a dropdown pick; never cache a row index across an AJAX action.
3. **Count-delta is the right oracle for membership tables** — presence checks break
   when the member legitimately exists in other parents.
4. **Toolbar submenus share item names** — Insert and Delete both have an
   "Object List Item" entry; always scope the menu xpath to the right menu-parent icon.
