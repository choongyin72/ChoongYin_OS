*** Settings ***
Documentation       EC IUD Test - Unit - Well Setup (Configuration > Assets > Royalty Objects).
...                 Parent-child setup screen: adds/removes a WELL SETUP membership row that
...                 links a Perf Interval (member) to an existing Unit Agreement (parent).
...                 The member object 108_WB1-1_PF1 is only REFERENCED (a membership row is
...                 created and physically deleted again) - the Perf Interval object itself is
...                 never modified. Parent Unit Agreement 3 (UNIT_3) is EMPTY before/after, so
...                 no existing data is touched. DB oracle = count-delta on DV_UNIT_WELL_SETUP,
...                 so pre-existing rows in other agreements never affect the result.

Resource            ../../../../pageobjects/Configuration/Assets/Royalty_Objects/unit_well_setup_page.resource

Suite Setup         Set Up Unit Well Setup Suite
Suite Teardown      Close EC

Test Tags           iud    unit-well-setup


*** Variables ***
# navigator + member values - pre-flight verified 2026-06-27 (UNIT_3 effective 2010-01-01,
# perf interval 108_WB1-1_PF1 effective 2003-01-01, both windows open; baseline 0 anywhere)
${UNIT_AGREEMENT}       Unit Agreement 3
${PERF_INTERVAL}        108_WB1-1_PF1
${FORM_DATE}            2011-01-01
${START_DATE}           2011-01-01
${UPD_COMMENT}          AUTOTEST_UWS_UPD
${BASE_COUNT}           ${EMPTY}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Record the DB baseline for the member code and confirm the row is
    ...    not currently in the chosen agreement's grid (and the update sentinel is absent).
    [Tags]    clean-state
    Well Setup Row Should Not Exist    ${PERF_INTERVAL}
    Comment Should Be Absent In DB    ${UPD_COMMENT}
    Capture Step    unit_well_setup_tc01_clean

TC02 Insert Well Setup
    [Documentation]    Add the membership row and confirm grid + DB (+1 vs baseline).
    [Tags]    insert
    Insert Well Setup    ${PERF_INTERVAL}    ${START_DATE}
    Well Setup Row Should Exist    ${PERF_INTERVAL}
    ${expected}=    Evaluate    ${BASE_COUNT} + 1
    Perf Interval Count In DB Should Be    ${PERF_INTERVAL}    ${expected}
    Capture Step    unit_well_setup_tc02_inserted

TC03 Update Well Setup
    [Documentation]    Edit the membership row's COMMENTS and confirm the new value
    ...    persisted in DV_UNIT_WELL_SETUP (DB ground truth, not just the grid).
    [Tags]    update
    Update Well Setup Comments    ${PERF_INTERVAL}    ${UPD_COMMENT}
    Comment Should Be Present In DB    ${UPD_COMMENT}
    Well Setup Row Should Exist    ${PERF_INTERVAL}
    Capture Step    unit_well_setup_tc03_updated

TC04 Delete Well Setup
    [Documentation]    Physically delete the membership row and confirm grid + DB (back to
    ...    baseline, and the update sentinel gone with the row).
    [Tags]    delete    cleanup
    Delete Well Setup    ${PERF_INTERVAL}
    Well Setup Row Should Not Exist    ${PERF_INTERVAL}
    Perf Interval Count In DB Should Be    ${PERF_INTERVAL}    ${BASE_COUNT}
    Comment Should Be Absent In DB    ${UPD_COMMENT}
    Capture Step    unit_well_setup_tc04_deleted


*** Keywords ***
Set Up Unit Well Setup Suite
    [Documentation]    Open the screen with the verified navigator context and record the
    ...    DB baseline count for the member code (delta-style verification).
    Open Unit Well Setup Screen    ${UNIT_AGREEMENT}    ${FORM_DATE}
    ${n}=    Perf Interval Count In DB    ${PERF_INTERVAL}
    VAR    ${BASE_COUNT}=    ${n}    scope=SUITE
