# Report Context (RP.0007)

_KB selector map, backfilled 2026-08-28 (`docs/lean-deliverable-backfill-workorder.md` Batch 12).
Transcribed from the existing `report_context_page.resource` Variables/Documentation sections
(PR #487, merged 2026-08-24) — no re-scan performed, no automation touched._

## Nav path
Reporting > Excel Report Templates > Report Context (BF_CODE `RP.0007`).

## Classification
OV (Manage-Object), custom-URL variant. `CLASS_NAME=REPT_CONTEXT`, `CLASS_TYPE=OBJECT`,
`TIME_SCOPE_CODE=VERSIONED`.

**Quirk:** `class_property_cnfg.LABEL` for this class is "Reporting context" (lowercase, generic),
NOT "Report Context" (the actual menu name / `BUSINESS_FUNCTION.NAME`). Any LABEL-keyed lookup
(e.g. the stock `resolve_ec_screen.py`/`scan_ec_screen.py` scripts) will silently miss this screen.
Resolve via a direct `class_cnfg` query by `CLASS_NAME=REPT_CONTEXT` instead.

## DB view
`OV_REPT_CONTEXT` (base table `REPT_CONTEXT`, version table `REPT_CONTEXT_VERSION`).

## Grid id
`nav:form:T_data` (NOT the `manage_object_nav_...:form:T_data` variant used by GO-navigator
screens).

## Navigator
**None at all.** Confirmed live 2026-08-24: navigator fields=[], go=[]. The grid renders directly
on screen open — no mandatory Date+GO cascade. Matches the WBS/Calendar/Account/Cost Centre/
Revenue Order custom-URL-OV family. Do NOT assume this because a sibling menu entry (Report Area,
also under top-level Reporting) uses a manage-object+GO shape — Report Context does not share it.

Toolbar Refresh fires via T2's `Save And Refresh List` GO/Refresh auto-detect fallback (there is no
navigator GO button to click on this screen).

## Insert selectors
- Form: `objectForm` (New Object form).
- Field labels: plain `Code` / `Name` (NOT screen-prefixed).
- Mandatory-and-empty: `Code`, `Name`, `Start Date` only.
- Optional (present but not mandatory, left unset): `End Date`, `Description`, `Comments`.
- Driven via shared T2 `Insert Object From Properties And Verify Code` +
  `testdata/report_context_insert.properties`.

## Update selectors
- Form: `updateAttributes` (row-select form). Only `Name` is writable here — `Code` is read-only,
  `Start Date` lives only in `objectdates`, not `updateAttributes` (same pattern as Bank/WBS).
- Driven via shared T2 `Update Object From Properties` +
  `testdata/report_context_update.properties`.

## Delete selectors
- Date-effective delete: End Date = Start Date via `objectdates` tab.
- Field id: `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` (framework-invariant
  `R:0:C:1`=Start Date / `R:0:C:3`=End Date layout, same as Bank/WBS).
- Driven via shared T2 `Delete Object Via End Date`.

## Grid-filter wiring
Explicit `Find/Clear Report Context Row By Filter` wrapper keywords (in
`report_context_page.resource`) around the shared T2 `Find Object Row By Filter`/
`Clear Object Row Filter`, wired into Update/Find/Verify-Found/Delete. Confirmed fired via an
`output.xml` grep: `Find Object Row By Filter` → 15 hits (both original build and this backfill's
re-run).

## Mandatory-yellow fields (summary)
Insert: `Code`, `Name`, `Start Date`. Update: `Name` only writable. Everything else
(`End Date`/`Description`/`Comments`) is optional and intentionally left unset
(IUD-fill-only-needed-fields convention).

## Test data
Fixed test code `AUTOTEST_REPORT_CONTEXT` (not generated/timestamped) — see
`testdata/report_context_{insert,update,form_verify,grid_verify}.properties`.

## Quirks
- LABEL-lookup mismatch (see Classification above) — the single biggest gotcha for this screen.
- First live attempt of the original build was 4/5 (a `nav:form:T:sfilter0_ft_filter` visibility
  timeout inside the shared T2 grid-filter-toggle mechanism); retried clean 5/5 with zero code
  changes — a one-off environment/timing flake, not a defect. This backfill's own re-run
  (2026-08-28) passed 5/5 first attempt.
- No shared T1/T2 file edits were needed for this screen at any point.

## Last verified
2026-08-28 (documentation backfill; live suite re-run confirmed 5/5 PASS + DB self-clean). EC env:
plutodev (`db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev`), EC 14.2.4.

