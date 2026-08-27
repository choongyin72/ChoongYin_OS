# EC Screen IUD — Statement of Work: **Carrier**
**Project:** Woodside Pluto ECaaS — EC Web App System Test
**Built by:** ec-object-iud-builder skill (autonomous run) — 2026-06-19
**Converted:** `ec-bank-pattern-converter` skill, PR #477 ("feat(ec-automation): convert Carrier to
full Bank pattern (Batch 11)"), merged 2026-08-23
**Result:** ✅ COMPLETE — live **5/5 PASS** (post-conversion RF suite: TC01 clean-state / TC02
insert / TC03 update / TC04 find / TC05 delete), DB-verified, self-cleaning (0 residue)
**Backfill note:** sections 1-5 below describe the ORIGINAL 2026-06-19 build (class/view/family
metadata is still accurate — the underlying screen classification did not change). Section 6 below
covers the Batch 11 Bank-pattern conversion that rebuilt the RF layer. This SOW's missing
documentation/evidence artifacts (JOURNAL, CHECKLIST, KB map, README refresh) were backfilled
2026-08-28 per `docs/lean-deliverable-backfill-workorder.md` (Batch 11), after the owner's
2026-08-27 decision retired the lean waiver that had let Bank-pattern conversions skip them.

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

## 5. DELIVERABLES (original 2026-06-19 build)
| Deliverable | Path |
|---|---|
| T3 page object | `pageobjects/Configuration/Assets/Cargo_Objects/carrier_page.resource` |
| RF suite | `tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot` |
| Playwright bundle | `screens/Configuration/Assets/Cargo_Objects/Carrier/playwright/ec_iud_carrier.py` |
| Recon scripts | `…/Carrier/investigation/` (resolve / scan / residue) |
| Evidence | `…/Carrier/evidence/` + `results/carrier_live/` |
| Reuse | T2 `manage_object.resource` + T1 `common`/`table` (`Select First EC Dropdown Option`) — **no shared-file changes** |

## 6. BANK-PATTERN CONVERSION (PR #477, Batch 11, merged 2026-08-23)

**What changed:** the RF T3 (`carrier_page.resource`) and suite (`carrier_iud.robot`) were rebuilt
from the older hardcoded-field-id (`Fill New Object Form`) pattern to the label-driven,
properties-file-driven, T2-consolidated Bank/Berth/Port pattern — same shape as every other
Bank-pattern screen in this project. Test code changed from a generated-unique
`AUTOTEST_CARR_<timestamp>` to the fixed `AUTOTEST_CARRIER` (matching Bank/Berth/Port's
convention), with per-TC login/logout replacing the old single-session flow. The class/view/family
classification (section 1 above) did not change — this was an RF-layer rebuild, not a
re-classification.

**Dev story (from PR #477's real body):**
- Mandatory field set confirmed unchanged: `Carrier Code` / `Carrier Name` / `Start Date` /
  **Unit** (mandatory reference dropdown, filled `__FIRST__`).
- The "Unit" dropdown is deliberately EXCLUDED from `@{CARRIER_FORM_LABELS}` so it is never
  round-trip-verified — this reuses the Batch 2 VAT Code gotcha precedent (a `__FIRST__`-filled
  mandatory dropdown fails round-trip verify if included in the compare list).
- Carrier's navigator ("unclear at survey time" per the original Batch 11 task brief) was
  re-confirmed NOT gated (optional date + GO only, no mandatory dropdown/cascade) by checking this
  repo's own prior SOW recon (section 2 above) and the already-proven Playwright driver — both
  agreed — rather than re-running a redundant fresh live DOM scan. This is the "trust the
  documented fact, only re-verify on contradiction" rule in practice.
- Robocop parity check: Carrier's 9 issues (5x DOC02 missing-test-doc + 1x VAR02) were compared
  against the already-merged `port_iud.robot` baseline (also exit 1, 9 issues) and found identical
  in kind/count — not a regression introduced by this conversion.
- No shared T1 (`common.resource`)/T2 (`manage_object.resource`) files were touched.

**Live evidence at conversion time (PR #477 body):**
- Live RF (`EC_HEADLESS=true`): **5/5 PASS**.
- `robot --dryrun` on the full `tests/` tree: **772/772 pass**.
- `Find Carrier Row By Filter` fired **14x** / `Clear Carrier Row Filter` fired **5x** (grep-confirmed
  on `output.xml`).
- DB self-clean: fresh `oracledb` connection, 0 residual `AUTOTEST_CARRIER` rows in `OV_CARRIER`.

**Updated deliverables (superseding section 5's RF-layer rows):**
| Deliverable | Path |
|---|---|
| T3 page object (rebuilt) | `pageobjects/Configuration/Assets/Cargo_Objects/carrier_page.resource` |
| RF suite (rebuilt) | `tests/Configuration/Assets/Cargo_Objects/carrier_iud.robot` |
| Properties files (new) | `testdata/carrier_{insert,update,form_verify,grid_verify}.properties` |
| Credentials (additive) | `resources/credentials.py` — `CARRIER_EC_USER`/`CARRIER_EC_PASS` |
| Playwright bundle | unchanged, `screens/.../Carrier/playwright/ec_iud_carrier.py` (waived from rebuild per Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` — the Universal Screen Engine is the owner-decided replacement going forward) |
