*** Settings ***
Documentation       T3 (screen) - Orifice Plate page object.
...                 Screen: Configuration > Assets > Stream_Objects > Orifice Plate (CO.0089). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SCREEN_NAME}          Orifice Plate
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Orifice Code" Name="Orifice Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Orifice Plate Screen
    [Documentation]    Suite Setup: launch, login, open Orifice Plate, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCREEN_NAME}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Orifice Plate Row Should Exist
    [Documentation]    Assert a orifice_plate with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Orifice Plate Row Should Not Exist
    [Documentation]    Assert a orifice_plate with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Orifice Plate Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_ORIFICE_PLATE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_ORIFICE_PLATE    ${code}

Orifice Plate Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_ORIFICE_PLATE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_ORIFICE_PLATE    ${code}

Orifice Plate Row Should Show Name
    [Documentation]    Assert the Orifice Plate row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Orifice Plate Record
    [Documentation]    Insert a new orifice_plate: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Orifice Code    ${code}
    Fill OV Field By Label    objectForm    Orifice Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Material    304/316 Stainless Steel
    Fill OV Field By Label    objectForm    Diameter [mm]    1
    Fill OV Field By Label    objectForm    Measurement Temp [°R]    1
    Save
    Apply Navigator

Update Orifice Plate Name
    [Documentation]    Select the orifice_plate, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Orifice Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Orifice Name    ${new_name}
    Save
    Apply Navigator

Delete Orifice Plate
    [Documentation]    Select the orifice_plate, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
