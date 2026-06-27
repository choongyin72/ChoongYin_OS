# JOURNAL — Product Group Setup IUD (RC.0054)

**Feature / branch:** `feature/product-group-setup-iud`
**PR:** (this PR) · **Base:** master (standalone — shares only the already-merged T2)
**Dates:** 2026-06-27
**Screen:** Configuration > Assets > Royalty Objects > Product Group Setup (8th/last of the Royalty batch; the most complex — 3-tier, multi-entity, tab-gated, no navigator)

## What was built
RF full I-U-D suite for ALL 3 sub-entities (Product Group Setup, Product Group Cost, Stream Calculation
Category), 10 TCs, nested under a test product added to ALL_GENERAL. **Live 10/10, DB-verified, self-cleaning.**

## Done badly or wrongly (don't repeat)
- **Declared SCC a hard blocker / no-backing too early.** After 5 DB-name searches I parked SCC as
  "no resolvable backing" — but the backing existed under a different name (`PRODUCT_STRM_BAL_CAT`,
  "Balance" not "Calculation"). LESSON: resolve from the grid-id segment + broad search; **label != table.**
- **Called the Delete gesture "flaky" / a blocker before diagnosing.** It was cascade pollution from the
  failed update step, not a delete bug — a 30-second read-only menu probe proved the menu opens cleanly.
  LESSON: diagnose the actual DOM state before declaring a blocker (don't infer a wall from a cascade).
- **Over-asked permission earlier** (read-only recon) when autonomy + "drive through" were already given.

## Done well (keep)
- **Methodical recon** of a genuinely new screen shape (3-tier, no-nav, tab-gated) — mapped every grid,
  cell, member dd, tab, and the per-tab Insert enablement before building.
- **Diagnosed both live failures from evidence, not guesswork:** silent-reject (UI ok / DB fail → mandatory
  cells) and 2nd-save-no-rearm (Save disabled → reload). Each fix was targeted and worked.
- **Generic T3** (per-entity dicts &{SETUP_E}/&{COST_E}/&{SCC_E} + shared keywords) kept 3 entities DRY.
- **Self-clean rigor:** when run #2 left 2 rows, I cleaned them (targeted DB delete, since UI delete was
  state-polluted) and verified ALL_GENERAL back to its original 7 before continuing.
- **Checkpoint discipline:** committed a WIP backup at the blocker, then resumed and finished.

## Could improve
- Predict "label != table" for tab sub-entities from the start (check the grid-id segment first).
- Recognise the silent-reject risk pre-emptively on rich grids (fill yellow ∪ NOT-NULL before run #1).

## Blockers faced -> how resolved
1. SCC backing unfindable by name -> grid-id segment + broad search -> `PRODUCT_STRM_BAL_CAT`.
2. Inserts silent-reject -> fill mandatory yellow/NOT-NULL cells (`Fill New Row Fields`).
3. Updates Save-disabled + "flaky" deletes -> reload context before each U/D (`Enter Setup/Sub Context`);
   read-only diagnostic confirmed the delete menu itself was fine.

## Key decisions
- **COMMENTS-sentinel oracle** (present-in-view) for all 3 entities — robust where member codes aren't
  unique across groups; no shared-file/DbVerify change.
- **Nested self-contained flow** under one test product, children deleted before parent — leaves the screen
  exactly as found.
- Standalone PR off master (independent of #130/#131; shares only merged T2).

## Evidence / verification summary
- robocop clean · dryrun 10/10
- RF live #3 (headless): **TC01-TC10 10/10 PASS** — 3 entities x I-U-D, each DB-verified (present/absent-in-view)
- Independent DB re-read: `DV_PRODUCT_GROUP_SETUP`/`DV_PRODUCT_GROUP_COST`/`PRODUCT_STRM_BAL_CAT` all 0;
  ALL_GENERAL back to its original 7 products
- 10 step screenshots in `evidence/`
