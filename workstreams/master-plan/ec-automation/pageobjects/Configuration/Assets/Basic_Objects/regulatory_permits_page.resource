*** Settings ***
Documentation       T3 (screen) — Regulatory Permits page object.
...                 Screen: Configuration > Assets > Basic Objects > Regulatory Permits.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${REGULATORY_PERMITS_SCREEN}            Regulatory Permits
${REGULATORY_PERMITS_TABLE}             nav:form:T_data
# objectForm field IDs (Insert — new object)
${REGULATORY_PERMITS_INS_CODE}          tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${REGULATORY_PERMITS_INS_NAME}          tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${REGULATORY_PERMITS_INS_DATE}          tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# Regulatory Agency is MANDATORY on this screen (EC: "Required fields are empty")
${REGULATORY_PERMITS_INS_DD}            tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd
# updateAttributes field IDs (Update — existing object)
${REGULATORY_PERMITS_UPD_CODE}          tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${REGULATORY_PERMITS_UPD_NAME}          tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${REGULATORY_PERMITS_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Regulatory Permits Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Regulatory Permits screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${REGULATORY_PERMITS_SCREEN}    ${user}    ${pass}

Regulatory Permits Row Should Exist
    [Documentation]    Assert a regulatory permits with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${REGULATORY_PERMITS_TABLE}    ${code}

Regulatory Permits Row Should Not Exist
    [Documentation]    Assert a regulatory permits with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${REGULATORY_PERMITS_TABLE}    ${code}

Regulatory Permits Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_REGULATORY_PERMITS.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_REGULATORY_PERMITS    ${code}

Regulatory Permits Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_REGULATORY_PERMITS.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_REGULATORY_PERMITS    ${code}

Regulatory Permits Row Should Show Name
    [Documentation]    Assert the Regulatory Permits row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${REGULATORY_PERMITS_TABLE}    ${code}    ${name}

Insert Regulatory Permits Record
    [Documentation]    Insert a new regulatory permits: Code/Name/Start Date + mandatory Regulatory Agency -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${agency}
    Fill New Object Form
    ...    ${REGULATORY_PERMITS_INS_CODE}
    ...    ${REGULATORY_PERMITS_INS_NAME}
    ...    ${REGULATORY_PERMITS_INS_DATE}
    ...    ${code}
    ...    ${name}
    ...    ${start_date}
    Select EC Dropdown Option    ${REGULATORY_PERMITS_INS_DD}    ${agency}
    Save And Refresh List

Update Regulatory Permits Name
    [Documentation]    Select the regulatory permits, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${REGULATORY_PERMITS_TABLE}
    ...    ${REGULATORY_PERMITS_UPD_CODE}
    ...    ${REGULATORY_PERMITS_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Regulatory Permits
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date
    ...    ${REGULATORY_PERMITS_TABLE}
    ...    ${REGULATORY_PERMITS_DEL_ENDDATE}
    ...    ${code}
    ...    ${date}
