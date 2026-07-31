*** Settings ***
Documentation       T3 (screen) - Trailer page object.
...                 Screen: Configuration > Assets > Transport_Objects > Trailer.
...                 PLAIN OV (Bank family): navigator is date-only - GO populates the grid (no
...                 mandatory cascade). Fields resolved BY LABEL (no hardcoded rows); extra mandatory
...                 dropdowns first-available. DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Trailer
${TBL}              trailer_object:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Trailer Screen
    [Documentation]    Suite Setup: launch, login, open the screen, GO (date-only navigator).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Navigator

Trailer Row Should Exist
    [Documentation]    Assert ${code} is present (await grid redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Trailer Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Trailer Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_TRAILER.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_TRAILER    ${code}

Trailer Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_TRAILER.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_TRAILER    ${code}

Trailer Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Fill Trailer Mandatory Fields
    [Documentation]    Fill every mandatory New-Object field BY LABEL (kept separate from the insert
    ...    keyword so screens with many mandatory fields stay within robocop LEN03).
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill OV Field By Label       objectForm    Trailer Code    ${code}
    Fill OV Field By Label       objectForm    Trailer Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Field By Label       objectForm    Licence Plate No    AUTOTEST-TRL-001
    Fill OV Dropdown By Label    objectForm    Trailer Type    __FIRST__
    Fill OV Dropdown By Label    objectForm    UOM    __FIRST__
    Fill OV Dropdown By Label    objectForm    Transport Company    __FIRST__

Insert Trailer Record
    [Documentation]    Open the New-Object form, fill the mandatory fields, Save + reload.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill Trailer Mandatory Fields    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Trailer Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Trailer Name    ${new_name}
    Save And Refresh List

Delete Trailer
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
