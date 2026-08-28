# JOURNAL — Account Mapping IUD

_Refreshed 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 8)
to cover the 2026-08-23 Bank-pattern conversion (PR #450), modeled on
`screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s structure. The original
2026-06-11/12 entry is kept below as history._

## Built
- **2026-06-11/12 (original build):** Playwright driver `playwright/ec_iud_account_mapping.py`
  (thin config over the shared engine) + `investigation/financial_objects_recon.py`. Original RF
  suite existed but its live batch was reported as "TC02 blocked; suite preserved in
  tests/.../_parked/" using per-run-timestamped `AUTOTEST_AM_<timestamp>` codes and __FIRST__
  -available dropdown picks (see the superseded v1.0 SOW).
- **2026-08-23 (PR #450, Bank-pattern conversion, Batch 6, FINAL screen of the original 23-screen
  candidate pool):** rebuilt (not merely un-parked) the T3
  `pageobjects/Configuration/Assets/Financial_Objects/account_mapping_page.resource` and suite
  `tests/Configuration/Assets/Financial_Objects/account_mapping_iud.robot` from the older
  hardcoded-field-id pattern to the label-driven, properties-file-driven, T2-consolidated Bank
  pattern (matching Bank/Customer/Cost Object Mapping), per-TC Login/Logout. New
  `testdata/account_mapping_{insert,update,form_verify,grid_verify}.properties`; additive
  `ACCOUNT_MAPPING_EC_USER`/`ACCOUNT_MAPPING_EC_PASS` in `resources/credentials.py`. Switched from
  per-run-timestamped codes to the FIXED test code `AUTOTEST_AM` (confirmed absent from
  `OV_FIN_ACCOUNT_MAPPING` before use).

## Done well
- Full I-U-D DB-verified vs `OV_FIN_ACCOUNT_MAPPING` (insert, update Name+Description, delete
  End=Start); fresh oracledb connection (localhost:1521/ORCL, ECKERNEL_EC) confirmed 0 residual
  `AUTOTEST_AM` rows after the PR #450 run (75 rows total, unchanged before/after).
- Reused the EXACT reference-dropdown combination this screen's own prior Playwright IUD bundle
  already proved live-PASS on 2026-06-12 (this bundle's `account_mapping_sow.md`/
  `evidence/account_mapping_results.json`) instead of guessing a new combination — a genuine
  reuse-of-prior-proof, not a fresh trial-and-error pick.
- Live DOM recon correctly identified that this screen's mandatory-dropdown CSS class sits on the
  input/dd-span itself, one level deeper than the usual wrapping-tableCell technique used on VAT
  Code/Customer/Cost Object Mapping — confirmed via a raw outerHTML/class dump rather than assumed
  from a similar-looking screen.
- Confirmed live that this is NOT a navigator-scope mismatch despite the "Mapping" name (genuine
  Code/Name manage-object OV, `objectForm`-New-Object flow, GO-button locator 0 matches) before
  proceeding, per the batch-6 shared-findings doc's explicit instruction to verify this live rather
  than assume from the screen name.
- Grid-filter wiring (`Find/Clear Account Mapping Row By Filter`) included from day one, confirmed
  fired 5x via a live output.xml grep — not bolted on after the fact.
- Isolated sparse-checkout clone under `Workplaces/account_mapping/`, own feature branch, synced
  with master before push — no shared-file (T1/T2) edits.

## Done wrong / lessons
- **Line Item Type re-render gotcha (1 genuine, evidence-based retry — not blind trial-and-error):**
  the field re-renders as the short internal code `ALL` after any `updateAttributes` reload,
  instead of the literal `All Line Item Types` text picked at Insert time. Root-caused via the
  exact live failure text ("Field 'Line Item Type' shows 'ALL' in updateAttributes, expected 'All
  Line Item Types'") — the SAME documented re-render gotcha as DOA Credit Limit's Role Name
  (Batch 4). Fix: excluded Line Item Type from the live-DOM round-trip form-label list
  (`@{ACCOUNT_MAPPING_FORM_LABELS}`), relying on DB ground truth (TC02's `Code Should Be Present In
  View` DbVerify assertion) for that field instead.
- The original 2026-06-11/12 SOW/README predated the JOURNAL/evidence/KB-map restoration rule and
  PR #450's conversion — this backfill is the direct fix for that gap (owner decision 2026-08-27
  retiring the 2026-08-23/26 lean waiver, Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`).

## Blockers -> resolution
- The Line Item Type re-render (above) is the only disclosed live blocker in PR #450's own body —
  resolved within the 2-strike cap (1 retry), no data damage, no grinding past the retry limit.
- This backfill's own evidence-capture run: see "Evidence" below for the actual result (pass/fail,
  retry count) of the one live re-run performed for this backfill.

## Decisions
- Playwright driver `playwright/ec_iud_account_mapping.py` and its
  `investigation/financial_objects_recon.py` stay unchanged and permanently un-rebuilt for
  Bank-pattern work — the Universal Screen Engine is the owner-decided replacement for hand-written
  Playwright drivers going forward (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows were
  updated IN PLACE by PR #450, not duplicated — this backfill does not touch them again.
- The fixed test code `AUTOTEST_AM` (not per-run timestamped) is deliberate, since PR #450: it must
  be confirmed absent from `OV_FIN_ACCOUNT_MAPPING` before first use, and TC05 (delete) must
  complete every run so the code stays free for the next run.
- Kept `ACCOUNT_MAPPING_TABLE` (`manageObject:form:T_data`) as its own screen-local grid-id
  constant rather than the shared T2 `${OV_MANAGE_OBJECT_TABLE}` (which resolves to the
  navigator-based `manage_object_nav_nav:form:T_data`) — this screen genuinely has no navigator,
  and pointing at the wrong constant would silently target the wrong grid.

## Evidence
- Original 2026-06-12 Playwright run: `evidence/account_mapping_01_loaded.png` through
  `account_mapping_08_final_state.png` + `evidence/account_mapping_results.json`.
- PR #450 conversion (2026-08-23): live RF 5/5 pass (1 retry, see "Done wrong / lessons"), fresh
  oracledb connection self-clean = 0 residual `AUTOTEST_AM` rows in `OV_FIN_ACCOUNT_MAPPING` (75
  total rows, unchanged before/after), grid-filter wired 5x confirmed via output.xml grep — all
  cited in PR #450's own body.
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` — see that folder's own
  `results_summary.md` for the dryrun/live-run/DB-self-clean numbers actually captured by this
  task (real numbers, not copied from the PR #450 body).
