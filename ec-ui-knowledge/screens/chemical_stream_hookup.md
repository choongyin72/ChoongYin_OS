# Screen: Chemical Stream Hookup

- **Type:** OV-GM (EC Object Configuration, date-effective) - manage-object groupmodel; navigator-GATED.
- **BF_CODE:** CO.0260 - **Treeview:** Configuration > Assets > Chemical_Objects > Chemical Stream Hookup
- **DB view:** `OV_CHEM_STRM_HOOKUP` (key `CODE`; `NAME`, `OBJECT_START/END_DATE`)
- **Last verified:** 2026-08-27 - EC 14.2.4 - local sandbox - transcribed from
  `chemical_stream_hookup_page.resource`'s own Variables/Documentation (PR #544, merged
  2026-08-26); original build verified 2026-08-01 via `verify_screen.py` OVERALL PASS (RF 4/4 pass
  + Playwright 8/8, DB-verified, self-clean). This backfill did not re-scan the screen live.

## Selectors
| Purpose | Selector |
|---|---|
| Open | search `Chemical Stream Hookup` -> `label.tv-link` "Chemical Stream Hookup" |
| Navigator (3-level same-row cascade) | `nav:form:G:0:R:1:C:1:dd` (Production Unit) -> `nav:form:G:0:R:1:C:2:dd` (Area) -> `nav:form:G:0:R:1:C:3:dd` (Facility Class 1) -> GO `#button:form:B` |
| Grid | `manageObject:form:T_data` (empty until cascade + GO) |
| Grid filter | `Find/Clear Chemical Stream Hookup Row By Filter` (T3, delegates to shared T2 `Find/Clear Object Row Filter` on `manageObject:form:T_data`'s Code column) |
| Insert (+) | hover `span.ui-icon-insert` -> "New Object" |
| Save / GO | `//a[@title='Save [Ctrl+s]' and not(...disabled)]` / `#button:form:B` |
| Delete (End Date field) | `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (hardcoded, not label-driven — same documented rationale as Area's/Bank's own del-enddate constant) |

### New Object form (`objectForm`) - labels (T3 resolves BY LABEL)
**Chemical Stream Hookup Code*** - **Chemical Stream Hookup Name*** - **Start Date*** (date). (`*`
mandatory). No "Op Production Unit" field on this screen's objectForm (confirmed live: mand=False,
not filled) — the row's visibility under the navigator scope comes purely from the cascade in
`chemical_stream_hookup_navigator.properties`.

### Update (`updateAttributes`) / Delete (`objectdates`)
`Chemical Stream Hookup Code` (ro, guard) - **`Chemical Stream Hookup Name`**. Delete: **`End Date`**
= Start Date -> true delete, row leaves `OV_CHEM_STRM_HOOKUP`.

### Grid columns
Chemical Stream Hookup Code / Chemical Stream Hookup Name / Start Date / End Date (per
`testdata/chemical_stream_hookup_grid_verify.properties`, same 4-column shape as Area/Sub Area/
Facility Class 1).

## Navigator values (this environment, confirmed LIVE 2026-08-26 via PR #544's temporary probe)
Production Unit = `AS1 EC Exploration Norway`, Area = `AS1_Area`, Facility Class 1 =
`AS1_Facility_01` — driven by `testdata/chemical_stream_hookup_navigator.properties` via the
shared T2 `Apply Navigator From Properties` keyword. These values are exactly what the screen's
PRIOR automation's `Apply OV-GM Navigator First Available` mechanism resolved to on this sandbox;
PR #544 made them explicit/properties-driven instead of re-resolving at every run. Confirmed via a
temporary probe reading back each navigator column's actual first-available resolution — NOT
guessed, NOT copied from Well's own "P1 ..." scope (a different screen's proven value).

## Mandatory-field pre-flight gate (owner-mandated design decision — do not remove/weaken)
This screen imports `resources/mandatory_field_gate.resource` and calls
`Assert No Empty Mandatory Field` BEFORE every Save (Insert and Update), via a T3-local
`Fill Object Form Fields And Save With Gate` helper. The gate scans every visible
input/select/textarea whose id starts with the given `${scope_prefix}` (e.g.
`tab:tabPanel:objectForm:form`) for EC's own mandatory-yellow background
(`rgb(252, 249, 192)`) that is still empty, and FAILS the test naming every offending field/id
BEFORE the caller clicks Save — the proactive counterpart to reading EC's post-Save error banner
reactively. It is opt-in and additive-only: `common.resource`/`manage_object.resource`/any other
shared keyword is NOT modified, so every other already-shipped screen is unaffected. Chemical
Stream Hookup was the SECOND screen (after Action Trigger) to adopt this mechanism (original
2026-08-01 build), deliberately chosen as the CASCADE-HEAVY comparison case (PU -> Area ->
Facility Class 1 + GO before the form is even open, where a missed mandatory field costs a full
cascade re-fill under a reactive-only approach). PR #544 kept this exactly as-is per explicit
owner instruction — it only extracted the gate call into the new T3-local helper to stay under the
house keyword-length convention.

## Automation (code in ec-automation)
- **RF (maintained/live test):** T3
  `pageobjects/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_page.resource`
  (label-driven, rewritten to the Area-pattern 5-TC structure by PR #544, 2026-08-26) + suite
  `tests/Configuration/Assets/Chemical_Objects/chemical_stream_hookup_iud.robot` (5 TC: Clean
  State / Insert / Update / Find / Delete, per-TC login/logout, fixed test code `AUTOTEST_CSH`).
- **Playwright (historical reference only, NOT maintained):** `py/chemical_stream_hookup_iud.py`
  (shared engine `ec_object_iud.py` + `apply_ovgm_navigator`) — original 2026-08-01 build,
  preserved unchanged; no new Playwright bundle is built for Area-pattern work (owner decision
  2026-08-27, Universal Screen Engine replaces this role).
- **Test data:** `testdata/chemical_stream_hookup_{navigator,insert,update,form_verify,grid_verify}.properties`.
- **Gate (original build):** `verify_screen.py` -> OVERALL PASS (2026-08-01, pre-conversion 4-TC
  state; not re-run for the 5-TC structure — see PR #544's own manual gate sequence instead, cited
  in `CHECKLIST.md`).

## Quirks
- OV-GM navigator-gated: grid empty until the 3-level cascade (PU -> Area -> Facility Class 1) + GO
  completes.
- No "Op Production Unit" field on this screen's `objectForm` (confirmed live: mand=False, not
  filled) — DIFFERENT from screens like Sub Area/Area where the Op PU/Op Area fields ARE filled on
  insert. Do not assume one screen's blank-field behavior applies to another; each is its own
  proven, tested shape.
- Delete End Date field id is hardcoded (`tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`), not
  label-driven — documented rationale matches Area's/Bank's own del-enddate constant.
- PR #544 (Area-pattern conversion) is a STRUCTURAL RF conversion only — the screen remains OV-GM
  with its genuine 3-level cascade; it was NOT reclassified as plain Bank-shaped.
