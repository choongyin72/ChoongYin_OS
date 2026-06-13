*** Settings ***
Documentation       T3 (screen) — HA.0002 "Daily Allocation" page object.
...                 Screen: EC Production (search) > Daily Allocation
...                 (URL /com.ec.prod.ha.screens/edit_daily_alloc; main frame, no iframe).
...                 N2 allocation-RUN pattern (see resources/allocation_run.resource): pick a
...                 DATE + Allocation Network + Calculation Job, RUN CALCULATIONS, read the
...                 log_list Exit Status; on a real persisted result, assert the DB conservation
...                 oracle on PWEL_DAY_ALLOC. RUN mechanism + scope DB-/UI-proven 2026-06-13
...                 (docs/pattern_n2_allocation_run_design.md).
...
...                 This screen owns: the screen name, the result table, and the scope data — a
...                 known-SUCCESS case ("Testing allocation RUN_NO" → "01 Run No .test") and a
...                 known-FAILURE case ("P1 Dashboard" → "Daily Well Volume" — a real calc-engine
...                 equation defect, a meaningful negative test). All RUN tests use Simulate (no
...                 DB write); the conservation oracle reads existing real allocation results.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/allocation_run.resource


*** Variables ***
${ALLOC_SCREEN}             Daily Allocation
${ALLOC_RESULT_TABLE}       PWEL_DAY_ALLOC
# Known-SUCCESS scope: the dedicated test network/job effective at the 2003 seed epoch.
${POS_DATE}                 2003-01-01
${POS_NETWORK}              Testing allocation RUN_NO
${POS_CALCJOB}              01 Run No .test
# Known-FAILURE scope: P1 daily well-volume calc on a real data day (errors out — real finding).
${NEG_DATE}                 2021-10-01
${NEG_NETWORK}              P1 Dashboard
${NEG_CALCJOB}              Daily Well Volume
# Conservation-oracle date: the richest real allocation day (22 wells persisted by a prior run).
${CONSERVATION_DATE}        2021-10-01


*** Keywords ***
Open Daily Allocation Screen
    [Documentation]    Suite Setup: launch, login, open HA.0002 Daily Allocation.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${ALLOC_SCREEN}    ${user}    ${pass}

Run Allocation Job
    [Documentation]    Run an allocation calc for ${network}/${calc_job} over ${date} (single day),
    ...    with Simulate ON (no DB write). Sets the navigator, applies it, enables Simulate, then
    ...    clicks RUN CALCULATIONS. Returns once the run is submitted (assert the exit status next).
    [Arguments]    ${date}    ${network}    ${calc_job}
    Set Allocation Date Range    ${date}    ${date}
    Select Allocation Network    ${network}
    Select Allocation Calc Job    ${calc_job}
    Apply Allocation Navigator
    Enable Allocation Simulate
    Run Allocation Calculations

Allocation Run Should Exit
    [Documentation]    Assert the latest run for ${network} exited with ${expected}
    ...    (e.g. Success / Failure).
    [Arguments]    ${network}    ${expected}
    Allocation Exit Status Should Be    ${network}    ${expected}

Allocation Results Should Conserve
    [Documentation]    DB ground-truth conservation oracle on the allocation results for ${date}:
    ...    rows exist AND no allocated ALLOC_* quantity is negative. Asserted against real persisted
    ...    data (a prior real allocation run's output).
    [Arguments]    ${date}
    Allocation Conservation Should Hold    ${ALLOC_RESULT_TABLE}    ${date}
