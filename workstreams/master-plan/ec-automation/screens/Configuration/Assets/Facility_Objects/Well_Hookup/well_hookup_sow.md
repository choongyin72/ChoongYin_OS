# SOW - Well Hookup IUD (Configuration > Assets > Facility_Objects)

- **Screen:** Well Hookup   **BF:** CO.0108   **View:** `OV_WELL_HOOKUP`   **Base:** `WELL_HOOKUP`
- **Type:** OV-GM (manage-object, groupmodel; grid `manageObject:form:T_data`), navigator-GATED,
  date-effective. Genuine 3-level Production Unit -> Area -> Facility Class 1 navigator cascade,
  same row increasing column (`nav:form:G:0:R:1:C:1/C:2/C:3:dd`), C:4 absent - confirmed live
  2026-08-26 via `tmp/recon_well_hookup_navigator_cascade.py`.
- **Pattern:** converted to Area's FULL pattern in PR #539 (merged 2026-08-26) - structural
  conversion, not a reclassification. Still OV-GM; the navigator cascade itself is unchanged from
  the 2026-07-30 base build, now driven through the shared T2 `Apply Navigator From Properties`
  keyword instead of the old "first-available" cascade helper.
- **Navigator values (EXPLICIT, `testdata/well_hookup_navigator.properties`):**
  `Op Production Unit=AS1 EC Exploration Norway`, `Op Area=AS1_Area`,
  `Op Facility Class 1=AS1_Facility_01` - the same values the prior first-available resolution
  already used successfully, captured explicitly via a live read-only recon script.
- **Grid id:** `manageObject:form:T_data`. Grid columns (confirmed live 2026-08-26,
  `manageObject:form:T_head` scan): Well Hookup Code / Well Hookup Name / Start Date / End Date.
- **Mandatory fields (objectForm, insert):** Well Hookup Code, Well Hookup Name, Start Date, and
  Op Production Unit (this screen's own already-proven driver treats Op Production Unit as
  mandatory and fills it first - unlike Facility Class 1, which leaves its Op Production Unit/Op
  Area blank on `objectForm`). Update (`updateAttributes`): Well Hookup Name only (Code read-only).
  Delete: End Date = Start Date via `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input`
  (hardcoded id, same documented rationale as Area's/Facility Class 1's del-enddate constant).
- **Test data:** fixed test code `AUTOTEST_WH` (confirmed absent from `OV_WELL_HOOKUP` before use,
  2026-08-26 fresh `oracledb` connection), `Automation Test Well Hookup` / `... UPDATED` names,
  Start Date `2000-01-01`, End Date = Start Date.

## Dev story (from PR #539's real body, merged 2026-08-26)

Well Hookup went through two real builds: a 2026-07-30 base OV-GM IUD build (4 TCs, generated-code
Playwright driver + label-driven T3, `verify_screen.py` OVERALL PASS - RF 4/4 + Playwright 8/8), then
a 2026-08-26 structural conversion (PR #539) to Area's full pattern under the owner's standing rule
that any navigator screen matching Area's layout must follow Area's full pattern, not just get the
shared navigator-fill piece. The conversion moved the suite to 5 TCs (Verify Clean State / Insert /
Update / Find / Delete), per-TC Login/Logout on one browser opened once in Suite Setup, a fixed test
code (`AUTOTEST_WH`) instead of a timestamped one, properties-file-driven insert/update/verify via
the shared T2 keywords, explicit `Find/Clear Well Hookup Row By Filter` grid-filter wiring, the
shared `Apply Navigator From Properties` keyword driven by explicit (not first-available) navigator
values, and removed all inline DB-verify calls from the `.robot` file (DB check now lives only in
the shared T2 `Verify Object Removed`). The genuine 3-level PU -> Area -> Facility Class 1 cascade
itself was kept unchanged - this was a structural conversion of the suite shape, not a
reclassification of the screen. No shared `resources/manage_object.resource` T2 file changes were
needed. Live 5/5 PASS, DB self-clean 0 residual `AUTOTEST%` rows in `OV_WELL_HOOKUP`, grid-filter
wiring fired 15x, robocop 7 issues (2 VAR02 + 5 DOC02, matching Facility Class 1's own accepted
Area-pattern baseline - no regression), full-tree dryrun 850/850 at the time of PR #539.

- Deliverables: RF T3 `pageobjects/Configuration/Assets/Facility_Objects/well_hookup_page.resource`,
  suite `tests/Configuration/Assets/Facility_Objects/well_hookup_iud.robot`, this SOW, `README.md`,
  `JOURNAL.md`, `evidence/`, `CHECKLIST.md`, KB map `ec-ui-knowledge/screens/well_hookup.md`.
  Legacy Playwright driver `py/well_hookup_iud.py` (and this bundle's original `investigation/`
  recon script + `evidence/` screenshots from the 2026-07-30 base build) left untouched - the
  Playwright bundle role is superseded by the Universal Screen Engine per owner decision
  2026-08-27 and is not part of this backfill.
