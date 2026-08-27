# Screen: Meter

- **Type:** OV-GM (BU-gated) + generic popup - Area-family (full Area-pattern conversion,
  properties-file-driven, T2-consolidated, PR #554, 2026-08-26).
- **Treeview:** Configuration > Assets > Dispatching_Objects > Meter _(DB treeview JSON)_
- **DB view:** `OV_METER` (versioned, key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - live RF 5/5, full `tests/` tree
  dryrun 883/883, robocop 7 issues (parity with Area's own baseline), hygiene PASS, DB self-clean
  0 residual via a fresh oracledb connection (backfill re-run; see
  `screens/Configuration/Assets/Dispatching_Objects/Meter/evidence/`).

## ⚠️ Gotcha: the navigator is NOT the insert-form popup — evaluate them separately
Meter's insert form has a mandatory field (Delivery Point Name) driven by a POPUP widget, which
looks unusual next to the navigator's plain dropdown. Earlier in the session that produced PR
#554, this popup was wrongly conflated with the navigator itself, producing an incorrect
"does not fit Area pattern" classification. A deeper live re-check found the navigator, examined
on its own, is exactly ONE mandatory Business Unit dropdown - the same single-dropdown shape as
Area's own Production Unit navigator. **Lesson for future screens:** classify the navigator's
shape by looking at the navigator section alone; an unusual widget on the INSERT FORM (a popup,
a multi-select, anything non-dropdown) says nothing about the navigator's own shape and must not
bias that call. See `screens/Configuration/Assets/Dispatching_Objects/Meter/JOURNAL.md`
"Done wrong / lessons" for the full account.

## Selectors `[from meter_page.resource Variables section, 2026-08-26/27]`
| Purpose | Selector |
|---|---|
| Open | search `Meter` -> `label`/`span.tv-link` "Meter" |
| Navigator | Business Unit dropdown `nav:form:G:0:R:1:C:1:dd` - **MANDATORY**, single dropdown, same shape as Area's own navigator. A second dropdown at `nav:form:G:0:R:1:C:2:dd` ("Delivery Point") is an OPTIONAL grid filter - GO succeeds with only C:1 filled. |
| GO | `button:form:B` (per Area-pattern convention) |
| Grid | `manageObject:form:T_data` |
| Insert (+) | hover insert icon -> "New Object" (generic T1 gesture) |
| Save | generic T1 Save gesture (properties-file-driven insert/update via shared T2) |
| Delete (End Date) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded - packed date row, End Date = Start Date = true delete in `OV_METER`) |

### Delivery Point Name popup mechanism (generic T1, NOT screen-local)
The Delivery Point Name field is the plain pin/pinB EC object popup, resolved by the shared T2
`Pick OV Popup By Label` / T1 `Pick From EC Object Popup` (`resources/popup.resource`) - no
screen-local popup wrapper is needed (unlike Chemical Stream's own From Connection popup). Recipe
(from `docs/meter_popup_notes.md`, proven live 2026-06-13):
1. JS-click the `pinB` button (actionability-checked clicks time out - a dialog mask races the
   click and intercepts it).
2. Wait for `#popupIFrame` visible, src containing `object_popup`.
3. Inside the iframe, match the target row by its grid input VALUE PROPERTY or row innerText -
   never XPath `@value` (EC populates grid inputs dynamically; the HTML attribute stays empty).
4. Row click selects + closes the popup + fills the main-form `pin` input.
The popup list is itself navigator-filtered - the Business Unit navigator must be set BEFORE
opening the insert form, or the popup returns "No records found".

### New Object form (`objectForm`) - labels, screen-prefixed (T3 resolves BY LABEL)
**Meter Code*** - **Meter Name*** - **Start Date*** (date) - **Meter Type*** (dropdown:
Entry/Exit/Fuel/Transit) - **Delivery Point Name*** (popup, see above). (`*` mandatory,
MandatoryCellStyle/yellow, confirmed live on the pristine insert form.)

Insert file ORDER is load-bearing: Start Date -> Delivery Point Name (popup) -> Meter Code ->
Meter Name -> Meter Type -> Save. The popup's close callback resets the form's dirty/save state,
so filling Code/Name/Type AFTER the popup re-arms Save; filling them before, or Saving right after
the popup, silently no-ops.

### Update (`updateAttributes`) / Delete (`objectdates`)
`Meter Code` (read-only in updateAttributes) - **`Meter Name`** (editable, the only field exercised
by TC03). Meter Type / Delivery Point Name are editable in updateAttributes but not re-exercised
by the suite. Delete: **`End Date`** = Start Date -> true delete, leaves `OV_METER`.

## Automation (code in ec-automation)
- **RF:** T3 `pageobjects/Configuration/Assets/Dispatching_Objects/meter_page.resource`
  (properties-file-driven, T2-consolidated, per-TC login `METER_EC_USER`/`METER_EC_PASS`) + suite
  `tests/Configuration/Assets/Dispatching_Objects/meter_iud.robot` (5 TCs: clean state, insert,
  update, find, delete) -> live 5/5.
- **Testdata:** `testdata/meter_navigator.properties`, `meter_insert.properties`,
  `meter_update.properties`, `meter_form_verify.properties`, `meter_grid_verify.properties`.
- **Playwright:** none maintained going forward - Universal Screen Engine (`py/engine.py`) is the
  owner-decided replacement (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`); no new Playwright
  driver was built for the Area-pattern conversion or this backfill.
- **Gate:** robocop 7 issues (parity with Area baseline), hygiene PASS, DB self-clean 0 residual.

## Quirks
- OV-GM with a genuine BU-gated navigator (single mandatory dropdown) PLUS a genuine mandatory
  insert-form popup - these are two separate mechanisms and must be evaluated independently (see
  the gotcha above).
- Field labels are screen-prefixed ("Meter Code"/"Meter Name"), not the generic "Code"/"Name"
  Bank/Object List use.
- Fixed test code `AUTOTEST_METER` (not generated/timestamped).
