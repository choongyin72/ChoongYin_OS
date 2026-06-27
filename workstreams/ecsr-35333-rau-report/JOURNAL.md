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
