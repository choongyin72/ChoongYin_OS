*** Settings ***
Documentation       EC IUD Test - Alarms (EC Production > Production Operations > Event > Alarms).
...                 EVENT-LOG pattern: a gated inline grid (PU/Area/Facility cascade + Date + GO) where
...                 you ADD alarm rows. No object code — rows are identified by a unique REASON marker.
...                 INSERT (pick Type of Alarm + type Reason), UPDATE (change Reason — DB-verifiable),
...                 DELETE (physical). DB oracle = count of DV_ALARMS by the REASON marker.
...                 NEVER touch existing data: a unique AUTOTEST_ALARM_<timestamp> Reason per run; the
...                 referenced facility + Type-of-Alarm list are READ-ONLY seed data.

Resource            ../../../../pageobjects/EC_Production/Production_Operations/Event/alarms_page.resource

Suite Setup         Set Up Alarms Suite
Suite Teardown      Close EC

Test Tags           iud    alarms


*** Variables ***
# Data-bearing facility-day (event screen — like the N1 screens, the date is pinned, not a master start date)
${ALARM_DATE}       2026-06-18
${NAV_PU}           P1 Production Unit
${NAV_AREA}         P1 Area
${NAV_FACILITY}     P1 Facility 1
${REASON}           ${EMPTY}
${REASON_UPD}       ${EMPTY}


*** Test Cases ***
TC01 Verify Clean State
    [Documentation]    Confirm the (freshly generated) test alarm does not exist before inserting.
    [Tags]    clean-state
    Alarm Row Should Not Exist    ${REASON}
    Alarm Count In DB Should Be    ${REASON}    0
    Capture Step    alarms_tc01_clean

TC02 Insert New Alarm
    [Documentation]    Insert a new alarm (Type of Alarm + Reason marker) and confirm it appears + persisted.
    [Tags]    insert
    Insert Alarm    ${REASON}
    Alarm Row Should Exist    ${REASON}
    Alarm Count In DB Should Be    ${REASON}    1
    Capture Step    alarms_tc02_inserted

TC03 Update Alarm Reason
    [Documentation]    Change the alarm Reason and confirm the DB reflects the new value (and not the old).
    [Tags]    update
    Update Alarm Reason    ${REASON}    ${REASON_UPD}
    Alarm Row Should Exist    ${REASON_UPD}
    Alarm Count In DB Should Be    ${REASON_UPD}    1
    Alarm Count In DB Should Be    ${REASON}    0
    Capture Step    alarms_tc03_updated

TC04 Delete Alarm
    [Documentation]    Physically delete the alarm and confirm it is gone (grid + DB).
    [Tags]    delete    cleanup
    Delete Alarm    ${REASON_UPD}
    Alarm Row Should Not Exist    ${REASON_UPD}
    Alarm Count In DB Should Be    ${REASON_UPD}    0
    Capture Step    alarms_tc04_deleted


*** Keywords ***
Set Up Alarms Suite
    [Documentation]    Generate a unique Reason marker (+ its _UPD variant), then open the Alarms screen
    ...    with the Date + P1 cascade navigator applied.
    ${code}=    Generate Unique Code    AUTOTEST_ALARM_
    VAR    ${REASON}    ${code}    scope=SUITE
    VAR    ${REASON_UPD}    ${code}_UPD    scope=SUITE
    Open Alarms Screen    ${ALARM_DATE}    ${NAV_PU}    ${NAV_AREA}    ${NAV_FACILITY}
