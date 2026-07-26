*** Settings ***
Documentation       T3 (screen) - Blend page object.
...                 Screen: Configuration > Assets > Hydrocarbon_Objects > Blend (CO.0219). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${BLEND_SCREEN}          Blend
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Blend Code" Name="Blend Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Blend Screen
    [Documentation]    Suite Setup: launch, login, open Blend, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${BLEND_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Blend Row Should Exist
    [Documentation]    Assert a blend with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Blend Row Should Not Exist
    [Documentation]    Assert a blend with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Blend Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_BLEND.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_BLEND    ${code}

Blend Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_BLEND.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_BLEND    ${code}

Blend Row Should Show Name
    [Documentation]    Assert the Blend row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Blend Record
    [Documentation]    Insert a new blend: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Blend Code    ${code}
    Fill OV Field By Label    objectForm    Blend Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Blend Name
    [Documentation]    Select the blend, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Blend Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Blend Name    ${new_name}
    Save
    Apply Navigator

Delete Blend
    [Documentation]    Select the blend, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
