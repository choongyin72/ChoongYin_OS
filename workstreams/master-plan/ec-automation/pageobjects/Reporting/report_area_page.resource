*** Settings ***
Documentation       T3 (screen) - Report Area page object.
...                 Screen: Reporting > Report Area (RP.0017). Manage-Object (OV) screen.
...                 Simplest OV: Code / Name / Start Date (no Description, no dropdowns).
...                 Locator variables + thin IUD wrappers delegating to T2 (manage_object) + T1 (common).

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/common.resource
Resource            ../../resources/manage_object.resource


*** Variables ***
${RPTA_SCREEN}          Report Area
${RPTA_TABLE}           manage_object_nav_nav:form:T_data
# NO hardcoded field ids - fields are resolved by LABEL at runtime (T2 Fill OV * By Label).
# Field labels (from recon): Code="Report Area Code" Name="Report Area Name" Date="Start date" End="End date".


*** Keywords ***
Open Report Area Screen
    [Documentation]    Suite Setup: launch, login, open Report Area, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${RPTA_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Report Area Row Should Exist
    [Documentation]    Assert a report area with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${RPTA_TABLE}    ${code}

Report Area Row Should Not Exist
    [Documentation]    Assert a report area with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${RPTA_TABLE}    ${code}

Report Area Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_REPORT_AREA.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_REPORT_AREA    ${code}

Report Area Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_REPORT_AREA.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_REPORT_AREA    ${code}

Report Area Row Should Show Name
    [Documentation]    Assert the Report Area row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${RPTA_TABLE}    ${code}    ${name}

Insert Report Area Record
    [Documentation]    Insert a new report area: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Report Area Code    ${code}
    Fill OV Field By Label    objectForm    Report Area Name    ${name}
    Fill OV Date By Label    objectForm    Start date    ${start_date}
    Save
    Apply Navigator

Update Report Area Name
    [Documentation]    Select the report area, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${RPTA_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Report Area Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Report Area Name    ${new_name}
    Save
    Apply Navigator

Delete Report Area
    [Documentation]    Select the report area, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${RPTA_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End date    ${date}
    Save
    Apply Navigator
