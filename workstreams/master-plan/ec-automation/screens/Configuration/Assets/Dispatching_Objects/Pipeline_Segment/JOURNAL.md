# JOURNAL — Pipeline Segment IUD

_Screen: Configuration > Assets > Dispatching Objects > Pipeline Segment (OV-GM,
Business-Unit-gated). View `OV_PIPELINE_SEGMENT`. This JOURNAL was backfilled 2026-08-27 under the
retired-lean-waiver work order (`docs/lean-deliverable-backfill-workorder.md`, Batch 3; Section H
of `docs/IUD-DELIVERABLE-CHECKLIST.md`) — this screen never had a `screens/` bundle at all before
this backfill. PR #558 (the Area-pattern conversion) is the source of the "Built" and "Done well"
content below, pulled from its real PR body and `docs/ec_screen_registry.md`'s row, not invented._

## Built

### Original build (live-verified 2026-06-12)
- RF page object + suite (4 TCs, suite-level login, generated/timestamped test code, inline
  DB-verify calls) — `pipeline_segment_page.resource` + `pipeline_segment_iud.robot`. No
  `screens/` documentation bundle was ever created for this build.

### Area-pattern conversion (PR #558, merged 2026-08-26)
- Live read-only DOM recon (temp recon `.robot` files, deleted before commit) re-confirmed the
  navigator is a single mandatory Business Unit dropdown at `nav:form:G:0:R:1:C:1:dd` — the SAME
  single-dropdown shape as Area's own Production Unit navigator. A second dropdown at `C:2`
  ("Pipeline") is confirmed `mandatory:false` — an optional grid filter, not a scope mismatch, so
  no entry was needed in `docs/navigator-screens-not-matching-area.md`.
- Converted the RF IUD suite from the OLD bespoke shape to the full Area-pattern structure:
  properties-file-driven navigator via the shared `Apply Navigator From Properties` T2 keyword,
  per-TC login/logout, 5 TCs (added TC04 Find), a fixed test code (`AUTOTEST_PIPELINE_SEGMENT`,
  confirmed 0 rows before use, replacing the old timestamped code), a dedicated credentials pair
  (`PIPELINE_SEGMENT_EC_USER`/`PIPELINE_SEGMENT_EC_PASS` in `resources/credentials.py`, additive
  only), explicit grid-filter wiring (`Find/Clear Pipeline Segment Row By Filter`), and zero
  inline DB-verify calls left in the `.robot` file (DB proof now comes solely from the shared T2
  `Verify Object Removed` + the mandatory live-run self-clean check).
- New test-data files: `testdata/pipeline_segment_{navigator,insert,update,form_verify,
  grid_verify}.properties`.
- The screen's genuine Business Unit navigator + GO gesture and its genuine mandatory "Pipeline
  Name" insert dropdown were KEPT unchanged — this was a structural conversion, not a
  reclassification of the screen.
- Registry (`docs/ec_screen_registry.md`) and scorecard (`docs/automation-scorecard.md`) rows
  MODIFIED in place; new R38 sections added to `docs/bank-pattern-conversion-checklist.md` and
  `docs/grid-filter-standardization-checklist.md`.

### This backfill (2026-08-27)
- Added the entire `screens/Configuration/Assets/Dispatching_Objects/Pipeline_Segment/` bundle
  from scratch (it never existed before): `pipeline_segment_sow.md`, this `JOURNAL.md`,
  `README.md`, `CHECKLIST.md`, the KB selector map `ec-ui-knowledge/screens/pipeline_segment.md`,
  and `evidence/backfill_2026-08-27/` (fresh dryrun + live re-run captured as evidence of the
  already-proven suite — no automation code touched).

## Done well
- Full I-U-D DB-verified vs `OV_PIPELINE_SEGMENT` (insert Pipeline Segment Code/Name, update
  Pipeline Segment Name, delete End=Start absent); self-clean 0 residual, confirmed via a FRESH
  oracledb connection both before and after the live run (PR #558 body: pre-run check found the
  fixed test code free, independent post-run self-clean check found 0 residual `AUTOTEST%` rows).
