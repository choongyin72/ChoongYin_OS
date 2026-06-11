*** Settings ***
Documentation       T3 (screen) — Bank Account page object.
...                 Screen: Configuration > Assets > Financial Objects > Bank Account.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${BANK_ACCOUNT_SCREEN}    Bank Account
${BANK_ACCOUNT_TABLE}    manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${BANK_ACCOUNT_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${BANK_ACCOUNT_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${BANK_ACCOUNT_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# mandatory extra: Sort Code (text)
${BANK_ACCOUNT_INS_X0}    tab:tabPanel:objectForm:form:G:0:R:8:C:1:in
# mandatory reference dd: Customer (banner-discovered; first option used)
${BANK_ACCOUNT_INS_DD0}    tab:tabPanel:objectForm:form:G:0:R:21:C:1:dd
# mandatory reference dd: Bank (banner-discovered; first option used)
${BANK_ACCOUNT_INS_DD1}    tab:tabPanel:objectForm:form:G:0:R:20:C:1:dd
# mandatory reference dd: Currency (banner-discovered; first option used)
${BANK_ACCOUNT_INS_DD2}    tab:tabPanel:objectForm:form:G:0:R:23:C:1:dd
# updateAttributes field IDs (Update — existing object)
${BANK_ACCOUNT_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${BANK_ACCOUNT_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${BANK_ACCOUNT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Bank Account Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Bank Account screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${BANK_ACCOUNT_SCREEN}

Bank Account Row Should Exist
    [Documentation]    Assert a bank account with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${BANK_ACCOUNT_TABLE}    ${code}

Bank Account Row Should Not Exist
    [Documentation]    Assert a bank account with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${BANK_ACCOUNT_TABLE}    ${code}

Bank Account Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_BANK_ACCOUNT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_BANK_ACCOUNT    ${code}

Bank Account Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_BANK_ACCOUNT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_BANK_ACCOUNT    ${code}

Bank Account Row Should Show Name
    [Documentation]    Assert the Bank Account row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${BANK_ACCOUNT_TABLE}    ${code}    ${name}

Insert Bank Account Record
    [Documentation]    Insert a new bank account: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${BANK_ACCOUNT_INS_CODE}    ${BANK_ACCOUNT_INS_NAME}    ${BANK_ACCOUNT_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Fill EC Field    ${BANK_ACCOUNT_INS_X0}    000000
    Select First EC Dropdown Option    ${BANK_ACCOUNT_INS_DD0}
    Select First EC Dropdown Option    ${BANK_ACCOUNT_INS_DD1}
    Select First EC Dropdown Option    ${BANK_ACCOUNT_INS_DD2}
    Save And Refresh List

Update Bank Account Name
    [Documentation]    Select the bank account, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${BANK_ACCOUNT_TABLE}    ${BANK_ACCOUNT_UPD_CODE}    ${BANK_ACCOUNT_UPD_NAME}    ${code}    ${new_name}

Delete Bank Account
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${BANK_ACCOUNT_TABLE}    ${BANK_ACCOUNT_DEL_ENDDATE}    ${code}    ${date}
