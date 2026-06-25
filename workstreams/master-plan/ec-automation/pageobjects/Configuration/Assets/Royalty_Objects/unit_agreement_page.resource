*** Settings ***
Documentation       T3 (screen) - Unit Agreement page object.
...                 Screen: Configuration > Assets > Royalty Objects > Unit Agreement.
...                 Manage-Object (OV) screen. Holds Unit Agreement's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${UA_SCREEN}            Unit Agreement
${UA_TABLE}             manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert - new object)
${UA_INS_CODE}          tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${UA_INS_NAME}          tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${UA_INS_DATE}          tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update - existing object)
${UA_UPD_CODE}          tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${UA_UPD_NAME}          tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${UA_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Unit Agreement Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Unit Agreement screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${UA_SCREEN}    ${user}    ${pass}

Unit Agreement Row Should Exist
    [Documentation]    Assert a unit agreement with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${UA_TABLE}    ${code}

Unit Agreement Row Should Not Exist
    [Documentation]    Assert a unit agreement with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${UA_TABLE}    ${code}

Unit Agreement Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_unit_agr.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_unit_agr    ${code}

Unit Agreement Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_unit_agr.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_unit_agr    ${code}

Unit Agreement Row Should Show Name
    [Documentation]    Assert the Unit Agreement row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${UA_TABLE}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Unit Agreement row ${code} does not show name ${name}

Insert Unit Agreement Record
    [Documentation]    Insert a new unit agreement: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${UA_INS_CODE}    ${code}
    Fill EC Field    ${UA_INS_NAME}    ${name}
    Fill EC Date    ${UA_INS_DATE}    ${start_date}
    Save
    Apply Navigator

Update Unit Agreement Name
    [Documentation]    Select the unit agreement, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${UA_TABLE}    ${code}
    ${loaded}=    Get Property    css=[id="${UA_UPD_CODE}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${UA_UPD_NAME}    ${new_name}
    Save
    Apply Navigator

Delete Unit Agreement
    [Documentation]    Select the unit agreement, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${UA_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${UA_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
