*** Settings ***
Documentation       T3 (screen) - Royalty Owner page object.
...                 Screen: Configuration > Assets > Royalty Objects > Royalty Owner.
...                 Manage-Object (OV) screen. Holds Royalty Owner's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${RO_SCREEN}            Royalty Owner
${RO_TABLE}             manage_object_nav_nav:form:T_data
# objectForm field IDs (Insert - new object)
${RO_INS_CODE}          tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${RO_INS_NAME}          tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${RO_INS_DATE}          tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# updateAttributes field IDs (Update - existing object)
${RO_UPD_CODE}          tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${RO_UPD_NAME}          tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${RO_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Royalty Owner Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to the env
    ...    user), navigate to the Royalty Owner screen. Pass a different user for role tests.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${RO_SCREEN}    ${user}    ${pass}

Royalty Owner Row Should Exist
    [Documentation]    Assert a royalty owner with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${RO_TABLE}    ${code}

Royalty Owner Row Should Not Exist
    [Documentation]    Assert a royalty owner with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${RO_TABLE}    ${code}

Royalty Owner Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_royalty_owner.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_royalty_owner    ${code}

Royalty Owner Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_royalty_owner.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_royalty_owner    ${code}

Royalty Owner Row Should Show Name
    [Documentation]    Assert the Royalty Owner row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${RO_TABLE}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Royalty Owner row ${code} does not show name ${name}

Insert Royalty Owner Record
    [Documentation]    Insert a new royalty owner: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill EC Field    ${RO_INS_CODE}    ${code}
    Fill EC Field    ${RO_INS_NAME}    ${name}
    Fill EC Date    ${RO_INS_DATE}    ${start_date}
    Save
    Apply Navigator

Update Royalty Owner Name
    [Documentation]    Select the royalty owner, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${RO_TABLE}    ${code}
    ${loaded}=    Get Property    css=[id="${RO_UPD_CODE}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${RO_UPD_NAME}    ${new_name}
    Save
    Apply Navigator

Delete Royalty Owner
    [Documentation]    Select the royalty owner, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${RO_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${RO_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
