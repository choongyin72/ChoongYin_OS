# JOURNAL - Create Calculation (CO.1042) TV-style calc-header IUD

## 2026-07-31
- **Branch:** `feature/create-calculation-iud`. Was a "name unverified" list item - owner supplied
  the real treeview label ("Calculation" = Create Calculation).
- **Prior art honoured:** DeepDiveLearnings/ec-calc-lab (branch feature/ec-calc-lab) had mapped this
  screen (recon09/10); its step-5 rule (prove the delete path in the same pass) held. Memory rule
  "No Raw DB for EC Calc Config" respected - all writes via the UI.
- **Recon facts:** nav = Date + ONE mandatory Calculation Context dd (14 contexts, first-available
  'Cargo Load/Unload') + GO; grids calculation / calculation_version / static_param; insert menu
  item = 'Public Calculations'.
- **Three empirical fixes, each from a real failure artifact:**
  1. First save SILENTLY rejected -> failure screenshot showed C4 Period/C5 Type as mandatory-YELLOW
     DROPDOWNS on the blank row (plain text on saved rows) + an UNSAVED CHANGES dialog after GO.
     Blank-row re-recon gave their dd ids; values 'Day'/'Equations' from sibling rows.
  2. Header C1 name edit did not persist -> failure screenshot revealed the VERSIONS grid (the
     authoritative Calculation Name) + the purpose-built DELETE CALCULATION button. Update rewired
     to `calculation_version:form:T:0:C0_in`.
  3. Delete rewired from End=Start to the DELETE CALCULATION button (+ YES confirm) - physically
     removes calc + version, DB-verified.
- One dryrun FAIL (missing manage_object.resource import for Save And Refresh List) - fixed, re-ran.
- `verify_screen.py` -> **OVERALL PASS**: robocop 0, hygiene 0, dryrun 4/4, LIVE RF 4/4,
  Playwright 8/8. Self-clean 0 residual (a mid-investigation leftover row was cleaned by the
  driver's TV-style pre-clean on the next run).

## Lessons
- TV blank rows can render mandatory dds that are INVISIBLE on saved rows (text render) - always
  re-recon the BLANK row, not just existing rows.
- "UI accepted, DB unchanged" on a dual-grid screen -> the edited cell may be a MIRROR; find the
  authoritative grid (here: VERSIONS).
- Purpose-built delete buttons beat family-default End=Start - check the panel buttons before
  assuming the delete gesture.
