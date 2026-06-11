*** Settings ***
Documentation       T3 (screen) — Field Group page object.
...                 Screen: Configuration > Assets > Commercial Objects > Field Group.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${FIELD_GROUP_SCREEN}           Field Group
${FIELD_GROUP_TABLE}            manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${FIELD_GROUP_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${FIELD_GROUP_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${FIELD_GROUP_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${FIELD_GROUP_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${FIELD_GROUP_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${FIELD_GROUP_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Field Group Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Field Group screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${FIELD_GROUP_SCREEN}

Field Group Row Should Exist
    [Documentation]    Assert a field group with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${FIELD_GROUP_TABLE}    ${code}

Field Group Row Should Not Exist
    [Documentation]    Assert a field group with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${FIELD_GROUP_TABLE}    ${code}

Field Group Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FIELD_GROUP.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FIELD_GROUP    ${code}

Field Group Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FIELD_GROUP.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FIELD_GROUP    ${code}

Field Group Row Should Show Name
    [Documentation]    Assert the Field Group row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${FIELD_GROUP_TABLE}    ${code}    ${name}

Insert Field Group Record
    [Documentation]    Insert a new field group: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${FIELD_GROUP_INS_CODE}    ${FIELD_GROUP_INS_NAME}    ${FIELD_GROUP_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Field Group Name
    [Documentation]    Select the field group, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${FIELD_GROUP_TABLE}
    ...    ${FIELD_GROUP_UPD_CODE}
    ...    ${FIELD_GROUP_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Field Group
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${FIELD_GROUP_TABLE}    ${FIELD_GROUP_DEL_ENDDATE}    ${code}    ${date}
