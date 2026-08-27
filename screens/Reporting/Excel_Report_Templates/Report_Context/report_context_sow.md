# SOW — Report Context (RP.0007)

_Backfilled 2026-08-28 under `docs/lean-deliverable-backfill-workorder.md` (Batch 12, final batch).
Original build: PR #487, merged 2026-08-24. This SOW documents facts pulled from the merged
`report_context_page.resource`/`report_context_iud.robot` and PR #487's own body — nothing here is
newly invented; the automation itself is untouched by this backfill._

## Classification
- **Screen:** Reporting > Excel Report Templates > Report Context (BF_CODE `RP.0007`).
- **Type:** OV (Manage-Object), custom-URL variant, `CLASS_TYPE=OBJECT`, `TIME_SCOPE_CODE=VERSIONED`.
- **Class:** `REPT_CONTEXT` — base table `REPT_CONTEXT`, version table `REPT_CONTEXT_VERSION`,
  view `OV_REPT_CONTEXT`.
- **Pattern:** Bank pattern — label-driven, properties-file-driven, T2-consolidated (mirrors
  `bank_page.resource`/WBS/Currency exactly). Built via the `ec-bank-pattern-new-screen` skill as a
  **brand-new build** (no prior automation existed for this screen before PR #487).
- **Gotcha (real, from the build):** `class_property_cnfg.LABEL` for `CLASS_NAME=REPT_CONTEXT` is
  "Reporting context" (lowercase, generic) — NOT "Report Context" (the actual menu name /
  `BUSINESS_FUNCTION.NAME`). The stock `resolve_ec_screen.py`/`scan_ec_screen.py` LABEL-keyed lookup
  silently misses this screen as a result. Resolved by querying `class_cnfg` directly by
  `CLASS_NAME` instead of trusting the LABEL lookup.

## Navigator / grid / cell shape
- **Navigator:** NONE at all — confirmed live 2026-08-24 (`fields=[]`, `go=[]`). The grid renders
  directly on screen open; there is no mandatory Date+GO cascade (unlike sibling Report Area, also
  under top-level Reporting). Matches the WBS/Calendar/Account/Cost Centre/Revenue Order
  custom-URL-OV family, not the manage-object+GO shape.
- **Grid id:** `nav:form:T_data` (not the `manage_object_nav_...` variant).
- **Toolbar refresh:** T2's `Save And Refresh List` GO/Refresh auto-detect fallback (no navigator
  GO button exists on this screen, so the fallback path is what fires).
- **Field labels:** plain `Code` / `Name` (NOT screen-prefixed) — confirmed live via both the New
  Object form (`objectForm`) and the row-select form (`updateAttributes`) label dumps.
- **Mandatory-and-empty fields (Insert):** `Code`, `Name`, `Start Date` only. `End Date`,
  `Description`, `Comments` are all present on the form but confirmed optional and left unset
  (IUD-fill-only-needed-fields convention).
- **Delete mechanism:** date-effective delete via `objectdates` End Date = Start Date (field id
  `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`), same convention as Bank/WBS.

## Test data used
- Fixed test code `AUTOTEST_REPORT_CONTEXT` (not a generated/timestamped code), matching Bank/WBS's
  convention. Confirmed absent from `OV_REPT_CONTEXT` before the original 2026-08-24 build.
- Insert: `Code=AUTOTEST_REPORT_CONTEXT`, `Name=AUTOTEST REPORT CONTEXT`, `Start Date=2000-01-01`.
- Update: `Name=AUTOTEST REPORT CONTEXT UPDATED`.
- Delete: End Date = Start Date (`2000-01-01`) — true delete in `OV_REPT_CONTEXT`.

## Dev story (from PR #487's real body, not invented)
Brand-new RF Bank-pattern IUD suite — no prior automation existed for Report Context before this
build. First live attempt was 4/5: TC02 failed on a `nav:form:T:sfilter0_ft_filter` visibility
timeout inside the shared T2 grid-filter-toggle mechanism. The identical suite was re-run with zero
code changes and passed clean 5/5, confirming a one-off environment/timing flake rather than a
defect in the new code — no shared T1/T2 file was touched either way. DB self-clean was confirmed
via a fresh oracledb connection (`AUTOTEST_REPORT_CONTEXT`: 0 rows before and after). Full `tests/`
dryrun ran 790/790 pass on the whole tree at build time. Robocop reported 9 issues (5 DOC02 + 1
VAR02 unused-var pattern), identical in kind/count to the already-merged WBS sibling's own
baseline — not a regression. The grid-filter keyword (`Find Object Row By Filter`) was confirmed
fired via an `output.xml` grep (15 hits). No shared T1/T2 file edits were needed; a new 3-level menu
subfolder (`Reporting/Excel_Report_Templates/`) was created under `pageobjects/`/`tests/`.
