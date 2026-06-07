*** Settings ***
Documentation       T3 (screen) — Equipment page object.
...                 Screen: Configuration > Assets > Equipment Objects > Equipment.
...                 Manage-Object (OV) screen WITH a 5-field cascading navigator.
...                 Holds Equipment's locators + thin IUD wrappers that delegate to
...                 T2 (manage_object), T1 (navigator/common), and DbVerify.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${EQP_SCREEN}           Equipment
${EQP_TABLE}            manageObject:form:T_data
# cascading navigator — EXACT values (typing is unreliable; chosen from dd_panel)
${EQP_NAV_PU}           Production Unit
${EQP_NAV_AREA}         Offshore area
${EQP_NAV_FACILITY}     Offshore facility
${EQP_NAV_CLASS}        Compressor
# objectForm field IDs (Insert) — Equipment Type R:0 auto-fills (read-only)
${EQP_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${EQP_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${EQP_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
# updateAttributes field ID (Update)
${EQP_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${EQP_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Equipment Screen
    [Documentation]    Suite Setup: launch, login as ${user} (default env user),
    ...    navigate to Equipment, and apply the cascading navigator.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${EQP_SCREEN}
    Apply Equipment Navigator

Apply Equipment Navigator
    [Documentation]    Set the 5-field cascading navigator (exact values) and load the list.
    Set Navigator Filter    G:1    ${EQP_NAV_PU}
    Set Navigator Filter    G:2    ${EQP_NAV_AREA}
    Set Navigator Filter    G:3    ${EQP_NAV_FACILITY}
    Set Navigator Filter    G:4    ${EQP_NAV_CLASS}
    Apply Navigator

Equipment Rows Should Be Loaded
    [Documentation]    Assert the navigator returned rows (proves the filter combo is correct).
    ${rows}=    Get Table Rows    ${EQP_TABLE}
    Should Not Be Empty    ${rows}    msg=Navigator returned no rows - filter combo wrong

Equipment Row Should Exist
    [Documentation]    Assert an equipment with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${EQP_TABLE}    ${code}

Equipment Row Should Not Exist
    [Documentation]    Assert an equipment with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${EQP_TABLE}    ${code}

Equipment Row Should Show Name
    [Documentation]    Assert the equipment row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${EQP_TABLE}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Equipment row ${code} does not show name ${name}

Equipment Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_EQPM.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_eqpm    ${code}

Equipment Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_EQPM.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_eqpm    ${code}

Insert Equipment Record
    [Documentation]    Insert a new equipment: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${EQP_INS_CODE}    ${code}
    Fill EC Field    ${EQP_INS_NAME}    ${name}
    Fill EC Date    ${EQP_INS_DATE}    ${start_date}
    Save
    Apply Navigator

Update Equipment Name
    [Documentation]    Select the equipment, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${EQP_TABLE}    ${code}
    Fill EC Field    ${EQP_UPD_NAME}    ${new_name}
    Save
    Apply Navigator

Delete Equipment
    [Documentation]    Select the equipment, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${EQP_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${EQP_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
