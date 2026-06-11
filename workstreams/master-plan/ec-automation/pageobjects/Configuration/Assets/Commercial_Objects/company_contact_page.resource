*** Settings ***
Documentation       T3 (screen) — Company Contact page object.
...                 Screen: Configuration > Assets > Commercial Objects > Company Contact.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${COMPANY_CONTACT_SCREEN}           Company Contact
${COMPANY_CONTACT_TABLE}            manageObject:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${COMPANY_CONTACT_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${COMPANY_CONTACT_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${COMPANY_CONTACT_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# mandatory reference dd: Company (banner-discovered; first option used)
${COMPANY_CONTACT_INS_DD0}          tab:tabPanel:objectForm:form:G:0:R:17:C:1:dd
# updateAttributes field IDs (Update — existing object)
${COMPANY_CONTACT_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${COMPANY_CONTACT_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${COMPANY_CONTACT_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Company Contact Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Company Contact screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${COMPANY_CONTACT_SCREEN}

Company Contact Row Should Exist
    [Documentation]    Assert a company contact with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${COMPANY_CONTACT_TABLE}    ${code}

Company Contact Row Should Not Exist
    [Documentation]    Assert a company contact with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${COMPANY_CONTACT_TABLE}    ${code}

Company Contact Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_COMPANY_CONTACT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_COMPANY_CONTACT    ${code}

Company Contact Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_COMPANY_CONTACT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_COMPANY_CONTACT    ${code}

Company Contact Row Should Show Name
    [Documentation]    Assert the Company Contact row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${COMPANY_CONTACT_TABLE}    ${code}    ${name}

Insert Company Contact Record
    [Documentation]    Insert a new company contact: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${COMPANY_CONTACT_INS_CODE}    ${COMPANY_CONTACT_INS_NAME}    ${COMPANY_CONTACT_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select First EC Dropdown Option    ${COMPANY_CONTACT_INS_DD0}
    Save And Refresh List

Update Company Contact Name
    [Documentation]    Select the company contact, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name
    ...    ${COMPANY_CONTACT_TABLE}
    ...    ${COMPANY_CONTACT_UPD_CODE}
    ...    ${COMPANY_CONTACT_UPD_NAME}
    ...    ${code}
    ...    ${new_name}

Delete Company Contact
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${COMPANY_CONTACT_TABLE}    ${COMPANY_CONTACT_DEL_ENDDATE}    ${code}    ${date}
