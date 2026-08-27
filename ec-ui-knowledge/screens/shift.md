# Screen: Shift

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel;
  navigator-GATED. Converted 2026-08-26 (PR #547) to the Area-pattern 5-TC/per-TC-login/
  pure-screen-verify **structure** - Shift remains OV-GM with its genuine 3-level navigator
  cascade; this is a structural conversion, not a reclassification as plain Bank-shaped.
- **BF_CODE:** CO.0224 - **Treeview:** Configuration > Assets > Facility_Objects > Shift
- **DB view:** `OV_SHIFT` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Grid id:** `manageObject:form:T_data`
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - live RF 5/5 PASS (this backfill's
  own re-run), full-tree dryrun 883/883, DB self-clean 0 residual, robocop exit 0 (7 DOC02-only
  warnings), hygiene PASS. Prior state: 2026-08-26 PR #547 (live RF 5/5, full-tree dryrun
  850/850, robocop parity, DB self-clean); before that, 2026-07-31 `verify_screen.py` OVERALL
  PASS (RF 4/4 + Playwright 8/8, DB-verified, self-clean - the pre-Area-pattern shape).

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Shift` -> `label.tv-link` "Shift" |
| Navigator (gated, genuine 3-level same-row cascade) | `nav:form:G:0:R:1:C:1:dd` (Production Unit) -> `nav:form:G:0:R:1:C:2:dd` (Area) -> `nav:form:G:0:R:1:C:3:dd` (Facility Class 1) -> GO `#button:form:B`. SPECIFIC P1 values (P1 Production Unit -> P1 Area -> P1 Facility 1), NOT first-available. Filled via the shared RF T2 keyword `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by `testdata/shift_navigator.properties`. |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Grid filter | shared T2 `Find Object Row By Filter` / `Clear Object Row Filter` on `manageObject:form:T_data`, wrapped screen-locally as `Find Shift Row By Filter` / `Clear Shift Row Filter`. |
| Delete End Date field (hardcoded, not label-driven) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (`${SHIFT_DEL_ENDDATE}`) - the `objectdates` row packs Start Date (C:1) + End Date (C:3) with the End Date label at C:2, a shape the one-field-per-row label scan cannot safely resolve; same documented rationale as Area's/Facility Class 1's own del-enddate constant. |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Shift Code*** - **Shift Name*** - **Start Date*** (date) + **Start Time (HH:MI)*** FREE TEXT
('07:00' - format from the existing P1 S001 row) + Op Production Unit = nav PU value
(parent-matching). (`*` mandatory-and-empty on a pristine Insert row.)
- Screen-prefixed labels ("Shift Code"/"Shift Name"), NOT the generic "Code"/"Name" that
  Bank/Object List use - confirmed live via the prior driver.

### Update (`updateAttributes`) / Delete (`objectdates`)
`Shift Code` (ro) - **`Shift Name`**. Delete: **`End Date`** = Start Date -> true-deletes from
`OV_SHIFT`.

## Automation (code in ec-automation)
- **RF (current, Area-pattern shape):** T3
  `pageobjects/Configuration/Assets/Facility_Objects/shift_page.resource` (label-driven except
  the documented `${SHIFT_DEL_ENDDATE}` hardcoded id) + suite
  `tests/Configuration/Assets/Facility_Objects/shift_iud.robot` (5 TCs: Verify Clean State /
  Insert / Update / Find / Delete; per-TC Login/Logout on one Suite-Setup browser; pure-screen
  verification - the only in-suite DB check is inside the shared T2 `Verify Object Removed`
  for TC05). Testdata: `testdata/shift_{navigator,insert,update,form_verify,grid_verify}.properties`.
  Credentials: `SHIFT_EC_USER`/`SHIFT_EC_PASS` (`resources/credentials.py`). Fixed test code
  `AUTOTEST_SHIFT`.
- **Playwright (pre-existing, out of scope for the Area-pattern conversion and this KB
  refresh):** `py/shift_iud.py` (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`) -
  Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md` permanently waives rebuilding/re-verifying
  this bundle; the Universal Screen Engine is the owner-decided replacement going forward.
- **Bundle:** `screens/Configuration/Assets/Facility_Objects/Shift/` (SOW/README/JOURNAL/
  evidence/CHECKLIST, backfilled 2026-08-28 per `docs/lean-deliverable-backfill-workorder.md`).

## Quirks
- OV-GM navigator-gated: grid empty until the 3-level cascade + GO. This is a genuine,
  data-dependent navigator scope (P1 objects) - SPECIFIC values, NOT first-available; a
  first-available PU is a sparse test scope that is not necessarily a valid Op Production Unit
  option (see `docs/OV_SWEEP_PARKED.md`).
- Mandatory free-text Start Time (HH:MI) - the field class the OV-GM generator cannot
  auto-fill; hand-built; field format read from the existing P1 S001 row (scan-existing-row
  technique). Auto-detected as a plain text field by the shared "Fill OV Field By Label Any
  Kind" mechanism once placed in the insert properties file - no special-casing needed.
- Real Windows/tooling incident (not a screen defect): the isolated git worktree used for the
  2026-08-26 Area-pattern conversion hit a Windows long-path failure during checkout; resolved
  via owner-approved `git config --local core.longpaths true`. See
  `screens/Configuration/Assets/Facility_Objects/Shift/JOURNAL.md` for the full account.
