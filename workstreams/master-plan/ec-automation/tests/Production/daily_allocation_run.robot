*** Settings ***
Documentation       EC N2 Test — HA.0002 Daily Allocation (calc RUN + verify). Proves the N2
...                 allocation-run pattern: open the screen, RUN an allocation for a
...                 date + Allocation Network + Calculation Job via RUN CALCULATIONS, read the
...                 log_list Exit Status, and assert the DB conservation oracle on the persisted
...                 results. Two run cases exercise both outcomes:
...                   - POSITIVE: "Testing allocation RUN_NO" / "01 Run No .test" → Success
...                   - NEGATIVE: "P1 Dashboard" / "Daily Well Volume" → Failure (a real calc-engine
...                     equation defect — an allocation that errors is a defect to catch).
...                 All RUN cases use Simulate (no DB write — safe). The conservation oracle
...                 (no-negatives) is asserted at the DB on real persisted allocation results
...                 (PWEL_DAY_ALLOC, 2021-10-01). Run mechanism DB-/UI-proven 2026-06-13.
...                 Layered: this test -> ha0002_daily_allocation_page (T3) ->
...                 allocation_run (T2) + common (T1) + DbVerify.

Resource            ../../pageobjects/Production/ha0002_daily_allocation_page.resource

Suite Setup         Open Daily Allocation Screen
Suite Teardown      Close EC

Test Tags           n2    daily_allocation


*** Test Cases ***
TC01 Positive Run Exits Success
    [Documentation]    The dedicated test network/job runs cleanly: RUN CALCULATIONS (Simulate)
    ...    over "Testing allocation RUN_NO" / "01 Run No .test" @ 2003-01-01 exits Success. Proves
    ...    the full run path works end to end (button wired, job executes, status surfaces).
    [Tags]    run    positive
    Run Allocation Job    ${POS_DATE}    ${POS_NETWORK}    ${POS_CALCJOB}
    Allocation Run Should Exit    ${POS_NETWORK}    Success
    Capture Step    ha0002_tc01_positive_success

TC02 Negative Run Exits Failure
    [Documentation]    A defective calc is caught: RUN CALCULATIONS (Simulate) over "P1 Dashboard" /
    ...    "Daily Well Volume" @ 2021-10-01 exits Failure (the calc errors on equation steps). The
    ...    run mechanism still works — the Failure status is the meaningful test signal.
    [Tags]    run    negative
    Run Allocation Job    ${NEG_DATE}    ${NEG_NETWORK}    ${NEG_CALCJOB}
    Allocation Run Should Exit    ${NEG_NETWORK}    Failure
    Capture Step    ha0002_tc02_negative_failure

TC03 Allocation Results Conserve (DB oracle)
    [Documentation]    Ground truth: a real allocation result must conserve — every allocated
    ...    ALLOC_* quantity (volume/mass/energy) is >= 0, and the day actually has rows. Asserted
    ...    at the DB on PWEL_DAY_ALLOC for 2021-10-01 (22 wells persisted by a prior real run).
    [Tags]    verify    conservation
    Allocation Results Should Conserve    ${CONSERVATION_DATE}
