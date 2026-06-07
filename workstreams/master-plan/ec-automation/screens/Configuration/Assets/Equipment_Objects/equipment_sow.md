# EC Screen IUD Operation Test — Equipment — Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Task:** EC Equipment screen Insert/Update/Delete (IUD) Automation
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-06
**Version:** 2.0 — COMPLETE (all IUD ops DB-verified in OV_EQPM)
**Pattern:** Manage Object — **screen 2 of 2** (confirms/generalises the Bank pattern)

---

## 1. REQUIREMENT

### 1.1 Objective
Automate Insert, Update, Delete (IUD) on the EC **Equipment** screen to:
1. Validate creation, modification, and deletion of equipment records
2. Confirm whether the **Manage Object** pattern learned from Bank generalises to a second screen
3. Learn the new variation: a **multi-field cascading navigator** + a toolbar **− (delete) button**

### 1.2 Scope
**In scope:** Equipment screen (production data / asset configuration), full IUD lifecycle, both
Playwright and Robot Framework implementations, DB-level verification.
**Out of scope:** other Manage Object screens (Company, Well, Facility) — separate tasks.

### 1.3 Constraints
- **NEVER touch existing data** — specifically `OFF_FLASH_GAS_CC`, `OFF_GINJ_COMP_A`, `OFF_GINJ_COMP_B`
- All test data prefixed `AUTOTEST_EQP_` (fresh incrementing code per run)
- Target: local EC sandbox `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (user `sysadmin`)
- DB verification: `localhost:1521/ORCL` (`ECKERNEL_EC` / `energy`)

### 1.4 Acceptance Criteria
| Operation | Pass Condition |
|---|---|
| INSERT | New `AUTOTEST_EQP_*` row appears in the filtered equipment list after save |
| UPDATE | Equipment Name changed and persisted after save |
| DELETE | Record removed/expired (method TBD — see §3.3); **confirmed at DB level** |
| INTEGRITY | The 3 existing equipment records remain untouched |

---

## 2. DESIGN

### 2.1 Screen type
Equipment is a **Manage Object** screen (EC14+) — same family as Bank: `NEW VERSION` tab,
Start/End Date, object form (left) + version list (right). The Bank IUD patterns are the
working hypothesis; this task's purpose is to **confirm what generalises vs what was Bank-specific**.

### 2.2 KEY DIFFERENCE vs Bank — the cascading navigator
Bank had a single Date navigator + Go button. Equipment has a **5-field navigator** that must be
set (in order, likely cascading) before the equipment list loads, then a green **▶ arrow** applies:

| Field | Value (per provided screenshot) |
|---|---|
| Date | `2026-06-05` |
| Production Unit | `Production Unit` |
| Area | `Offshore area` |
| Facility Class 1 | `Offshore facility` |
| Equipment Type | `Compressor` |
| (apply) | green **▶** arrow button |

These are PrimeFaces dropdowns; each selection may trigger an AJAX reload that filters the next
dropdown's options. **Must be handled in order with waits** (resolved in Phase 0 scan).

### 2.3 IUD pattern (hypothesis — to confirm in Phase 0)
```
INSERT:  Set navigator (5 filters) → ▶ → Insert (+ toolbar / New Object)
         → objectForm: Equipment Type (likely auto = Compressor, read-only),
           Equipment Code, Equipment Name, Start Date → Save
UPDATE:  Click equipment row → updateAttributes form → edit Equipment Name → Save
DELETE:  Try the − (minus) toolbar button first (NEW — Bank lacked this).
         If disabled / only soft-deletes → fall back to End Date = Start Date.
         Verify the TRUE effect at the DB either way.
