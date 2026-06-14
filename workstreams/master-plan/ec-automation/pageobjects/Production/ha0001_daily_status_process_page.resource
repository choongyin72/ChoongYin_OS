*** Settings ***
Documentation       T3 (screen) — HA.0001 "Daily Data Status Processes" page object.
...                 Screen: EC Production (search) > Daily Data Status Processes
...                 (com.ec.prod.ha family; main frame, no iframe).
...                 N3 status-process RUN pattern (see resources/status_process_run.resource):
...                 pick a DATE + a Status Process in the navigator, Run Process, then assert the
...                 DB ground truth — the scoped rows move RECORD_STATUS P->V and the engine logs a
...                 STAT_PROCESS_STATUS row with ROWS_UPDATED. Run mechanism + scope DB-proven
...                 2026-06-14 (docs/pattern_n3_status_process_design.md;
...                 DeepDiveLearnings/ec-bpm/ec-worker-and-scheduler.md "N3 PROVEN").
...
...                 This screen owns: the screen name, the chosen process + its PROCESS_ID, a scope
...                 day with Provisional data, and the DB oracle wiring. Positive process =
...                 "P1 Forward Status Update" (PROCESS_ID P1_FwdUpd, P->V) on 2024-02-06 (the P1
...                 facility has 15 liftable P rows that day: PWEL + IWEL + OBJECT_DAY_WEATHER).
...                 Self-clean = DB-restore V->P across the day-status family (the EC reverse
...                 process lifts 0 rows here — proven; so a scoped DB-restore is the teardown).

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/status_process_run.resource


*** Variables ***
${STATUS_SCREEN}                Daily Data Status Processes
# Positive case: P1 Forward Status Update (P->V), scoped to the P1 facility.
${STATUS_PROCESS_NAME}          P1 Forward Status Update
${STATUS_PROCESS_ID}            P1_FwdUpd
# A data-bearing day where the P1 facility scope has Provisional rows to lift (proven = 15 rows).
${STATUS_RUN_DATE}              2024-02-06
# Async-run poll budget (ec-worker executes within seconds once running; allow for a transient
# worker restart — UnknownHostException: ec-messaging — to recover).
${STATUS_POLL_RETRIES}          25x
${STATUS_POLL_INTERVAL}         3s


*** Keywords ***
Open Daily Status Process Screen
    [Documentation]    Suite Setup: launch, login, open HA.0001 Daily Data Status Processes.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${STATUS_SCREEN}    ${user}    ${pass}

Status Process Day Should Be Clean
    [Documentation]    Baseline guard (DB ground truth): NO Verified ('V') rows exist on ${date}
    ...    across the day-status family before the run, so the V-count after the run is exactly the
    ...    lift. A non-clean baseline (leftover V from an aborted run) fails fast and honestly.
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    ${v}=    Record Status Family Count    ${date}    V
    Should Be Equal As Integers    ${v}    ${0}
    ...    msg=Expected 0 Verified rows on ${date} before the run (dirty baseline — a prior run left V)

Run Forward Status Process
    [Documentation]    Capture the STAT_PROCESS_STATUS baseline (the log is append-only, so a fresh
    ...    run is proven by a +1 delta, not by absence), then submit the run on the screen.
    [Arguments]    ${date}=${STATUS_RUN_DATE}    ${process}=${STATUS_PROCESS_NAME}
    ${baseline}=    Status Process Run Count    ${STATUS_PROCESS_ID}    ${date}
    VAR    ${STATUS_RUN_BASELINE}    ${baseline}    scope=SUITE
    Submit Status Process Run    ${date}    ${process}

Wait For Status Process Run
    [Documentation]    Poll the DB until a NEW STAT_PROCESS_STATUS run row appears for the process on
    ...    ${date} (count > the captured baseline). Times out if ec-worker isn't executing the run.
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    Wait Until Keyword Succeeds    ${STATUS_POLL_RETRIES}    ${STATUS_POLL_INTERVAL}
    ...    A New Status Process Run Should Be Logged    ${date}

A New Status Process Run Should Be Logged
    [Documentation]    True once STAT_PROCESS_STATUS has more rows than the baseline = a fresh run
    ...    has executed and self-reported.
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    ${now}=    Status Process Run Count    ${STATUS_PROCESS_ID}    ${date}
    Should Be True    ${now} > ${STATUS_RUN_BASELINE}
    ...    msg=No new STAT_PROCESS_STATUS row yet for ${STATUS_PROCESS_ID} on ${date} (run still WAITING / ec-worker idle?)

Status Process Lift Should Verify
    [Documentation]    The N3 oracle (DB ground truth): the engine lifted rows (ROWS_UPDATED > 0)
    ...    AND the actual data agrees — the Verified ('V') row count across the day-status family on
    ...    ${date} EQUALS the engine's reported ROWS_UPDATED. The two independent sources agreeing is
    ...    the trustworthy proof that the P->V transition really persisted (not a UI/optimistic state).
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    ${rows}=    Latest Status Process Rows Updated    ${STATUS_PROCESS_ID}    ${date}
    Should Not Be Equal    ${rows}    ${None}
    ...    msg=No STAT_PROCESS_STATUS run row for ${STATUS_PROCESS_ID} on ${date} (the run never logged)
    Should Be True    ${rows} > 0
    ...    msg=STAT_PROCESS_STATUS ROWS_UPDATED=${rows} for ${STATUS_PROCESS_ID} on ${date} (expected > 0)
    ${verified}=    Record Status Family Count    ${date}    V
    Should Be Equal As Integers    ${verified}    ${rows}
    ...    msg=Data V-count (${verified}) != engine ROWS_UPDATED (${rows}) — lift count disagrees with the data

Restore Status Process Day
    [Documentation]    Self-clean teardown (DB-restore V->P across the day-status family on ${date})
    ...    so the suite leaves the sandbox exactly as found, then assert ZERO residual Verified rows.
    ...    Idempotent — safe to run again from Suite Teardown after the TC already restored.
    [Arguments]    ${date}=${STATUS_RUN_DATE}
    ${n}=    Restore Record Status Family    ${date}    V    P
    Log    Self-clean: restored ${n} row(s) V->P on ${date}
    ${residual}=    Record Status Family Count    ${date}    V
    Should Be Equal As Integers    ${residual}    ${0}
    ...    msg=Residual Verified rows on ${date} after self-clean (expected 0)
