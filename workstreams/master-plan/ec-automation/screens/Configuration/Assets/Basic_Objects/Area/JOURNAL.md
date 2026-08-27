# JOURNAL — Area IUD (RF)

_Screen: Configuration > Assets > Basic Objects > Area (**CO.0003**), OV-GM (groupmodel manage-object,
date-effective). View `OV_AREA`. Area is the **role-model / reference pattern** for the whole
navigator-screen (OV-GM) family (owner's 2026-08-26 standing rule)._

_This JOURNAL was backfilled 2026-08-27 under `docs/lean-deliverable-backfill-workorder.md` (owner
decision retiring the 2026-08-23/26 lean waiver — Section H of `docs/IUD-DELIVERABLE-CHECKLIST.md`).
The RF automation described below was already built and merged in PRs #521 and #523 on 2026-08-25;
this JOURNAL narrates what those PRs' bodies and commit messages actually recorded — it is not a new
build and no automation file was touched to produce it._

## Built (2026-08-25, PRs #521 + #523)
- **PR #521** — converted Area's pre-existing RF suite (base IUD, `verify_screen` PASS 2026-08-01,
  4-TC structure) to the **Bank-pattern 5-TC structure**: added TC04 Find; per-TC
  `Login To EC Application`/`Logout From EC Application`; fixed test code `AUTOTEST_AREA` (replacing
  a generated/unique code); properties-file-driven Insert/Update
  (`testdata/area_{insert,update,form_verify,grid_verify}.properties`); explicit
  `Find/Clear Area Row By Filter` grid-filter wiring into Update/Find/Verify-Found/Delete; removed
  the screen-local DB-verify wrapper keywords, delegating verification purely to shared T2 keywords.
  This was an owner-directed **one-off exception** — Area REMAINS OV-GM and kept its genuine
  mandatory Production Unit navigator + GO gesture; the conversion changed the suite's structure,
  not its screen classification.
- **PR #523** (same day, superseding a stale unmerged PR #522 built off pre-#521 master) — extracted
  the navigator-fill logic out of Area's own page object into a brand-new **shared T2 keyword**,
  `Apply Navigator From Properties` (`resources/manage_object.resource`), driven by the new
  `testdata/area_navigator.properties`. Area was the first screen this shared keyword was built for.

