# EC Screen IUD — Statement of Work: **Contract Area**
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Built by:** ec-object-iud-builder skill (autonomous run) — 2026-06-18
**Result:** ✅ COMPLETE — live **4/4 PASS**, DB-verified, self-cleaning (0 residue)

---

## 1. REQUIREMENT / METADATA (auto-derived from screen name)
| Property | Value | Source |
|---|---|---|
| Screen | **Contract Area** | input |
| Treeview path | **Configuration > Assets > Contract Objects > Contract Area** | tv-link `title=` (recon) |
| Class | `CONTRACT_AREA` | `class_property_cnfg.LABEL` |
| Class type | `OBJECT` ⇒ **OV (Manage-Object)** | `class_cnfg.CLASS_TYPE` |
| Time scope | `VERSIONED` ⇒ date-effective ⇒ **DELETE = End Date = Start Date** | `class_cnfg.TIME_SCOPE_CODE` |
| Base / version table | `CONTRACT_AREA` / `CONTRACT_AREA_VERSION` | `class_cnfg` |
| Verify view | `OV_CONTRACT_AREA` (29 seed rows) | resolver |
| App space | `EC_TRAN` | `class_cnfg` |
| Family | **OV-GM (Business-Unit-gated)** — sibling of Transport System / Nomination Point / Transport Zone | registry |

## 2. LIVE RECON (read-only scans)
**Navigator** — the grid stays empty until a Business Unit is chosen + GO:
| Element | Locator | Mandatory |
|---|---|---|
| Nav date | `nav:form:G:0:R:1:C:0:da_input` | optional |
| **Nav Business Unit** (dd) | `nav:form:G:0:R:1:C:1:dd` | **yes** |
| GO | `button:form:B` | — |
| Grid | `manageObject:form:T_data` (first column = Contract Area Code) | — |

**Insert — `objectForm` (New Object):**
| Field | Locator | Mandatory |
|---|---|---|
| Contract Area Code | `tab:tabPanel:objectForm:form:G:0:R:0:C:1:in` | **yes** |
| Contract Area Name | `tab:tabPanel:objectForm:form:G:0:R:1:C:1:in` | **yes** |
| Start Date | `tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input` | **yes** |
| End Date | `…R:3:C:1:da_input` | optional |
| Comments | `…R:4:C:1:in` | optional |
| **Business Unit Name** (dd) | `tab:tabPanel:objectForm:form:G:0:R:5:C:1:dd` | **yes** — must equal the nav BU or the row never appears in the filtered grid |
| Use as Property | `…R:6:C:1:cb` | optional |

**Update — `updateAttributes`:** Code `…R:0:C:1:in` (read-only), **Name `…R:1:C:1:in`** (edited).
**Delete — `objectdates`:** **End Date `…G:0:R:0:C:3:da_input`** ← set = Start Date ⇒ true delete from `OV_CONTRACT_AREA`.

**Scope chosen:** Business Unit **ECP Norway** (`ECP_NO`, 5 existing areas — most populated). Date `2003-01-01` (ref-dd screen, must post-date seed Business Units).

## 3. IUD DESIGN (clone of Transport System OV-GM pattern)
```
SETUP : open screen → Select EC Dropdown Option nav BU = ECP Norway → Apply Navigator (GO)
INSERT: New Object → Code/Name/Start Date + Business Unit Name = ECP Norway → Save → GO
UPDATE: select row by code → updateAttributes Name → Save → GO
DELETE: select row → objectdates End Date = Start Date → Save → GO (+1 extra GO; GM grid redraws lazily)
```
Test data: unique `AUTOTEST_CA_<YYYYMMDDHHMMSS>` per run (OV codes linger after delete — never reused). The referenced Business Unit is **read-only seed**; existing rows are never touched.

## 4. ISSUE FOUND & FIXED (this build)
**OV-GM grid redraws lazily after Save+GO.** First live run: insert *persisted* (update + delete + DB confirmed it) but `Row Should Exist` (T1, an *instant* DOM read) ran before the row rendered → false FAIL on TC02. TC03's `Click` auto-waited, so it found the row — masking the timing.
**Fix:** T3 `Contract Area Row Should Exist` now `Wait For Elements State … visible 20s` on the row span *before* the instant first-cell assertion. Screen-specific knowledge kept in T3; no shared-file change. Re-run → **4/4 PASS**.

## 5. EVIDENCE (DB ground truth)
- **RF live (headed):** `tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot` — **4/4 PASS** (`results/ca_live2/`).
  - TC02 in-suite assert: `Code Should Be Present In View    ov_contract_area    ${code}` → PASS
  - TC04 in-suite assert: `Code Should Be Absent In View     ov_contract_area    ${code}` → PASS
- **Playwright bundle:** `playwright/ec_iud_contract_area.py` — ALL PASS (`evidence/` 9 screenshots + result JSON).
- **Independent DB re-read:** `OV_CONTRACT_AREA` AUTOTEST residue = **0** (self-clean confirmed, twice).

## 6. DELIVERABLES
| Deliverable | Path |
|---|---|
| T3 page object | `pageobjects/Configuration/Assets/Contract_Objects/contract_area_page.resource` |
| RF suite | `tests/Configuration/Assets/Contract_Objects/contract_area_iud.robot` |
| Playwright bundle | `screens/Configuration/Assets/Contract_Objects/Contract_Area/playwright/ec_iud_contract_area.py` |
| Recon scripts | `…/Contract_Area/investigation/` (db / live / bu_distribution / treeview_path / grid_columns) |
| Evidence | `…/Contract_Area/evidence/` + `results/ca_live2/` |
| Reuse | T2 `manage_object.resource` + T1 `common`/`table`/`navigator` (no shared-file changes) |
