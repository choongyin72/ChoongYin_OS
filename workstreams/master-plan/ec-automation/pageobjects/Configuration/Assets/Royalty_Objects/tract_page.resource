*** Settings ***
Documentation       T3 (screen) - Tract page object.
...                 Screen: Configuration > Assets > Royalty Objects > Tract.
...                 OV-GM behaviour: the grid (manageObject:form:T_data) loads ONLY after a
...                 Unit Agreement is picked in the navigator + GO. The inserted object's
...                 "Unit Agreement" must equal that nav scope or the filtered grid will never
...                 list it (recon 2026-06-26; same family as Transport System, gated by Unit
...                 Agreement instead of Business Unit).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource


*** Variables ***
${TRACT_SCREEN}           Tract
${TRACT_TABLE}            manageObject:form:T_data
# navigator: Unit Agreement dropdown - MANDATORY before the grid loads
${TRACT_NAV_UA}           nav:form:G:1:R:1:C:0:dd
# objectForm field IDs (Insert - new object)
${TRACT_INS_CODE}         tab:tabPanel:objectForm:form:G:0:R:0:C:1:in
${TRACT_INS_NAME}         tab:tabPanel:objectForm:form:G:0:R:1:C:1:in
${TRACT_INS_DATE}         tab:tabPanel:objectForm:form:G:0:R:2:C:1:da_input
# Insert form's "Unit Agreement" dropdown (mandatory / grid-visibility parent)
${TRACT_INS_PARENT}       tab:tabPanel:objectForm:form:G:0:R:3:C:1:dd
# updateAttributes field IDs (Update - existing object)
${TRACT_UPD_CODE}         tab:tabPanel:updateAttributes:form:G:0:R:0:C:1:in
${TRACT_UPD_NAME}         tab:tabPanel:updateAttributes:form:G:0:R:1:C:1:in
# objectdates field ID (Delete - End Date = Start Date)
${TRACT_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Tract Screen
    [Documentation]    Suite Setup: launch, login, navigate, pick the Unit Agreement
    ...    navigator context and apply it (grid is empty until then).
    [Arguments]    ${unit_agreement}    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${TRACT_SCREEN}    ${user}    ${pass}
    Select EC Dropdown Option    ${TRACT_NAV_UA}    ${unit_agreement}
    Apply Navigator

Tract Row Should Exist
    [Documentation]    Assert a tract with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${TRACT_TABLE}    ${code}

Tract Row Should Not Exist
    [Documentation]    Assert a tract with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TRACT_TABLE}    ${code}

Tract Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_tract.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_tract    ${code}

Tract Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_tract.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_tract    ${code}

Tract Row Should Show Name
    [Documentation]    Assert the Tract row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TRACT_TABLE}    ${code}    ${name}

Insert Tract Record
    [Documentation]    Insert a new tract: New Object form -> Code/Name/Start Date +
    ...    "Unit Agreement" = ${parent} (mandatory / grid-visibility link) -> Save.
    [Arguments]    ${code}    ${name}    ${start_date}    ${parent}
    Fill New Object Form    ${TRACT_INS_CODE}    ${TRACT_INS_NAME}    ${TRACT_INS_DATE}
    ...    ${code}    ${name}    ${start_date}
    Select EC Dropdown Option    ${TRACT_INS_PARENT}    ${parent}
    Save And Refresh List
    # OV-GM grid redraws lazily after save - re-apply the UA nav filter so the new row renders
    # before TC02 asserts (R17). The same extra GO is used by Delete Tract.
    Apply Navigator

Update Tract Name
    [Documentation]    Select the tract, confirm it loaded, edit Name, Save.
    [Arguments]    ${code}    ${new_name}
    Update Object Name    ${TRACT_TABLE}    ${TRACT_UPD_CODE}    ${TRACT_UPD_NAME}    ${code}    ${new_name}

Delete Tract
    [Documentation]    Select the tract, set End Date = Start Date (true delete), Save.
    ...    Versioned GM grids redraw lazily - one extra Apply Navigator before asserting.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TRACT_TABLE}    ${TRACT_DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
