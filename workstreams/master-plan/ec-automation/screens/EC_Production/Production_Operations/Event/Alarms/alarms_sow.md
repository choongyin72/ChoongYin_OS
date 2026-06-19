# EC Screen IUD — Statement of Work: **Alarms** (NEW pattern: EVENT-LOG)
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Built by:** ec-object-iud-builder skill (autonomous run) — 2026-06-19
**Result:** ✅ COMPLETE — live **4/4 PASS**, DB-verified by REASON marker, self-cleaning (0 residue)

---

## 1. METADATA
| Property | Value | Source |
|---|---|---|
| Screen | **Alarms** | input |
| Treeview path | **EC Production > Production Operations > Event > Alarms** | tv-link `title=` (live scan) |
| Class | `ALARMS` | `class_property_cnfg.LABEL` |
| Class type | **`DATA`** (time-scope `DAY`) ⇒ **EVENT-LOG (NOT OV/TV master-data)** | `class_cnfg` |
| Base table | `FCTY_DAY_ALARM` (facility-day; key OBJECT_ID + DAYTIME + ALARM_NO) | `class_cnfg` |
| Verify view | `DV_ALARMS` (has a **REASON** VARCHAR2 column) | DB recon |
| App space | `EC_PROD` | `class_cnfg` |
| Family | **EVENT-LOG (NEW)** — gated inline grid; add alarm rows per facility-day; physical delete; no object code | recon |

## 2. PATTERN — why this is new
The "Alarms" screen is a **DATA/DAY** class (not OBJECT/TABLE), rendered as a **gated inline grid**: the
PU → Area → Facility-Class-1 cascade navigator (+ Date) **+ GO** must be applied before the grid loads,
then you **ADD alarm rows** (TV-style cells). It is the **PC/Object-List-Setup shape** (gated inline grid,
insert/delete-by-label, count-delta oracle) applied to **production event data**, with one twist: **there
is no object code** — rows are identified by a unique **REASON marker**, and the DB oracle counts
`DV_ALARMS` by that marker.

## 3. LIVE RECON
- **Toolbar:** New + Delete enabled (submenu item = **"Alarms"** under both Insert and Delete parents).
- **Navigator:** Date `nav:form:G:0…da_input` + **PU (G:1) → Area (G:2) → Facility Class 1 (G:3)** cascade dds (at `…:R:1:C:0:dd`, so `Set Navigator Filter` works) + GO `button:form:B`. All gate the grid.
- **Grid:** `alarms:form:T_data`. Headers: Time [hh:mm] · Area · Type of Alarm · Reason · Report · Duration.
- **Insert row cells** (only Type of Alarm is mandatory/yellow):
  | Col | Field | Cell | Kind | Mandatory |
  |---|---|---|---|---|
  | C0 | Time [hh:mm] | `…T:{r}:C0_da_input` | time | no |
  | C1 | Area | `…C1_dd` | dropdown | no |
  | **C2** | **Type of Alarm** | `…C2_dd` | dropdown | **YES** |
  | C3 | Reason | `…C3_in` | text | no — **used as the unique marker / oracle key** |
  | C4 | Report | `…C4_cb` | checkbox | no |
  | C5 | Duration | `…C5_in` | text | no |

**Scope:** Date `2026-06-18` (pinned data-bearing facility-day, like the N1 screens) · P1 Production Unit → P1 Area → P1 Facility 1.

## 4. IUD DESIGN (gated inline-grid event log, marker oracle)
```
SETUP : open Alarms → Date + PU/Area/Facility cascade → GO (grid empty until applied)
INSERT: Insert→"Alarms" → blank row → Type of Alarm (mandatory dd, first option) → Reason = AUTOTEST_ALARM_<ts> → Save → GO
UPDATE: find row by Reason marker → change Reason to <ts>_UPD → Save → GO   (a Reason-change = DB-verifiable update)
DELETE: select row by Reason marker → Delete→"Alarms" → Save → GO   (PHYSICAL)
```
DB oracle (all three ops): `View Count Where Should Be    DV_ALARMS    REASON    <marker>    <n>` — the marker is unique per run, so it's exactly the test alarm (count-delta safe). Self-clean = the delete; 0 residual verified in DV_ALARMS **and** FCTY_DAY_ALARM.

## 5. EVIDENCE (DB ground truth)
- **RF live (headed):** `tests/EC_Production/Production_Operations/Event/alarms_iud.robot` — **4/4 PASS** (`results/alarms_live/`).
  - TC02 insert: `View Count Where Should Be DV_ALARMS REASON <M0> 1` → PASS
  - TC03 update: `… REASON <M0_UPD> 1` AND `… REASON <M0> 0` → PASS
  - TC04 delete: `… REASON <M0_UPD> 0` → PASS
- **Playwright bundle:** `playwright/ec_iud_alarms.py` — ALL PASS (`evidence/` 7 shots + JSON).
- **Independent DB re-read:** `DV_ALARMS` + `FCTY_DAY_ALARM` AUTOTEST_ALARM residue = **0** (twice). R16 hygiene guard = PASS.
- **Note:** passed live first try.

## 6. DELIVERABLES & REUSE
| Deliverable | Path |
|---|---|
| T3 page object | `pageobjects/EC_Production/Production_Operations/Event/alarms_page.resource` |
| RF suite | `tests/EC_Production/Production_Operations/Event/alarms_iud.robot` |
| Playwright bundle | `screens/EC_Production/Production_Operations/Event/Alarms/playwright/ec_iud_alarms.py` |
| Recon scripts | `…/Alarms/investigation/` (find_alarm_screens / recon_alarms_row / alarms_db_recon / alarms_residue) |
| Evidence | `…/Alarms/evidence/` + `results/alarms_live/` |
| Reuse | T2 `table_class.resource` (Insert/Find/Delete grid row) + T1 `navigator`/`table` + DbVerify `View Count Where` — **no shared-file changes** |
