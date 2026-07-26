*** Settings ***
Documentation       T3 (screen) - Canal page object.
...                 Screen: Configuration > Assets > Transport_Objects > Canal (CO.2069). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${CANAL_SCREEN}          Canal
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Canal Code" Name="Canal Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Canal Screen
    [Documentation]    Suite Setup: launch, login, open Canal, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${CANAL_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Canal Row Should Exist
    [Documentation]    Assert a canal with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Canal Row Should Not Exist
    [Documentation]    Assert a canal with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Canal Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_CANAL.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CANAL    ${code}

Canal Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_CANAL.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CANAL    ${code}

Canal Row Should Show Name
    [Documentation]    Assert the Canal row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Canal Record
    [Documentation]    Insert a new canal: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Canal Code    ${code}
    Fill OV Field By Label    objectForm    Canal Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Canal Name
    [Documentation]    Select the canal, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Canal Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Canal Name    ${new_name}
    Save
    Apply Navigator

Delete Canal
    [Documentation]    Select the canal, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
