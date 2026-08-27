# Screen: Calculation Context

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain
  (optional dropdowns only, none mandatory beyond the universal Date + GO bar)
- **BF_CODE:** CO.1059 - **Treeview:** Configuration > Assets > Calculation_Objects > Calculation
  Context _(DB treeview JSON)_. Distinct sibling screen from Calculation Group Context (CO.0245) -
  do not confuse the two.
- **DB view:** `OV_CALC_CONTEXT` (versioned; key `CODE`; `NAME`, `DESCRIPTION`, `COMMENTS`,
  `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - live headless RF run 5/5 PASS, DB
  self-clean 0 residual, full-tree dryrun 883/883, robocop 13 issues (DOC02 style-only)

## Selectors `[from calculation_context_page.resource Variables section, 2026-08-28]`
| Purpose | Selector |
|---|---|
| Open | search `Calculation Context` -> `label.tv-link` "Calculation Context" |
| Grid | `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`; needs GO/`Apply Navigator` to load - no default rows on open) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete (objectdates End Date) | hardcoded `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (independently live-verified on this exact screen, 2026-08-23) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, no hardcoded ids)
**Calc Context Code*** - **Calc Context Name*** - **Start Date*** (date) - End Date - Description -
Comments (optional). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Calc Context Code` (read-only) - **`Calc Context Name`** - `Description` - `Comments`. Start/End
Date live only in `objectdates`, not `updateAttributes` (confirmed live 2026-08-23). Delete:
**`End Date`** = Start Date -> row leaves `OV_CALC_CONTEXT`.

### Grid-filter wiring (added PR #456, Batch 7 Bank-pattern conversion)
`Find Calculation Context Row By Filter <code>` / `Clear Calculation Context Row Filter` — thin T3
wrappers delegating to shared T2 `Find/Clear Object Row By Filter`. Wired into Update/Find/
Verify-Found/Delete (matches Bank/Account's explicit-filter convention, owner 2026-08-22).

## Automation (code in ec-automation)
- **Playwright** (pre-existing, waived from further build per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`, 2026-08-27; Universal Screen Engine replaces this role going
  forward): `py/calculation_context_iud.py` -> 7/7 (2026-07-26; not re-run by this backfill).
- **RF:** T3 `pageobjects/Configuration/Assets/Calculation_Objects/calculation_context_page.resource`
  (label-driven, NO hardcoded ids except the one independently-verified Delete field id above) +
  suite `tests/.../calculation_context_iud.robot` -> **5 TCs** (clean-state/insert/update/find/
  delete), per-TC `Login To EC Application`/`Logout From EC Application` on one browser opened once
  in Suite Setup, dedicated `CALC_CONTEXT_EC_USER`/`CALC_CONTEXT_EC_PASS` credentials, fixed test
  code `AUTOTEST_CALCCTX`, properties-file-driven via
  `testdata/calculation_context_{insert,update,form_verify,grid_verify}.properties` -> live 5/5
  (re-confirmed 2026-08-28).
- **Verification convention:** PURE SCREEN verification only (2026-08-25 alignment fix, PR #514) -
  no inline DB-verify calls remain in the `.robot` suite; DB ground truth lives solely in the shared
  T2 `Verify Object Removed` (TC05) and this KB's own documented DB self-clean check.
- **Gate history:** `verify_screen.py` OVERALL PASS at the 2026-07-26 build (pre-conversion 4-TC
  shape); PR #456/#514 each re-verified live 5/5 + full-tree dryrun manually (this screen's
  properties-file-driven shape post-dates `verify_screen.py`'s original scaffold assumptions, so the
  Bank-pattern conversions cite manual gate runs in their PR bodies instead).

## Quirks
- Plain OV; no mandatory dropdowns beyond the universal Date + GO bar. Generic engine handles
  appear/absent/pagination with zero screen-specific tuning.
- Fixed test code `AUTOTEST_CALCCTX` is reused every run - EC never lets a deleted code be reused
  again until TC05 (delete) actually completes, so every run must reach TC05 to keep the code free
  for the next run.
- A Bank-pattern STRUCTURAL conversion (5-TC, filter wiring, properties files) does not by itself
  guarantee pure-screen-verify compliance if the pre-conversion suite had its own bespoke inline
  DB-verify keyword - this screen needed a separate follow-up fix (PR #514) to actually remove that
  residue after the structural conversion (PR #456) left it in place.
