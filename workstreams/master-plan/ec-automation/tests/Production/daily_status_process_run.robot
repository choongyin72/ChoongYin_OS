*** Settings ***
Documentation       EC N3 Test — HA.0001 Daily Data Status Processes (status-process RUN + verify).
...                 Proves the N3 record-status pattern: open the screen, RUN a Status Process for
...                 a date + process via "Run Process", and assert the DB ground truth — the scoped
...                 day-status rows move RECORD_STATUS Provisional ('P') -> Verified ('V'), and the
...                 engine logs a STAT_PROCESS_STATUS row whose ROWS_UPDATED equals the actual count
...                 of lifted rows. The two independent sources agreeing is the trustworthy oracle.
...
...                   - TC01 LIFT: "P1 Forward Status Update" @ 2024-02-06 lifts the P1-facility
...                     scope P->V; ROWS_UPDATED > 0 AND data V-count == ROWS_UPDATED.
...                   - TC02 SELF-CLEAN: DB-restore V->P leaves the day exactly as found (0 residual
...                     V) — the no-residue discipline made an explicit, tested guarantee.
...
...                 The run is ASYNC (executed by the ec-worker scheduler node; status processes
...                 have NO synchronous Simulate), so TC01 polls the DB for the result. Requires
...                 ec-worker RUNNING (DeepDiveLearnings/ec-bpm/ec-worker-and-scheduler.md). Run
...                 mechanism + scope DB-proven 2026-06-14 (docs/pattern_n3_status_process_design.md).
...                 Layered: this test -> ha0001_daily_status_process_page (T3) ->
...                 status_process_run (T2) + common (T1) + DbVerify.

Resource            ../../pageobjects/Production/ha0001_daily_status_process_page.resource

Suite Setup         Open Daily Status Process Screen
Suite Teardown      Run Keywords    Restore Status Process Day    AND    Close EC

Test Tags           n3    daily_status_process


*** Test Cases ***
TC01 Forward Status Process Lifts Provisional To Verified
    [Documentation]    The keystone N3 proof: from a clean baseline (0 Verified rows on the day),
    ...    RUN "P1 Forward Status Update" @ 2024-02-06, wait for the async run to execute, then
    ...    assert the DB oracle — the engine's STAT_PROCESS_STATUS.ROWS_UPDATED is > 0 AND the
    ...    Verified row count in the data equals it (the P->V lift really persisted).
    [Tags]    run    positive
    Status Process Day Should Be Clean
    Run Forward Status Process
    Wait For Status Process Run
    Status Process Lift Should Verify
    Capture Step    ha0001_tc01_forward_lift_pv

TC02 Self-Clean Restores The Day To Provisional
    [Documentation]    The suite leaves no residue: DB-restore the lifted rows V->P and assert ZERO
    ...    Verified rows remain on the day (the EC reverse process lifts 0 rows here, so a scoped
    ...    DB-restore is the reliable self-clean — same discipline as the N1 IWEL/EQPM suites).
    [Tags]    cleanup    verify
    Restore Status Process Day
    Status Process Day Should Be Clean
    Capture Step    ha0001_tc02_self_clean
