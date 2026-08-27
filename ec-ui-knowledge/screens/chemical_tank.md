# Screen: Chemical Tank

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
  Converted to the Area RF pattern (5-TC, per-TC login/logout) by PR #549 (2026-08-26).
- **BF_CODE:** CO.0070 - **Treeview:** Configuration > Assets > Chemical_Objects > Chemical Tank
- **DB view:** `OV_CHEM_TANK` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - fresh live re-run
  (`EC_HEADLESS=true robot tests/Configuration/Assets/Chemical_Objects/chemical_tank_iud.robot`) ->
  5 tests, 5 passed, 0 failed. PR #549 also reported: full-tree dryrun 850/850, DB self-clean 0
  residual (fresh `oracledb` connection). Earlier 2026-07-30 `verify_screen.py` OVERALL PASS
  (RF 4/4 + Playwright 8/8) superseded by the 5-TC conversion above.

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Chemical Tank` -> `label.tv-link` "Chemical Tank" |
| Navigator (gated) | cascade `nav:form:G:0:R:1:C:1..3:dd` = Production Unit -> Area -> Facility Class 1 -> GO `#button:form:B`. **Post-PR #549:** filled via shared T2 `Apply Navigator From Properties` with EXPLICIT values (`testdata/chemical_tank_navigator.properties`: Op Production Unit=`AS1 EC Exploration Norway`, Op Area=`AS1_Area`, Op Facility Class 1=`AS1_Facility_01`) — same values the prior first-available cascade resolved to. |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter | explicit `Find/Clear Chemical Tank Row By Filter` wrappers around shared T2 `Find/Clear Object Row By Filter` (`${CT_TABLE}`, Code column) — added by PR #549, matching every other Area/Bank-converted screen. |
| Delete End Date input | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (`${CT_DEL_ENDDATE}` in the page object; Start Date is C:1, End Date label is C:2, End Date input is C:3, same row). |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Chemical Tank Code*** - **Chemical Tank Name*** - **Start Date*** (date) + dropdowns Measure unit
(`__FIRST__`) - Op Production Unit (`__FIRST__`). (`*` mandatory)

**Quirk (confirmed live 2026-08-26, `tmp/recon_ct_insert_exact_properties_order.py`):** unlike
Area's own equivalent field, this screen's "Op Production Unit" dropdown does NOT need to (and
cannot) be forced to equal the navigator's own PU value — its option list becomes FILTERED once
Start Date/Measure unit are set and does not include the nav's PU at all. Forcing it (Area's
default rule) reproducibly timed out TC02 live. `testdata/chemical_tank_insert.properties` keeps
`Op Production Unit=__FIRST__`, matching the already-proven Playwright driver's behavior — same
class of issue as Chemical Injection Point / Production Separator.

### Update (`updateAttributes`) / Delete (`objectdates`)
`Chemical Tank Code` (ro) - **`Chemical Tank Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_CHEM_TANK`.

## Automation (code in ec-automation)
- **Playwright:** `py/chemical_tank_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`) —
  unchanged since 2026-07-30; still the proven flow. Per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H,
  new Playwright drivers are no longer built for Bank-/Area-pattern conversions (Universal Screen
  Engine replaces that role); this one is pre-existing/incidental.
- **RF:** T3 `pageobjects/Configuration/Assets/Chemical_Objects/chemical_tank_page.resource`
  (**label-driven**, rewritten to Area's 5-TC shape by PR #549) + suite
  `tests/Configuration/Assets/Chemical_Objects/chemical_tank_iud.robot` (5 TCs: clean-check, insert,
  update, find, delete; per-TC login/logout; fixed test code `AUTOTEST_CT`).
- **Gate (pre-conversion):** `verify_screen.py` -> OVERALL PASS (2026-07-30). PR #549's own gate
  was hand-cited in the PR body (robocop parity, dryrun 850/850, live 5/5, DB self-clean) since the
  screen's RF shape changed after `verify_screen.py`'s report was generated.

## Quirks
- OV-GM navigator-gated: grid empty until cascade + GO.
- Post-PR #549: navigator now uses EXPLICIT properties-file values, not first-available (see
  Selectors table). Insert form's Op Production Unit deliberately stays `__FIRST__` — see the
  New Object form quirk above. Measure unit stays `__FIRST__` too (grid-visibility requirement,
  unrelated to the nav-PU question).
- Mandatory-yellow fields on insert: Chemical Tank Code, Chemical Tank Name, Start Date, Measure unit.
