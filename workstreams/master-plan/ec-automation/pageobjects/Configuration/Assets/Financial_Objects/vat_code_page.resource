*** Settings ***
Documentation       T3 (screen) — VAT Code page object.
...                 Screen: Configuration > Assets > Financial Objects > VAT Code.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${VAT_CODE_SCREEN}          VAT Code
${VAT_CODE_TABLE}           manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${VAT_CODE_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${VAT_CODE_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:6:C:1:in
${VAT_CODE_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:da_input
# mandatory extra: VAT Code (text)
${VAT_CODE_INS_X0}          tab:tabPanel:objectForm:form:G:0:R:3:C:1:in
# mandatory extra: Rate (Decimal) (text)
${VAT_CODE_INS_X1}          tab:tabPanel:objectForm:form:G:0:R:7:C:1:in
# mandatory reference dd: Country (banner-discovered; first option used)
${VAT_CODE_INS_DD0}         tab:tabPanel:objectForm:form:G:0:R:4:C:1:dd
# mandatory reference dd: VAT Type (banner-discovered; first option used)
${VAT_CODE_INS_DD1}         tab:tabPanel:objectForm:form:G:0:R:5:C:1:dd
# updateAttributes field IDs (Update — existing object)
${VAT_CODE_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${VAT_CODE_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:4:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${VAT_CODE_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open VAT Code Screen
    [Documentation]    Suite Setup: launch, login, navigate to the VAT Code screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${VAT_CODE_SCREEN}

VAT Code Row Should Exist
    [Documentation]    Assert a vat code with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${VAT_CODE_TABLE}    ${code}

VAT Code Row Should Not Exist
    [Documentation]    Assert a vat code with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${VAT_CODE_TABLE}    ${code}

VAT Code Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_VAT_CODE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_VAT_CODE    ${code}

VAT Code Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_VAT_CODE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_VAT_CODE    ${code}

VAT Code Row Should Show Name
    [Documentation]    Assert the VAT Code row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${VAT_CODE_TABLE}    ${code}    ${name}

Insert VAT Code Record
    [Documentation]    Insert a new vat code: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${VAT_CODE_INS_CODE}    ${VAT_CODE_INS_NAME}    ${VAT_CODE_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Fill EC Field    ${VAT_CODE_INS_X0}    AT9
    Fill EC Field    ${VAT_CODE_INS_X1}    0.1
    Select First EC Dropdown Option    ${VAT_CODE_INS_DD0}
    Select First EC Dropdown Option    ${VAT_CODE_INS_DD1}
    Save And Refresh List

Update VAT Code Name
    [Documentation]    Select the vat code, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${VAT_CODE_TABLE}    ${VAT_CODE_UPD_CODE}    ${VAT_CODE_UPD_NAME}    ${code}    ${new_name}

Delete VAT Code
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${VAT_CODE_TABLE}    ${VAT_CODE_DEL_ENDDATE}    ${code}    ${date}
