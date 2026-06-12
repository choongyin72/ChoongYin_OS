*** Settings ***
Documentation       T3 (screen) — Account Mapping page object.
...                 Screen: Configuration > Assets > Financial Objects > Account Mapping.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${ACCOUNT_MAPPING_SCREEN}    Account Mapping
${ACCOUNT_MAPPING_TABLE}    manageObject:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${ACCOUNT_MAPPING_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${ACCOUNT_MAPPING_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:in
${ACCOUNT_MAPPING_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:3:C:1:da_input
# Reference dropdowns: a VALID-AND-UNUSED combination cloned from the 75 existing
# rows (the combination IS the unique key - ALT_CODE = FIN_PRODUCT_LIT_CC_STATUS_CLASS).
# Test combo = JOU_ENT_ALL_ALL_ALL_ACCRUAL_CREDIT (verified free 2026-06-12);
# Account Category 'Revenue' + Financial Account 'ACCRUAL CR Acct' + PKs 40/50 are a
# proven trio from existing row ACC_GEN_CR. Values selected by label in Insert.
${ACCOUNT_MAPPING_INS_DD_LIT}    tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd
${ACCOUNT_MAPPING_INS_DD_FIN}    tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd
${ACCOUNT_MAPPING_INS_DD_CC}    tab:tabPanel:objectForm:form:G:0:R:9:C:1:dd
${ACCOUNT_MAPPING_INS_DD_STATUS}    tab:tabPanel:objectForm:form:G:0:R:11:C:1:dd
${ACCOUNT_MAPPING_INS_DD_DRCR}    tab:tabPanel:objectForm:form:G:0:R:12:C:1:dd
${ACCOUNT_MAPPING_INS_DD_DPK}    tab:tabPanel:objectForm:form:G:0:R:13:C:1:dd
${ACCOUNT_MAPPING_INS_DD_CPK}    tab:tabPanel:objectForm:form:G:0:R:14:C:1:dd
${ACCOUNT_MAPPING_INS_DD_ACAT}    tab:tabPanel:objectForm:form:G:0:R:15:C:1:dd
${ACCOUNT_MAPPING_INS_DD_FACC}    tab:tabPanel:objectForm:form:G:0:R:16:C:1:dd
# updateAttributes field IDs (Update — existing object)
${ACCOUNT_MAPPING_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${ACCOUNT_MAPPING_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${ACCOUNT_MAPPING_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Account Mapping Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Account Mapping screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${ACCOUNT_MAPPING_SCREEN}    ${user}    ${pass}

Account Mapping Row Should Exist
    [Documentation]    Assert a account mapping with ${code} is present in the list.
    ...    This 75-row custom grid repopulates slowly after save/refresh - WAIT for
    ...    the row instead of scanning the tbody instantly.
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${ACCOUNT_MAPPING_TABLE}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s

Account Mapping Row Should Not Exist
    [Documentation]    Assert a account mapping with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${ACCOUNT_MAPPING_TABLE}    ${code}

Account Mapping Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FIN_ACCOUNT_MAPPING.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FIN_ACCOUNT_MAPPING    ${code}

Account Mapping Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FIN_ACCOUNT_MAPPING.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FIN_ACCOUNT_MAPPING    ${code}

Account Mapping Row Should Show Name
    [Documentation]    Assert the Account Mapping row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${ACCOUNT_MAPPING_TABLE}    ${code}    ${name}

Insert Account Mapping Record
    [Documentation]    Insert a new account mapping: Code/Name/Start Date + the
    ...    validated reference combination (see Select Valid Reference Combination) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${ACCOUNT_MAPPING_INS_CODE}    ${ACCOUNT_MAPPING_INS_NAME}    ${ACCOUNT_MAPPING_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select Valid Reference Combination
    Save And Refresh List

Select Valid Reference Combination
    [Documentation]    The VALID-AND-UNUSED combination JOU_ENT_ALL_ALL_ALL_ACCRUAL_CREDIT
    ...    (the combination is the screen's unique key; trio Revenue / ACCRUAL CR Acct /
    ...    PKs 40-50 cloned from the existing proven row ACC_GEN_CR).
    Select EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD_LIT}    All Line Item Types
    Select EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD_FIN}    Journal Entry
    Select EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD_CC}    All
    Select EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD_STATUS}    Accrual
    Select EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD_DRCR}    Credit
    Select EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD_DPK}    Debit General Ledger (40)
    Select EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD_CPK}    Credit General Ledger (50)
    Select EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD_ACAT}    Revenue
    Select EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD_FACC}    ACCRUAL CR Acct

Update Account Mapping Name
    [Documentation]    Select the account mapping, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${ACCOUNT_MAPPING_TABLE}    ${ACCOUNT_MAPPING_UPD_CODE}    ${ACCOUNT_MAPPING_UPD_NAME}    ${code}    ${new_name}

Delete Account Mapping
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${ACCOUNT_MAPPING_TABLE}    ${ACCOUNT_MAPPING_DEL_ENDDATE}    ${code}    ${date}
