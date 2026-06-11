*** Settings ***
Documentation       T3 (screen) — Licence page object.
...                 Screen: Configuration > Assets > Commercial Objects > Licence.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${LICENCE_SCREEN}           Licence
${LICENCE_TABLE}            manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${LICENCE_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${LICENCE_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${LICENCE_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:6:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${LICENCE_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${LICENCE_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${LICENCE_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Licence Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Licence screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${LICENCE_SCREEN}

Licence Row Should Exist
    [Documentation]    Assert a licence with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${LICENCE_TABLE}    ${code}

Licence Row Should Not Exist
    [Documentation]    Assert a licence with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${LICENCE_TABLE}    ${code}

Licence Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_LICENCE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_LICENCE    ${code}

Licence Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_LICENCE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_LICENCE    ${code}

Licence Row Should Show Name
    [Documentation]    Assert the Licence row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${LICENCE_TABLE}    ${code}    ${name}

Insert Licence Record
    [Documentation]    Insert a new licence: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${LICENCE_INS_CODE}    ${LICENCE_INS_NAME}    ${LICENCE_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Licence Name
    [Documentation]    Select the licence, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${LICENCE_TABLE}    ${LICENCE_UPD_CODE}    ${LICENCE_UPD_NAME}    ${code}    ${new_name}

Delete Licence
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${LICENCE_TABLE}    ${LICENCE_DEL_ENDDATE}    ${code}    ${date}
