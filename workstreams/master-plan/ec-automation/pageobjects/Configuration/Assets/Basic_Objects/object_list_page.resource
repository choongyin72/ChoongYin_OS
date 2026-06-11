*** Settings ***
Documentation       T3 (screen) — Object List page object.
...                 Screen: Configuration > Assets > Basic Objects > Object List.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${OBJECT_LIST_SCREEN}           Object List
${OBJECT_LIST_TABLE}            manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${OBJECT_LIST_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${OBJECT_LIST_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${OBJECT_LIST_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# Class Name is MANDATORY on this screen (EC: "Required fields are empty")
${OBJECT_LIST_INS_DD}           tab:tabPanel:objectForm:form:G:0:R:5:C:1:dd
# updateAttributes field IDs (Update — existing object)
${OBJECT_LIST_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${OBJECT_LIST_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${OBJECT_LIST_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Object List Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Object List screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${OBJECT_LIST_SCREEN}

Object List Row Should Exist
    [Documentation]    Assert a object list with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OBJECT_LIST_TABLE}    ${code}

Object List Row Should Not Exist
    [Documentation]    Assert a object list with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OBJECT_LIST_TABLE}    ${code}

Object List Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_OBJECT_LIST.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_OBJECT_LIST    ${code}

Object List Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_OBJECT_LIST.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_OBJECT_LIST    ${code}

Object List Row Should Show Name
    [Documentation]    Assert the Object List row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OBJECT_LIST_TABLE}    ${code}    ${name}

Insert Object List Record
    [Documentation]    Insert a new object list: Code/Name/Start Date + mandatory Class Name -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${class_name}
    Fill New Object Form    ${OBJECT_LIST_INS_CODE}    ${OBJECT_LIST_INS_NAME}    ${OBJECT_LIST_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${OBJECT_LIST_INS_DD}    ${class_name}
    Save And Refresh List

Update Object List Name
    [Documentation]    Select the object list, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${OBJECT_LIST_TABLE}
    ...    ${OBJECT_LIST_UPD_CODE}
    ...    ${OBJECT_LIST_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Object List
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${OBJECT_LIST_TABLE}    ${OBJECT_LIST_DEL_ENDDATE}    ${code}    ${date}
