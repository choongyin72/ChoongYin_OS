*** Settings ***
Documentation       T3 (screen) - Royalty Depositor page object.
...                 Screen: Configuration > Assets > Royalty Objects > Royalty Depositor.
...                 Manage-Object (OV) screen. Holds Royalty Depositor's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${RD_SCREEN}            Royalty Depositor
${RD_TABLE}             manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert - new object)
${RD_INS_CODE}          tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${RD_INS_NAME}          tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${RD_INS_DATE}          tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update - existing object)
${RD_UPD_CODE}          tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${RD_UPD_NAME}          tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${RD_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Royalty Depositor Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Royalty Depositor screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${RD_SCREEN}    ${user}    ${pass}

Royalty Depositor Row Should Exist
    [Documentation]    Assert a royalty depositor with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${RD_TABLE}    ${code}

Royalty Depositor Row Should Not Exist
    [Documentation]    Assert a royalty depositor with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${RD_TABLE}    ${code}

Royalty Depositor Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_royalty_depositor.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_royalty_depositor    ${code}

Royalty Depositor Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_royalty_depositor.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_royalty_depositor    ${code}

Royalty Depositor Row Should Show Name
    [Documentation]    Assert the Royalty Depositor row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${RD_TABLE}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Royalty Depositor row ${code} does not show name ${name}

Insert Royalty Depositor Record
    [Documentation]    Insert a new royalty depositor: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${RD_INS_CODE}    ${code}
    Fill EC Field    ${RD_INS_NAME}    ${name}
    Fill EC Date    ${RD_INS_DATE}    ${start_date}
    Save
    Apply Navigator

Update Royalty Depositor Name
    [Documentation]    Select the royalty depositor, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${RD_TABLE}    ${code}
    ${loaded}=    Get Property    css=[id="${RD_UPD_CODE}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${RD_UPD_NAME}    ${new_name}
    Save
    Apply Navigator

Delete Royalty Depositor
    [Documentation]    Select the royalty depositor, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${RD_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${RD_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
