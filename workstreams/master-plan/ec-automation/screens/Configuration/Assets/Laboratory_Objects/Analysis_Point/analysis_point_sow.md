# EC Screen IUD — Statement of Work: **Analysis Point**
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Built by:** ec-object-iud-builder skill (autonomous run) — 2026-06-19
**Result:** ✅ COMPLETE — live **4/4 PASS**, DB-verified, self-cleaning (0 residue)

---

## 1. METADATA
| Property | Value | Source |
|---|---|---|
| Screen | **Analysis Point** | input |
| Treeview path | **Configuration > Assets > Laboratory Objects > Analysis Point** | tv-link `title=` (scan) |
| Class | `ANALYSIS_POINT` | `class_property_cnfg.LABEL` |
| Class type | `OBJECT` ⇒ **OV** | `class_cnfg.CLASS_TYPE` |
| Time scope | `VERSIONED` ⇒ date-effective ⇒ **DELETE = End Date = Start Date** | `class_cnfg.TIME_SCOPE_CODE` |
| Base / version table | `ANALYSIS_POINT` / `ANALYSIS_POINT_VERSION` | `class_cnfg` |
| Verify view | `OV_ANALYSIS_POINT` | resolver |
| App space | `EC_CHEM` (laboratory) | `class_cnfg` |
| Family | **OV-GM (groupmodel, 3-level cascade)** — like Field/Sub Area; Op-parent is settable in the form (NOT a Pipeline-style parked screen) | recon |

## 2. LIVE RECON
- **Toolbar:** New + Delete enabled.
- **Navigator (gated):** Date `nav:form:G:0:R:1:C:0:da_input` (optional) + **PU `…C:1:dd` → Area `…C:2:dd` → Facility Class 1 `…C:3:dd`** (all mandatory, multi-column single group) + GO `button:form:B`. The 3 dds sit at C:1/C:2/C:3 (not C:0), so the suite drives them with `Select EC Dropdown Option` (not `Set Navigator Filter`).
- **Grid:** `manageObject:form:T_data` (6 existing rows under the P1 scope).
- **Insert `objectForm`** (mandatory = yellow): Start Date **R:0** · End Date R:1 · **Analysis Point Code R:2** · **Analysis Point Name R:3** · **Analysis Point Type R:4 (dd)** · Purpose R:5 · … · **Op Production Unit R:10 / Op Area R:11 / Op Facility Class 1 R:12 (dds)** · Cp* / Geo* R:13–18. The Op PU/Area/Facility dds are the **groupmodel link** — set = nav scope or the row never lists in the filtered grid (even though they're not yellow).
- **Update `updateAttributes`:** Code R:0 · **Name R:1** (edited) · Type R:2 · … Op PU/Area/Facility R:8–10.
- **Delete `objectdates`:** **End Date `…G:0:R:0:C:3:da_input`** = Start Date ⇒ true delete from `OV_ANALYSIS_POINT`.

**Scope:** P1 Production Unit → P1 Area → P1 Facility 1 (codes P1_PU/P1_AREA/P1_FCTY_1). Start/End date `2003-01-01` (`TEST_START_DATE_REFDD` — ref dds). Type dd = first option.

## 3. IUD DESIGN (OV-GM 3-level cascade, clone of Field/Sub Area extended)
```
SETUP : open → Select EC Dropdown Option PU/Area/Facility cascade → Apply Navigator (GO)
INSERT: New Object → Code/Name/Start Date + Type (first) + Op PU/Area/Facility = nav scope → Save → GO
UPDATE: select row → updateAttributes Name → Save → GO
DELETE: select row → objectdates End Date = Start Date → Save → GO (+1 extra GO; GM grid redraws lazily, R17)
```
Test data: unique `AUTOTEST_AP_<YYYYMMDDHHMMSS>` per run. Referenced PU/Area/Facility + Type are read-only seed.

## 4. EVIDENCE (DB ground truth)
- **RF live (headed):** `tests/Configuration/Assets/Laboratory_Objects/analysis_point_iud.robot` — **4/4 PASS** (`results/ap_live/`).
  - TC02: `Code Should Be Present In View    ov_analysis_point    ${code}` → PASS
  - TC04: `Code Should Be Absent In View     ov_analysis_point    ${code}` → PASS
- **Playwright bundle:** `playwright/ec_iud_analysis_point.py` — ALL PASS (`evidence/` 8 shots + JSON).
- **Independent DB re-read:** `OV_ANALYSIS_POINT` AUTOTEST residue = **0** (twice). R16 hygiene guard = PASS.
- **OV-GM lazy redraw handled** via the T3 `Row Should Exist` wait (R17). Passed live first try.

## 5. DELIVERABLES & REUSE
| Deliverable | Path |
|---|---|
| T3 page object | `pageobjects/Configuration/Assets/Laboratory_Objects/analysis_point_page.resource` |
| RF suite | `tests/Configuration/Assets/Laboratory_Objects/analysis_point_iud.robot` |
| Playwright bundle | `screens/Configuration/Assets/Laboratory_Objects/Analysis_Point/playwright/ec_iud_analysis_point.py` |
| Recon scripts | `…/Analysis_Point/investigation/` (db_recon / scope / live / residue) |
| Evidence | `…/Analysis_Point/evidence/` + `results/ap_live/` |
| Reuse | T2 `manage_object.resource` + T1 `common`/`table` (`Select EC Dropdown Option`, `Select First EC Dropdown Option`) — **no shared-file changes** |
