*** Settings ***
Documentation       EC IUD Test - Tract - Well Setup (Configuration > Assets > Royalty Objects).
...                 Parent-child setup screen (sibling of Unit - Well Setup over the same
...                 WELL_SETUP base): adds/updates/removes a WELL SETUP membership row that
...                 links a Perf Interval (member) to an existing Tract (parent). The member
...                 108_WB1-1_PF1 is only REFERENCED (a membership row is created, updated and
...                 physically deleted again) - the Perf Interval object itself is never
...                 modified. The Tract (Unit 3 Tract 01) is an EXISTING object and already has
...                 other rows (P1 PI-5 / P1 PI-6) which the test NEVER touches. DB oracle =
...                 count-delta on DV_TRACT_WELL_SETUP, so pre-existing rows never affect the result.

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/tract_well_setup_page.resource

Suite Setup         Set Up Tract Well Setup Suite
Suite Teardown      Close EC

Test Tags           iud    tract-well-setup


*** Variables ***
# navigator + member values - pre-flight verified 2026-06-27 (Tract effective 2010-01-01,
# member 108_WB1-1_PF1 effective 2003-01-01, baseline 0 in any tract; cascade UA -> Tract)
${UNIT_AGREEMENT}       Unit Agreement 3
${TRACT}                Unit 3 Tract 01
${PERF_INTERVAL}        108_WB1-1_PF1
${FORM_DATE}            2011-01-01
${START_DATE}           2011-01-01
${UPD_COMMENT}          AUTOTEST_TWS_UPD
${BASE_COUNT}           ${EMPTY}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Record the DB baseline for the member code and confirm the row is
    ...    not currently in the chosen tract's grid (and the update sentinel is absent).
    [Tags]    clean-state
    Well Setup Row Should Not Exist    ${PERF_INTERVAL}
    Comment Should Be Absent In DB    ${UPD_COMMENT}
    Capture Step    tract_well_setup_tc01_clean

TC02 Insert Well Setup
    [Documentation]    Add the membership row under the existing Tract and confirm grid + DB
    ...    (+1 vs baseline). Existing rows (P1 PI-5 / P1 PI-6) are untouched.
    [Tags]    insert
    Insert Well Setup    ${PERF_INTERVAL}    ${START_DATE}
    Well Setup Row Should Exist    ${PERF_INTERVAL}
    ${expected}=    Evaluate    ${BASE_COUNT} + 1
    Perf Interval Count In DB Should Be    ${PERF_INTERVAL}    ${expected}
    Capture Step    tract_well_setup_tc02_inserted

TC03 Update Well Setup
    [Documentation]    Edit the membership row's COMMENTS and confirm the new value
    ...    persisted in DV_TRACT_WELL_SETUP (DB ground truth, not just the grid).
    [Tags]    update
    Update Well Setup Comments    ${PERF_INTERVAL}    ${UPD_COMMENT}
    Comment Should Be Present In DB    ${UPD_COMMENT}
    Well Setup Row Should Exist    ${PERF_INTERVAL}
    Capture Step    tract_well_setup_tc03_updated

TC04 Delete Well Setup
    [Documentation]    Physically delete the membership row and confirm grid + DB (back to
    ...    baseline, and the update sentinel gone with the row).
    [Tags]    delete    cleanup
    Delete Well Setup    ${PERF_INTERVAL}
    Well Setup Row Should Not Exist    ${PERF_INTERVAL}
    Perf Interval Count In DB Should Be    ${PERF_INTERVAL}    ${BASE_COUNT}
    Comment Should Be Absent In DB    ${UPD_COMMENT}
    Capture Step    tract_well_setup_tc04_deleted


*** Keywords ***
Set Up Tract Well Setup Suite
    [Documentation]    Open the screen with the verified cascade navigator context and record
    ...    the DB baseline count for the member code (delta-style verification).
    Open Tract Well Setup Screen    ${UNIT_AGREEMENT}    ${TRACT}    ${FORM_DATE}
    ${n}=    Perf Interval Count In DB    ${PERF_INTERVAL}
    VAR    ${BASE_COUNT}=    ${n}    scope=SUITE
