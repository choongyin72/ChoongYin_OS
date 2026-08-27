# Screen: Chemical Injection Point

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED
  (genuine 3-level Production Unit -> Area -> Facility Class 1 cascade).
- **BF_CODE:** CO.0212 - **Treeview:** Configuration > Assets > Chemical_Objects > Chemical Injection Point
- **DB view:** `OV_CHEM_INJ_POINT` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - RF live 5/5 PASS (this session,
  reproducing PR #550's cited evidence), DB-verified, self-clean confirmed via fresh connection.
  (Converted to Area's full pattern in PR #550, merged 2026-08-26.)

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Chemical Injection Point` -> `label.tv-link` "Chemical Injection Point" |
| Navigator (gated, mandatory) | same-row cascade `nav:form:G:0:R:1:C:1:dd` (Production Unit) -> `C:2:dd` (Area) -> `C:3:dd` (Facility Class 1); C:4 absent -> GO. Filled via shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by `testdata/chem_injection_point_navigator.properties` (`Op Production Unit=AS1 EC Exploration Norway`, `Op Area=AS1_Area`, `Op Facility Class 1=AS1_Facility_01`). |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter | shared T2 `Find/Clear Object Row Filter` on `manageObject:form:T_data`, filtering the Chem Inj Point Code column |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven - same rationale as Area/Facility Class 1's own del-enddate constant) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, screen-prefixed)
**Chem Inj Point Code*** - **Chem Inj Point Name*** - **Start Date*** (date) - Op Production Unit
(see quirk below). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Chem Inj Point Code` (ro) - **`Chem Inj Point Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_CHEM_INJ_POINT`.

### Grid columns (confirmed live, `manageObject:form:T_head`)
Chem Inj Point Code / Chem Inj Point Name / Start Date / End Date - same 4-column shape as Area/
Facility Class 1.

## Automation (code in ec-automation)
- **RF (maintained, current pattern):** T3
  `pageobjects/Configuration/Assets/Chemical_Objects/chem_injection_point_page.resource`
  (label-driven, Area-pattern 5-TC/per-TC-login shape, properties-file-driven) + suite
  `tests/Configuration/Assets/Chemical_Objects/chem_injection_point_iud.robot`.
  Testdata: `testdata/chem_injection_point_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Legacy Playwright (reference only, waived going forward per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`):** `py/chem_injection_point_iud.py` (shared engine
  `ec_object_iud.py` + `apply_ovgm_navigator`), `verify_screen.py` PASS 2026-07-30.

## Quirks
- OV-GM navigator-gated: grid empty until the 3-level cascade + GO. The cascade values used
  (`AS1 EC Exploration Norway` / `AS1_Area` / `AS1_Facility_01`) are the same first-available picks
  the original driver already selected - confirmed live 2026-08-26, not re-derived.
- **Op Production Unit `__FIRST__` gotcha (PR #550, 2026-08-26):** the Insert form's own "Op
  Production Unit" `objectForm` field (separate from the navigator) is a long (~25-row)
  autocomplete that renders only a small (~5-row) MRU/default subset before its full reference
  list finishes loading. A hardcoded exact-label wait for the navigator's picked value was flaky
  against that subset. Fix: use `__FIRST__` for this ONE field in
  `chem_injection_point_insert.properties`, matching the already-proven legacy driver's own
  tolerant mechanism for this field. The resulting row still shows under the navigator scope
  regardless of which specific value gets picked - this field is NOT required to match the nav
  scope for grid visibility on this screen (unlike Area's/Facility Class 1's own Op-PU-must-match
  convention, which does not hold here).
- Versioned groupmodel grid may redraw lazily after a delete - the shared T2's `Save And Refresh
  List` already re-applies the navigator before the TC05 assertion reads the grid.
