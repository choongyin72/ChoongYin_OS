*** Settings ***
Documentation       T3 (screen) - Berth page object.
...                 Screen: Configuration > Assets > Transport Objects > Berth (CO.2012). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (Port Name/Business Unit/Capacity/Op
...                 dropdowns all optional). NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${BERTH_SCREEN}         Berth
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Berth Code" Name="Berth Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Berth Screen
    [Documentation]    Suite Setup: launch, login, open Berth, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${BERTH_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Berth Row Should Exist
    [Documentation]    Assert a berth with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Berth Row Should Not Exist
    [Documentation]    Assert a berth with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Berth Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_BERTH.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_BERTH    ${code}

Berth Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_BERTH.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_BERTH    ${code}

Berth Row Should Show Name
    [Documentation]    Assert the Berth row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Berth Record
    [Documentation]    Insert a new berth: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Berth Code    ${code}
    Fill OV Field By Label    objectForm    Berth Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Berth Name
    [Documentation]    Select the berth, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Berth Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Berth Name    ${new_name}
    Save
    Apply Navigator

Delete Berth
    [Documentation]    Select the berth, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
