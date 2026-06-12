*** Settings ***
Documentation       T3 (screen) — Region page object.
...                 Screen: Configuration > Assets > Basic Objects > Region.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${REGION_SCREEN}            Region
${REGION_TABLE}             manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${REGION_INS_CODE}          tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${REGION_INS_NAME}          tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${REGION_INS_DATE}          tab:tabPanel:objectForm:form:G:0:R:4:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${REGION_UPD_CODE}          tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${REGION_UPD_NAME}          tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${REGION_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Region Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Region screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${REGION_SCREEN}    ${user}    ${pass}

Region Row Should Exist
    [Documentation]    Assert a region with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${REGION_TABLE}    ${code}

Region Row Should Not Exist
    [Documentation]    Assert a region with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${REGION_TABLE}    ${code}

Region Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_REGION.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_REGION    ${code}

Region Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_REGION.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_REGION    ${code}

Region Row Should Show Name
    [Documentation]    Assert the Region row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${REGION_TABLE}    ${code}    ${name}

Insert Region Record
    [Documentation]    Insert a new region: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${REGION_INS_CODE}    ${REGION_INS_NAME}    ${REGION_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Region Name
    [Documentation]    Select the region, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${REGION_TABLE}    ${REGION_UPD_CODE}    ${REGION_UPD_NAME}    ${code}    ${new_name}

Delete Region
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${REGION_TABLE}    ${REGION_DEL_ENDDATE}    ${code}    ${date}
