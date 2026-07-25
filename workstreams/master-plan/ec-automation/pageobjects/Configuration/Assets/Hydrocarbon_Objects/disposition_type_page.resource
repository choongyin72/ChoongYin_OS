*** Settings ***
Documentation       T3 (screen) - Disposition Type page object.
...                 Screen: Configuration > Assets > Hydrocarbon Objects > Disposition Type (CO.0208).
...                 Manage-Object (OV) screen. Locator variables + thin IUD wrappers delegating to
...                 T2 (manage_object) and T1 (common). Plain OV (no mandatory dropdowns).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${DISP_SCREEN}          Disposition Type
${DISP_TABLE}           manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert - new object); mandatory rows R2/R3/R4 (R0/R1 = optional Master System)
${DISP_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${DISP_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:3:C:1:in
${DISP_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
# updateAttributes field IDs (Update - existing object)
${DISP_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
${DISP_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:3:C:1:in
${DISP_UPD_DESC}        tab:tabPanel:updateAttributes:form:G:0:R:5:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${DISP_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Disposition Type Screen
    [Documentation]    Suite Setup: launch, login, open the Disposition Type screen, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${DISP_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Disposition Type Row Should Exist
    [Documentation]    Assert a disposition type with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${DISP_TABLE}    ${code}

Disposition Type Row Should Not Exist
    [Documentation]    Assert a disposition type with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${DISP_TABLE}    ${code}

Disposition Type Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_DISPOSITION_TYPE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_DISPOSITION_TYPE    ${code}

Disposition Type Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_DISPOSITION_TYPE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_DISPOSITION_TYPE    ${code}

Disposition Type Row Should Show Name
    [Documentation]    Assert the Disposition Type row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${DISP_TABLE}    ${code}    ${name}

Insert Disposition Type Record
    [Documentation]    Insert a new disposition type: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${DISP_INS_CODE}    ${code}
    Fill EC Field    ${DISP_INS_NAME}    ${name}
    Fill EC Date    ${DISP_INS_DATE}    ${start_date}
    Save
    Apply Navigator

Update Disposition Type
    [Documentation]    Select the disposition type, edit Name + Description, save + reload.
    [Arguments]    ${code}    ${new_name}    ${new_desc}
    Select Object Row    ${DISP_TABLE}    ${code}
    ${loaded}=    Get Property    css=[id="${DISP_UPD_CODE}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${DISP_UPD_NAME}    ${new_name}
    Fill EC Field    ${DISP_UPD_DESC}    ${new_desc}
    Save
    Apply Navigator

Delete Disposition Type
    [Documentation]    Select the disposition type, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${DISP_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${DISP_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
