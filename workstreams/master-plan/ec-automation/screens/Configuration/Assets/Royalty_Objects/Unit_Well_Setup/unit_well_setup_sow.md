# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Delete (membership IUD) Automation — Unit - Well Setup
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-27
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live + DB-verified)

---

## 1. REQUIREMENT
Automate adding and removing a WELL SETUP membership row (links a Perf Interval to a
Unit Agreement) and prove it at DB level. Constraints: NEVER modify existing data —
the Perf Interval is only referenced; the membership row created by the test is
physically deleted again; the chosen parent (Unit Agreement 3) is EMPTY before and after.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT membership | row in grid AND `DV_UNIT_WELL_SETUP` count = baseline+1 | PASS |
| DELETE membership | row gone AND count back to baseline | PASS |
| CLEANUP | zero leftover rows (delta oracle proves it) | PASS |

## 2. DESIGN

### 2.1 Screen classification — PC pattern (parent-child setup)
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Royalty Objects > Unit - Well Setup |
| Navigator (mandatory) | Form date (G:0) + Unit Agreement (G:1) + GO (`button:form:B`) |
| Member grid | `well_setup:form:T_data` (inline TV-style cells) |
| Toolbar | Insert > "Well Setup" / Delete > "Well Setup" (both submenus) |
| Membership delete semantics | PHYSICAL row delete |
| Backing | base `WELL_SETUP`; view `DV_UNIT_WELL_SETUP` (`OBJECT_CODE`=Unit Agreement, `PERF_INTERVAL_CODE`=member) |
| DB oracle | count-delta on `DV_UNIT_WELL_SETUP.PERF_INTERVAL_CODE` |

### 2.2 Row DOM (from recon — NEW vs SAVED rows differ)
```
row cells: well_setup:form:T:{row}:C{col}...
  NEW (blank) row:   C0_da_input (start, CALENDAR), C1_da_input (end), C2_dd_input (Perf Interval)
  SAVED row:         C0_in       (start, TEXT),      C1_da_input (end), C2_dd_input,  C3_in, C4_in
Blank-row detection: row whose C2_dd_input value is empty.
RE-FIND the row after the dropdown selection — the grid can re-index.
Row SELECT (for delete) clicks the SAVED row's C0_in (text), NOT C0_da_input.
```

### 2.3 Test data (pre-flight verified 2026-06-27, read-only)
| Field | Value | Pre-flight fact |
|---|---|---|
| Unit Agreement (parent) | `Unit Agreement 3` (UNIT_3) | effective 2010-01-01 (open); 0 well-setup rows = clean target |
| Perf Interval (member) | `108_WB1-1_PF1` | effective 2003-01-01 (open); baseline 0 rows ANYWHERE |
| Form date / membership start | `2011-01-01` | inside both effective windows |

## 3. DEVELOPMENT — what it took (2026-06-27 session)
- Read-only pre-flight FIRST (effective windows + clean target + delta baseline) — picked a
  date inside both windows up front (the date-effective-parent lesson from Tract), so the
  navigator and insert both worked on live run #1.
- Live recon of the insert/delete gesture confirmed the Insert/Delete submenu label = "Well Setup"
  and the blank-row cells (C0 calendar / C2 Perf Interval dd).
- **Live run #1: TC01+TC02 PASS (insert persisted, DB +1), TC03 delete FAILED** — `Select Well
  Setup Row` clicked `C0_da_input`, but a SAVED row renders its start date as the TEXT cell
  `C0_in` (the calendar cell only exists on a NEW row). Same class of finding OLS recorded.
  Fix = click `C0_in` for the persisted-row select. The insert's leftover row was cleaned via a
  dedicated cleanup pass (DB 1 → 0) before re-running, so the sandbox was never left dirty.
- Count-delta oracle: the member starts at 0 rows anywhere, so the +1 / back-to-baseline deltas
  are unambiguous and pre-existing data in other agreements is irrelevant.

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| robocop lint | — | No issues found |
| RF dryrun | — | 3/3 PASS |
| RF live #1 | HEADED | TC01-02 PASS, TC03 FAIL (saved-row select-cell) → fixed |
| RF live #2 | HEADED | TC01-TC03 3/3 PASS, count-delta verified |
| Playwright reference | headless | see `evidence/unit_well_setup_results.json` |

## 5. DELIVERABLES
| Deliverable | Where |
|---|---|
| RF suite (maintained test) | `tests/Configuration/Assets/Royalty_Objects/unit_well_setup_iud.robot` |
| RF page object | `pageobjects/Configuration/Assets/Royalty_Objects/unit_well_setup_page.resource` |
| Playwright reference | `playwright/ec_iud_unit_well_setup.py` |
| Recon / pre-flight scripts | `investigation/` |
| Shared keywords reused (T2) | `Insert New Grid Row By Label`, `Find Grid Row By Cell Input Value`, `Delete Selected Grid Row` (`table_class.resource`); `View Count Where` (DbVerify) |
| Registry / scorecard | rows appended in `docs/ec_screen_registry.md` + `docs/automation-scorecard.md` |

## 6. LESSONS LEARNED
1. **NEW rows ≠ SAVED rows on inline grids** — the start-date cell is a calendar (`C0_da_input`)
   while editing a new row but a text cell (`C0_in`) once persisted; select the saved row by
   `C0_in`. (Cost one live run; the OLS bundle had already recorded this — re-confirmed here.)
2. **Pre-flight paid off again** — verifying the parent's effective window + a clean empty parent
   + a zero-baseline member up front made insert succeed on live run #1 (no Tract-style date repeats).
3. **Count-delta is the right oracle for membership tables** — robust to the member existing in
   other parents; here it was 0 everywhere, so the deltas are crisp.
4. **Self-clean is non-negotiable** — when TC03 failed mid-suite it left one row; a dedicated
   cleanup pass restored the sandbox to 0 before re-running and before any commit.
