*** Settings ***
Documentation       T3 (screen) — Bank page object.
...                 Screen: Configuration > Assets > Financial Objects > Bank.
...                 Manage-Object (OV) screen. Holds Bank's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${BANK_SCREEN}          Bank
${BANK_TABLE}           manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert — new object)
${BANK_INS_CODE}        tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${BANK_INS_NAME}        tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${BANK_INS_DATE}        tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update — existing object)
${BANK_UPD_CODE}        tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${BANK_UPD_NAME}        tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete — End Date = Start Date)
${BANK_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Bank Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Bank screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Open EC Browser
    Login To EC    ${user}    ${pass}
    Navigate To Screen    ${BANK_SCREEN}

Bank Row Should Exist
    [Documentation]    Assert a bank with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${BANK_TABLE}    ${code}

Bank Row Should Not Exist
    [Documentation]    Assert a bank with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${BANK_TABLE}    ${code}

Bank Row Should Show Name
    [Documentation]    Assert the Bank row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${BANK_TABLE}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Bank row ${code} does not show name ${name}

Insert Bank Record
    [Documentation]    Insert a new bank: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${BANK_INS_CODE}    ${code}
    Fill EC Field    ${BANK_INS_NAME}    ${name}
    Fill EC Date    ${BANK_INS_DATE}    ${start_date}
    Save
    Click Go

Update Bank Name
    [Documentation]    Select the bank, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${BANK_TABLE}    ${code}
    ${loaded}=    Get Property    css=[id="${BANK_UPD_CODE}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${BANK_UPD_NAME}    ${new_name}
    Save
    Click Go

Delete Bank
    [Documentation]    Select the bank, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${BANK_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${BANK_DEL_ENDDATE}    ${date}
    Save
    Click Go
