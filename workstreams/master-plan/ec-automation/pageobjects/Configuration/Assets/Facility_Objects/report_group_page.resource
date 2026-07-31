*** Settings ***
Documentation       T3 (screen) - Report Group page object.
...                 Screen: Configuration > Assets > Facility_Objects > Report Group.
...                 PLAIN OV (Bank family): navigator is date-only - GO populates the grid (no
...                 mandatory cascade). Fields resolved BY LABEL (no hardcoded rows); extra mandatory
...                 dropdowns first-available. DELETE = End Date = Start Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCR}              Report Group
${TBL}              report_group_table:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Report Group Screen
    [Documentation]    Suite Setup: launch, login, open the screen, GO (date-only navigator).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    Apply Navigator

Report Group Row Should Exist
    [Documentation]    Assert ${code} is present (await grid redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Report Group Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Report Group Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_REPORT_GROUP.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_REPORT_GROUP    ${code}

Report Group Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_REPORT_GROUP.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_REPORT_GROUP    ${code}

Report Group Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Fill Report Group Mandatory Fields
    [Documentation]    Fill every mandatory New-Object field BY LABEL (kept separate from the insert
    ...    keyword so screens with many mandatory fields stay within robocop LEN03).
    [Arguments]    ${code}    ${name}    ${start_date}
    Fill OV Field By Label       objectForm    Reporting Group Code    ${code}
    Fill OV Field By Label       objectForm    Reporting Group Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Fill OV Field By Label       objectForm    Description    AUTOTEST Report Group description
    Fill OV Dropdown By Label    objectForm    Business Area    __FIRST__

Insert Report Group Record
    [Documentation]    Open the New-Object form, fill the mandatory fields, Save + reload.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill Report Group Mandatory Fields    ${code}    ${name}    ${start_date}
    Save And Refresh List

Update Report Group Name
    [Documentation]    Select the row, edit Name (by label), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Reporting Group Name    ${new_name}
    Save And Refresh List

Delete Report Group
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
