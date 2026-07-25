*** Settings ***
Documentation       T3 (screen) - Report Area page object.
...                 Screen: Reporting > Report Area (RP.0017). Manage-Object (OV) screen.
...                 Simplest OV: Code / Name / Start Date (no Description, no dropdowns).
...                 Locator variables + thin IUD wrappers delegating to T2 (manage_object) + T1 (common).

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/common.resource
Resource            ../../resources/manage_object.resource


*** Variables ***
${RPTA_SCREEN}          Report Area
${RPTA_TABLE}           manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert - new object)
${RPTA_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${RPTA_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${RPTA_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update - existing object)
${RPTA_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${RPTA_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${RPTA_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Report Area Screen
    [Documentation]    Suite Setup: launch, login, open Report Area, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${RPTA_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Report Area Row Should Exist
    [Arguments]    ${code}
    Row Should Exist    ${RPTA_TABLE}    ${code}

Report Area Row Should Not Exist
    [Arguments]    ${code}
    Row Should Not Exist    ${RPTA_TABLE}    ${code}

Report Area Should Exist In DB
    [Arguments]    ${code}
    Code Should Be Present In View    OV_REPORT_AREA    ${code}

Report Area Should Not Exist In DB
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_REPORT_AREA    ${code}

Report Area Row Should Show Name
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${RPTA_TABLE}    ${code}    ${name}

Insert Report Area Record
    [Documentation]    Insert a new report area: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${RPTA_INS_CODE}    ${code}
    Fill EC Field    ${RPTA_INS_NAME}    ${name}
    Fill EC Date    ${RPTA_INS_DATE}    ${start_date}
    Save
    Apply Navigator

Update Report Area Name
    [Documentation]    Select the report area, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${RPTA_TABLE}    ${code}
    ${loaded}=    Get Property    css=[id="${RPTA_UPD_CODE}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${RPTA_UPD_NAME}    ${new_name}
    Save
    Apply Navigator

Delete Report Area
    [Documentation]    Select the report area, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${RPTA_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${RPTA_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
