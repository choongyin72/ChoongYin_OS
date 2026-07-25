*** Settings ***
Documentation       T3 (screen) - Choke page object.
...                 Screen: Configuration > Assets > Well and Reservoir Objects > Choke (CO.0185).
...                 Manage-Object (OV) screen. Mandatory Code/Name/Start Date (optional Choke Type dd skipped).
...                 Locator variables + thin IUD wrappers delegating to T2 (manage_object) + T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CHOKE_SCREEN}         Choke
${CHOKE_TABLE}          manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert - new object)
${CHOKE_INS_CODE}       tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${CHOKE_INS_NAME}       tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${CHOKE_INS_DATE}       tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update - existing object)
${CHOKE_UPD_CODE}       tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${CHOKE_UPD_NAME}       tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
${CHOKE_UPD_COMMENTS}   tab:tabPanel:updateAttributes:form:G:0:R:4:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${CHOKE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Choke Screen
    [Documentation]    Suite Setup: launch, login, open Choke, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CHOKE_SCREEN}    ${user}    ${pass}
    Apply Navigator

Choke Row Should Exist
    [Documentation]    Assert a choke with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${CHOKE_TABLE}    ${code}

Choke Row Should Not Exist
    [Documentation]    Assert a choke with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CHOKE_TABLE}    ${code}

Choke Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CHOKE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CHOKE    ${code}

Choke Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CHOKE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CHOKE    ${code}

Choke Row Should Show Name
    [Documentation]    Assert the Choke row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CHOKE_TABLE}    ${code}    ${name}

Insert Choke Record
    [Documentation]    Insert a new choke: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${CHOKE_INS_CODE}    ${code}
    Fill EC Field    ${CHOKE_INS_NAME}    ${name}
    Fill EC Date    ${CHOKE_INS_DATE}    ${start_date}
    Save
    Apply Navigator

Update Choke
    [Documentation]    Select the choke, confirm loaded, edit Name + Comments, Save.
    [Arguments]    ${code}    ${new_name}    ${new_comments}
    Select Object Row    ${CHOKE_TABLE}    ${code}
    ${loaded}=    Get Property    css=[id="${CHOKE_UPD_CODE}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${CHOKE_UPD_NAME}    ${new_name}
    Fill EC Field    ${CHOKE_UPD_COMMENTS}    ${new_comments}
    Save
    Apply Navigator

Delete Choke
    [Documentation]    Select the choke, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${CHOKE_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${CHOKE_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
