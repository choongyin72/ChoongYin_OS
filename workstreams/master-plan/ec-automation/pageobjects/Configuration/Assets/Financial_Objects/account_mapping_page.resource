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
# mandatory reference dd: Line Item Type (banner-discovered; first option used)
${ACCOUNT_MAPPING_INS_DD0}    tab:tabPanel:objectForm:form:G:0:R:7:C:1:dd
# mandatory reference dd: Financial Code (banner-discovered; first option used)
${ACCOUNT_MAPPING_INS_DD1}    tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd
# mandatory reference dd: Company Category (banner-discovered; first option used)
${ACCOUNT_MAPPING_INS_DD2}    tab:tabPanel:objectForm:form:G:0:R:9:C:1:dd
# mandatory reference dd: Status (banner-discovered; first option used)
${ACCOUNT_MAPPING_INS_DD3}    tab:tabPanel:objectForm:form:G:0:R:11:C:1:dd
# mandatory reference dd: Debit / Credit (banner-discovered; first option used)
${ACCOUNT_MAPPING_INS_DD4}    tab:tabPanel:objectForm:form:G:0:R:12:C:1:dd
# mandatory reference dd: Debit PK (banner-discovered; first option used)
${ACCOUNT_MAPPING_INS_DD5}    tab:tabPanel:objectForm:form:G:0:R:13:C:1:dd
# mandatory reference dd: Credit PK (banner-discovered; first option used)
${ACCOUNT_MAPPING_INS_DD6}    tab:tabPanel:objectForm:form:G:0:R:14:C:1:dd
# updateAttributes field IDs (Update — existing object)
${ACCOUNT_MAPPING_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${ACCOUNT_MAPPING_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:2:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${ACCOUNT_MAPPING_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Account Mapping Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Account Mapping screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${ACCOUNT_MAPPING_SCREEN}

Account Mapping Row Should Exist
    [Documentation]    Assert a account mapping with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${ACCOUNT_MAPPING_TABLE}    ${code}

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
    [Documentation]    Insert a new account mapping: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${ACCOUNT_MAPPING_INS_CODE}    ${ACCOUNT_MAPPING_INS_NAME}    ${ACCOUNT_MAPPING_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select First EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD0}
    Select First EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD1}
    Select First EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD2}
    Select First EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD3}
    Select First EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD4}
    Select First EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD5}
    Select First EC Dropdown Option    ${ACCOUNT_MAPPING_INS_DD6}
    Save And Refresh List

Update Account Mapping Name
    [Documentation]    Select the account mapping, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${ACCOUNT_MAPPING_TABLE}    ${ACCOUNT_MAPPING_UPD_CODE}    ${ACCOUNT_MAPPING_UPD_NAME}    ${code}    ${new_name}

Delete Account Mapping
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${ACCOUNT_MAPPING_TABLE}    ${ACCOUNT_MAPPING_DEL_ENDDATE}    ${code}    ${date}
