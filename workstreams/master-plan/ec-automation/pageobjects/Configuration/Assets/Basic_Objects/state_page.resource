*** Settings ***
Documentation       T3 (screen) — State page object.
...                 Screen: Configuration > Assets > Basic Objects > State.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${STATE_SCREEN}         State
${STATE_TABLE}          manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${STATE_INS_CODE}       tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${STATE_INS_NAME}       tab:tabPanel:objectForm:form:G:0:R:3:C:1:in
${STATE_INS_DATE}       tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${STATE_UPD_CODE}       tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
${STATE_UPD_NAME}       tab:tabPanel:updateAttributes:form:G:0:R:3:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${STATE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open State Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the State screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${STATE_SCREEN}    ${user}    ${pass}

State Row Should Exist
    [Documentation]    Assert a state with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${STATE_TABLE}    ${code}

State Row Should Not Exist
    [Documentation]    Assert a state with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${STATE_TABLE}    ${code}

State Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_STATE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_STATE    ${code}

State Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_STATE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_STATE    ${code}

State Row Should Show Name
    [Documentation]    Assert the State row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${STATE_TABLE}    ${code}    ${name}

Insert State Record
    [Documentation]    Insert a new state: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${STATE_INS_CODE}    ${STATE_INS_NAME}    ${STATE_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update State Name
    [Documentation]    Select the state, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${STATE_TABLE}    ${STATE_UPD_CODE}    ${STATE_UPD_NAME}    ${code}    ${new_name}

Delete State
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${STATE_TABLE}    ${STATE_DEL_ENDDATE}    ${code}    ${date}
