# SOW — Port IUD

_Backfilled 2026-08-28 (Batch 10 of `docs/lean-deliverable-backfill-workorder.md`) to reflect the
current Bank-pattern shape from PR #465 (merged 2026-08-23). This SOW originally documented the
2026-07-26 pre-conversion build; that build was **superseded**, not extended, by #465 — see
JOURNAL.md for both states._

## Classification
- **Screen:** Configuration > Assets > Transport Objects > Port (BF_CODE **CO.2003**)
- **Type/pattern:** OV (Manage-Object, plain Bank-family, `manage_object_nav`) — date-effective;
  **no mandatory navigator/dropdowns**. Full Bank-pattern conversion (Batch 9, PR #465, 2026-08-23):
  label-driven, properties-file-driven Insert/Update/Verify, explicit grid-filter wiring, matching
  `bank_page.resource`/`berth_page.resource` exactly.
- **DB view:** `OV_PORT` (base `PORT`/versioned); key `CODE`
- **Delete:** End Date = Start Date -> row leaves `OV_PORT`

## Nav / grid / cells
- **Open:** menu search "Port" -> `label.tv-link`. Navigator = single **Date + GO**; grid needs GO to populate.
- **Grid:** shared T2 `${OV_MANAGE_OBJECT_TABLE}` (= `manage_object_nav_nav:form:T_data`). **Paginated
  (2 pages)** — the shared T2 filter/row-locate keywords (`Find Object Row By Filter`/`Clear Object Row
  Filter`) already walk all pages (confirmed live 2026-08-23, re-confirmed by this backfill's live
  re-run 2026-08-28).
- **NO hardcoded field ids** — fields resolved BY LABEL via T2:
  - **Insert (objectForm):** `Port Code` (mandatory), `Port Name` (mandatory), `Start Date` (mandatory).
    Optional and skipped: End Date, Comments, Country Name (dd), Receiver Rate, Max Tanker Size,
    Canal Restriction Indicator, Canal (dd), Time Zone (dd), Pilot In/Out [hr], Carrier Alloc Priority (dd).
  - **Update (updateAttributes):** `Port Name` (Code read-only).
  - **Delete (objectdates):** `End Date` = Start Date.
- **Grid-filter wiring:** explicit `Find Port Row By Filter`/`Clear Port Row Filter` (T3, delegates to
  shared T2 `Find/Clear Object Row By Filter`) fired before/after every grid-dependent step
  (Update/Find/Verify-Found/Delete) — 15 `Find Port Row By Filter` hits confirmed via `output.xml` grep
  (both the original PR #465 run and this backfill's re-run).

## Test data
- Fixed test code `AUTOTEST_PORT` (not a generated unique code — confirmed free in `OV_PORT` via a
  fresh `oracledb` connection before use, matching Bank/Berth's convention). Start/End = `2000-01-01`.
  Update target: `AUTOTEST Port UPDATED`. Never touch the real ports (ANY_PORT_USA, GAS_NO, MID_*,
  RBS_*, RHEA_FPSO, TERMINAL_NO, TS1_*, ...).

## Dev story (pulled from PR #465's real body)
Upgraded Port from the older arg-based/no-filter page object (built 2026-07-26, 4/4 RF + 7/7
Playwright) to the full Bank-pattern shape: label-driven, properties-file-driven Insert/Update/Verify,
and explicit grid-filter wiring (`Find Port Row By Filter`/`Clear Port Row Filter` -> shared T2),
matching `bank_page.resource`/`berth_page.resource` exactly. Port's grid is paginated (2 pages) —
confirmed the shared engine's existing pager-walking behavior in the T2 filter/row-locate keywords
still works correctly, no engine change needed. Result: 5 TCs (Verify Clean State/Insert/Update/
Find/Delete), per-TC login/logout on one browser opened once in Suite Setup, fixed test code
`AUTOTEST_PORT`, dedicated `PORT_EC_USER`/`PORT_EC_PASS` credential pair. Live RF 5/5 pass; full-tree
dryrun 762/762 pass at the time; DB self-clean via fresh connection = 0 residual `AUTOTEST%` rows in
`OV_PORT`; robocop 9 issues (VAR02/DOC02-style), same count/kind as the established Berth baseline —
not a regression.

## Lessons / known risks
- **Paginated OV grids** (Port = 2 pages): a freshly inserted row can render on a later page or after
  an async redraw — never assert presence on the rendered page alone. The shared engine/T2 keywords
  handle this for all OV screens.
- Label-driven T3 removes the need to recon update-tab field ids (labels are stable across
  objectForm / updateAttributes / objectdates on this screen: Port Code / Port Name / Start Date /
  End Date).
- The Playwright driver `py/port_iud.py` was left **unchanged** by PR #465 (out of scope; the
  Universal Screen Engine is the owner-decided replacement for hand-written Playwright drivers going
  forward, per `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — its 2026-07-26 evidence (7/7) stays in
  `evidence/` as historical record alongside this backfill's fresh RF evidence.
