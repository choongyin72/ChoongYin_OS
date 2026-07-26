*** Settings ***
Documentation       T3 (screen) - Dummy Tag Event Object page object.
...                 Screen: Configuration > Integration_Services > Dummy Tag Event Object (CO.1063). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../libraries/DbVerify.py
Resource            ../../../resources/common.resource
Resource            ../../../resources/manage_object.resource


*** Variables ***
${DUMMY_TAG_EVENT_OBJECT_SCREEN}          Dummy Tag Event Object
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Dummy Tag Event Object Code" Name="Dummy Tag Event Object Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Dummy Tag Event Object Screen
    [Documentation]    Suite Setup: launch, login, open Dummy Tag Event Object, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${DUMMY_TAG_EVENT_OBJECT_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Dummy Tag Event Object Row Should Exist
    [Documentation]    Assert a dummy_tag_event_object with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Dummy Tag Event Object Row Should Not Exist
    [Documentation]    Assert a dummy_tag_event_object with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Dummy Tag Event Object Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_DUMMY_TAG_EVENT.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_DUMMY_TAG_EVENT    ${code}

Dummy Tag Event Object Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_DUMMY_TAG_EVENT.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_DUMMY_TAG_EVENT    ${code}

Dummy Tag Event Object Row Should Show Name
    [Documentation]    Assert the Dummy Tag Event Object row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Dummy Tag Event Object Record
    [Documentation]    Insert a new dummy_tag_event_object: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Dummy Tag Event Object Code    ${code}
    Fill OV Field By Label    objectForm    Dummy Tag Event Object Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Dummy Tag Event Object Name
    [Documentation]    Select the dummy_tag_event_object, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Dummy Tag Event Object Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Dummy Tag Event Object Name    ${new_name}
    Save
    Apply Navigator

Delete Dummy Tag Event Object
    [Documentation]    Select the dummy_tag_event_object, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
