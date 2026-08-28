# JOURNAL — Operator Lease (OV) IUD

_Written 2026-08-28 (deliverable backfill, `docs/lean-deliverable-backfill-workorder.md` Batch 6,
first Bank-pattern wave) to cover the 2026-08-23 Bank-pattern conversion (PR #436), modeled on
`screens/Configuration/Assets/Financial_Objects/Bank/JOURNAL.md`'s structure. This bundle predated
the JOURNAL/evidence/KB-map restoration rule (Section H, `docs/IUD-DELIVERABLE-CHECKLIST.md`,
2026-08-27) — the original 2026-06-12 SOW/README/Playwright bundle is kept as history, appended to
rather than overwritten._

## Built

- **2026-06-12 (original build):** Playwright reference (`playwright/ec_iud_operator_lease.py`,
  thin config over the shared `ec_object_iud.py` engine) + `investigation/` recon scripts + the
  original SOW, using a per-run `AUTOTEST_OPL_<timestamp>` test code.
- **2026-08-23 (PR #436, Bank-pattern conversion, Batch 3 of 5 — Customer/Field Group/Licence/MMS
  Lease/Operator Lease, 5 parallel isolated clones):** rebuilt the T3
  (`operator_lease_page.resource`) and suite (`operator_lease_iud.robot`) from the older
  hardcoded-field-id, no-properties-file pattern to the label-driven, properties-file-driven,
  T2-consolidated Bank/State/Country pattern — 5 TCs (Clean State/Insert/Update/Find/Delete),
  per-TC login/logout with `OPERATOR_LEASE_EC_USER`/`OPERATOR_LEASE_EC_PASS`, new
  `testdata/operator_lease_{insert,update,form_verify,grid_verify}.properties`, explicit grid-filter
  wiring (`Find/Clear Operator Lease Row By Filter`) included from day one — not deferred to a later
  pass. Fixed test code changed to `AUTOTEST_OPERATOR_LEASE` (confirmed absent from
  `OV_OPERATOR_LEASE` via a fresh `oracledb` connection before use).

## Done well

- Full I-U-D DB-verified vs `OV_OPERATOR_LEASE` (insert Operator Lease Code/Name, update Operator
  Lease Name, delete End=Start); self-clean 0 residual, confirmed via a fresh independent
  `oracledb` connection both at PR #436's own merge and again by this backfill's 2026-08-28 re-run.
- The conversion correctly did NOT assume the screen was navigator-gated just because the top of the
  page shows a Date field + GO button — it confirmed live (direct side-by-side screenshot compare
  against the already-proven Bank screen) that this is the same universal pre-filled as-at-date
  filter Bank also carries, not a blocking mandatory nav requirement. That distinction matters: a
  shallower read could have wrongly classified this as an OV-GM screen.
- The grid held 0 real Operator Lease rows in this sandbox at conversion time, so `updateAttributes`
  labels could not be read off an existing row. Resolved via a live throwaway Insert+Delete
  round-trip (`RECON_OL_TMP`), self-cleaned and DB re-verified empty before the real suite was built
  — not guessed from a similar-looking screen's field set.
- Reused the existing `${code_label}` T2 parameter unchanged; zero shared T1/T2 file edits needed.

## Done wrong / lessons

- The original 2026-06-12 SOW/README/Playwright bundle predated the JOURNAL/evidence/KB-map
  restoration rule and PR #436's conversion — this backfill is the direct fix for that gap (owner
  decision 2026-08-27 retiring the 2026-08-23/26 lean waiver, Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- No live-run blocker, flake, or misclassification is recorded in PR #436's own body — it reports
  RF 5/5 pass on the first cited attempt, full-tree dryrun 735/735, and a clean self-clean. Nothing
  is smoothed over here: this is a genuinely clean conversion, not a disclosure gap.

## Blockers -> resolution

- No hard blockers recorded in PR #436. The only real recon obstacle — an empty grid preventing a
  live-row read for `updateAttributes` labels — was resolved via the throwaway Insert+Delete
  round-trip described above, not worked around with an assumption.
- This backfill's own evidence-capture run (2026-08-28): dryrun 5/5 pass, full-tree dryrun 883/883
  pass, live headless 5/5 pass on the FIRST attempt (no retry needed), DB self-clean confirmed 0
  residual before and after, hygiene PASS. No regression found.

## Decisions

- Playwright driver `playwright/ec_iud_operator_lease.py` and its `investigation/` recon scripts
  stay unchanged and permanently un-rebuilt for Bank-pattern work — the Universal Screen Engine is
  the owner-decided replacement for hand-written Playwright drivers going forward (Section H,
  `docs/IUD-DELIVERABLE-CHECKLIST.md`).
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows were
  already updated by PR #436 — this backfill does not re-append them.
- The fixed test code `AUTOTEST_OPERATOR_LEASE` (not a per-run timestamp, unlike the pre-conversion
  Playwright driver's `AUTOTEST_OPL_<timestamp>`) is deliberate: it must stay confirmed absent from
  `OV_OPERATOR_LEASE` before each use, and TC05 (delete) must complete every run so the code stays
  free for the next run — same convention as every other Bank-pattern-converted screen.

## Evidence

- Original 2026-06-12 build: `evidence/operator_lease_0[1-8]_*.png` + `evidence/operator_lease_results.json`.
- PR #436 conversion (2026-08-23): live RF 5/5 pass, full-tree dryrun 735/735, robocop 9 issues (4
  VAR02 + 5 DOC02, exact parity with the Bank/State/Country baseline), fresh-connection DB
  self-clean = 0 residual, 5 `Find Operator Lease Row By Filter` hits in `output.xml` — all cited in
  PR #436's own body.
- This backfill (2026-08-28): `evidence/backfill_2026-08-28/` — see that folder's own
  `results_summary.md` for the real dryrun/live-run/DB-self-clean/hygiene numbers captured by this
  task (all re-run fresh, not copied from the PR #436 body): robocop 9 issues (parity confirmed),
  dryrun 5/5, full-tree dryrun 883/883, live 5/5 on attempt 1, DB self-clean 0/0 before+after, filter
  fired 5x, hygiene PASS.
