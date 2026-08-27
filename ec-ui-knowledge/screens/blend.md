# Screen: Blend

- **Type:** OV (EC Object Configuration, date-effective) - Bank-family (`manage_object_nav`); plain
  (no navigator, optional dropdowns only, none mandatory) - FULL Bank-pattern (properties-file-driven,
  grid-filter-wired, T2-consolidated, 5-TC) since PR #457 (Batch 7, 2026-08-23).
- **BF_CODE:** CO.0219 - **Treeview:** Configuration > Assets > Hydrocarbon_Objects > Blend _(DB treeview JSON)_
- **DB view:** `OV_BLEND` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-28 - EC 14.2.4 - local sandbox - live re-run 5/5 (first attempt),
  robocop exit=1 (7 DOC02 advisory warnings, no new category), hygiene exit=0, DB self-clean 0
  residual `AUTOTEST_BLEND` rows in `OV_BLEND` (fresh connection).

## Selectors `[from screens/Blend/blend_page.resource Variables section, 2026-08-23 recon]`
| Purpose | Selector |
|---|---|
| Open | search `Blend` -> `label.tv-link` "Blend" |
| Grid | `${OV_MANAGE_OBJECT_TABLE}` = `manage_object_nav_nav:form:T_data` (needs GO to load) |
| Grid filter | `Find Blend Row By Filter <code>` / `Clear Blend Row Filter` -> shared T2 `Find/Clear Object Row By Filter` |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete End Date field | hardcoded `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (NOT
  label-driven, by design - objectdates row packs Start Date C:1 / End Date C:3, label at C:2;
  same shape as Bank's/Customer's own delete-field ids). |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL, code_label=`Blend Code`)
**Blend Code*** - **Blend Name*** - **Start Date*** (date, mandatory via `MandatoryCellStyle`) -
End Date - Sort Order - Description - Master System Code - Master System Name (all optional,
skipped). (`*` mandatory)

### Update (`updateAttributes`) / Delete (`objectdates`)
`Blend Code` (read-only there) - **`Blend Name`** - `Description`. Delete: **`End Date`** =
Start Date -> row leaves `OV_BLEND`.

## Automation (code in ec-automation)
- **Playwright:** `py/blend_iud.py` -> 7/7 (2026-07-26; unchanged, not rebuilt - Universal Screen
  Engine is the owner-decided replacement for new Playwright drivers going forward).
- **RF:** T3 `pageobjects/Configuration/Assets/Hydrocarbon_Objects/blend_page.resource`
  (properties-file-driven via shared T2: `Insert/Update Object From Properties`, `Verify Object
  Insert Exists/Form Record/Found`; explicit grid-filter wiring; `code_label=Blend Code` threaded
  through since Blend's Code field is screen-prefixed, matching State's precedent) + suite
  `tests/.../blend_iud.robot` (5-TC: clean-state/insert/update/find/delete, fixed test code
  `AUTOTEST_BLEND`, per-TC login/logout) -> live 5/5.
- **Gate:** screen-scoped dryrun 5/5, robocop exit=1 (advisory only), hygiene exit=0, DB self-clean
  0 residual (2026-08-28 re-run); full-tree dryrun 753/753 at PR #457 merge (2026-08-23).

## Quirks
- Plain OV; no mandatory dropdowns. Generic engine handles appear/absent/pagination.
- Code/Name fields are screen-prefixed ("Blend Code"/"Blend Name"), not the generic "Code"/"Name"
  Bank/Customer use - matches State's own precedent. Any new T2 keyword call for this screen must
  pass `code_label=Blend Code` where the keyword supports it.
- Delete's End Date field id is deliberately hardcoded, not label-driven - documented exception,
  same shape as Bank/Customer.
