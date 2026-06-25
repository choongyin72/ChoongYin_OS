# EC Screen IUD — Statement of Work: **Carrier**
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Built by:** ec-object-iud-builder skill (autonomous run) — 2026-06-19
**Result:** ✅ COMPLETE — live **4/4 PASS**, DB-verified, self-cleaning (0 residue)

---

## 1. METADATA (auto-derived from screen name)
| Property | Value | Source |
|---|---|---|
| Screen | **Carrier** | input |
| Treeview path | **Configuration > Assets > Cargo Objects > Carrier** | tv-link `title=` (live scan) |
| Class | `CARRIER` | `class_property_cnfg.LABEL` |
| Class type | `OBJECT` ⇒ **OV (Manage-Object)** | `class_cnfg.CLASS_TYPE` |
| Time scope | `VERSIONED` ⇒ date-effective ⇒ **DELETE = End Date = Start Date** | `class_cnfg.TIME_SCOPE_CODE` |
| Base / version table | `CARRIER` / `CARRIER_VERSION` | `class_cnfg` |
| Verify view | `OV_CARRIER` | resolver |
| App space | `EC_PROD` | `class_cnfg` |
| Family | **OV (plain manage-object, Bank-family grid)** — NOT gated. Resolver candidate-family hint + live scan confirmed no mandatory nav dropdown. | registry JSON + scan |

## 2. LIVE RECON (read-only scan)
- **Toolbar:** New + Delete enabled.
- **Navigator:** one field — a date (`nav:form:G:0:R:1:C:0:da_input`, **optional**) + GO `button:form:B`. Not gated → grid loads without a mandatory dropdown; **no OV-GM lazy-redraw risk**.
- **Grid:** `manage_object_nav_nav:form:T_data` (Bank-family — first column = Carrier Code; `Row Should Exist` works directly).

**Insert — `objectForm` (New Object):** (30 fields total; mandatory = yellow)
| Field | Locator | Mandatory |
|---|---|---|
| Carrier Code | `objectForm…R:0:C:1:in` | **yes** |
| Carrier Name | `objectForm…R:1:C:1:in` | **yes** |
| Carrier Group (dd) / Carrier Type | R:2 / R:3 | optional |
| **Start Date** | `objectForm…R:4:C:1:da_input` | **yes** (note: R:4, not R:2 — Group/Type precede it) |
| End Date | R:5 | optional |
| **Unit** (dd) | `objectForm…R:9:C:1:dd` | **yes** — reference dd; first option used for the throwaway record |
| Capacity Volume/Mass, Dead Weight, Nationality, Rating, Product Group, Speed, … | R:6–R:29 | optional |

**Update — `updateAttributes`:** Code R:0 (read-only), **Name R:1** (edited).
**Delete — `objectdates`:** **End Date `…G:0:R:0:C:3:da_input`** ← set = Start Date ⇒ true delete from `OV_CARRIER`.

**Scope:** Start/End date `2003-01-01` (`TEST_START_DATE_REFDD` — the screen has reference dds; date must post-date seed reference objects).

## 3. IUD DESIGN (Bank_Account-style: plain OV + mandatory ref dd)
```
SETUP : launch + login + open Carrier (grid loads; no gating)
INSERT: New Object → Code/Name/Start Date + Unit dd (first option) → Save → GO
UPDATE: select row by code → updateAttributes Name → Save → GO
DELETE: select row → objectdates End Date = Start Date → Save → GO
```
Test data: unique `AUTOTEST_CARR_<YYYYMMDDHHMMSS>` per run (OV codes linger after delete — never reused). Referenced **Unit** is read-only seed; existing rows never touched.

## 4. EVIDENCE (DB ground truth)
- **RF live (headed):** `tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot` — **4/4 PASS** (`results/carrier_live/`).
  - TC02 in-suite assert: `Code Should Be Present In View    OV_CARRIER    ${code}` → PASS
  - TC04 in-suite assert: `Code Should Be Absent In View     OV_CARRIER    ${code}` → PASS
- **Playwright bundle:** `playwright/ec_iud_carrier.py` — ALL PASS (`evidence/` 9 screenshots + result JSON).
- **Independent DB re-read:** `OV_CARRIER` AUTOTEST residue = **0** (self-clean confirmed, twice).
- **R16 hygiene guard:** PASS (bundle reads creds from env).
- **Note:** passed live first try — being a plain OV (Bank grid), there was no OV-GM lazy-redraw false-fail.

## 5. DELIVERABLES
| Deliverable | Path |
|---|---|
| T3 page object | `pageobjects/Configuration/Assets/Cargo_Objects/carrier_page.resource` |
| RF suite | `tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot` |
| Playwright bundle | `screens/Configuration/Assets/Cargo_Objects/Carrier/playwright/ec_iud_carrier.py` |
| Recon scripts | `…/Carrier/investigation/` (resolve / scan / residue) |
| Evidence | `…/Carrier/evidence/` + `results/carrier_live/` |
| Reuse | T2 `manage_object.resource` + T1 `common`/`table` (`Select First EC Dropdown Option`) — **no shared-file changes** |
