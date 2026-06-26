# Work Journal — ECSR-35236

**Feature / branch:** scope 8 PHD check rules by method / on-stream — `feature/ecsr-35236-phd-check-rules`
**PR:** #126 → master   **Dates:** 2026-06-25 (SQL) · 2026-06-26 (UT)   **Env:** COPSDEV / plutodev (write-with-rollback); ECAASTEST (read-only pristine)

## What was built
Idempotent, env-portable Flyway SQL (keyed by `CHECK_NAME`) that adds a method / on-stream criterion to 8 PHD validation check rules so they only fire when a value is genuinely expected — stopping the false-positive PHD validations on tags added since 1 Dec 2025. Plus apply/rollback, reproducible verification scripts, and a UT evidence doc that leads with EC **screen** evidence.

## Done badly or wrongly (don't repeat)
- First built the UT as **DB-layer evidence** (row counts, formula tables) — a business user can't read that. Had to rebuild as on-screen evidence. **Lead UT deliverables with EC screen evidence; DB proof is the appendix.**
- Cited an **env-local `CHECK_ID` (1149)** when describing a rule — meaningless across envs. Always identify rules by **`CHECK_NAME`** (CHECK_ID differs: plutodev 1149 vs ECAASTEST 1147).

## Done well (keep)
- **Pre-flight before the live screen run:** picked the demo date (2026-06-06) and group names from the DB *first*, so I knew the expected result (20→12) before logging in → landed first try.
- Reused proven assets (the reference `capture_ec_screenshots.py` + the `validation_overview_pluto_scarborough.resource` locators) — no gesture-guessing.
- Verified ground truth at every step (DB before/after/clean, pristine ECAASTEST cross-check, independent re-read).
- Kept everything in scope: plutodev only, left clean, no client repo, explicit-path commits.

## Could improve
- Decide the UT *format* (screen-first) up front for a client deliverable, instead of building DB-first then redoing.
- The screen evidence covers the tank hero group only; stream/PWEL groups rely on the DB appendix — could add their screenshots if a fuller visual set is wanted.

## Blockers faced → how resolved
1. **Apply-bearing run could leave plutodev dirty** (fix applied between before/after shots). → apply + rollback in a `finally` inside ONE subprocess, so rollback always runs regardless of interruption; DB-verified clean (8/8 ORIGINAL) after. *Engineer the blocker away, don't avoid the task.*
2. **"Does the rollback truly restore original?"** → proved 3 ways: round-trip `S0 == S2`; cross-check vs **pristine ECAASTEST** (rollback's "original" strings match exactly; the 7 method/const vars are net-new); independent re-read.
3. **Need a date showing both false positives AND genuine cases** → DB query found 2026-06-06 (3 gross-mass + 5 std-density FP, plus 2 genuine MEASURED gross-mass).
4. **Unknowns on the remote screen** (content frame, group display names) → frame-polling helper + resolved names from `CTRL_CHECK_GROUP.DESCRIPTION` before driving the UI.
5. **ECAASTEST unreachable (VPN)** → retried; came up; completed the pristine cross-check.

## Key decisions
- SQL keyed by `CHECK_NAME` (not `CHECK_ID`) for env portability.
- Implement Mel's literal `=` criteria as specified; flag in the UT (for client test) that `STD_DENSITY = 'MEASURED'` suppresses 100% on current data (rows are `STREAM_SAMPLE_ANALYSIS`), the PWEL `ON_STREAM_HRS > 0` NULL handling, and `=` vs `IN`.
- RF/DB evidence kept as a supporting appendix; screen evidence is the headline.

## Evidence / verification summary
- Round-trip on plutodev: S0 (all ORIGINAL) → apply (all 8 SCOPED) → rollback → **S2 == S0**. PASS.
- Screen (Validation Overview, *Daily Tank Status - VCF Calc - PHD Validations*, 2026-06-06): **BEFORE 20 Errors → AFTER 12 Errors** (8 false positives suppressed; genuine remain). Screenshots in `UT/screens/`.
- DB behavioural (the check's own COUNT): GRS_MASS 641→56, STD_DENSITY 741→0, stream DENSITY 1393→168, GCV 916→1, PWEL ~348→0 each.
- plutodev left CLEAN (8/8 rules ORIGINAL).
