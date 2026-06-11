*** Settings ***
Documentation       T3 (screen) — County page object.
...                 Screen: Configuration > Assets > Basic Objects > County.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${COUNTY_SCREEN}            County
${COUNTY_TABLE}             manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${COUNTY_INS_CODE}          tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${COUNTY_INS_NAME}          tab:tabPanel:objectForm:form:G:0:R:3:C:1:in
${COUNTY_INS_DATE}          tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${COUNTY_UPD_CODE}          tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
${COUNTY_UPD_NAME}          tab:tabPanel:updateAttributes:form:G:0:R:3:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${COUNTY_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open County Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the County screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${COUNTY_SCREEN}

County Row Should Exist
    [Documentation]    Assert a county with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${COUNTY_TABLE}    ${code}

County Row Should Not Exist
    [Documentation]    Assert a county with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${COUNTY_TABLE}    ${code}

County Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_COUNTY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_COUNTY    ${code}

County Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_COUNTY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_COUNTY    ${code}

County Row Should Show Name
    [Documentation]    Assert the County row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${COUNTY_TABLE}    ${code}    ${name}

Insert County Record
    [Documentation]    Insert a new county: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${COUNTY_INS_CODE}    ${COUNTY_INS_NAME}    ${COUNTY_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update County Name
    [Documentation]    Select the county, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${COUNTY_TABLE}    ${COUNTY_UPD_CODE}    ${COUNTY_UPD_NAME}    ${code}    ${new_name}

Delete County
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${COUNTY_TABLE}    ${COUNTY_DEL_ENDDATE}    ${code}    ${date}
