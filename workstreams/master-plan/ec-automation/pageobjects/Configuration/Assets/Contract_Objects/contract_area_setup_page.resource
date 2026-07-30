*** Settings ***
Documentation       T3 (screen) - Contract Area Setup page object.
...                 Screen: Configuration > Assets > Contract_Objects > Contract Area Setup (CO.2038).
...                 CUSTOM-URL OV: grid nav:form:T_data, NO navigator, NO GO button (Save And
...                 Refresh List falls back to the toolbar Refresh). Fields resolved BY LABEL.
...                 Extra mandatory over plain OV: Contract Area Name + Contract Name reference
...                 dropdowns (first-available). Start Date 2020-01-01 (ref dds only offer objects
...                 effective at the form Start Date). DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Contract Area Setup
${TBL}              nav:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Contract Area Setup Screen
    [Documentation]    Suite Setup: launch, login, open the screen (custom-URL OV: grid loads
    ...    directly, no navigator cascade to fill).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}

Contract Area Setup Row Should Exist
    [Documentation]    Assert ${code} is present (await grid redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Contract Area Setup Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Contract Area Setup Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_CONTRACT_AREA_SETUP.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CONTRACT_AREA_SETUP    ${code}

Contract Area Setup Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_CONTRACT_AREA_SETUP.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CONTRACT_AREA_SETUP    ${code}

Contract Area Setup Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Contract Area Setup Record
    [Documentation]    Insert (all fields BY LABEL) + Save. Ref dropdowns first-available.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Contract Area Setup Code    ${code}
    Fill OV Field By Label       objectForm    Contract Area Setup Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Contract Area Name    __FIRST__
    Fill OV Dropdown By Label    objectForm    Contract Name    __FIRST__
    Save And Refresh List

Update Contract Area Setup Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Contract Area Setup Name    ${new_name}
    Save And Refresh List

Delete Contract Area Setup
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
