# EC Screen IUD Operation Test — Equipment — Statement of Work (SOW)
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Task:** EC Equipment screen Insert/Update/Delete (IUD) Automation
**Author:** Choong-Yin Lee / Claude Opus 4.8
**Date:** 2026-06-06
**Version:** 1.0 — PLANNING (pre-execution)
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
*(to be completed during execution)*

| Run | Date | Result | Notes |
|---|---|---|---|
| — | — | pending | Phase 0 scan not yet run |

---

## 5. COMPLETION CRITERIA
| Deliverable | Status |
|---|---|
| Playwright script (`ec_iud_equipment.py`) | ☐ |
| Robot Framework suite (`ec_iud_equipment.robot`) | ☐ |
| DB verification scripts + findings | ☐ |
| Screenshots evidence | ☐ |
| SOW updated with final results + Lessons Learned | ☐ |
| `equipment-iud/` folder (README, requirements.txt, repo-relative paths) | ☐ |
| Committed + pushed | ☐ |

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
