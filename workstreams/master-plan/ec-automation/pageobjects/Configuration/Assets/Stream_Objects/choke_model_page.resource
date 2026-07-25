*** Settings ***
Documentation       T3 (screen) - Choke Model page object.
...                 Screen: Configuration > Assets > Stream Objects > Choke Model (CO.0217).
...                 Manage-Object (OV). Mandatory Code/Name/Start Date (many optional dropdowns skipped).
...                 Locator variables + thin IUD wrappers delegating to T2 (manage_object) + T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CHKM_SCREEN}          Choke Model
${CHKM_TABLE}           manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert) - Start Date at R4 (Sort Order R2 + Description R3 precede it)
${CHKM_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${CHKM_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${CHKM_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
# updateAttributes field IDs
${CHKM_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${CHKM_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
${CHKM_UPD_DESC}        tab:tabPanel:updateAttributes:form:G:0:R:3:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${CHKM_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Choke Model Screen
    [Documentation]    Suite Setup: launch, login, open Choke Model, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CHKM_SCREEN}    ${user}    ${pass}
    Apply Navigator

Choke Model Row Should Exist
    [Documentation]    Assert a choke model with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${CHKM_TABLE}    ${code}

Choke Model Row Should Not Exist
    [Documentation]    Assert a choke model with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CHKM_TABLE}    ${code}

Choke Model Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CHOKE_MODEL.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CHOKE_MODEL    ${code}

Choke Model Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CHOKE_MODEL.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CHOKE_MODEL    ${code}

Choke Model Row Should Show Name
    [Documentation]    Assert the Choke Model row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CHKM_TABLE}    ${code}    ${name}

Insert Choke Model Record
    [Documentation]    Insert a new choke model: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${CHKM_INS_CODE}    ${code}
    Fill EC Field    ${CHKM_INS_NAME}    ${name}
    Fill EC Date    ${CHKM_INS_DATE}    ${start_date}
    Save
    Apply Navigator

Update Choke Model
    [Documentation]    Select the choke model, confirm loaded, edit Name + Description, Save.
    [Arguments]    ${code}    ${new_name}    ${new_desc}
    Select Object Row    ${CHKM_TABLE}    ${code}
    ${loaded}=    Get Property    css=[id="${CHKM_UPD_CODE}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${CHKM_UPD_NAME}    ${new_name}
    Fill EC Field    ${CHKM_UPD_DESC}    ${new_desc}
    Save
    Apply Navigator

Delete Choke Model
    [Documentation]    Select the choke model, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${CHKM_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${CHKM_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
