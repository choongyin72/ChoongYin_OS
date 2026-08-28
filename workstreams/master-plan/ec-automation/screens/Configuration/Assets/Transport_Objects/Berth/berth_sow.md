# SOW — Berth IUD

_Refreshed 2026-08-28 (lean-deliverable backfill, Batch 8 of `docs/lean-deliverable-backfill-workorder.md`)
to reflect the full Bank-pattern conversion landed in PR #454 (merged 2026-08-23). The "Nav / grid / cells"
and "Dev story" sections below now describe the CURRENT (post-#454) automation; the original 2026-07-26
build narrative is kept in `JOURNAL.md` for history, not deleted._

## Classification
- **Screen:** Configuration > Assets > Transport Objects > Berth (BF_CODE **CO.2012**)
- **Type/pattern:** OV (Manage-Object, `manage_object_nav`) — date-effective; plain Bank-pattern OV, **no
  navigator dropdown/cascade** (single Date + GO only). One of the **two original exemplar screens** (with
  Bank itself) the whole Bank-pattern initiative is named after — referenced as `bank_page.resource`/
  `berth_page.resource` throughout other screens' SOWs/registry rows.
- **DB view:** `OV_BERTH` (base `BERTH`/versioned); key `CODE`; 11 real rows (never touched; re-confirmed
  live via `SELECT COUNT(*) FROM OV_BERTH` = 11, 2026-08-28)
- **Delete:** End Date = Start Date → row leaves `OV_BERTH`

## Nav / grid / cells
- **Open:** menu search "Berth" → `label.tv-link`. Navigator = single **Date + GO**; grid needs GO to populate.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`). **Single page** (11 rows,
  no paginator) — unlike its folder-sibling Port (2 pages). Verified by recon, not assumed.
- **NO hardcoded field ids** — fields resolved BY LABEL via T2 `Fill OV * By Label` / `OV Field Id By Label`:
  - **Insert (objectForm):** `Berth Code` (mandatory), `Berth Name` (mandatory), `Start Date` (mandatory).
    Optional and skipped: End Date, Comments, **Port Name (dd)**, Business Unit (dd), Reserved/Design Capacity,
    Capacity Uom (dd), Op Production Unit / Op Area / Op Facility Class 1 (dds).
  - **Update (updateAttributes):** `Berth Name` (Code read-only; loaded-check via `OV Field Id By Label` on `Berth Code`).
  - **Delete (objectdates):** `End Date` = Start Date.
- **Grid-filter wiring (added PR #454, 2026-08-23):** `Find Berth Row By Filter`/`Clear Berth Row Filter`
  (`berth_page.resource`) call the shared T2 `Find/Clear Object Row Filter` explicitly on the Code column —
  wired into Update/Find/Verify-Found/Delete, matching `bank_page.resource`/`state_page.resource` exactly
  (owner, 2026-08-22: "others (Bank, State, List_Object) should follow Account... utilise same filter
  feature"). Confirmed live 2026-08-28: 15 `Find Berth Row By Filter` hits / 5 `Clear Berth Row Filter` hits
  in a fresh live-run `output.xml`.
- **Test code (changed PR #454):** fixed `AUTOTEST_BERTH` (not a `<timestamp>`-suffixed unique code) —
  matching Bank/State's convention. Confirmed free from `OV_BERTH` before/after each run; every run must
  complete TC05 (delete) so the code stays reusable.
- **Credentials (changed PR #454):** dedicated `BERTH_EC_USER`/`BERTH_EC_PASS` (falls back to `EC_USER`/
  `EC_PASS`/`sysadmin` if unset) — standing decision (owner, 2026-08-22) that every EC screen gets its own
  credential pair, plus per-TC Login/Logout (5 independent TCs, not one shared session).

## Test data
- Playwright driver (`py/berth_iud.py`, unchanged by PR #454): `AUTOTEST_BERTH_<timestamp>` unique per run.
- RF suite (`berth_iud.robot`, rebuilt PR #454): fixed `AUTOTEST_BERTH` / `AUTOTEST Berth` → updated to
  `AUTOTEST Berth UPDATED`; Start/End = `2000-01-01`. Test data lives in `testdata/berth_insert.properties`,
  `berth_update.properties`, `berth_form_verify.properties`, `berth_grid_verify.properties` (all new in
  PR #454). Never touch the real berths (MID_*, RBS_LNG_JETTY_*, TS1_BERTH_*).

## Dev story
**Original build (2026-07-26):** Recon-first (DB `CLASS_TYPE=OBJECT` ⇒ OV; live form). Two predictions from
the Port sibling were verified WRONG by recon: Berth is single-page (not paginated like Port) and its Port
Name dropdown is optional (not a mandatory reference). Built label-driven from the start. Playwright driver
→ INSERT/UPDATE passed; DELETE first failed the grid-absence check — DB confirmed the row WAS deleted, so
the grid was just mid-async-redraw at check-instant; fixed generically via a new engine `wait_for_row_absent`
helper. Re-run → 7/7. RF T3+suite (label-driven, 4-TC, one shared login) → live 4/4.

**PR #454 "Berth Bank-pattern completion" (Batch 7, merged 2026-08-23):** rebuilt `berth_page.resource`/
`berth_iud.robot` from the July build's partially label-driven shape to the full properties-file-driven,
T2-consolidated Bank/State pattern — added `Insert Object From Properties And Verify Code`/`Update Object
From Properties`/`Verify Object Insert Exists`/`Verify Object Form Record`/`Verify Object Found`/`Verify
Object Does Not Exist` consolidated keywords and explicit `Find/Clear Berth Row By Filter` grid-filter
wiring, matching `bank_page.resource`/`state_page.resource` exactly. Suite went from 4 TCs (shared session)
to 5 TCs (TC01 clean-state check added) with per-TC Login/Logout and the fixed test code `AUTOTEST_BERTH`.
Recon-first via the existing KB map (`ec-ui-knowledge/screens/berth.md`) + the already-proven Playwright
driver `py/berth_iud.py` — no live-DOM re-scan needed, both were mutually consistent on mandatory fields
Berth Code/Berth Name/Start Date. Live run: 5/5 pass, DB self-clean confirmed via a fresh connection (0
residual `AUTOTEST_BERTH` rows). Full-tree dryrun: 753/753 pass. No changes to `resources/manage_object.resource`
or `resources/common.resource` (shared T1/T2 untouched). robocop on `berth_page.resource`/`berth_iud.robot`:
pre-existing DOC02/COM04/DOC03/MISC06 warnings confirmed to match the exact same baseline already present on
`bank_iud.robot`, not a new issue introduced by the change.

**This backfill (2026-08-28, Batch 8):** no automation touched. Re-ran dryrun (5/5) and a fresh live run
(5/5, output.xml/log.html/report.html + screenshots captured to `evidence/`) purely as evidence capture;
robocop re-run (9 issues, same DOC02/COM04/DOC03/MISC06 baseline class, confirmed against Bank's own
robocop output — 13 issues, same category — not a new class); hygiene `check_bundle_hygiene.py` → PASS;
DB re-read confirmed `OV_BERTH` still has exactly 11 real rows and 0 residual `AUTOTEST_BERTH` rows.

## Lessons / known risks
- **Don't assume folder-siblings match** — Port (paginated, its own optional dds) vs Berth (single page,
  optional Port-ref dd). Recon each; both predictions were wrong here (2026-07-26 build).
- **Delete needs absence-polling too** — after delete+GO the grid redraws async; the Playwright engine
  asserts with `wait_for_row_absent`, never an immediate `not row_exists`. RF's Browser library auto-wait
  already tolerates the same redraw.
- **Berth is one of the two exemplar screens** — any regression here is high-blast-radius since other
  screens' docs point at `berth_page.resource` as a reference pattern; treat with the same care as Bank.
