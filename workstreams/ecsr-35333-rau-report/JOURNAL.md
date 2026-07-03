# Work Journal — ECSR-35333 (fact-finding)

**Branch:** `feature/ecsr-35333-deep-dive`   **Date:** 2026-06-26   **Env:** ECAASDEV (read-only)
**Type:** root-cause fact-finding (no fix applied — awaiting client re-test).

## What was done
Root-caused **Issue 1** of the Pluto Hub Monthly Deferments & RAU Report (Period/YTD Actual blank on the RAU Performance Summary tab). Traced report → Jasper subreport → `ZWP_V_DEF_RAU_SUB_004` view → contract-account events → the `ZWP_P_DEF_RAU_CALC` calculation, and proved the cause with live ECAASDEV data + the As-Built Calc DDS §4.1. Deliverable: `FINDINGS.md` + read-only repro scripts in `investigation/`.

## Done badly / wrongly (don't repeat)
- **Concluded from a truncated tool-output file.** Grepped a `read_resource`/query dump that had been cut off after `C_PLU_LNG_1`, and wrongly concluded "only PLA contracts have ACT events / facility = PLA-vs-Pluto." Disproved by a proper query. **Re-query complete data; never grep a possibly-truncated dump.**
- **Over-generalised twice** before verifying (the "PLA vs Pluto" framing; a fan-out/mis-map hypothesis) — both wrong. The user pushing on Train 1 vs Train 2 forced the correct, data-backed answer.

## Done well (keep)
- **Methodical trace the user asked for:** report date → which calc runs for that period → DDS → view → data. Each hop verified.
- **Chopped large docs** (28 MB Calc DDS, 100k-char dumps) — grep-to-locate then read the slice, never the whole thing.
- **Proved the root cause four independent ways** (DDS, code, data, the calc's own run log) — and disproved my own wrong hypotheses with read-only queries rather than asserting.
- **Stayed strictly read-only** on ECAASDEV; all scripts read creds from env (no secrets committed).

## Could improve
- Verify before framing a conclusion (the truncated-file and fan-out detours cost a couple of rounds).
- Pull complete query output up front (avoid head/tail truncation when the answer depends on the full set).

## Blockers faced → how resolved
- **Big As-Built docs / oversized tool-results exceeding token limits** → chop: grep to locate the section, read only that slice (`extract_cdefrau_dds.py`, targeted greps).
- **ECAASDEV connect slow over VPN** → ran queries as background tasks and read the output files.
- **"Why Train 1 NULL but Train 2 populated?"** (looked like a view bug) → diagnostic query proved the eqpm join is clean 1:1; the difference is the source events (Train 1 = 0 ACT events, gate-skipped; Train 2 = verified, ran but produced garbage).

## Key decisions / outcome
- Issue 1 = **operational/data** (unverified deferments block the calc), **not a report/code bug**. Fix = verify deferments → re-run `ZWP_RAU_CALC_PLUSCA`.
- Issue 2 = same root cause. Issue 3 = deferred. Train-2 garbage capacity = separate defect, logged.
- **Stop point:** fact-finding delivered; await client re-test after they receive the findings.

---

## Session 2 — 2026-07-03 (re-opened RCA)

**Trigger:** ticket re-opened 2026-06-30 (Swapnil verified SCA + re-ran the calc clean, but Issues 1/2/3 persisted) and re-assigned to CY.

### What was done
Re-investigated read-only on ECAASDEV (VPN up). Established the ticket has **three distinct root causes** across facilities (not one). Corrected the earlier single-cause conclusion. Traced SCA's capacity all the way to source (`getCapacity → getStreamReferCapacity → GetPlannedVolumes → getGroupForecastId = NULL` → no capacity forecast loaded for Scarborough), and confirmed LNG Train 1's capacity is healthy (73,166 t via `LNG_TRAIN_1_DEF_CAP`) so its blank actuals are the verification gate, not capacity. Appended the full RE-OPENED RCA to `FINDINGS.md`; added read-only trace scripts.

### Done badly / wrongly (don't repeat)
- **Prematurely declared the verification gate "disproven"** after the re-open. Actually it's still the cause for 4 facilities; the re-open just exposed two *additional* causes (SCA capacity, Train 2 negatives). Should have said "the fix was only applied to SCA" before pivoting the whole theory.
- **Investigated capacity=0 on SCA when the priority facility was LNG Train 1** (user corrected). Cost a detour — should have confirmed the target facility first.

### Done well (keep)
- Traced the capacity chain function-by-function to the exact missing config (forecast load), not just "capacity is 0".
- Re-queried current data after the client's 06-30 re-run rather than trusting stale recon; owned the correction honestly.
- Stayed read-only; all new scripts read creds from env.

### Key outcome
- **Cause 1** unverified deferments (Train 1/Cond/DG/PNI); **Cause 2** SCA no capacity forecast; **Cause 3** negative auto-deferments (Train 2 + latent). Fixes: #1 verify+re-run, #2 load SCA capacity forecast, #3 floor/exclude negatives (calc logic, Grant Hewton). Deploy env NOT ECAASDEV.
- **Stop point (user):** work halted on ECSR-35333; findings backed up. RCA Jira comment drafted but not yet posted.
