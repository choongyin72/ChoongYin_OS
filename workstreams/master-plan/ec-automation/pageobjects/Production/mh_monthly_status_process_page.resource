*** Settings ***
Documentation       T3 (screen) — "Monthly Data Status Processes" page object (N3 at the MONTH grain).
...                 Sibling of the proven daily HA.0001 T3; same com.ec.prod.ha RUN engine + same
...                 async ec-worker dispatch + same STAT_PROCESS_STATUS oracle, at month grain.
...
...                 Screen model VERIFIED LIVE 2026-06-15 (read-only recon, n3_monthly_screen_recon.py):
...                 non-iframed; nav = SINGLE Date (nav:form:G:0:R:1:C:0:da_input) + Process selector
...                 at GROUP 1 (NOT From/To + G:2 like the daily screen) → GO (button:form:B) →
...                 Run Process (RunProcessButton:form). The Process dd lists the monthly processes,
...                 incl. "P1 Parent1 Forward Status Update" (PROCESS_ID P1_FwdUpdPar1, →A) and its
...                 reverse "P1 Parent1 Reverse Status Update".
...
...                 Process: P1_FwdUpdPar1 (FROM=null → TO=A, MTH) → STAT_PROCESS_TASK targets
...                 IWEL_DAY_STATUS (AIR/CO2 scope; no WHERE filter). IWEL_DAY_STATUS holds 19,659 'P'
...                 rows in this sandbox → there IS liftable data (unlike the daily V→A pair, which is
...                 data-blocked on empty STIM_DAY_VALUE).
...
...                 ⚠️ STATUS: BUILD-READY, dryrun-green — the LIVE run is GATED. Two things to confirm
...                 on the FIRST OBSERVED live run (do NOT run unattended — no WHERE filter ⇒ a month's
...                 worth of rows may lift; a large state change, reversible via DB-restore A→P):
...                   1. BLAST RADIUS — how many rows P1_FwdUpdPar1 lifts for the chosen month, and at
...                      which DAYTIME(s). Pick a scoped month with modest P volume first.
...                   2. ORACLE GRAIN — RESOLVED: the baseline, A-delta oracle and teardown now use the
...                      MONTH-range family helpers (Record/Restore ...Family Month), so they are correct
...                      whether the no-WHERE lift spans one day or the whole month. The ROBUST assertions
...                      (ROWS_UPDATED>0 + A-family delta>0) remain the gating proof. Still confirm the
...                      BLAST RADIUS (#1) on the first observed run before claiming live N/N.
...                 Self-clean = DB-restore A→P across the day-status family (proven teardown pattern).

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/status_process_run.resource


*** Variables ***
${STATUS_SCREEN}                Monthly Data Status Processes
# Positive case: P1 Parent1 Forward Status Update (→A), the monthly roll-up.
${STATUS_PROCESS_NAME}          P1 Parent1 Forward Status Update
${STATUS_PROCESS_ID}            P1_FwdUpdPar1
# A month date whose IWEL_DAY_STATUS scope has Provisional rows to lift.
# ⚠️ CONFIRM the scope date + resulting blast radius on the first observed live run.
${STATUS_RUN_DATE}              2024-02-06
${STATUS_POLL_RETRIES}          25x
${STATUS_POLL_INTERVAL}         3s


*** Keywords ***
Open Monthly Status Process Screen
    [Documentation]    Suite Setup: launch, login, open "Monthly Data Status Processes".
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${STATUS_SCREEN}    ${user}    ${pass}

Monthly Live Run Gate
    [Documentation]    SAFETY GATE — the monthly run lifts to 'A' with NO WHERE filter, so it can mutate
    ...    a large row set. The live TC executes ONLY when explicitly opted-in with --variable LIVE_OK:yes
    ...    (after confirming blast radius on an observed run). Without it the TC is SKIPPED, so
    ...    canary / random-suite / unattended runs never trigger the mutation.
    ${ok}=    Get Variable Value    ${LIVE_OK}    ${EMPTY}
    Skip If    '${ok}' == '${EMPTY}'
    ...    Monthly live run is GATED — rerun with --variable LIVE_OK:yes (observed; blast radius confirmed)

Monthly Process Day Should Be Clean
    [Documentation]    Baseline guard (DB ground truth): NO Approved ('A') rows exist anywhere in
    ...    ${date}'s MONTH across the day-status family before the run, so the A-count delta after the
    ...    run is exactly the monthly lift — correct whether the no-WHERE monthly process lifts one day
    ...    or the whole month. A dirty baseline (leftover A) fails fast and honestly.
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    ${a}=    Record Status Family Count Month    ${date}    A
    Should Be Equal As Integers    ${a}    ${0}
    ...    msg=Expected 0 Approved rows in ${date}'s month before the run (dirty baseline — a prior run left A)

Run Monthly Forward Status Process
    [Documentation]    Capture the STAT_PROCESS_STATUS baseline (append-only log → a fresh run is a +1
    ...    delta) and the A-count baseline, then submit the monthly run on the screen.
    [Arguments]    ${date}=${STATUS_RUN_DATE}    ${process}=${STATUS_PROCESS_NAME}
    ${baseline}=    Status Process Run Count    ${STATUS_PROCESS_ID}    ${date}
    VAR    ${STATUS_RUN_BASELINE}    ${baseline}    scope=SUITE
    ${a_base}=    Record Status Family Count Month    ${date}    A
    VAR    ${STATUS_A_BASELINE}    ${a_base}    scope=SUITE
    Submit Monthly Status Process Run    ${date}    ${process}

Wait For Monthly Status Process Run
    [Documentation]    Poll the DB until a NEW STAT_PROCESS_STATUS run row appears for the process on
    ...    ${date} (count > baseline). Times out if ec-worker isn't executing the run.
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    Wait Until Keyword Succeeds    ${STATUS_POLL_RETRIES}    ${STATUS_POLL_INTERVAL}
    ...    A New Monthly Run Should Be Logged    ${date}

A New Monthly Run Should Be Logged
    [Documentation]    True once STAT_PROCESS_STATUS has more rows than the baseline = a fresh monthly
    ...    run executed and self-reported.
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    ${now}=    Status Process Run Count    ${STATUS_PROCESS_ID}    ${date}
    Should Be True    ${now} > ${STATUS_RUN_BASELINE}
    ...    msg=No new STAT_PROCESS_STATUS row yet for ${STATUS_PROCESS_ID} on ${date} (run WAITING / ec-worker idle?)

Monthly Lift Should Approve
    [Documentation]    The N3 oracle at month grain (DB ground truth, robust): the engine lifted rows
    ...    (ROWS_UPDATED > 0) AND the data agrees — Approved ('A') rows across the day-status family
    ...    INCREASED over the captured baseline. The A-count uses the MONTH-range family count, so it
    ...    holds whether the no-WHERE monthly process lifts one day or the whole month. ROWS_UPDATED>0
    ...    + A delta>0 are the trustworthy gating proof.
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    ${rows}=    Latest Status Process Rows Updated    ${STATUS_PROCESS_ID}    ${date}
    Should Not Be Equal    ${rows}    ${None}
    ...    msg=No STAT_PROCESS_STATUS run row for ${STATUS_PROCESS_ID} on ${date} (the run never logged)
    Should Be True    ${rows} > 0
    ...    msg=STAT_PROCESS_STATUS ROWS_UPDATED=${rows} for ${STATUS_PROCESS_ID} on ${date} (expected > 0)
    ${approved}=    Record Status Family Count Month    ${date}    A
    Should Be True    ${approved} > ${STATUS_A_BASELINE}
    ...    msg=Approved count (${approved}) did not increase over baseline (${STATUS_A_BASELINE}) — no lift to A

Restore Monthly Status Process Day
    [Documentation]    Self-clean teardown (DB-restore A→P across the day-status family for the WHOLE
    ...    month of ${date}) so the suite leaves the sandbox as found even if the no-WHERE monthly
    ...    process lifted every day of the month, then assert ZERO residual Approved rows in the month.
    ...    Idempotent.
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    ${n}=    Restore Record Status Family Month    ${date}    A    P
    Log    Self-clean: restored ${n} row(s) A→P across ${date}'s month
    ${residual}=    Record Status Family Count Month    ${date}    A
    Should Be Equal As Integers    ${residual}    ${0}
    ...    msg=Residual Approved rows in ${date}'s month after self-clean (expected 0)