```

### 2.4 Test data
| Field | Value |
|---|---|
| Equipment Code | `AUTOTEST_EQP_001` (fresh incrementing code each run) |
| Equipment Name (Insert) | `AUTOTEST Equipment 001` |
| Equipment Name (Update) | `AUTOTEST Equipment 001 UPDATED` |
| Equipment Type | `Compressor` (from navigator filter) |
| Start Date | `2000-01-01` |
| End Date (delete fallback) | `2000-01-01` (= Start Date → true delete, Bank-proven) |

### 2.5 Technology stack
Playwright (Python sync) + Robot Framework (Browser library) + oracledb (DB verify) — identical
to the Bank deliverable. Paths resolved relative to repo root; env-overridable.

---

## 3. DEVELOPMENT PLAN

### 3.1 Phases
| Phase | Activity | Output |
|---|---|---|
| 0 | **Deep-dive DOM scan** — navigator dropdown IDs, ▶ arrow ID, objectForm / updateAttributes / objectdates field IDs, − button behaviour | element-ID map |
| 1 | Build + run Insert → Update → Delete (Playwright) | `ec_iud_equipment.py` |
| 2 | DB verification (find real object view, confirm each op + delete semantics) | DB scripts + findings |
| 3 | Robot Framework suite | `ec_iud_equipment.robot` |
| 4 | Folder, requirements.txt, README, commit | `equipment-iud/` |

### 3.2 Unknowns to resolve in Phase 0 (not guessed)
- Exact navigator dropdown element IDs + whether they cascade (and in what order)
- The ▶ apply-button element ID
- objectForm / updateAttributes / objectdates field IDs for Equipment
- Whether Equipment Type is auto-set from the navigator (appears read-only "Compressor")
- Mandatory-field set (expected: Equipment Code, Name, Start Date)
- **What the − toolbar button actually does** (physical delete vs end-dating)
- The Equipment object-view name for DB verification (hypothesis: `ov_equipment`)

### 3.3 Delete approach (decided)
Per task decision: **try the − toolbar button first**; fall back to **End Date = Start Date** if it
is disabled or only soft-deletes. DB query confirms whether the row is physically removed.

---

## 4. TEST EXECUTION

### 4.1 Phase 0 — DOM scan findings
- Navigator = 5 `ui-autocomplete-dd` dropdowns (`nav:form:G:0..4`). **All empty on load** — the
  screenshot values are selections, not defaults. Driven via **`…:dd_button` chevron → click exact
  option in `…:dd_panel`** (typing fires re-render AJAX and drops characters — 5 nav iterations to learn this).
- Result table id = **`manageObject:form:T_data`** (NOT Bank's `manage_object_nav_nav`).
- Equipment Type is **read-only, auto-set from the navigator** (= Compressor). Mandatory editable: Code, Name, Start Date.
- Toolbar `−` button parent `<li>` has `ui-submenu-state-disabled` → **delete = End Date = Start Date** (same as Bank).
- Object view = **`OV_EQPM`** (found by probing 585 OV_ views for `OFF_FLASH_GAS_COMP`).

### 4.2 Test runs
| Run | Tool | Code | Result |
|---|---|---|---|
| 1 | Playwright | AUTOTEST_EQP_001 | full IUD — **ALL PASS** (2 iterations: nav crack + `.trim()` typo) |
| 2 | Playwright (skip-delete) | AUTOTEST_EQP_002 | insert+update — PASS |
| 3 | Playwright (delete-only) | AUTOTEST_EQP_002 | delete — PASS |
| 4 | Robot Framework | AUTOTEST_EQP_003 | 4/4 tests PASS |

### 4.3 DB verification (OV_EQPM, localhost:1521/ORCL)
| Check | Operation | DB result |
|---|---|---|
| 1 | EQP_001 full IUD | **gone** — true delete |
| 2 | EQP_002 insert+update | **present, name "AUTOTEST Equipment 002 UPDATED"** (rows 238→239) |
| 3 | EQP_002 delete | **gone** (239→238) |
| 4 | EQP_003 (RF run) | **gone** |
| — | 17 `OFF_` equipment | **all untouched** (`end=None`) |

All three operations proven at the DB level — not just the green UI.

---

## 5. COMPLETION CRITERIA
| Deliverable | Status |
|---|---|
| Playwright script (`ec_iud_equipment.py`) | ✅ ALL PASS |
| Robot Framework suite (`ec_iud_equipment.robot`) | ✅ 4/4 PASS |
| DB verification scripts + findings | ✅ OV_EQPM, all ops verified |
| Screenshots evidence | ✅ `docs/EC/screenshots/iud_equipment/` |
| SOW updated with final results + Lessons Learned | ✅ this doc (v2.0) |
| `equipment-iud/` folder (README, requirements.txt, repo-relative paths) | ✅ |
| Committed + pushed | ☐ (in progress) |

## 8. LESSONS LEARNED
1. **The Manage Object pattern generalised from Bank** — objectForm (insert) / updateAttributes
   (update) / objectdates (delete), End=Start true-delete, disabled `−` button. Screen 2 confirmed
   the pattern is real, not Bank-specific. Took **2 build iterations** vs Bank's 6.
2. **The new variable was the cascading navigator** — `ui-autocomplete-dd` fields must be driven by
   clicking the `dd_button` chevron and selecting the exact `dd_panel` option. **Typing is unreliable**
   (each keystroke fires re-render AJAX that drops characters — "pressor" residue). This cost 5 scan
   iterations; now captured as a reusable technique.
3. **Object view names are not "ov_<screen>"** — Equipment is `OV_EQPM`, not `ov_equipment`. Find the
   real view by probing OV_ views for a known code rather than guessing.
4. **Exact filter values matter** — "Production Unit" ≠ "Production Unit 1"; both are valid configured
   values. I wrongly substituted "Production Unit 1" and was corrected — always confirm exact spec values.
5. **DB verification remains essential** — used skip-delete / delete-only modes to prove insert+update
   persist *before* deleting, so each op is independently confirmed in OV_EQPM.

---

## 6. RISKS
| Risk | Likelihood | Mitigation |
|---|---|---|
| Cascading navigator dropdowns hard to drive (AJAX/order) | Medium | Phase 0 scan; set in order with networkidle waits; PrimeFaces type/click patterns |
| − button behaves unexpectedly | Medium | Fallback to End=Start (Bank-proven); DB-verify either way |
| Equipment object-view name differs from `ov_equipment` | Low | Query `all_views` / EC catalog to find it |
| Duplicate code rejected on re-run | Medium | Fresh `AUTOTEST_EQP_*` code each run |
| Accidentally touching existing equipment | Low (high impact) | Hard guard: only operate on `AUTOTEST_EQP_*`; verify clean state first |

---

## 7. CONFIDENCE (pre-execution, honest)
- Insert / Update: **~90%** (Manage Object pattern owned from Bank)
- Cascading navigator: **~65%** (new; main wildcard)
- Delete via − button: **unknown until scanned**; outcome safe via End=Start fallback
- DB verify: **~90%**
- **Overall ~80%** to full ALL-PASS + DB-verified. Escalate to user if it reaches ~8 build iterations.
