# SOW - Canal IUD

_Refreshed 2026-08-28 under `docs/lean-deliverable-backfill-workorder.md` (Batch 9). This bundle
predates the lean rule (originally written 2026-07-26 for the old 4-TC argument-driven build) and
was NOT re-created from scratch — it is updated here to reflect the screen's CURRENT state after
PR #458 (merged 2026-08-23, "Canal - full Bank-pattern conversion (Batch 7)"), which is the real
automation live in `pageobjects/`/`tests/`/`testdata/` today. No RF file was touched to produce
this refresh._

## Classification
- **Screen:** Configuration > Assets > Transport Objects > Canal (BF_CODE **CO.2069**)
- **Type/pattern:** OV (Manage-Object), **Bank family**, full Bank-pattern conversion (properties-
  file-driven + explicit grid-filter wiring) — plain OV, no mandatory navigator/dropdown cascade.
- **DB view:** `OV_CANAL` (base `CANAL` table, versioned/date-effective); key `CODE`.
- **Delete:** End Date = Start Date -> row leaves `OV_CANAL` (true date-effective delete).

## Nav / grid / cells
- **Open:** treeview search "Canal" -> `label.tv-link`. Navigator = date field + **GO to load**
  (`manage_object_nav_nav:form:T_data`).
- **Grid:** shared T2 constant `${OV_MANAGE_OBJECT_TABLE}` (aliased `${CANAL_TABLE}` in
  `canal_page.resource`); single page, 2 real rows (`PANAMA`/`SUEZ`).
- **Fields resolved BY LABEL** via the shared T2 (`manage_object.resource`), zero hardcoded field
  ids except the one documented exception below:
  - **Insert (`objectForm`):** `Canal Code`, `Canal Name`, `Start Date` (mandatory). `Time Zone`
    dropdown optional, deliberately skipped.
  - **Update (`updateAttributes`):** `Canal Name` only (Code read-only there; Start/End Date live
    only in `objectdates`).
  - **Delete (`objectdates`):** `End Date` = Start Date. One deliberate hardcoded id,
    `${CANAL_DEL_ENDDATE}` = `tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input` — same documented
    shape as Bank's/Customer's own `${BANK_DEL_ENDDATE}`/`${CUSTOMER_DEL_ENDDATE}` (the row packs
    Start Date C:1 / End Date label C:2 / End Date field C:3), confirmed live via the already-
    proven Playwright driver's `END_DATE_ID` default.
- Labels are screen-prefixed ("Canal Code"/"Canal Name", not the generic Bank "Code"/"Name") —
  same shape as State's own "State Code"/"State Name" precedent (2026-08-22) — threaded through
  every T2 call via `code_label=Canal Code`.

## Test data
- Fixed test code `CANAL_KIEL` (not a generated unique code) — confirmed absent from `OV_CANAL`
  live before being wired in 2026-08-23 (only real rows are `SUEZ`/`PANAMA`); re-confirmed absent
  again live 2026-08-28 (fresh `oracledb` connection, this backfill's own evidence run).
- `testdata/canal_insert.properties` — `Canal Code=CANAL_KIEL`, `Canal Name=Kiel Canal`,
  `Start Date=2000-01-01`.
- `testdata/canal_update.properties` — `Canal Name=Kiel Canal UPDATED`.
- `testdata/canal_form_verify.properties` / `testdata/canal_grid_verify.properties` — merged
  post-update state used by TC04's find/verify round-trip.

## Dev story (from PR #458's real body)
PR #458 brought Canal's RF suite from an older **argument-driven** page object
(`Insert Canal Record`/`Update Canal Name`/`Delete Canal` keyword shapes, live 4/4) up to the full
**Bank pattern**: properties-file-driven insert/update/verify via the shared T2 keywords
(`Insert/Update Object From Properties`, `Verify Object Insert Exists/Form Record/Found/Removed/
Does Not Exist`) plus explicit grid-filter wiring (`Find/Clear Canal Row By Filter`, wired into
Update/Find/Verify-Found/Delete) — a 5-TC suite (TC01 clean-state, TC02 insert, TC03 update, TC04
find, TC05 delete). No shared T1/T2 file (`manage_object.resource`/`common.resource`) was touched
— every needed T2 keyword already existed, per the batch's shared-keyword-freeze rule. The
screen-specific gotcha carried forward from the original 2026-07-26 build: Canal's on-screen
labels are screen-prefixed, not the generic Bank "Code"/"Name" — this SOW's predecessor already
flagged it, and PR #458 kept it via `code_label=Canal Code` rather than re-discovering it live.

## Verification (PR #458, cited then; re-confirmed live 2026-08-28 for this backfill)
- Live 5/5: `EC_HEADLESS=true robot tests/Configuration/Assets/Transport_Objects/canal_iud.robot`
  — re-run 2026-08-28, 5/5 pass, first attempt (no retry needed). See `evidence/rf_batch9_2026-08-28/`.
- DB ground-truth / self-clean: fresh `oracledb` connection (this backfill's own check, 2026-08-28)
  — `SELECT CODE FROM OV_CANAL` returns only `SUEZ`/`PANAMA`; 0 `CANAL_KIEL` residual rows.
- Grid-filter keywords fired: `output.xml` grep (this run) — `Find Canal Row By Filter` x15,
  `Clear Canal Row Filter` x5 (5 wired call sites across TC02-05).
- robocop (this run, 2026-08-28): `robocop check pageobjects/.../canal_page.resource
  tests/.../canal_iud.robot` -> 9 issues (all DOC02/style-baseline, same category/count PR #458
  cited as matching Bank's own accepted baseline — no new categories).
- hygiene (this run, 2026-08-28): `py scripts/check_bundle_hygiene.py` -> exit 0, RESULT: PASS.
- dryrun (this run, 2026-08-28): `robot --dryrun tests/.../canal_iud.robot` -> 5/5 pass.

## This backfill's scope
Documentation/evidence only — refreshed SOW (this file), README, JOURNAL, evidence/ (a fresh live
+ dryrun re-run's artifacts), CHECKLIST.md, KB selector map. **No RF file
(`canal_page.resource`/`canal_iud.robot`/`testdata/canal_*.properties`) was modified.**
