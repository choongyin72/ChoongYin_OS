# JOURNAL — State Lease IUD

_Screen: Configuration > Assets > Commercial Objects > State Lease (OV, plain manage-object,
no mandatory navigator/cascade). View `OV_STATE_LEASE`._
_This JOURNAL is a lean-deliverable backfill (owner decision 2026-08-27, Section H of
`docs/IUD-DELIVERABLE-CHECKLIST.md`) — content is pulled from the real conversion PR (#440,
merged 2026-08-23, Batch 4) and the pre-existing bundle files (SOW/README/evidence dated
2026-06-12), not invented after the fact._

## Built
- **2026-06-12 (original):** standalone Playwright reference flow (`playwright/ec_iud_state_lease.py`,
  thin config over the shared `../../Basic_Objects/_shared/iud_engine.py`) generated from the
  section recon `investigation/commercial_objects_recon.py`. RF suite existed already but used the
  older hardcoded-field-id pattern.
- **2026-08-23 (PR #440, Batch 4):** converted the RF suite —
  `pageobjects/Configuration/Assets/Commercial_Objects/state_lease_page.resource` (T3, rewritten,
  +172/-58) and `tests/Configuration/Assets/Commercial_Objects/state_lease_iud.robot` (suite,
  rewritten to 5 TCs, +46/-42) — from the old hardcoded-field-id pattern to the label-driven,
  properties-file-driven, T2-consolidated "Bank pattern." Added 4 new properties files
  (`testdata/state_lease_{insert,update,form_verify,grid_verify}.properties`), additive
  `STATE_LEASE_EC_USER`/`STATE_LEASE_EC_PASS` credentials, and explicit grid-filter wiring
  (`Find State Lease Row By Filter` / `Clear State Lease Row Filter`) from day one — matching the
  owner's "others should follow Account... utilise same filter feature" instruction.
- **2026-08-28 (this backfill):** added SOW refresh, this JOURNAL, `CHECKLIST.md`, KB selector map
  `ec-ui-knowledge/screens/state_lease.md`, and a fresh evidence re-run — no RF/page-object files
  touched.

## Done well
- Full I-U-D-Find DB-verified vs `OV_STATE_LEASE`: insert (Code/Name/Start Date/Description),
  update (Name + Description), find (grid + form round-trip), delete (End Date = Start Date, true
  delete — row leaves `OV_STATE_LEASE`).
- Recon-first discipline: PR #440 did a live field-inventory scan of `objectForm`/`updateAttributes`
  before writing any properties file, which is what surfaced that this screen labels its fields
  "State Lease Code"/"State Lease Name" (screen-prefixed) rather than Bank/Customer's generic
  "Code"/"Name" — avoided a wrong-selector assumption before it happened.
- No mandatory reference dropdowns exist on this screen, so no `__FIRST__`/literal-value resolution
  was needed — simpler than Vendor/Product Description in the same batch.
- Grid-filter wiring (`Find`/`Clear State Lease Row Filter`) included from day one, per the
  grid-filter-standardization convention, rather than as a follow-up patch.
- Full-tree dryrun 740/740 PASS and live 5/5 PASS both cited in the PR body with a fresh
  `oracledb` connection for the DB-verify (not a cached/session connection).

## Done wrong / lessons
- A stray `RECON_STL` row was left behind by an earlier interrupted recon attempt (before the final
  PR #440 build). It was found and cleaned up, then DB-reconfirmed absent, before the live run that
  produced the cited 5/5 evidence — a reminder that any interrupted probe/recon script must be
  DB-reverified clean before treating a screen as "clean state" for the next attempt.
- The bundle's SOW/README predated the Bank-pattern conversion (still described the old
  hardcoded-field-id DOM paths and a timestamp-suffixed test code) until this backfill refreshed
  them — a live artifact (RF automation) moved on while its documentation bundle did not, which is
  exactly the gap Section H of the deliverable checklist exists to close.

## Blockers -> resolution
- No live blockers reported in PR #440's body beyond the stray-row cleanup above; robocop ran clean
  relative to baseline (7 issues: 2 VAR02 + 5 DOC02, fewer than the 9-issue baseline for this batch).

## Decisions
- Playwright driver + `investigation/` recon scripts stay as historical artifacts only (2026-06-12
  build) — no new Playwright bundle is built for this screen going forward; the Universal Screen
  Engine (`py/engine.py`) is the owner-decided replacement (Section H, items 4/5 stay waived).
- RF suite is the current, maintained automation for State Lease; this bundle's SOW/README now
  point callers at the RF commands, not the legacy Playwright script, as the primary path.

## Evidence
- Playwright (historical, 2026-06-12): `evidence/state_lease_0[1-8]_*.png` + `evidence/state_lease_results.json`
  (login/navigate/clean/insert/update/delete all PASS).
- RF (PR #440, 2026-08-23): full-tree dryrun 740/740 PASS; live headless 5/5 PASS
  (TC01 Verify Clean State, TC02 Insert, TC03 Update, TC04 Find, TC05 Delete); DB self-clean via a
  fresh oracledb connection, 0 residual `AUTOTEST_STL` rows before and after; `Find State Lease Row
  By Filter` confirmed fired 5 times via output.xml grep.
- RF (this backfill, 2026-08-28): see `evidence/` (this bundle) and `CHECKLIST.md` items 11/12/13/15
  for the re-run citation.
