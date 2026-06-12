*** Settings ***
Documentation       T3 (screen) — Exchange Rate Source page object.
...                 Screen: Configuration > Assets > Financial Objects > Exchange Rate Source.
...                 Manage-Object (OV) screen: locator variables + thin one-line
...                 delegations to T2 (manage_object) and T1 (common) shared keywords.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${EXCHANGE_RATE_SOURCE_SCREEN}    Exchange Rate Source
${EXCHANGE_RATE_SOURCE_TABLE}    manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object); rows derived from recon LABELS
${EXCHANGE_RATE_SOURCE_INS_CODE}    tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${EXCHANGE_RATE_SOURCE_INS_NAME}    tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${EXCHANGE_RATE_SOURCE_INS_DATE}    tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${EXCHANGE_RATE_SOURCE_UPD_CODE}    tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${EXCHANGE_RATE_SOURCE_UPD_NAME}    tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${EXCHANGE_RATE_SOURCE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Exchange Rate Source Screen
    [Documentation]    Suite Setup: launch, login, navigate to the Exchange Rate Source screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${EXCHANGE_RATE_SOURCE_SCREEN}    ${user}    ${pass}

Exchange Rate Source Row Should Exist
    [Documentation]    Assert a exchange rate source with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}

Exchange Rate Source Row Should Not Exist
    [Documentation]    Assert a exchange rate source with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}

Exchange Rate Source Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_FOREX_SOURCE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_FOREX_SOURCE    ${code}

Exchange Rate Source Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_FOREX_SOURCE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_FOREX_SOURCE    ${code}

Exchange Rate Source Row Should Show Name
    [Documentation]    Assert the Exchange Rate Source row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${EXCHANGE_RATE_SOURCE_TABLE}    ${code}    ${name}

Insert Exchange Rate Source Record
    [Documentation]    Insert a new exchange rate source: Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill New Object Form    ${EXCHANGE_RATE_SOURCE_INS_CODE}    ${EXCHANGE_RATE_SOURCE_INS_NAME}    ${EXCHANGE_RATE_SOURCE_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Exchange Rate Source Name
    [Documentation]    Select the exchange rate source, edit Name, save + reload.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${EXCHANGE_RATE_SOURCE_TABLE}    ${EXCHANGE_RATE_SOURCE_UPD_CODE}    ${EXCHANGE_RATE_SOURCE_UPD_NAME}    ${code}    ${new_name}

Delete Exchange Rate Source
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${EXCHANGE_RATE_SOURCE_TABLE}    ${EXCHANGE_RATE_SOURCE_DEL_ENDDATE}    ${code}    ${date}
