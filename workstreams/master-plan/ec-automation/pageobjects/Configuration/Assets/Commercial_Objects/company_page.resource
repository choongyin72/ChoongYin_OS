*** Settings ***
Documentation       T3 (screen) — Company page object.
...                 Screen: Configuration > Assets > Commercial Objects > Company.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${COMPANY_SCREEN}           Company
${COMPANY_TABLE}            manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${COMPANY_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${COMPANY_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${COMPANY_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:5:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${COMPANY_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${COMPANY_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${COMPANY_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Company Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Company screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${COMPANY_SCREEN}

Company Row Should Exist
    [Documentation]    Assert a company with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${COMPANY_TABLE}    ${code}

Company Row Should Not Exist
    [Documentation]    Assert a company with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${COMPANY_TABLE}    ${code}

Company Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_COMPANY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_COMPANY    ${code}

Company Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_COMPANY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_COMPANY    ${code}

Company Row Should Show Name
    [Documentation]    Assert the Company row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${COMPANY_TABLE}    ${code}    ${name}

Insert Company Record
    [Documentation]    Insert a new company: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${COMPANY_INS_CODE}    ${COMPANY_INS_NAME}    ${COMPANY_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Company Name
    [Documentation]    Select the company, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${COMPANY_TABLE}    ${COMPANY_UPD_CODE}    ${COMPANY_UPD_NAME}    ${code}    ${new_name}

Delete Company
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${COMPANY_TABLE}    ${COMPANY_DEL_ENDDATE}    ${code}    ${date}
