*** Settings ***
Documentation       T3 (screen) - Split Item Other page object.
...                 Screen: Configuration > Assets > Revenue_Split_Keys > Split Item Other (CD.0017). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory (optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label). Thin IUD wrappers over T2 + T1.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${SPLIT_ITEM_OTHER_SCREEN}          Split Item Other
# NO hardcoded ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}; fields resolved by LABEL (T2 Fill OV * By Label).
# Field labels (from recon): Code="Split Item Code" Name="Name" Date="Start Date" End="End Date".


*** Keywords ***
Open Split Item Other Screen
    [Documentation]    Suite Setup: launch, login, open Split Item Other, load the list (GO).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SPLIT_ITEM_OTHER_SCREEN}    ${user}    ${pass}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Split Item Other Row Should Exist
    [Documentation]    Assert a split_item_other with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Split Item Other Row Should Not Exist
    [Documentation]    Assert a split_item_other with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Split Item Other Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_SPLIT_ITEM_OTHER.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_SPLIT_ITEM_OTHER    ${code}

Split Item Other Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_SPLIT_ITEM_OTHER.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_SPLIT_ITEM_OTHER    ${code}

Split Item Other Row Should Show Name
    [Documentation]    Assert the Split Item Other row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${OV_MANAGE_OBJECT_TABLE}    ${code}    ${name}

Insert Split Item Other Record
    [Documentation]    Insert a new split_item_other: New Object form -> Code/Name/Start Date -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    Split Item Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Update Split Item Other Name
    [Documentation]    Select the split_item_other, confirm it loaded (code id resolved by label), edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Split Item Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save
    Apply Navigator

Delete Split Item Other
    [Documentation]    Select the split_item_other, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator
