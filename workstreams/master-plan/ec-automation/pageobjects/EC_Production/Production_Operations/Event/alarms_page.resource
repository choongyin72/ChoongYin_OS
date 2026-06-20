*** Settings ***
Documentation       T3 (screen) — Alarms page object.
...                 Screen: EC Production > Production Operations > Event > Alarms.
...                 EVENT-LOG pattern (NEW): a DATA/DAY class (FCTY_DAY_ALARM) shown as a gated
...                 inline grid — the PU/Area/Facility-Class-1 cascade navigator (+ Date) + GO must be
...                 applied before the grid loads, then you ADD alarm rows (TV-style cells). There is
...                 no object code; rows are identified by a unique REASON marker. Insert/Delete are
...                 PHYSICAL (event rows). DB oracle = count of OV view DV_ALARMS by the REASON marker
...                 (reuses T2 table_class + T1 navigator/table + DbVerify View Count Where).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/table_class.resource


*** Variables ***
${ALARMS_SCREEN}        Alarms
${ALARMS_TABLE}         alarms:form:T_data
${ALARMS_CELL_PREFIX}    alarms:form:T
# navigator: Date (G:0) + cascade PU(G:1) -> Area(G:2) -> Facility Class 1(G:3), all gate the grid; + GO
${ALARMS_NAV_DATE}      nav:form:G:0:R:1:C:0:da_input
${ALARMS_NAV_PU}        G:1
${ALARMS_NAV_AREA}      G:2
${ALARMS_NAV_FACILITY}    G:3
# inline-grid cell suffixes (recon 2026-06-19): C0 Time / C1 Area dd / C2 Type-of-Alarm dd (MANDATORY) /
# C3 Reason (text — the marker/oracle key) / C4 Report cb / C5 Duration
${ALARMS_TYPE_CELL}     C2_dd
${ALARMS_REASON_SUFFIX}    C3_in
# DB oracle
${ALARMS_DB_VIEW}       DV_ALARMS
${ALARMS_DB_COLUMN}     REASON


*** Keywords ***
Open Alarms Screen
    [Documentation]    Suite Setup: launch, login, navigate, set the Date + PU/Area/Facility cascade
    ...    and apply it (the alarm grid is empty until the navigator + GO are applied).
    [Arguments]    ${date}    ${pu}    ${area}    ${facility}    ${user}=${EC_USER}    ${pass}=${EC_PASS}    # robocop: off=LEN07
    Launch EC And Open Screen    ${ALARMS_SCREEN}    ${user}    ${pass}
    Fill EC Date    ${ALARMS_NAV_DATE}    ${date}
    Set Navigator Filter    ${ALARMS_NAV_PU}    ${pu}
    Set Navigator Filter    ${ALARMS_NAV_AREA}    ${area}
    Set Navigator Filter    ${ALARMS_NAV_FACILITY}    ${facility}
    Apply Navigator

Alarm Count In DB Should Be
    [Documentation]    DB ground-truth: assert DV_ALARMS rows whose REASON = ${reason} equals ${expected}
    ...    (the REASON marker is unique per run, so this is exactly the test alarm — count-delta safe).
    [Arguments]    ${reason}    ${expected}
    View Count Where Should Be    ${ALARMS_DB_VIEW}    ${ALARMS_DB_COLUMN}    ${reason}    ${expected}

Insert Alarm
    [Documentation]    Insert toolbar -> "Alarms" -> blank row -> pick Type of Alarm (mandatory dd, first
    ...    option) -> RE-FIND the row -> type the REASON marker -> Save -> reload (Apply Navigator).
    [Arguments]    ${reason}
    Insert New Grid Row By Label    Alarms
    ${row}=    Find Grid Row By Cell Input Value    ${ALARMS_TABLE}    ${ALARMS_REASON_SUFFIX}    ${EMPTY}
    Should Be True    ${row} >= 0    msg=No blank alarm row appeared after Insert
    Select First EC Dropdown Option    ${ALARMS_CELL_PREFIX}:${row}:${ALARMS_TYPE_CELL}
    ${row}=    Find Grid Row By Cell Input Value    ${ALARMS_TABLE}    ${ALARMS_REASON_SUFFIX}    ${EMPTY}
    Should Be True    ${row} >= 0    msg=Blank alarm row vanished after Type-of-Alarm selection
    Type Cell By Id    ${ALARMS_CELL_PREFIX}:${row}:${ALARMS_REASON_SUFFIX}    ${reason}
    Save
    Apply Navigator

Update Alarm Reason
    [Documentation]    Edit the alarm's Reason from ${old} to ${new} (Reason is the marker, so a
    ...    Reason-change is a DB-verifiable UPDATE), Save, reload.
    [Arguments]    ${old}    ${new}
    ${row}=    Find Grid Row By Cell Input Value    ${ALARMS_TABLE}    ${ALARMS_REASON_SUFFIX}    ${old}
    Should Be True    ${row} >= 0    msg=Alarm row with Reason ${old} not found for update
    Type Cell By Id    ${ALARMS_CELL_PREFIX}:${row}:${ALARMS_REASON_SUFFIX}    ${new}
    Save
    Apply Navigator

Delete Alarm
    [Documentation]    Select the alarm row by its REASON marker, Delete toolbar -> "Alarms" -> Save -> reload.
    [Arguments]    ${reason}
    ${row}=    Find Grid Row By Cell Input Value    ${ALARMS_TABLE}    ${ALARMS_REASON_SUFFIX}    ${reason}
    Should Be True    ${row} >= 0    msg=Alarm row with Reason ${reason} not found for delete
    Click    css=[id="${ALARMS_CELL_PREFIX}:${row}:${ALARMS_REASON_SUFFIX}"]
    Sleep    0.8s
    Delete Selected Grid Row    Alarms
    Save
    Apply Navigator

Alarm Row Should Exist
    [Documentation]    Assert an alarm row whose Reason cell = ${reason} is present in the grid.
    [Arguments]    ${reason}
    ${row}=    Find Grid Row By Cell Input Value    ${ALARMS_TABLE}    ${ALARMS_REASON_SUFFIX}    ${reason}
    Should Be True    ${row} >= 0    msg=Expected alarm row with Reason ${reason} in ${ALARMS_TABLE}

Alarm Row Should Not Exist
    [Documentation]    Assert no alarm row shows ${reason} in its Reason cell.
    [Arguments]    ${reason}
    ${row}=    Find Grid Row By Cell Input Value    ${ALARMS_TABLE}    ${ALARMS_REASON_SUFFIX}    ${reason}
    Should Be Equal As Integers    ${row}    -1    msg=Alarm row ${reason} should NOT exist
