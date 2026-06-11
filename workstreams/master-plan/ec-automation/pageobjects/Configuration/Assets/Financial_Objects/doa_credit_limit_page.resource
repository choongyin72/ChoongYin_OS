*** Settings ***
Documentation       T3 (screen) — DOA Credit Limit page object.
...                 Screen: Configuration > Assets > Financial Objects > DOA Credit Limit.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${DOA_CREDIT_LIMIT_SCREEN}    DOA Credit Limit
${DOA_CREDIT_LIMIT_TABLE}    manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${DOA_CREDIT_LIMIT_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${DOA_CREDIT_LIMIT_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${DOA_CREDIT_LIMIT_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# mandatory extra: Credit Limit (text)
${DOA_CREDIT_LIMIT_INS_X0}    tab:tabPanel:objectForm:form:G:0:R:5:C:1:in
# mandatory reference dd: DOA Type (banner-discovered; first option used)
${DOA_CREDIT_LIMIT_INS_DD0}    tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd
# mandatory reference dd: Currency (banner-discovered; first option used)
${DOA_CREDIT_LIMIT_INS_DD1}    tab:tabPanel:objectForm:form:G:0:R:6:C:1:dd
# mandatory reference dd: Role Name (banner-discovered; first option used)
${DOA_CREDIT_LIMIT_INS_DD2}    tab:tabPanel:objectForm:form:G:0:R:8:C:1:dd
# updateAttributes field IDs (Update — existing object)
${DOA_CREDIT_LIMIT_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${DOA_CREDIT_LIMIT_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${DOA_CREDIT_LIMIT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open DOA Credit Limit Screen
    [Documentation]    Suite Setup: launch, login, navigate to the DOA Credit Limit screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${DOA_CREDIT_LIMIT_SCREEN}

DOA Credit Limit Row Should Exist
    [Documentation]    Assert a doa credit limit with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${DOA_CREDIT_LIMIT_TABLE}    ${code}

DOA Credit Limit Row Should Not Exist
    [Documentation]    Assert a doa credit limit with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${DOA_CREDIT_LIMIT_TABLE}    ${code}

DOA Credit Limit Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_DOA_CREDIT_LIMIT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_DOA_CREDIT_LIMIT    ${code}

DOA Credit Limit Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_DOA_CREDIT_LIMIT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_DOA_CREDIT_LIMIT    ${code}

DOA Credit Limit Row Should Show Name
    [Documentation]    Assert the DOA Credit Limit row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${DOA_CREDIT_LIMIT_TABLE}    ${code}    ${name}

Insert DOA Credit Limit Record
    [Documentation]    Insert a new doa credit limit: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${DOA_CREDIT_LIMIT_INS_CODE}    ${DOA_CREDIT_LIMIT_INS_NAME}    ${DOA_CREDIT_LIMIT_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Fill EC Field    ${DOA_CREDIT_LIMIT_INS_X0}    1000
    Select First EC Dropdown Option    ${DOA_CREDIT_LIMIT_INS_DD0}
    Select First EC Dropdown Option    ${DOA_CREDIT_LIMIT_INS_DD1}
    Select First EC Dropdown Option    ${DOA_CREDIT_LIMIT_INS_DD2}
    Save And Refresh List

Update DOA Credit Limit Name
    [Documentation]    Select the doa credit limit, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${DOA_CREDIT_LIMIT_TABLE}    ${DOA_CREDIT_LIMIT_UPD_CODE}    ${DOA_CREDIT_LIMIT_UPD_NAME}    ${code}    ${new_name}

Delete DOA Credit Limit
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${DOA_CREDIT_LIMIT_TABLE}    ${DOA_CREDIT_LIMIT_DEL_ENDDATE}    ${code}    ${date}
