# Screen: Well Bore Interval

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED,
  genuine PER-FIELD navigator groups shape (NOT a same-row/increasing-column cascade).
- **BF_CODE:** CO.0057 - **Treeview:** Configuration > Assets > Well_and_Reservoir_Objects > Well Bore Interval
- **DB view:** `OV_WELL_BORE_INTERVAL` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`; 167 rows)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - RF suite re-run live 5/5 PASS (this
  backfill), on top of PR #563's Area-pattern STRUCTURE conversion (2026-08-27) and the
  2026-07-31 base build (`verify_screen.py` OVERALL PASS at the time, RF 4/4 + Playwright 8/8).

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Well Bore Interval` -> `label.tv-link` "Well Bore Interval" |
| Navigator (gated, BESPOKE T3 fill) | PER-FIELD groups `nav:form:G:<n>:R:1:C:0:dd`, filled by the screen-local `Apply Well Bore Interval Navigator` keyword (`well_bore_interval_page.resource`) via its `Select Nav Group Value` helper, in this exact group sequence: **G:1** Production Unit = `P1 Production Unit` -> **G:2** Area = `P1 Area` -> **G:3** Facility Class 1 = `P1 Facility 1` -> **G:4** 'Well & Well Hookup' = `P1 W008 OP` (a REAL well) -> **G:6** 'Well Bore' = `P1 W008 WB001` (the WELL BORE) -> GO once. **G:5** ('Well') is deliberately OMITTED — present in the DOM with mandatory-yellow styling when empty, but 0 usable options under this scope (live-reconfirmed 2026-08-27 and again this backfill). NOT filled by the shared T2 `Apply Navigator From Properties` (`resources/manage_object.resource`) — that keyword only supports the single-row/increasing-column cascade shape, which this per-field-groups screen genuinely is not. Values read from `testdata/well_bore_interval_navigator.properties`. |
| Grid | `manageObject:form:T_data` (empty until navigator + GO); explicit Code-column filter via shared T2 `Find/Clear Object Row Filter` wrapped as `Find/Clear Well Bore Interval Row By Filter` |
| Insert (+) | `Open New Object Form` (shared T2) |
| Mandatory 'Well Bore' popup | screen-local `Pick Well Bore Popup` keyword — waits for list grid **`Objects:form:T_data`** (NOT the generic `PopupList:form:T_data` the shared "Fill OV Field By Label Any Kind" auto-detector expects, which would report a false "empty source"), clicks the row whose value starts with the navigator's own G:6 value (FIELD-REUSE RULE — read straight from `well_bore_interval_navigator.properties`, never duplicated) |
| Save / GO | shared T2 `Save And Refresh List` / `Apply Navigator` (GO button click, bespoke keyword's last step) |
| Delete | `objectdates` End Date cell — hardcoded id `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (documented exception, same rationale as Area/Well); End Date = Start Date via shared T2 `Delete Object Via End Date` |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Well Bore Interval Code*** - **Well Bore Interval Name*** - **Start Date*** (date) + mandatory
**Well Bore** popup (screen-local picker, see above). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Well Bore Interval Code` (ro) - **`Well Bore Interval Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_WELL_BORE_INTERVAL`.

## Automation (code in ec-automation)
- **Playwright:** `py/well_bore_interval_iud.py` (shared engine `ec_object_iud.py` + screen-local
  `apply_wbi_navigator`/`pick_well_bore_popup`; live 8/8, 2026-07-31). Left untouched by PR #563's
  RF-only conversion; permanently waived from a new build (Section H,
  `docs/IUD-DELIVERABLE-CHECKLIST.md`) — the Universal Screen Engine replaces that role.
- **RF:** T3
  `pageobjects/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_page.resource`
  (BESPOKE navigator keyword + screen-local popup picker, both label-driven for form fields) +
  suite `tests/Configuration/Assets/Well_and_Reservoir_Objects/well_bore_interval_iud.robot` — 5
  TCs (Verify Clean State / Insert / Update / Find / Delete), per-TC Login/Logout, fixed test code
  `AUTOTEST_WBI`, zero inline DB-verify calls (delegates to shared T2 `Verify Object *` family).
- **Gate:** re-run live 2026-08-28 (this backfill) — 5/5 PASS, robocop 7 issues (parity with
  Area's own baseline), full-tree dryrun 883/883, hygiene PASS, DB self-clean 0 residual.

## Quirks
- Genuine PER-FIELD navigator groups (`nav:form:G:1..G:6`), not the single-row cascade shape most
  other converted Area-pattern screens use — this is why the navigator fill is a BESPOKE
  screen-local T3 keyword rather than the shared `Apply Navigator From Properties`. Confirmed a
  genuine non-fit on two separate live checks (2026-07-31 and 2026-08-27) — distinct from
  Meter/Tract elsewhere in this project, where an initial "non-fit" call was later found wrong.
- "Phantom mandatory nav group": G:5 ('Well') shows mandatory-yellow styling when empty but offers
  ZERO usable options in every scope tried — a known EC quirk shared with this screen's own
  siblings (Well G:5, Well Bore G:5). Skip it; GO still succeeds.
- The 'Well Bore' popup list grid is `Objects:form:T_data`, not the generic `PopupList:form:T_data`
  — generic popup helpers report a false "empty source" here; pick the nav-scope bore BY VALUE.
  Popup LABEL is 'Well Bore' (not 'Well').
- Well Bore Interval is the third screen of the well hierarchy (Well -> Well Bore -> Well Bore
  Interval), all three now automated.
