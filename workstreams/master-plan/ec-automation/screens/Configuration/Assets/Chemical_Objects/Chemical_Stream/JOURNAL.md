# JOURNAL - Chemical Stream (CO.0258) OV-GM + mandatory-popup IUD

## 2026-07-30
- **Branch:** `feature/chemical-stream-iud-v3`. Previously PARKED twice: the mandatory From
  Connection popup reported "empty source list" under the first-available AS1 nav scope.
- **UNPARKED in two steps, all real facts:**
  1. Owner screenshot proved the popup HAS entries under the P1 scope (Object Type CHEM_TANK,
     P1 CT001..CT014) -> navigator switched to SPECIFIC P1 values.
  2. First P1 driver run STILL failed -> popup recon (`investigation/recon_chs_popup*.py`) found this
     is NOT the standard object_popup: `stream_node_ref_popup` has an inner navigator (inherits the
     outer scope), an **Object Type dd** (`nav:form:G:4`, EMPTY on open), an **inner GO**
     (`button:form:B`), and its list grid is **`manage_object_nav_nav:form:T_data`** (NOT
     `PopupList:form:T_data`) - the generic engine `pick_popup` / T1 popup keywords wait for
     PopupList and drive no inner steps, hence the misleading "empty source" error.
- **Built HAND-WRITTEN with screen-LOCAL popup handlers** (shared engine + T1 popup.resource
  untouched): driver `pick_from_connection_popup` + T3 `Open From Connection Popup List` /
  `Pick From Connection Popup` (split to satisfy robocop LEN03 after a first FAIL exit=1).
  Insert: Start Date FIRST (form quirk: R:0 precedes Code), Chemical Stream Type first-available,
  From Connection = first CHEM_TANK row.
- `verify_screen.py` -> **OVERALL PASS** (2nd run; 1st = robocop LEN03 only, live 4/4 both runs):
  robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4, Playwright 8/8. DB residual 0.
- **#265 lesson applied:** registry/scorecard rows column-diffed vs the Channel sibling; wording
  corrected to the popup + specific-values facts.

## Lessons
- "Popup empty source" can mean the popup NEEDS INNER DRIVING (Object Type + GO), not that data is
  missing - recon the popup's inner frame before concluding. Popup grid ids differ per popup TYPE
  (object_popup = PopupList:form:T_data; stream_node_ref_popup = manage_object_nav_nav:form:T_data).
- Third data-scope unpark in a row (Lifting Account, Well, Chemical Stream): first-available is a
  convention, not a guarantee - a known-good scope beats structural workarounds.
