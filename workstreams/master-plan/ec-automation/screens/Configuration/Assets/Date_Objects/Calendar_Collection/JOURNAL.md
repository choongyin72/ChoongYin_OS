# JOURNAL - Calendar Collection IUD (CD.0105)

_Screen: Configuration > Assets > Date Objects > Calendar Collection. Custom-URL OV,
date-effective. View `OV_CALENDAR_COLLECTION`._
_This JOURNAL covers two builds — the original PR #144 (pre-lean-rule) and the PR #449
Bank-pattern conversion (Batch 6) — plus this backfill pass (Batch 8, 2026-08-27/28) that brought
the docs up to date with the current automation, per `docs/lean-deliverable-backfill-workorder.md`._

## Built
- **PR #144 (original):** full IUD automation (OV, date-effective, custom-URL): T3, RF suite (4
  TCs clean->insert->update->delete, in-suite DB asserts), Playwright flow, recon, evidence, SOW,
  README, CHECKLIST. 5th/last of 5 Date Objects screens.
- **PR #449 (2026-08-23, Batch 6 conversion):** rebuilt the T3 (`calendar_collection_page.resource`)
  and suite (`calendar_collection_iud.robot`) to the label-driven, properties-file-driven,
  T2-consolidated Bank pattern; added `testdata/calendar_collection_{insert,update,form_verify,
  grid_verify}.properties`, dedicated `CALENDAR_COLLECTION_EC_USER`/`CALENDAR_COLLECTION_EC_PASS`
  credentials, and explicit grid-filter wiring (`Find/Clear Calendar Collection Row By Filter`)
  from day one. Added the missing TC04 Find (prior suite had only 4 TCs).
- **This backfill (Batch 8, 2026-08-27/28):** no automation changes — added/updated SOW, README,
  JOURNAL (this file), CHECKLIST.md, a new evidence subfolder, and the KB selector map, to bring
  the doc bundle up to date with PR #449's current state.

## Done well
- **PR #144:** recon FIRST (the Calendar lesson) confirmed grid `nav:form:T_data` + no GO
  (custom-URL OV) and the simplest form (Code/Name/Start Date only) before cloning -> clean clone
  of the Calendar bundle. Confirmed the "collection" does NOT make this a parent-child screen at
  the object level: member calendars are a separate child grid, out of scope. T3 thin; zero
  shared-file edits; full I-U-D.
- **PR #449:** did NOT trust the prior build's stale docstring implying weekday checkboxes might
  carry over from Calendar — a live field-label recon (8 `objectForm` labels, 4 `updateAttributes`
  labels) confirmed generic "Code"/"Name" and NO weekday checkboxes on this EC build. Fixed test
  code `AUTOTEST_CALENDAR_COLLECTION` confirmed free via DB before use. Grid-filter wiring included
  from the start (owner standing instruction) rather than retrofitted later. Zero shared-file
  edits (`resources/manage_object.resource`'s Refresh fallback already handled this screen's
  no-GO shape).
- **This backfill:** re-ran the existing suite (dryrun + live headless) exactly once, first
  attempt, no retry needed — matches the "don't re-verify from scratch, just capture evidence"
  scope of this task.

## Done wrong / lessons
- **PR #144:** clone left the lowercase test tag as `calendar` -> fixed to `calendar-collection`
  (same short-token clone-sub gap noted on Calendar; minor).
- **PR #449:** none disclosed in the PR body beyond the docstring-trust lesson already captured
  above (no flake, no wrong classification, no shared-file regression reported).
- **This backfill:** none — live run passed 5/5 first attempt; hygiene PASS; no automation touched.

## To improve
- **PR #144 era note (retained):** a clone helper that takes a token map (incl. short label + tag
  variants) would remove tag/name sub-misses across sibling clones. Worth a small generator if
  more Date-Objects-like batches come — largely superseded now by the Bank-pattern's
  properties-file-driven approach, which removed most of that per-screen bespoke code entirely.

## Blockers -> resolution
- None at either build, and none during this backfill's re-run/re-check.

## Decisions
- Object-level IUD only (member-calendar child grid out of scope -- it is not the object's
  identity). This holds unchanged across both builds.
- **PR #449:** dedicated per-screen credential pair (additive only, owner standing decision
  2026-08-22); fixed reusable test code over a generated-unique code, matching Bank/Country/State's
  convention.
- **This backfill:** kept the original Playwright bundle/investigation/evidence artifacts as
  historical record rather than deleting them; added a clearly-dated new evidence subfolder
  instead of overwriting, per item 4/5's permanent waiver (Universal Screen Engine supersedes
  hand-written Playwright drivers going forward, so no new one was built).

## Evidence
- **PR #144:** live RF 4/4 PASS; Playwright ALL PASS (`evidence/results.json`).
- **PR #449:** live RF 5/5 PASS (first attempt, no retry). DB ground-truth: TC02
  `Code Should Be Present In View OV_CALENDAR_COLLECTION`; TC05 `Code Should Be Absent In View`.
  Independent fresh-connection re-check after the run: 0 residual `AUTOTEST_CALENDAR_COLLECTION`
  rows; 0 residual `RECON_CC%` rows after a throwaway recon round-trip. Robocop 9 issues (matches
  established baseline); full-tree dryrun 750/750; output.xml filter-fired grep 5 hits.
- **This backfill (2026-08-28):** dryrun 5/5 PASS; live headless 5/5 PASS, first attempt, no
  retry. Independent fresh-connection self-clean re-check:
  `SELECT COUNT(*) FROM OV_CALENDAR_COLLECTION WHERE CODE = 'AUTOTEST_CALENDAR_COLLECTION'` = 0;
  `SELECT COUNT(*) FROM OV_CALENDAR_COLLECTION` = 7 (unchanged). robocop 9 issues on the T3+suite
  (parity with PR #449's own baseline). Hygiene `py scripts/check_bundle_hygiene.py` = PASS.
  Screenshots + `output.xml` saved to `evidence/rf_backfill_2026-08-28/` (see `RESULTS.md` there).
