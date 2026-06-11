*** Settings ***
Documentation       T3 (screen) — Currency page object.
...                 Screen: Configuration > Assets > Financial Objects > Currency.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CURRENCY_SCREEN}          Currency
${CURRENCY_TABLE}           manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${CURRENCY_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${CURRENCY_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${CURRENCY_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# mandatory extra: Active (checkbox)
${CURRENCY_INS_X0}          tab:tabPanel:objectForm:form:G:0:R:6:C:1:cb
# updateAttributes field IDs (Update — existing object)
${CURRENCY_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${CURRENCY_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${CURRENCY_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Currency Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Currency screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${CURRENCY_SCREEN}

Currency Row Should Exist
    [Documentation]    Assert a currency with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${CURRENCY_TABLE}    ${code}

Currency Row Should Not Exist
    [Documentation]    Assert a currency with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${CURRENCY_TABLE}    ${code}

Currency Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CURRENCY.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CURRENCY    ${code}

Currency Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CURRENCY.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CURRENCY    ${code}

Currency Row Should Show Name
    [Documentation]    Assert the Currency row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${CURRENCY_TABLE}    ${code}    ${name}

Insert Currency Record
    [Documentation]    Insert a new currency: Code/Name/Start Date + mandatory extras -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${CURRENCY_INS_CODE}    ${CURRENCY_INS_NAME}    ${CURRENCY_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Check Checkbox    css=[id="${CURRENCY_INS_X0}"]
    Save And Refresh List

Update Currency Name
    [Documentation]    Select the currency, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${CURRENCY_TABLE}    ${CURRENCY_UPD_CODE}    ${CURRENCY_UPD_NAME}    ${code}    ${new_name}

Delete Currency
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${CURRENCY_TABLE}    ${CURRENCY_DEL_ENDDATE}    ${code}    ${date}
