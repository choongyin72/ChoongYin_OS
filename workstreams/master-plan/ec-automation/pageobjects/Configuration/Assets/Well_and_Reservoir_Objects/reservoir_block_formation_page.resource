*** Settings ***
Documentation       T3 (screen) - Reservoir Block Formation page object (MULTI-OBJECT).
...                 Screen: Configuration > Assets > Well and Reservoir Objects > Reservoir Block Formation (CO.0137).
...                 RBF is a JUNCTION OV: its Reservoir Block + Reservoir Formation are DEPENDENT dropdowns
...                 (Formation options appear only after a Block is chosen). A valid pair can't be picked from
...                 unrelated seed data, so this suite creates a fresh Reservoir Block + Reservoir Formation,
...                 links them via RBF, then tears down in reverse order (RBF -> Formation -> Block).
...                 Label-driven (no hardcoded ids); grid = shared T2 ${OV_MANAGE_OBJECT_TABLE}.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Keywords ***
Open Reservoir Block Formation Suite
    [Documentation]    Suite Setup: launch + login, open the Reservoir Block screen first (parents built first).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    Reservoir Block    ${user}    ${pass}
    Apply Navigator

Go To Screen
    [Documentation]    Navigate to another EC screen in the SAME session, then load its list (GO).
    [Arguments]    ${screen}
    Navigate To Screen    ${screen}
    Apply Navigator

Insert Plain Object
    [Documentation]    On the current screen: New Object -> Code/Name/Start Date -> Save -> GO.
    [Arguments]    ${code_label}    ${name_label}    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label    objectForm    ${code_label}    ${code}
    Fill OV Field By Label    objectForm    ${name_label}    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Save
    Apply Navigator

Insert Reservoir Block Formation
    [Documentation]    New Object -> Code/Name/Start Date, select Reservoir Block (populates Formation),
    ...    then select Reservoir Formation -> Save -> GO. Block chosen BEFORE Formation (dependent dropdown).
    ...    The Formation cascade's rendered options key off its CODE, not its Name (verified via DOM probe,
    ...    issue 237 item 4) - unlike the Block dropdown, which matches by Name. Pass the Formation CODE here.
    [Arguments]    ${code}    ${name}    ${start_date}    ${block_name}    ${formation_code}
    Open New Object Form
    Fill OV Field By Label    objectForm    Resv Block Formation Code    ${code}
    Fill OV Field By Label    objectForm    Resv Block Formation Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    Fill OV Dropdown By Label    objectForm    Reservoir Block    ${block_name}
    # Reservoir Formation is a DEPENDENT dropdown - its options are AJAX-repopulated only after a
    # Reservoir Block is chosen. Wait for that round-trip to settle before selecting the Formation.
    Wait For Load State    networkidle    timeout=15s
    Sleep    1s
    Fill OV Dropdown By Label    objectForm    Reservoir Formation    ${formation_code}
    Save
    Apply Navigator

Update Object Name By Label
    [Documentation]    Select ${code}, confirm loaded (code id by label), edit Name, Save, GO.
    [Arguments]    ${code_label}    ${name_label}    ${code}    ${new_name}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    ${code_label}
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    ${name_label}    ${new_name}
    Save
    Apply Navigator

Delete Object By End Date
    [Documentation]    Select ${code}, set End Date = Start Date (true delete), Save, GO.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${OV_MANAGE_OBJECT_TABLE}    ${code}
    Fill OV Date By Label    objectdates    End Date    ${date}
    Save
    Apply Navigator

Row Present
    [Documentation]    Assert the object ${code} is present in the current screen's list.
    [Arguments]    ${code}
    Row Should Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}

Row Absent
    [Documentation]    Assert the object ${code} is absent from the current screen's list.
    [Arguments]    ${code}
    Row Should Not Exist    ${OV_MANAGE_OBJECT_TABLE}    ${code}
