# JOURNAL — Unit - Well Setup IUD (RC.0050)

**Feature / branch:** `feature/unit-well-setup-iud`
**PR:** (this PR) · **Base:** master
**Dates:** 2026-06-27
**Screen:** Configuration > Assets > Royalty Objects > Unit - Well Setup (PC pattern — 6th of 8 Royalty Objects screens, 2nd PC after Object List Setup)

## What was built
RF IUD suite + Playwright reference bundle for the Unit - Well Setup parent-child membership
grid: insert a Perf Interval membership under an (empty) Unit Agreement, verify +1 on
`DV_UNIT_WELL_SETUP`, physically delete it, verify back to baseline. Live 3/3, self-cleaning.

## Done badly or wrongly (don't repeat)
- **Selected the saved row for delete with the wrong cell (`C0_da_input`) — cost one live run.**
  A NEW (unsaved) grid row's start-date is a calendar (`C0_da_input`); once SAVED the same row
  renders it as a TEXT cell (`C0_in`). The Object List Setup bundle had ALREADY recorded this exact
  "new rows != saved rows" lesson — I cloned the structure but not the lesson. Should have used
  `C0_in` for the persisted-row select from the start (as OLS does). Re-confirmed live, fixed.
- **Used `py -c` for the independent DB re-read** — violates my standing rule (write a script file
  in tmp, never inline `py -c`). Minor, read-only, but the rule is literal. Don't repeat.

## Done well (keep)
- **Pre-flight before live run #1** (read-only): verified the parent's effective window
  (UNIT_3 = 2010-01-01), an empty clean target, the member's window, and a zero baseline — so
  navigator + insert worked first try (no Tract-style date repeats). The pre-flight lesson paid off.
- **Self-clean rigor under a mid-suite failure:** when TC03 failed it left one row; I ran a dedicated
  cleanup pass (DB 1 → 0) and an independent re-read BEFORE re-running and before any commit — the
  sandbox was never left dirty.
- **Two independent proofs:** RF suite 3/3 + Playwright bundle ALL PASS, both DB count-delta verified.
- **Cloned the proven PC exemplar** (Object List Setup) — robocop clean + dryrun green first try.

## Could improve
- Fold the "new-row calendar vs saved-row text cell" check INTO the recon step for PC screens, so the
  select-cell is known before live run #1 (it's a recurring PC trait, not a one-off).

## Blockers faced -> how resolved
- TC03 delete TimeoutError on `C0_da_input` -> recon dumped the saved row's real cell ids
  (`C0_in`, `C1_da_input`, `C2_dd_input`, `C3_in`, `C4_in`) and cleaned the leftover in the same pass;
  fixed the select cell to `C0_in` in both the T3 and the Playwright bundle; re-ran 3/3 green.

## Key decisions
- **Count-delta oracle on `DV_UNIT_WELL_SETUP.PERF_INTERVAL_CODE`** (robust to the member existing
  in other agreements; here it was 0 everywhere → crisp deltas).
- **Test pair UNIT_3 (empty) × 108_WB1-1_PF1** + form/start date 2011-01-01 (inside both windows).
- Reuse T2 `table_class.resource` keywords only — **no shared-file edits** (no R12 canary needed).

## Evidence / verification summary
- robocop: No issues found · dryrun: 3/3 PASS
- RF live #1 (headed): TC01-02 PASS, TC03 FAIL (saved-row select) → fixed
- RF live #2 (headed): **TC01-TC03 3/3 PASS**, count-delta verified (insert +1, delete back to 0)
- Playwright bundle (headless): login/navigate/clean/insert/delete **ALL PASS (physical)**
- Independent DB re-read after the run: **UNIT_3 well-setup rows = 0** (clean)
- Hygiene guard (R16/R20): **PASS**
