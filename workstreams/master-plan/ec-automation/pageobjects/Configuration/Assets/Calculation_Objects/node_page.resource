*** Settings ***
Documentation       T3 (screen) - Node page object.
...                 Screen: Configuration > Assets > Calculation Objects > Node.
...                 OV-GM (manage-object, groupmodel) screen: the grid loads ONLY after the
...                 navigator cascade (Production Unit -> Area -> Facility Class 1) is filled
...                 + GO. The inserted node MUST carry the same Op Production Unit (the captured
...                 nav top-parent) to appear in the filtered grid. Fields resolved BY LABEL
...                 (no hardcoded row ids) - robust to per-screen row shifts. Extra mandatory
...                 over the plain OV: Calculation Sequence Number (numeric).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${NODE_SCREEN}          Node
${NODE_TABLE}           manageObject:form:T_data
# objectdates End Date input (Delete = End Date = Start Date) - EC-wide stable id
${NODE_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# captured navigator top-parent PU (set at suite setup, reused for the insert Op Production Unit)
${NODE_PU}              ${EMPTY}


*** Keywords ***
Open Node Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the OV-GM navigator cascade
    ...    first-available (PU -> Area -> Facility Class 1) + GO, and RETURN the top-parent PU
    ...    (the grid is empty until then; the PU is reused as the insert Op Production Unit).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${NODE_SCREEN}    ${user}    ${pass}
    ${pu}=    Apply OV-GM Navigator First Available
    RETURN    ${pu}

Node Row Should Exist
    [Documentation]    Assert a node with ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${NODE_TABLE}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${NODE_TABLE}    ${code}

Node Row Should Not Exist
    [Documentation]    Assert a node with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${NODE_TABLE}    ${code}

Node Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in OV_NODE.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_NODE    ${code}

Node Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from OV_NODE.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_NODE    ${code}

Node Row Should Show Name
    [Documentation]    Assert the Node row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${NODE_TABLE}    ${code}    ${name}

Insert Node Record
    [Documentation]    Insert a new node (all fields BY LABEL): Code/Name/Start Date +
    ...    Calculation Sequence Number + Op Production Unit (= the navigator top-parent so the
    ...    new row shows in the filtered grid) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${calc_seq}    ${op_production_unit}
    Open New Object Form
    Fill OV Field By Label       objectForm    Node Code                     ${code}
    Fill OV Field By Label       objectForm    Node Name                     ${name}
    Fill OV Date By Label        objectForm    Start Date                    ${start_date}
    Fill OV Field By Label       objectForm    Calculation Sequence Number   ${calc_seq}
    Fill OV Dropdown By Label    objectForm    Op Production Unit            ${op_production_unit}
    Save And Refresh List

Update Node Name
    [Documentation]    Select the node, edit Name (by label in updateAttributes), save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${NODE_TABLE}    ${code}
    Fill OV Field By Label    updateAttributes    Node Name    ${new_name}
    Save And Refresh List

Delete Node
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    ...    OV-GM grids redraw lazily after a delete - apply the navigator once more so the
    ...    assertion reads a fresh list, not stale state.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${NODE_TABLE}    ${NODE_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
