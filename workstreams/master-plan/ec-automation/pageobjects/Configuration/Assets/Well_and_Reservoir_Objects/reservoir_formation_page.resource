*** Settings ***
Documentation       T3 (screen) - Reservoir Formation page object.
...                 Screen: Configuration > Assets > Well_and_Reservoir_Objects > Reservoir Formation (CO.0135). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${RESERVOIR_FORMATION_SCREEN}          Reservoir Formation
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Reservoir Formation Code" Name="Reservoir Formation Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Reservoir Formation Screen
    [Documentation]    Suite Setup: launch, login, open Reservoir Formation, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${RESERVOIR_FORMATION_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Reservoir Formation Row Should Exist
    [Documentation]    Assert a reservoir_formation with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Reservoir Formation Row Should Not Exist
    [Documentation]    Assert a reservoir_formation with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Reservoir Formation Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_RESV_FORMATION.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_RESV_FORMATION    ${code}

Reservoir Formation Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_RESV_FORMATION.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_RESV_FORMATION    ${code}

Reservoir Formation Row Should Show Name
    [Documentation]    Assert the Reservoir Formation row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Reservoir Formation Record
    [Documentation]    Insert a new reservoir_formation: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Reservoir Formation Code    ${code}
    Fill OV Field By Label    objectForm    Reservoir Formation Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Reservoir Formation Name
    [Documentation]    Select the reservoir_formation, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Reservoir Formation Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Reservoir Formation Name    ${new_name}
    Save
    Apply Navigator

Delete Reservoir Formation
    [Documentation]    Select the reservoir_formation, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
