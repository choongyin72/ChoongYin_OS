*** Settings ***
Documentation       Issue_1052 SUM 98-102% check — EC web SCREEN EVIDENCE (headed).
...                 Validation Overview - Pluto Scarborough -> group tree PAGE 2
...                 ("Daily Sampling Validations") -> select the gas-component sum group ->
...                 filter the result grid's Message column to isolate the mole% (1156/1157)
...                 and molecular-weight% (1077) sum-check ERRORs -> screenshot each.

Library             Browser
Resource            ../../../../pageobjects/Configuration/System/Validation/validation_overview_pluto_scarborough.resource

Suite Setup         Open Validation Overview Screen
Suite Teardown      Close EC

Test Tags           sum    evidence    issue_1052    layer2


*** Variables ***
${SHOTS}            ${OUTPUT DIR}
${WELL_GRP}         Well Gas Component Analysis - Daily Sampling Validations
${STREAM_GRP}       Stream Gas Component Analysis - Daily Sampling Validations


*** Test Cases ***
Stream Sum — Mole% And WT% Isolated
    [Documentation]    Isolate the stream mole% (1156) then WT% (1077) sum-check errors in the
    ...    result grid and screenshot each (fresh group select between filters).
    [Tags]    stream
    Select Daily Sampling Group    ${STREAM_GRP}    2026-05-01    2026-05-31
    Show Only Log Messages By Ticking    sum of mole percentage
    ${m}=    Count Message Rows
    Log    STREAM_MOLE :: ${m}    console=True
    Take Screenshot    filename=${SHOTS}/sum_stream_MOLE_pct.png    fullPage=True
    # reset the grid (restores all message options) before isolating WT%
    Select Daily Sampling Group    ${STREAM_GRP}    2026-05-01    2026-05-31
    Show Only Log Messages By Ticking    weight percentage
    ${w}=    Count Message Rows
    Log    STREAM_WT :: ${w}    console=True
    Take Screenshot    filename=${SHOTS}/sum_stream_WT_pct.png    fullPage=True

Well Sum — Mole% Isolated (1157 fires)
    [Documentation]    Isolate the well mole% (1157) sum-check errors and screenshot them.
    [Tags]    well
    Select Daily Sampling Group    ${WELL_GRP}    2026-06-01    2026-06-11
    Show Only Log Messages By Ticking    sum of mole percentage
    ${m}=    Count Message Rows
    Log    WELL_MOLE :: ${m}    console=True
    Take Screenshot    filename=${SHOTS}/sum_well_MOLE_pct.png    fullPage=True


*** Keywords ***
Select Daily Sampling Group
    [Documentation]    Set date window, GO, jump to tree page 2, select the named group so its
    ...    logged results populate the detail grid (no re-run — uses existing CTRL_CHECK_LOG).
    [Arguments]    ${group_desc}    ${from_date}    ${to_date}
    # full screen reload first — clears any persisted column filter (cascading filter trap)
    Navigate To Screen    ${VO_SCREEN}
    Wait For Load State    networkidle    timeout=30s
    Sleep    1s
    Set Validation Date Range And Go    ${from_date}    ${to_date}
    Go To Groups Tree Page    2
    ${idx}=    Find Group Row Index    ${group_desc}
    Should Be True    ${idx} >= 0    msg=Group not found on page 2: ${group_desc}
    Select Validation Group    ${group_desc}
    Sleep    1.5s

Count Message Rows
    [Documentation]    Return {mole, molwt, rows} counts from the visible result-detail grid.
    ${counts}=    Evaluate JavaScript    ${None}
    ...    () => { const tb=document.querySelector('[id="logs:form:T_data"]'); const txt=tb?(tb.innerText||''):''; return { mole:(txt.match(/sum of mole percentage/g)||[]).length, molwt:(txt.match(/molecular weight percentage/g)||[]).length, rows: tb?tb.querySelectorAll('tr').length:-1 }; }
    RETURN    ${counts}
