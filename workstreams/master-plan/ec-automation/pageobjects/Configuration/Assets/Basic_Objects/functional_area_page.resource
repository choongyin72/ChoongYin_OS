*** Settings ***
Documentation       T3 (screen) — Functional Area page object.
...                 Screen: Configuration > Assets > Basic Objects > Functional Area.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${FUNCTIONAL_AREA_SCREEN}           Functional Area
${FUNCTIONAL_AREA_TABLE}            manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${FUNCTIONAL_AREA_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${FUNCTIONAL_AREA_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${FUNCTIONAL_AREA_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${FUNCTIONAL_AREA_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${FUNCTIONAL_AREA_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${FUNCTIONAL_AREA_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Functional Area Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Functional Area screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${FUNCTIONAL_AREA_SCREEN}

Functional Area Row Should Exist
    [Documentation]    Assert a functional area with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${FUNCTIONAL_AREA_TABLE}    ${code}

Functional Area Row Should Not Exist
    [Documentation]    Assert a functional area with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${FUNCTIONAL_AREA_TABLE}    ${code}

Functional Area Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FUNCTIONAL_AREA.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FUNCTIONAL_AREA    ${code}

Functional Area Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FUNCTIONAL_AREA.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FUNCTIONAL_AREA    ${code}

Functional Area Row Should Show Name
    [Documentation]    Assert the Functional Area row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${FUNCTIONAL_AREA_TABLE}    ${code}    ${name}

Insert Functional Area Record
    [Documentation]    Insert a new functional area: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${FUNCTIONAL_AREA_INS_CODE}    ${FUNCTIONAL_AREA_INS_NAME}    ${FUNCTIONAL_AREA_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Functional Area Name
    [Documentation]    Select the functional area, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${FUNCTIONAL_AREA_TABLE}
    ...    ${FUNCTIONAL_AREA_UPD_CODE}
    ...    ${FUNCTIONAL_AREA_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Functional Area
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${FUNCTIONAL_AREA_TABLE}    ${FUNCTIONAL_AREA_DEL_ENDDATE}    ${code}    ${date}
