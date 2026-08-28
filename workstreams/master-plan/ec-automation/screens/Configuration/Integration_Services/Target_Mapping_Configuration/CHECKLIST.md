# IUD Task — Deliverable Checklist — Target Mapping Configuration (IS.0002)

_Copied from `docs/IUD-DELIVERABLE-CHECKLIST.md`. This screen is genuinely FIND-ONLY by owner
confirmation (not a build limitation) — Insert/Update/Delete toolbar items are disabled/absent on
this screen. Items tied to that scope are marked N/A with the owner-confirmed reason, per
instruction, not treated as gaps. Backfilled 2026-08-28, Batch 12 of
`docs/lean-deliverable-backfill-workorder.md`, against the already-merged PR #488
(2026-08-24)._

## Step 0. CHECK-EXISTING-FIRST GATE
- [x] **0a.** `ec-ui-knowledge/screens/target_mapping_configuration.md` did not exist before this
      backfill — created now (see item 20).
- [x] **0b.** `grep -ril "target_mapping_configuration" workstreams/master-plan/ec-automation/{py,pageobjects,tests,screens}`
      → found: `pageobjects/Configuration/Integration_Services/target_mapping_configuration_page.resource`,
      `tests/Configuration/Integration_Services/target_mapping_configuration_find.robot`. Existing
      impl confirmed and REUSED as-is — this backfill adds docs/evidence only, no automation edits.
- [x] **0c.** N/A for this screen's original build — bespoke Find-only page object, no shared
      OV-IUD engine applies (no Insert/Update/Delete exists to drive).

## A. Bundle artifacts — `screens/Configuration/Integration_Services/Target_Mapping_Configuration/`
- [x] **1. `target_mapping_configuration_sow.md`** — classification, non-standard nav/GO/grid ids,
      test data, dev story from PR #488's real body.
- [x] **2. `README.md`** — bundle overview + exact run commands (dryrun, live headless, DB
      row-count-unchanged check).
- [x] **3. `JOURNAL.md`** — Built/Done well/Done wrong/Blockers/Decisions/Evidence, pulled from
      PR #488's real body + this backfill's own re-run.
- [ ] **4. `playwright/...`** — N/A, permanently waived (Section H): Universal Screen Engine
      replaces hand-written Playwright drivers going forward; not built for this screen.
- [ ] **5. `investigation/`** — N/A, permanently waived (Section H), same reason as #4.
- [x] **6. `evidence/`** — real live-run artifacts captured this session: `log.html`,
      `report.html`, `output.xml`, `tmc_tc01_clean_load.png`, `tmc_tc04_found.png`,
      `playwright-log.txt` (all well under the 2MB raw-commit limit; largest is `log.html` at
      ~258KB).
- [x] **7. `CHECKLIST.md`** — this file.

## B. RF files — treeview-mirrored
- [x] **8. T3 page object** `pageobjects/Configuration/Integration_Services/target_mapping_configuration_page.resource`
      — pre-existing (PR #488), NOT modified by this backfill.
- [x] **9. Suite** `tests/Configuration/Integration_Services/target_mapping_configuration_find.robot`
      — pre-existing (PR #488), NOT modified by this backfill. Named `_find` not `_iud`
      intentionally: TC01 (clean-load) + TC04 (find) only, no TC02/TC03/TC05.

## C. Verification gates
- [x] **10. robocop clean** — re-ran this session: `robocop check tests/.../target_mapping_configuration_find.robot pageobjects/.../target_mapping_configuration_page.resource` → `No issues found.`
- [x] **11. `--dryrun` N/N PASS** — suite: **2/2 PASS**. Full tree: **883/883 PASS** (grown since
      PR #488's 792/792; no collisions), both re-run this session.
- [x] **12. LIVE headless run N/N PASS** — **2/2 PASS** (`EC_HEADLESS=true`), re-run this session.
      (Screen has no headed-vs-headless distinction issue reported; original PR also ran headless.)
- [x] **13. DB ground-truth** — `Target Mapping Configuration Row Should Exist In DB` asserts
      `OV_IMP_TARGET_MAPPING` contains the row with EC Key `ecValue16` via
      `Code Should Be Present In View` (DbVerify). Confirmed passing as part of TC04 in this
      session's live run.
- [ ] **14. FULL I-U-D scope** — **N/A, owner-confirmed.** This screen does NOT support
      Insert/Update/Delete: Insert and Delete toolbar `<li>` both carry class
      `ui-submenu-state-disabled`; no Update icon exists at all (count=0), confirmed live in the
      original build session. Only Find (TC04) + clean-load (TC01) apply. This is a genuine screen
      limitation, not a gap in the automation.
- [x] **15. Self-clean confirmed** — N/A in the usual sense (nothing is ever inserted); equivalent
      proof is the DB row-count-unchanged check: fresh oracledb connection,
      `OV_IMP_TARGET_MAPPING` row count **117 before -> 117 after** the live run, re-verified this
      session (matches PR #488's original 117 -> 117 exactly).
- [x] **16. Hygiene PASS** — `py scripts/check_bundle_hygiene.py` → `RESULT: PASS` (repo-wide scan
      this session; the one WARN reported is pre-existing in Contract Area's `investigation/`,
      unrelated to this screen).

## D. Delivery
- [x] **17. Registry row** — already present, appended in PR #488
      (`workstreams/master-plan/ec-automation/docs/ec_screen_registry.md`, line ~345). Not
      re-appended by this backfill (would violate append-only/no-duplicate).
- [x] **18. Scorecard row** — already present, appended in PR #488 (`docs/automation-scorecard.md`).
      Not re-appended by this backfill.
- [x] **19. PR** — this backfill's own PR (`docs/target-mapping-configuration-backfill-artifacts`),
      standard body, base branch master, R8 synced before push, never self-merged.

## E. Knowledge base
- [x] **20. KB selector map** `ec-ui-knowledge/screens/target_mapping_configuration.md` — created
      by this backfill (did not exist before): nav path, DB view, grid id, non-standard
      navigator/GO ids, the real pre-existing find-target row, last-verified date.
- [x] **21. Reuse clause** — Step 0 found the screen already implemented (PR #488); this backfill
      is exactly the "reuse run" the clause requires: JOURNAL (#3), evidence (#6), and KB map (#20)
      all produced/refreshed, not just green tests re-confirmed.

---

**Overall: all applicable items PASS.** Items 4/5 (Playwright driver + investigation/) are
permanently waived per Section H (Universal Screen Engine replacement). Item 14 (full I-U-D) is
N/A per the owner-confirmed Find-only nature of this screen — not a gap. No automation files
(`pageobjects/`, `tests/`) were modified by this backfill.