## Done well
- Full 5-TC I-U-D-Find cycle, DB-verified vs `OV_AREA` at the fixed code `AUTOTEST_AREA`.
- PR #521: live 5/5, full-tree dryrun 846/846, DB self-clean 0/0 before+after (fresh connection),
  grid-filter keyword confirmed firing (29 hits in `output.xml`), robocop 7 issues (DOC02/VAR02 —
  same categories as Bank's own baseline, parity not regression).
- PR #523: live 5/5 re-confirmed on the new shared keyword, full-tree dryrun 846/846 (matched the
  post-#521 baseline exactly, zero collisions), robocop +3 issues vs the 19-issue pre-existing
  baseline for the 3 touched files (1 LEN01 on the new keyword's own name + 2 DEPR05 `Set Variable`
  — same categories as the sibling `Apply OV-GM Navigator First Available` keyword, parity not a new
  issue type). Two OTHER OV-GM screens with their own bespoke navigator logic (Well, Test Separator)
  were re-run live UNCHANGED to prove zero regression from the shared-file edit: **4/4 each**.
- The shared `Apply Navigator From Properties` keyword this pair of PRs introduced went on to be
  reused by 20+ further OV-GM navigator screens, which is why Area subsequently became the
  role-model pattern for the whole navigator-screen family (owner's 2026-08-26 standing rule).

## Done wrong / lessons
- **PR #522 went stale.** It was built off `origin/master` BEFORE #521 merged, so its Area-side
  edits targeted the OLD 4-TC structure (`Open Area Screen`, `Set Up Area Suite`, no TC04 Find). It
  never merged and had to be superseded cleanly by #523 rather than relying on a `Closes #522`
  auto-close, since "superseded" was a more accurate characterization than "fixed by this PR." The
  lesson recorded in #523's body: rebuild against CURRENT master state rather than assuming a
  parallel branch's diff still applies as-is.
- **This backfill session (2026-08-27), evidence capture run 1 of 2:** the FIRST live evidence run
  hit a **TC05 grid-assertion flake** — `Row AUTOTEST_AREA should NOT exist in manageObject:form:T_data:
  1 != 0` — i.e. the screen still showed the row in the grid right after delete. A fresh-connection
  DB read taken immediately after (`DbVerify.fetch_object("OV_AREA", "AUTOTEST_AREA")`) returned
  `None` — the delete had genuinely succeeded at the DB level; only the UI grid had not yet
  redrawn. This matches this screen's OWN documented quirk from the original 2026-06-11 build
  ("versioned grid redraws lazily after a delete — one extra GO") and the OV-GM T2 docstring's own
  caveat ("versioned groupmodel grids redraw lazily after a delete"). A second live run, same
  session, passed clean **5/5** with the same 0-residual DB result. Recorded here as a real,
  disclosed flake (per this backfill's instruction not to smooth over a real PR-adjacent issue) —
  not treated as a regression requiring an automation fix, since (a) it is a pre-existing, already-
  documented characteristic of this exact screen, not something this backfill's read-only evidence
  capture introduced, and (b) the DB ground truth confirms the underlying operation is correct both
  times; only the grid's own redraw timing varied.

## Blockers -> resolution
- No hard blockers on the original conversion (PRs #521/#523) — both merged same-day with clean
  evidence.
- This backfill session's TC05 flake (above) resolved itself on a second live run; no code or
  automation change was made or needed.

## Decisions
- Area stays classified **OV-GM**, not reclassified as plain Bank-shaped, despite adopting Bank's
  5-TC RF STRUCTURE — the genuine mandatory Production Unit navigator + GO gesture was kept
  throughout both PRs.
- The Playwright driver (`playwright/ec_iud_area.py`) was deliberately left untouched by both PRs —
  the owner's directive was specifically for the RF `.robot` suite. Per Section H of
  `docs/IUD-DELIVERABLE-CHECKLIST.md` (2026-08-27), the Playwright driver + `investigation/` stay
  permanently waived for Bank-/Area-pattern work going forward (Universal Screen Engine replaces
  that role) — the pre-existing bundle here is kept as historical reference, not rebuilt.
- `Apply Navigator From Properties` lives in the SHARED `resources/manage_object.resource` (T2), not
  Area's own T3 page object, specifically so other OV-GM navigator screens could reuse it —
  confirmed by its subsequent reuse across 20+ screens.

## Evidence
- PR #521/#523: cited live 5/5 + 4/4 (x2) results, full-tree dryrun 846/846, DB self-clean 0/0, robocop
  deltas — see PR bodies (`gh pr view 521`, `gh pr view 523`) for the exact commands/output cited.
- This backfill session (2026-08-27):
  - `robot --dryrun tests/Configuration/Assets/Basic_Objects/area_iud.robot` → **5/5 PASS**.
  - `EC_HEADLESS=true robot --outputdir .../Area/evidence tests/.../area_iud.robot` → run 1: **4/5
    PASS** (TC05 grid-redraw flake, DB confirmed correct — see "Done wrong" above); run 2: **5/5
    PASS** clean.
  - DB self-clean: `DbVerify.fetch_object("OV_AREA", "AUTOTEST_AREA")` → `None` (confirmed absent)
    after both runs.
  - `py -m robocop check` on `area_page.resource` + `area_iud.robot` → **7 issues** (DOC02 missing
    TC/keyword docs) — matches PR #521's cited 7-issue baseline exactly, no drift.
  - `py scripts/check_bundle_hygiene.py` (repo-wide) → **PASS** — "no hardcoded creds (R16), pure
    ASCII (R20), no CHECKLIST/VERIFY-REPORT contradictions, doc rows match declared families."
  - Evidence artifacts: `evidence/log.html`, `evidence/output.xml`, `evidence/report.html`,
    `evidence/playwright-log.txt`, per-TC screenshots (`TC0N ..._{login,open_screen,action,verify,
    logout}.png`) from the clean run-2 pass, alongside the pre-existing 2026-06-11 Playwright
    evidence (`area_01_loaded.png` ... `area_08_final_state.png`, `area_results.json`).
