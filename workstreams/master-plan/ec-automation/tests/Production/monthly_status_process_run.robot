*** Settings ***
Documentation       EC N3 Test — "Monthly Data Status Processes" (status-process RUN + approve, MONTH
...                 grain). Sibling of the proven daily HA.0001 suite; same com.ec.prod.ha RUN engine
...                 + async ec-worker dispatch + STAT_PROCESS_STATUS oracle, extended to the monthly
...                 approve roll-up "P1 Parent1 Forward Status Update" (P1_FwdUpdPar1, →A).
...
...                   - TC01 LIFT: run P1_FwdUpdPar1 for the month → engine ROWS_UPDATED > 0 AND the
...                     Approved ('A') row count across the day-status family increases (the lift to A
...                     persisted). Target = IWEL_DAY_STATUS (AIR/CO2 scope; 19,659 'P' rows exist).
...                   - TC02 SELF-CLEAN: DB-restore A→P leaves the month as found (0 residual A).
...
...                 ⚠️ STATUS: BUILD-READY, dryrun-green — the LIVE run is GATED behind --variable
...                 LIVE_OK:yes (TC01 Skips otherwise) because the monthly approve has NO WHERE filter
...                 and can lift a large row set (a big, though DB-restore-reversible, state change). Run
...                 live only when OBSERVED, after confirming the blast radius + the exact oracle grain
...                 (single-date family count vs month-span lift) — see the T3 screen-doc gate.
...                 Screen model verified live 2026-06-15 (n3_monthly_screen_recon.py). Requires
...                 ec-worker RUNNING. Layered: this test -> mh_monthly_status_process_page (T3) ->
...                 status_process_run (T2) + common (T1) + DbVerify.

Resource            ../../pageobjects/Production/mh_monthly_status_process_page.resource

Suite Setup         Open Monthly Status Process Screen
Suite Teardown      Run Keywords    Restore Monthly Status Process Day    AND    Close EC

Test Tags           n3    monthly_status_process


*** Test Cases ***
TC01 Monthly Forward Status Process Lifts To Approved
    [Documentation]    The N3 month-grain proof: from a clean baseline (0 Approved rows), RUN "P1 Parent1
    ...    Forward Status Update", wait for the async run, then assert the DB oracle — engine
    ...    STAT_PROCESS_STATUS.ROWS_UPDATED > 0 AND the Approved row count increased (lift to 'A'
    ...    persisted). GATED: Skips unless --variable LIVE_OK:yes (the run can mutate many rows).
    [Tags]    run    positive    gated_live
    Monthly Live Run Gate
    Monthly Process Day Should Be Clean
    Run Monthly Forward Status Process
    Wait For Monthly Status Process Run
    Monthly Lift Should Approve
    Capture Step    mh_monthly_tc01_forward_lift_to_a

TC02 Self-Clean Restores The Month To Provisional
    [Documentation]    The suite leaves no residue: DB-restore the lifted rows A→P and assert ZERO
    ...    Approved rows remain (scoped DB-restore is the reliable self-clean, per the daily N3 suite).
    [Tags]    cleanup    verify
    Restore Monthly Status Process Day
    Monthly Process Day Should Be Clean
    Capture Step    mh_monthly_tc02_self_clean
