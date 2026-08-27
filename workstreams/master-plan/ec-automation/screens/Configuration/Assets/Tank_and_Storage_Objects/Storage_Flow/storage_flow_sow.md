# SOW - Storage Flow (CO.2091) - Bank-pattern OV IUD

_Backfilled 2026-08-28 (Batch 11 of `docs/lean-deliverable-backfill-workorder.md`) to reflect the
screen's REAL current state after PR #472 (Batch 10 of the Bank-pattern conversion project,
merged 2026-08-23). This SOW supersedes the 2026-07-26 version, which described the screen's
older, now-replaced label-driven-only build (unique-timestamped code, single login, no grid
filter)._

## Classification
- **Screen:** Configuration > Assets > Tank_and_Storage_Objects > Storage Flow (BF_CODE **CO.2091**)
- **Type/pattern:** OV (manage-object, `manage_object_nav`) - date-effective, plain (no navigator
  dropdown, universal Date + GO bar only) - **FULL Bank pattern** (mirrors
  `bank_page.resource`/`berth_page.resource`: label-driven, properties-file-driven,
  T2-consolidated, explicit grid-filter wiring)
- **DB view:** `OV_STORAGE_FLOW` (versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_STORAGE_FLOW`

## Nav / grid / cells
- **Open:** menu search "Storage Flow" -> `label.tv-link`. Navigator = universal Date + GO bar
  only (no mandatory dropdown); grid needs GO to load.
- **Grid:** shared T2 constant `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`),
  referenced in the T3 as `${STORAGE_FLOW_TABLE}`.
- **Grid filter:** explicit `Find/Clear Storage Flow Row By Filter` wired into Update/Find/
  Verify-Found/Delete (T2 `Find Object Row By Filter`/`Clear Object Row Filter`) - added in the
  Batch 10 conversion; the pre-conversion build relied only on `Select Object Row`'s implicit
  fallback.
- **NO hardcoded field ids** - resolved BY LABEL via T2 `Insert/Update/Verify Object From
  Properties`:
  - **Insert (objectForm):** `Storage Flow Code`, `Storage Flow Name`, `Start Date` (mandatory) +
    mandatory dropdowns `Flow Direction`/`Storage` (`__FIRST__`, carried over from the screen's own
    already-proven page object/Playwright driver per the Batch-9 Process Train lesson - trust the
    existing proven field set over a static CSS mandatory scan).
  - **Update (updateAttributes):** `Storage Flow Name` only (Code read-only; Start Date lives only
    in objectdates).
  - **Delete (objectdates):** `End Date` = Start Date, field id
    `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`.

## Test data
- **Fixed** test code `AUTOTEST_STFLOW` (Batch 10 changed this from the earlier unique-timestamped
  `AUTOTEST_SF_<timestamp>` scheme to match Bank/Berth's convention) - confirmed absent from
  `OV_STORAGE_FLOW` before being wired in; every run must complete TC05 (delete) to keep the code
  free for the next run.
- 4 `testdata/storage_flow_*.properties` files: `_insert` (Code/Name/Start Date + Flow
  Direction/Storage = `__FIRST__`), `_update` (Name only), `_form_verify` (Code/Name post-update),
  `_grid_verify` (Code/Name/Start Date post-update).
- Start/End dates: `2000-01-01`.
- Dedicated credentials `STORAGE_FLOW_EC_USER`/`STORAGE_FLOW_EC_PASS` (`resources/credentials.py`,
  falls back to `EC_USER`/`EC_PASS`/`sysadmin`), one per-TC Login/Logout on a single browser opened
  in Suite Setup (Bank/Berth convention).

## Dev story
Originally built 2026-07-26 as a plain, label-driven OV IUD (Playwright 7/7 + RF 4/4,
`verify_screen.py` OVERALL PASS) with a unique-timestamped code, a single suite-level login, and no
explicit grid filter. **Rebuilt 2026-08-23 via PR #472** (Batch 10 of the Bank-pattern conversion
project, `ec-bank-pattern-converter`) to the full Bank-pattern shape: fixed `AUTOTEST_STFLOW` code,
per-TC Login/Logout, properties-file-driven insert/update/verify, and explicit
`Find/Clear Storage Flow Row By Filter` grid-filter wiring - replacing the older
unique-timestamped-code/single-login/no-filter approach. Real gotcha carried forward from the
Batch-9 Process Train lesson: `Flow Direction`/`Storage` are de-facto-mandatory dropdowns (not
caught by a static mandatory-field scan) - kept from the already-proven page object/driver rather
than re-derived. Live 5/5 RF; robocop 12 issues (4 VAR02 + 5 DOC02 + 3 credentials.py baseline
noise, identical in kind/count to the merged Berth baseline, no new categories); full `tests/`
dryrun 767/767; grid-filter keyword fired 15x (output.xml-confirmed); DB self-clean 0 residual
`AUTOTEST%` rows in `OV_STORAGE_FLOW` (fresh connection, before and after). `py/storage_flow_iud.py`
(Playwright driver) was read but not modified - used as the source of truth for the mandatory
`Flow Direction`/`Storage` dropdowns; no shared T1/T2 (`manage_object.resource`/`common.resource`)
edits.

## Lessons / known risks
- `Flow Direction`/`Storage` are `__FIRST__`-filled and excluded from the round-trip form-label
  compare (their live-rendered option label is not knowable ahead of time - a resolved reference
  value can re-render as different display text after reload, same as Bank Account's
  Bank/Customer/Currency).
- Delete uses the engine's `wait_for_row_absent`-equivalent (async grid redraw); TC05 must complete
  every run or the fixed code stays "used" in EC's date-effective history.
- This is a backfill task (owner decision 2026-08-27, Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`): the RF automation itself was NOT touched by this backfill -
  only documentation/evidence artifacts were added/refreshed to match the real, already-merged
  Batch 10 state.
