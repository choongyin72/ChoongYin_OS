# SOW - Calendar Collection IUD (CD.0105)

_Backfilled 2026-08-27/28 (Batch 8, `docs/lean-deliverable-backfill-workorder.md`, owner decision
2026-08-27 retiring the lean waiver). This SOW originally described the pre-conversion,
hardcoded-field-id build (PR #144, 2026-06-xx). Sections 2/3/5/6 below are updated to describe the
CURRENT state after the Bank-pattern conversion (PR #449, 2026-08-23, Batch 6 — final of the
5-screen Date Objects pool). No RF automation files were touched by this backfill pass — this is
documentation/evidence only._

## 1. Screen identity
- **Screen:** Calendar Collection
- **BF code:** CD.0105
- **Treeview path:** Configuration > Assets > Date Objects > Calendar Collection
- **Bundle folder:** `screens/Configuration/Assets/Date_Objects/Calendar_Collection/`

## 2. Classification (DB-derived ground truth)
- **Class:** `CALENDAR_COLLECTION` -- **OV (Manage-Object)**, `TIME_SCOPE_CODE=VERSIONED` -> date-effective -> DELETE = End Date = Start Date.
- **Base table:** `CALENDAR_COLLECTION`; **OV view:** `OV_CALENDAR_COLLECTION` (7 rows at original recon; still 7 pre-existing rows confirmed at this backfill's fresh-connection self-clean re-check, 2026-08-28).
- **Toolbar:** Insert + Delete enabled. **Custom-URL OV:** grid **`nav:form:T_data`**, **NO navigator GO** (toolbar Refresh via T2's `Save And Refresh List` GO/Refresh auto-detect fallback) -- same shape as Calendar (CD.0024).
- **Pattern (current, since PR #449):** label-driven, properties-file-driven, T2-consolidated
  "Bank pattern" (mirrors `bank_page.resource`/`calendar_page.resource`), replacing the older
  per-screen bespoke Insert/Update/Delete keywords (hardcoded field ids, no properties-file-driven
  insert) that PR #144 originally built.
- **Member calendars** (the calendars belonging to a collection) live in a child grid/tab; the **object-level IUD** tested here is just Code/Name/Start Date -- the membership child grid is out of scope for object IUD.

## 3. New-Object form layout (current, confirmed live 2026-08-23 per PR #449's own field-label scan)
| Row | Field | Mandatory | Maps to |
|---|---|---|---|
| R:0:C:1:in | Code | YES (generic label "Code", NOT screen-prefixed) | OBJECT_CODE / CODE |
| R:1:C:1:in | Name | YES (generic label "Name") | NAME |
| R:2:C:1:da_input | Start Date | effective | OBJECT_START_DATE |
| R:3:C:1:da_input | End Date | no | - |
| R:4 / R:5 :C:1:in | Description / Comments | no | DESCRIPTION / COMMENTS |

- **Mandatory set = Code + Name** (Start Date = effective, Insert-only). No dropdown, no number,
  no checkbox -- confirmed live 2026-08-23 to have **NO weekday-indicator checkboxes on this EC
  build**, contrary to the pre-conversion page object's stale docstring (which had implied Calendar's
  weekday checkboxes might carry over). Simplest OV form of the batch.
- **Update (`updateAttributes`):** exposes Code (read-only), Name, Description, Comments -- Start/End
  Date are NOT part of `updateAttributes` (they live in the separate `objectdates` form, same as
  Bank/Country). Only Name is changed by the current suite.
- **Delete (`objectdates`):** End Date `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`.

## 4. Test data + known risks
- **Current (post-conversion) test code:** fixed `AUTOTEST_CALENDAR_COLLECTION` (matches Bank/Country/State's
  convention), confirmed free via a live DB check before use, and confirmed absent again (0 rows)
  by this backfill's own independent self-clean re-check.
- **Prior (pre-conversion) test code, historical only:** `AUTOTEST_CC_<unique>` (RF) / `AUTOTEST_CC_001`
  (Playwright) -- superseded by the fixed-code convention adopted across the Bank-pattern batches.
- **Risk:** custom-URL OV (grid `nav:form:T_data`, no GO) -- carried over from the Calendar lesson;
  the conversion confirmed live (2026-08-23) that `manage_object_nav` grid count=0 and GO button
  count=0, so the T2 toolbar-Refresh fallback (already built into `Save And Refresh List`) handles
  this screen with zero shared-file changes. No other risks.

## 5. Deliverables
- T3: `pageobjects/Configuration/Assets/Date_Objects/calendar_collection_page.resource` (rebuilt
  PR #449 -- Bank-pattern, label-driven, properties-file-driven).
- Suite: `tests/Configuration/Assets/Date_Objects/calendar_collection_iud.robot` (rebuilt PR #449;
  5 TCs -- clean/insert/update/find/delete).
- Properties: `testdata/calendar_collection_{insert,update,form_verify,grid_verify}.properties` (new in PR #449).
- Credentials: `resources/credentials.py` additive `CALENDAR_COLLECTION_EC_USER`/`CALENDAR_COLLECTION_EC_PASS`.
- **Playwright bundle (`playwright/ec_iud_calendar_collection.py`), `investigation/`, `evidence/`
  (original PR #144 artifacts):** left as-is, untouched by this backfill or by PR #449 -- Section H
  of `docs/IUD-DELIVERABLE-CHECKLIST.md` keeps items 4/5 permanently waived for Bank-/Area-pattern
  work (the Universal Screen Engine replaces the Playwright-driver role going forward); a NEW
  RF live-run evidence subfolder (`evidence/rf_backfill_2026-08-28/`) was added by this backfill
  pass alongside the original Playwright evidence, not in place of it.

## 6. Dev story + lessons

### Original build (PR #144, pre-conversion)
- 5th/last of 5 Date Objects screens. Recon confirmed custom-URL OV (grid `nav:form:T_data`, no GO)
  + simplest form -> clean clone of the Calendar bundle (the custom-URL OV exemplar). The Calendar
  grid-id lesson meant zero surprises here.
- T3 thin (T2 `manage_object`, Refresh fallback); no shared-file edits; full I-U-D. Stacked on CD.0024 (PR #144).
- Completed the Date Objects folder: 5/5 (pre-conversion baseline).

### Bank-pattern conversion (PR #449, 2026-08-23, Batch 6 -- FINAL batch)
- **What was built:** converted Calendar Collection from the older hardcoded-field-id IUD pattern
  to the label-driven, properties-file-driven, T2-consolidated Bank pattern, including explicit
  grid-filter wiring from day one.
- **Real gotcha hit:** did NOT trust the prior build's stale docstring (which suggested weekday
  checkboxes might be present, mirroring Calendar) -- a live field-label recon dumping every
  ECCell label in both `objectForm` (8 labels) and `updateAttributes` (4 labels) confirmed generic
  "Code"/"Name" labels and NO weekday-indicator checkboxes on this EC build.
- **Live evidence (per PR #449's own body):** RF suite 5/5 pass, first attempt, no retry. DB
  ground-truth via `DbVerify.Code Should Be Present/Absent In View` against `OV_CALENDAR_COLLECTION`
  for `AUTOTEST_CALENDAR_COLLECTION` (TC02 insert / TC05 delete). Independent fresh-connection
  check after the full run: 0 residual rows. A separate throwaway recon round-trip (`RECON_CC%`)
  also confirmed 0 residual rows afterward.
- **Rules applied (per PR #449):** recon-first; grid-filter wiring from day one (owner standing
  instruction); dedicated per-screen credential pair (additive only); fixed reusable test code
  confirmed free via DB before use; robocop (9 issues, matches established baseline) + full-tree
  dryrun (750/750) + live 5/5 + output.xml filter-fired grep (5 hits) all actually run before the
  PR.
- Stacked on CD.0024 (Calendar, PR #144-era lineage); completes the Date Objects folder + the full
  23-screen Bank-pattern candidate pool per the registry row.

### This backfill (Batch 8, 2026-08-27/28)
- Re-ran the existing, already-merged RF suite ONE more time (dryrun 5/5 + live headless 5/5,
  first attempt, no retry needed) purely to capture fresh evidence -- no automation file edits.
- Ran an independent fresh-connection self-clean re-check: 0 residual `AUTOTEST_CALENDAR_COLLECTION`
  rows, 7 pre-existing rows in `OV_CALENDAR_COLLECTION` untouched.
- Backfilled SOW/README/JOURNAL/CHECKLIST/KB-map to describe the CURRENT (post-PR #449) shape,
  since the pre-existing bundle predated both the lean rule and PR #449's own conversion.
