# Screen: Pilot

- **Type:** OV-GM (EC Object Configuration, groupmodel manage-object, date-effective) -
  navigator-GATED: genuine 3-level same-row cascade (Production Unit -> Area -> Facility Class 1),
  same shape as Well and the Area role-model pattern.
- **BF_CODE:** CO.2079 - **Treeview:** Configuration > Assets > Transport_Objects > Pilot
- **DB view (ground truth):** `OV_PILOT` (key `CODE`; also `NAME`, `OBJECT_START_DATE`,
  `OBJECT_END_DATE`)
- **Last verified:** 2026-08-28 (this backfill's live re-run) - EC 14.2.4 - local sandbox
  (`localhost:1521/ORCL`). Base build verified 2026-07-31 (`verify_screen.py` OVERALL PASS, RF 4/4 +
  Playwright 8/8); RF suite converted to the Area-pattern 5-TC structure by PR #560 (2026-08-26),
  re-confirmed live 5/5 by this backfill without any automation changes.

## Selectors `[from pilot_page.resource Variables/Documentation section, transcribed 2026-08-28]`

| Purpose | Selector |
|---|---|
| Open | search `Pilot` -> `label.tv-link` "Pilot" |
| Navigator (gated) | single group, same-row 3-level cascade `nav:form:G:0:R:1:C:1/C:2/C:3:dd` =
  Production Unit -> Area -> Facility Class 1 (all MandatoryCellStyle, confirmed live 2026-08-26) ->
  GO |
| Navigator fill mechanism | Shared T2 `Apply Navigator From Properties`
  (`resources/manage_object.resource`), driven by `testdata/pilot_navigator.properties` - replaced
  the pre-existing driver's own `apply_ovgm_navigator`-style inline fill |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Grid-filter | `Find/Clear Pilot Row By Filter` -> shared T2 `Find/Clear Object Row By Filter` on
  the grid's Code column |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Insert/Update/Verify | Delegates to shared T2 `Insert/Update/Verify Object *` keywords, all
  called with `code_label=Pilot Code` (screen-prefixed label, like Well's "Well Code"/"Well Name" -
  NOT the generic "Code"/"Name" Bank/Object List use) |
| Delete End Date field | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not
  label-driven - same documented rationale as Area's/Well's own delete-date fields; value reused
  verbatim from the pre-existing driver's own `${DEL_ENDDATE}`) |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / navigator GO button |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Pilot Code*** - **Pilot Name*** - **Start Date*** (date). Op Production Unit present but NOT
mandatory-styled (see Quirks - kept `__FIRST__`). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Pilot Code` (ro) - **`Pilot Name`**. Delete: **`End Date`** = Start Date -> leaves `OV_PILOT`.

## Mandatory / yellow fields
- **Navigator (before the grid loads any rows):** Production Unit -> Area -> Facility Class 1,
  all three MandatoryCellStyle, same-row single group + GO.
- **Insert form:** Pilot Code, Pilot Name, Start Date (mandatory, confirmed live 2026-08-26 via
  MandatoryCellStyle scan). Op Production Unit is present but NOT mandatory-styled.
- **Update form:** Pilot Name only (Pilot Code is read-only in `updateAttributes`).

## Quirks
- **OV-GM navigator-gated:** grid stays empty until the 3-level cascade is filled + GO'd.
- **Op Production Unit `__FIRST__` exception (documented, not a fit violation):** unlike Area
  (where Op Production Unit = the navigator's own Production Unit value), Pilot's Op Production
  Unit value domain is INDEPENDENT of the navigator's Production Unit - the pre-existing
  `py/pilot_iud.py` driver's own code comment states "the nav PU is not necessarily a valid Op PU
  option." Kept as `__FIRST__` rather than forced to match the navigator's value; this is a
  live-evidenced exception to the general field-reuse rule applied to other converted OV-GM
  screens, applied deliberately in PR #560, not an oversight.
- First-available nav PU is a sparse test scope - can empty nav-scoped popups elsewhere on similar
  screens (see issue OV_SWEEP_PARKED); this screen's own recon (2026-08-26) reconfirmed the
  first-available value at each cascade level is stable and usable.
- Fixed test code `AUTOTEST_PILOT` (not a generated/unique code, since PR #560's conversion) -
  every run must complete TC05 so the code is free for the next run.

## Automation (code lives in ec-automation - this file is the MD selector reference)
- **RF (the maintained suite):** T3
  `ec-automation/pageobjects/Configuration/Assets/Transport_Objects/pilot_page.resource` (T2
  `resources/manage_object.resource` + `libraries/PropertiesReader.py`) + suite
  `ec-automation/tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` (5 TCs: Clean
  State/Insert/Update/Find/Delete, per-TC Login/Logout, fixed test code `AUTOTEST_PILOT`, zero
  inline DB-verify calls). Run:
  `EC_HEADLESS=true robot tests/Configuration/Assets/Transport_Objects/pilot_iud.robot` -> 5/5
  PASS, self-clean 0 residual in `OV_PILOT` (re-confirmed 2026-08-28).
- **Playwright (pre-existing reference, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` - Universal Screen Engine replaces this role going forward):**
  `ec-automation/py/pilot_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`), kept
  unchanged since the 2026-07-31 build.
- **Gate history:** base build `verify_screen.py` -> OVERALL PASS (2026-07-31, RF 4/4 + Playwright
  8/8); PR #560's own re-run -> live 5/5 (x2 runs, shared tree + isolated worktree), full-tree
  dryrun 875/875, robocop 7 issues (parity w/ Area's baseline), DB self-clean 0 residual, grid-filter
  fired 15x; this backfill's 2026-08-28 re-run -> live 5/5 (first attempt, no retry), dryrun 5/5,
  robocop 7 issues (unchanged), hygiene PASS, DB self-clean 0 residual, grid-filter fired 29x.
- Full bundle (SOW/README/JOURNAL/evidence/CHECKLIST):
  `ec-automation/screens/Configuration/Assets/Transport_Objects/Pilot/`.
