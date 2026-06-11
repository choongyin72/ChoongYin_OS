*** Settings ***
Documentation       T3 (screen) — Sub Field page object.
...                 Screen: Configuration > Assets > Commercial Objects > Sub Field.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SUB_FIELD_SCREEN}         Sub Field
${SUB_FIELD_TABLE}          manageObject:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${SUB_FIELD_INS_CODE}       tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${SUB_FIELD_INS_NAME}       tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${SUB_FIELD_INS_DATE}       tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${SUB_FIELD_UPD_CODE}       tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${SUB_FIELD_UPD_NAME}       tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${SUB_FIELD_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Sub Field Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Sub Field screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${SUB_FIELD_SCREEN}

Sub Field Row Should Exist
    [Documentation]    Assert a sub field with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${SUB_FIELD_TABLE}    ${code}

Sub Field Row Should Not Exist
    [Documentation]    Assert a sub field with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${SUB_FIELD_TABLE}    ${code}

Sub Field Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_SUB_FIELD.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_SUB_FIELD    ${code}

Sub Field Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_SUB_FIELD.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_SUB_FIELD    ${code}

Sub Field Row Should Show Name
    [Documentation]    Assert the Sub Field row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${SUB_FIELD_TABLE}    ${code}    ${name}

Insert Sub Field Record
    [Documentation]    Insert a new sub field: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${SUB_FIELD_INS_CODE}    ${SUB_FIELD_INS_NAME}    ${SUB_FIELD_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Sub Field Name
    [Documentation]    Select the sub field, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${SUB_FIELD_TABLE}
    ...    ${SUB_FIELD_UPD_CODE}
    ...    ${SUB_FIELD_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Sub Field
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${SUB_FIELD_TABLE}    ${SUB_FIELD_DEL_ENDDATE}    ${code}    ${date}
