# EC Screen IUD Operation Test — Statement of Work (SOW)
**Project:** EC Web App System Test (local sandbox)
**Task:** EC Screen Insert/Update/Delete (membership IUD) Automation — Tract - Well Setup
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-27
**Version:** 1.0 — COMPLETE (RF suite + Playwright reference, live 4/4 + DB-verified)

---

## 1. REQUIREMENT
Automate adding, updating and removing a WELL SETUP membership row (links a Perf Interval to
an existing **Tract**) and prove it at DB level. Constraints: NEVER modify existing data — the
Perf Interval is only referenced; the membership row is created, updated and physically deleted
again; the parent Tract is an EXISTING object and its other rows (P1 PI-5 / P1 PI-6) are untouched.

| Operation | Pass condition | Status |
|---|---|---|
| INSERT membership | row in grid AND `DV_TRACT_WELL_SETUP` count = baseline+1 | PASS |
| UPDATE membership | edit COMMENTS (`C3_in`) -> sentinel present in `DV_TRACT_WELL_SETUP` | PASS |
| DELETE membership | row gone AND count back to baseline (sentinel gone) | PASS |
| CLEANUP | zero leftover rows; existing P1 PI-5/PI-6 intact | PASS |

## 2. DESIGN

### 2.1 Screen classification — PC pattern (parent-child setup), Tract sibling of Unit - Well Setup
| Property | Value |
|---|---|
| Treeview path | Configuration > Assets > Royalty Objects > Tract - Well Setup |
| Navigator (mandatory, CASCADE) | Form date (G:0) + **Unit Agreement (G:1)** + **Tract (G:2)** + GO (`button:form:B`) |
| Member grid | `well_setup:form:T_data` (inline TV-style cells) |
| Toolbar | Insert > "Well Setup" / Delete > "Well Setup" (both submenus) |
| Membership delete semantics | PHYSICAL row delete |
| Backing | base `WELL_SETUP` (shared with Unit - Well Setup); view `DV_TRACT_WELL_SETUP` (`OBJECT_CODE`=Tract, `PERF_INTERVAL_CODE`=member) |
| DB oracle | count-delta on `DV_TRACT_WELL_SETUP.PERF_INTERVAL_CODE`; COMMENTS present-in-view for UPDATE |

### 2.2 Navigator CASCADE (the one real difference vs Unit - Well Setup)
```
G:0 da_input  form date
G:1 dd        Unit Agreement   <- pick FIRST
G:2 dd        Tract            <- only POPULATES after a Unit Agreement is chosen
              (e.g. Unit Agreement 3 -> 'Unit 3 Tract 01' / 'Unit 3 Tract 02')
GO  button:form:B
```
Row DOM identical to Unit - Well Setup: NEW row start = calendar `C0_da_input`; SAVED row start =
text `C0_in` (select saved row for delete by `C0_in`). `C3_in`=COMMENTS, `C4_in`=SORT_ORDER, both
appear only after save.

### 2.3 Test data (pre-flight verified 2026-06-27, read-only)
| Field | Value | Pre-flight fact |
|---|---|---|
| Unit Agreement (G:1) | `Unit Agreement 3` | gates the Tract dd |
| Tract (parent, G:2) | `Unit 3 Tract 01` (TRACT_U3_T01) | existing object, effective 2010-01-01; has P1 PI-5/PI-6 |
| Perf Interval (member) | `108_WB1-1_PF1` | effective 2003-01-01; baseline 0 in ANY tract |
| Form date / membership start | `2011-01-01` | inside both effective windows |

## 3. DEVELOPMENT — what it took (2026-06-27 session)
- Built as a clone of the just-finished **Unit - Well Setup (RC.0050)** bundle, with the RC.0050
  lessons applied up front: full **I-U-D** scope from the start, saved-row select by `C0_in`,
  `C3_in`=COMMENTS update verified via present-in-view, pre-flight before live run #1.
- **Recon caught the one real difference:** the navigator is a CASCADE (Unit Agreement -> Tract),
  not a single dd. The Tract dd (G:2) is empty until a Unit Agreement is picked; my first recon
  pass mis-set the agreement and never reached a Tract, so the well-setup grid never loaded —
  re-ran with the correct cascade (Unit Agreement 3 -> Unit 3 Tract 01). No live test run wasted.
- **No empty Tract exists** (all 4 have rows), so the test inserts a baseline-0 member under an
  existing Tract and touches only its own row — count-delta + selecting by the unique member code
  keep the existing P1 PI-5/PI-6 rows safe.
- Result: **live 4/4 on the first test run** — the RC.0050 lessons removed the repeats.

## 4. TEST EXECUTION
| Run | Mode | Result |
|---|---|---|
| robocop lint | — | No issues found |
| RF dryrun | — | 4/4 PASS |
| RF live (full I-U-D) | HEADED | **TC01-TC04 4/4 PASS**, count-delta + COMMENTS verified, first run |
| Playwright reference | headless | INSERT+UPDATE+DELETE — see `evidence/tract_well_setup_results.json` |
| Independent DB re-read | — | TRACT_U3_T01 = P1 PI-5/PI-6 only; member 0; sentinel 0 |

## 5. DELIVERABLES
| Deliverable | Where |
|---|---|
| RF suite | `tests/Configuration/Assets/Royalty_Objects/tract_well_setup_iud.robot` |
| RF page object | `pageobjects/Configuration/Assets/Royalty_Objects/tract_well_setup_page.resource` |
| Playwright reference | `playwright/ec_iud_tract_well_setup.py` |
| Recon / pre-flight scripts | `investigation/` |
| Shared keywords reused (T2) | `Insert New Grid Row By Label`, `Find Grid Row By Cell Input Value`, `Delete Selected Grid Row`, `Type Cell By Id`; `View Count Where` + `Code Should Be Present/Absent In View` (DbVerify) |
| Registry / scorecard | rows appended |

## 6. LESSONS LEARNED
1. **Recon the navigator shape before building** — a sibling screen can gate differently (here a
   Unit Agreement -> Tract CASCADE vs Unit - Well Setup's single Unit Agreement dd).
2. **Lessons from the previous screen pay off** — full I-U-D scope, `C0_in` saved-row select, and
   pre-flight were all applied from the start, giving live 4/4 on the first run (vs RC.0050's
   one wasted run on the saved-row cell).
3. **Count-delta + unique-member select protect existing data** — with no empty parent available,
   inserting a baseline-0 member and selecting only by that member code left P1 PI-5/PI-6 untouched.
