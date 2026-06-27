# JOURNAL — Tract - Well Setup IUD (RC.0057)

**Feature / branch:** `feature/tract-well-setup-iud`
**PR:** (this PR) · **Base:** master (standalone — shares only the already-merged T2)
**Dates:** 2026-06-27
**Screen:** Configuration > Assets > Royalty Objects > Tract - Well Setup (PC pattern — 7th of 8 Royalty Objects screens, 3rd PC; sibling of Unit - Well Setup over the same WELL_SETUP base)

## What was built
RF full I-U-D suite + Playwright reference bundle for the Tract - Well Setup membership grid:
insert a Perf Interval membership under an existing Tract (verify +1 on `DV_TRACT_WELL_SETUP`),
UPDATE its COMMENTS (DB-verified), then physically delete it (back to baseline). **Live 4/4 on
the first test run**, self-cleaning, existing rows untouched.

## Done badly or wrongly (don't repeat)
- **First recon pass mis-handled the cascade navigator** — I probed the dds for a "Tract" option
  before selecting a Unit Agreement, so the Tract dd (G:2) was still empty and went unidentified;
  the script then picked the wrong Unit Agreement and never selected a Tract, so the grid never
  loaded. Caught immediately (read-only recon, no test run wasted); re-ran with the correct cascade.
  **Lesson: for cascade navigators, recon by *driving* the cascade (pick parent, THEN read child),
  not by snapshotting all dds up front.**

## Done well (keep)
- **Applied the previous screen's lessons up front** → live **4/4 on the first run** (vs RC.0050's
  one wasted run): full I-U-D scope from the start, `C0_in` saved-row select, `C3_in`=COMMENTS
  update via present-in-view, pre-flight before live run #1.
- **Heeded the user's observation** ("based on the Tract object — ensure an existing Tract first"):
  confirmed OBJECT_CODE = Tract, used the existing TRACT_U3_T01, never created/touched a Tract object.
- **Protected existing data with no empty parent available:** inserted a baseline-0 member and
  selected only by that unique member code → existing P1 PI-5 / P1 PI-6 rows verified intact after.
- Reused T2 keywords only — no shared-file edits; robocop clean + dryrun green first try.

## Could improve
- Could have predicted the cascade from the Tract codes (TRACT_**U3**_T01 implies a Unit grouping)
  before the first recon — a 10-second look at the pre-flight data would have set the recon up right.

## Blockers faced -> how resolved
- Recon v1 loaded an empty grid (`manageObject:form:T_data`, no well-setup) because the Tract was
  never selected -> identified the cascade from the nav dump (G:1 Unit Agreement populated, G:2
  empty), re-ran recon v2 with Unit Agreement 3 -> Unit 3 Tract 01 -> grid `well_setup:form:T_data`
  loaded, full gesture map captured.

## Key decisions
- **Count-delta oracle on `DV_TRACT_WELL_SETUP.PERF_INTERVAL_CODE`** + **COMMENTS present-in-view**
  for UPDATE — same proven approach as Unit - Well Setup; no DbVerify/shared-file change.
- **Test pair: existing Tract `Unit 3 Tract 01` × baseline-0 member `108_WB1-1_PF1`**, date 2011-01-01.
- Standalone PR off master (no git dependency on RC.0050 #130 — only shares the merged T2).

## Evidence / verification summary
- robocop: No issues found · dryrun: 4/4 PASS
- RF live (headed, full I-U-D): **TC01-TC04 4/4 PASS** on the first run — count-delta + COMMENTS verified
- Playwright bundle (headless): login/navigate/clean/insert/update/delete **ALL PASS**
- Independent DB re-read: **TRACT_U3_T01 = P1 PI-5 / P1 PI-6 only** (existing intact), member 0, sentinel 0
- Hygiene guard (R16/R20): PASS
