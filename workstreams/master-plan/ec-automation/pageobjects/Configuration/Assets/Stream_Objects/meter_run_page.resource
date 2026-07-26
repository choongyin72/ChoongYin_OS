*** Settings ***
Documentation       T3 (screen) - Meter Run page object.
...                 Screen: Configuration > Assets > Stream_Objects > Meter Run (CO.0091). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Meter Run
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Meter Run Code" Name="Meter Run Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Meter Run Screen
    [Documentation]    Suite Setup: launch, login, open Meter Run, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Meter Run Row Should Exist
    [Documentation]    Assert a meter_run with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Meter Run Row Should Not Exist
    [Documentation]    Assert a meter_run with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Meter Run Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_METER_RUN.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_METER_RUN    ${code}

Meter Run Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_METER_RUN.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_METER_RUN    ${code}

Meter Run Row Should Show Name
    [Documentation]    Assert the Meter Run row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Meter Run Record
    [Documentation]    Insert a new meter_run: New Object form -> Code/Name/Start Date (+ mandatory dropdowns/extra fields) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Meter Run Code    ${code}
    Fill OV Field By Label    objectForm    Meter Run Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill Meter Run Mandatory Extras
    Save
    Apply Navigator

Fill Meter Run Mandatory Extras
    [Documentation]    Fill the mandatory dropdown(s) + extra field(s) for Meter Run, split out of Insert to keep
    ...    the Insert keyword within the keyword-count limit. All label-driven (no hardcoded ids).
    Fill OV Dropdown By Label    objectForm    Type of Taps    Pipe
    Fill OV Dropdown By Label    objectForm    Pipe Material    Stainless Steel
    Fill OV Dropdown By Label    objectForm    Location of Taps    Upstream
    Fill OV Field By Label    objectForm    Pipe Diameter (temp uncorrected) [mm]    1
    Fill OV Field By Label    objectForm    Diameter Meas Temp [°R]    1
    Fill OV Field By Label    objectForm    All Calibration Factor    1

Update Meter Run Name
    [Documentation]    Select the meter_run, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Meter Run Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Meter Run Name    ${new_name}
    Save
    Apply Navigator

Delete Meter Run
    [Documentation]    Select the meter_run, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
