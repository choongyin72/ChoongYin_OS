*** Settings ***
Documentation       T3 (screen) - Inventory Area page object.
...                 Screen: Configuration > Assets > Inventory_Objects > Inventory Area (CD.0115). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${INVENTORY_AREA_SCREEN}          Inventory Area
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Inventory Area Code" Name="Inventory Area Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Inventory Area Screen
    [Documentation]    Suite Setup: launch, login, open Inventory Area, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${INVENTORY_AREA_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Inventory Area Row Should Exist
    [Documentation]    Assert a inventory_area with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Inventory Area Row Should Not Exist
    [Documentation]    Assert a inventory_area with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Inventory Area Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_INVENTORY_AREA.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_INVENTORY_AREA    ${code}

Inventory Area Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_INVENTORY_AREA.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_INVENTORY_AREA    ${code}

Inventory Area Row Should Show Name
    [Documentation]    Assert the Inventory Area row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Inventory Area Record
    [Documentation]    Insert a new inventory_area: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Inventory Area Code    ${code}
    Fill OV Field By Label    objectForm    Inventory Area Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Inventory Area Name
    [Documentation]    Select the inventory_area, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Inventory Area Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Inventory Area Name    ${new_name}
    Save
    Apply Navigator

Delete Inventory Area
    [Documentation]    Select the inventory_area, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