- Screen-prefixed labels confirmed live, not assumed: PR #558's page object documents that
  `objectForm`/`updateAttributes` use "Pipeline Segment Code"/"Pipeline Segment Name"
  (SCREEN-PREFIXED, like Area's own "Area Code"/"Area Name"), NOT the generic "Code"/"Name" that
  Bank/Object List use.
- Full-tree dryrun stayed 100% pass (878/878) at conversion time (per PR #558 body); this
  backfill's own fresh dryrun re-confirmed the Pipeline Segment suite alone: 5/5 PASS.
- Robocop parity check performed and passed: 7 issues (2x VAR02 + 5x DOC02) on the 2 changed
  files, identical count/kind to Area's own established baseline — confirmed independently again
  during this backfill (also cross-checked against Meter's own conversion, PR #554).
- Filter keyword fired 15 times (`grep -c "Find Object Row By Filter" output.xml`), matching PR
  #558's cited count exactly, on this backfill's own passing retry run.

## Done wrong / lessons
- **Real shared-checkout git-plumbing incident, disclosed at PR #558's own body, NOT smoothed
  over here:** this session's shared repo checkout had its HEAD moved to a detached state by
  concurrent agents working other screens (Contract Inventory/Property/Pilot mid-conversion at the
  same time). Rather than risk cross-contaminating Pipeline Segment's commit with another
  in-flight agent's uncommitted state on the shared branch, PR #558's commit was built via
  **isolated git plumbing** (`read-tree`/`hash-object`/`commit-tree` against the shared branch's
  fork point) — producing a commit containing ONLY the 12 Pipeline Segment files, independent of
  whatever else the shared working tree held at that moment. PR #558's own body notes that
  `check_bundle_hygiene.py`'s live overall exit code at build time reflected the OTHER in-flight
  agents' state too, not a Pipeline Segment defect — Pipeline Segment's own R38 four-doc-set
  requirement was satisfied within its own diff regardless. This is the same class of
  multi-agent-collision risk disclosed on Contract Area's sibling backfill (PR #542 vs #546
  branch-name collision), but caught and avoided BEFORE the commit landed here, via isolated git
  plumbing rather than a shared-branch push.
- No other regressions or wrong turns disclosed in PR #558's body for this specific conversion.
- **Backfill-specific: one real live-run flake, disclosed not hidden.** The FIRST evidence-capture
  attempt of `EC_HEADLESS=true robot ...` failed all 5 TCs with `Could not find active page` /
  `Target page, context or browser has been closed` — the browser context died mid-suite.
  `tasklist | grep -i chrome` immediately after showed 0 chrome processes running (already torn
  down), consistent with resource contention from other agents' concurrent live runs in this
  shared environment at the time, not a Pipeline Segment code defect. An immediate retry of the
  identical, unmodified command passed clean: 5/5 PASS. Reported here as a real regression
  candidate that self-resolved on retry, per this task's explicit instruction not to silently
  smooth over a live-run failure.

## Blockers -> resolution
- **Shared-checkout detached-HEAD risk** (PR #558's own build) — resolved by building the commit
  via isolated git plumbing rather than committing on the shared, possibly-contaminated working
  tree. No data loss; the merged PR contains exactly the 12 Pipeline Segment files.
- **Live-run flake** (this backfill, 2026-08-27) — resolved by an immediate retry after confirming
  0 stray chrome processes; the retry passed 5/5 on the first attempt with no code change.
- No other hard blockers during the conversion or this backfill.

## Decisions
- Playwright bundle stays waived permanently for Area-pattern work (owner decision 2026-08-27,
  `docs/IUD-DELIVERABLE-CHECKLIST.md` Section H) — no Playwright bundle is built for this screen;
  the Universal Screen Engine is the owner-decided replacement going forward.
- The RF suite is the maintained/live test for this screen; there is no legacy Playwright
  reference to preserve (unlike Contract Area/Sub Area's earlier builds — Pipeline Segment's
  original 2026-06-12 build was RF-only).
- Code lives in `ec-automation`; `ec-ui-knowledge/` stays MD-only.

## Evidence
- PR #558 conversion (2026-08-26): live run `5 tests, 5 passed, 0 failed` (TC01-TC05), 15 `Find
  Object Row By Filter` hits in output.xml, robocop 7 issues (parity with Area), full-tree dryrun
  878/878 — all cited in the PR body.
- This backfill (2026-08-27): `evidence/backfill_2026-08-27/` — `dryrun/` (5/5 PASS,
  `log.html`/`report.html`/`output.xml`) and `live/` (the PASSING RETRY's artifacts, 5/5 PASS
  headless, `log.html`/`report.html`/`output.xml`; the failing first attempt's raw output was not
  additionally archived, only disclosed above and in `summary.json`), plus a DB self-clean result
  (`OV_PIPELINE_SEGMENT`: 0 rows for `AUTOTEST_PIPELINE_SEGMENT`, 0 residual `AUTOTEST%`, fresh
  connection, run after the passing retry), a re-confirmed 15-hit filter-fired grep, a
  re-confirmed 7-issue robocop parity check against Area's own baseline, and
  `py scripts/check_bundle_hygiene.py` → `RESULT: PASS`. Full detail in
  `evidence/backfill_2026-08-27/summary.json`.
