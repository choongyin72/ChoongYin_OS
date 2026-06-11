*** Settings ***
Documentation       T3 (screen) — Business Unit page object.
...                 Screen: Configuration > Assets > Basic Objects > Business Unit.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${BUSINESS_UNIT_SCREEN}         Business Unit
${BUSINESS_UNIT_TABLE}          manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${BUSINESS_UNIT_INS_CODE}       tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${BUSINESS_UNIT_INS_NAME}       tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${BUSINESS_UNIT_INS_DATE}       tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${BUSINESS_UNIT_UPD_CODE}       tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${BUSINESS_UNIT_UPD_NAME}       tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${BUSINESS_UNIT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Business Unit Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Business Unit screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${BUSINESS_UNIT_SCREEN}

Business Unit Row Should Exist
    [Documentation]    Assert a business unit with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${BUSINESS_UNIT_TABLE}    ${code}

Business Unit Row Should Not Exist
    [Documentation]    Assert a business unit with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${BUSINESS_UNIT_TABLE}    ${code}

Business Unit Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_BUSINESS_UNIT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_BUSINESS_UNIT    ${code}

Business Unit Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_BUSINESS_UNIT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_BUSINESS_UNIT    ${code}

Business Unit Row Should Show Name
    [Documentation]    Assert the Business Unit row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${BUSINESS_UNIT_TABLE}    ${code}    ${name}

Insert Business Unit Record
    [Documentation]    Insert a new business unit: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${BUSINESS_UNIT_INS_CODE}    ${BUSINESS_UNIT_INS_NAME}    ${BUSINESS_UNIT_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Business Unit Name
    [Documentation]    Select the business unit, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${BUSINESS_UNIT_TABLE}
    ...    ${BUSINESS_UNIT_UPD_CODE}
    ...    ${BUSINESS_UNIT_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Business Unit
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${BUSINESS_UNIT_TABLE}    ${BUSINESS_UNIT_DEL_ENDDATE}    ${code}    ${date}
