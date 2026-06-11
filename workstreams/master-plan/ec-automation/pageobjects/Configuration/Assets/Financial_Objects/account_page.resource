*** Settings ***
Documentation       T3 (screen) — Account page object.
...                 Screen: Configuration > Assets > Financial Objects > Account.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${ACCOUNT_SCREEN}           Account
${ACCOUNT_TABLE}            nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${ACCOUNT_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${ACCOUNT_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${ACCOUNT_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# mandatory extra: GL Account (text)
${ACCOUNT_INS_X0}           tab:tabPanel:objectForm:form:G:0:R:8:C:1:in
# mandatory reference dd: Cost Object Type (banner-discovered; first option used)
${ACCOUNT_INS_DD0}          tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd
# updateAttributes field IDs (Update — existing object)
${ACCOUNT_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${ACCOUNT_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${ACCOUNT_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Account Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Account screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${ACCOUNT_SCREEN}

Account Row Should Exist
    [Documentation]    Assert a account with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${ACCOUNT_TABLE}    ${code}

Account Row Should Not Exist
    [Documentation]    Assert a account with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${ACCOUNT_TABLE}    ${code}

Account Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FIN_ACCOUNT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FIN_ACCOUNT    ${code}

Account Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FIN_ACCOUNT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FIN_ACCOUNT    ${code}

Account Row Should Show Name
    [Documentation]    Assert the Account row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${ACCOUNT_TABLE}    ${code}    ${name}

Insert Account Record
    [Documentation]    Insert a new account: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${ACCOUNT_INS_CODE}    ${ACCOUNT_INS_NAME}    ${ACCOUNT_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Fill EC Field    ${ACCOUNT_INS_X0}    999999
    Select First EC Dropdown Option    ${ACCOUNT_INS_DD0}
    Save And Refresh List

Update Account Name
    [Documentation]    Select the account, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${ACCOUNT_TABLE}    ${ACCOUNT_UPD_CODE}    ${ACCOUNT_UPD_NAME}    ${code}    ${new_name}

Delete Account
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${ACCOUNT_TABLE}    ${ACCOUNT_DEL_ENDDATE}    ${code}    ${date}
