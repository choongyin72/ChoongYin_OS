# SOW - Chemical Tank IUD (Configuration > Assets > Chemical Objects > Chemical Tank)

## 1. Screen identity
- **Screen:** Chemical Tank   **BF code:** CO.0070   **View:** `OV_CHEM_TANK`   **Base:** `CHEM_TANK`
- **Type:** OV-GM (manage-object, groupmodel) - grid `manageObject:form:T_data`, navigator-GATED. Sibling of Node.
- **Date-effective:** YES (VERSIONED) -> DELETE = End Date = Start Date.

## 2. Navigator (gated)
`nav:form:G:0:R:1:C:1..3:dd` = Production Unit -> Area -> Facility Class 1.
**As of the 2026-08-26 Area-pattern conversion (PR #549):** filled via the shared T2
`Apply Navigator From Properties` with EXPLICIT values (`testdata/chemical_tank_navigator.properties`:
Op Production Unit=`AS1 EC Exploration Norway`, Op Area=`AS1_Area`, Op Facility Class 1=
`AS1_Facility_01`) — the same values the original 2026-07-30 build's
"Apply OV-GM Navigator First Available" call already resolved to, captured live and pinned explicit.

## 3. New-Object form (scanned; fields BY LABEL)
| Field | Label | Mandatory | Kind |
|---|---|---|---|
| Code | Chemical Tank Code | yes | text |
| Name | Chemical Tank Name | yes | text |
| Start Date | Start Date | yes | date |
| **Measure unit** | Measure unit | **yes** | dropdown (first-available) |
| Op Production Unit | Op Production Unit | no* | dropdown (first-available) |

*Set first-available for grid visibility (probe per screen - the nav PU is not necessarily a valid Op PU option; see Node).

## 4. IUD plan
INSERT: New Object -> Code/Name/Start Date + Measure unit + Op Production Unit -> Save -> GO.
UPDATE: select row -> edit Chemical Tank Name -> Save -> GO. DELETE: End Date = Start Date -> Save -> GO.
Test data fixed code `AUTOTEST_CT` (post-PR #549; was `AUTOTEST_CT_<timestamp>` pre-conversion);
self-clean = absent in OV_CHEM_TANK; 0 residual re-read.

## 5. Deliverables
Driver `py/chemical_tank_iud.py`; T3 `pageobjects/.../Chemical_Objects/chemical_tank_page.resource`;
suite `tests/.../Chemical_Objects/chemical_tank_iud.robot`; this SOW; `VERIFY-REPORT.md` (auto-generated
2026-07-30, pre-conversion — see Section 6 for the PR #549 conversion evidence).

## 6. Area-pattern conversion (PR #549, 2026-08-26)

Chemical Tank matches Area's OV-GM navigator layout, so under the owner's 2026-08-26 standing rule
("Area is the role model for navigator screens") it was upgraded from the original 2026-07-30
suite-level-login/4-TC shape to Area's full pattern:

- **5 TCs** (adds TC04 Find), **per-TC login/logout**, fixed test code `AUTOTEST_CT`, explicit
  grid-filter wiring (`Find/Clear Chemical Tank Row By Filter`).
- Navigator cascade filled via the shared T2 `Apply Navigator From Properties` with explicit values
  (see Section 2) instead of the prior bespoke "Apply OV-GM Navigator First Available" call.
- **Dev story / gotcha:** live recon (`tmp/recon_ct_insert_exact_properties_order.py`) proved the
  insert form's own "Op Production Unit" dropdown becomes FILTERED once Start Date/Measure unit
  are set and does NOT include the navigator's own PU value — unlike Area's own equivalent field,
  which must equal the nav's PU. Forcing it (Area's default rule) reproducibly timed out TC02 live.
  Resolution: kept `Op Production Unit=__FIRST__` in `chemical_tank_insert.properties`, matching
  the already-proven Playwright driver's real behavior (`py/chemical_tank_iud.py`, unchanged) — the
  same class of issue as Chemical Injection Point/Production Separator.
- Evidence: live 5/5 (`EC_HEADLESS=true robot tests/.../chemical_tank_iud.robot`), full-tree
  dryrun 850/850, robocop parity (13 issues, same as Area/Facility Class 1 baseline), DB self-clean
  0 residual via fresh `oracledb` connection. Playwright driver untouched/still passing.
