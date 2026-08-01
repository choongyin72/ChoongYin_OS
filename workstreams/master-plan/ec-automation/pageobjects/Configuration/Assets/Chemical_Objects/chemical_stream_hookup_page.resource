*** Settings ***
Documentation       T3 (screen) - Chemical Stream Hookup page object.
...                 Screen: Configuration > Assets > Chemical_Objects > Chemical Stream Hookup.
...                 OV-GM (manage-object, groupmodel): the grid loads ONLY after the navigator
...                 cascade + GO (capability Apply OV-GM Navigator First Available). Fields resolved
...                 BY LABEL (no hardcoded rows). No Op Production Unit field on this screen (confirmed
...                 live: mand=False, not filled).
...
...                 SECOND screen to adopt the standalone mandatory_field_gate.resource - the
...                 CASCADE-HEAVY comparison case (PU -> Area -> Facility Class 1 + GO). Insert/Update
...                 keywords inline Save And Refresh List's own logic with the gate call before Save -
...                 manage_object.resource itself is NOT modified.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/mandatory_field_gate.resource


*** Variables ***
${SCR}              Chemical Stream Hookup
${TBL}              manageObject:form:T_data
${DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${GM_PU}            ${EMPTY}
${NAV_DD}            nav:form:G:0:R:1:C:1:dd


*** Keywords ***
Open Chemical Stream Hookup Screen
    [Documentation]    Suite Setup: launch, login, navigate, fill the OV-GM navigator cascade
    ...    first-available + GO, RETURN the top-parent PU (grid empty until then).
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${SCR}    ${user}    ${pass}
    ${pu}=    Apply OV-GM Navigator First Available
    RETURN    ${pu}

Chemical Stream Hookup Row Should Exist
    [Documentation]    Assert ${code} is present (await lazy OV-GM redraw first).
    [Arguments]    ${code}
    Wait For Elements State
    ...    xpath=//tbody[@id='${TBL}']//span[normalize-space(text())='${code}']
    ...    visible    timeout=20s
    Row Should Exist    ${TBL}    ${code}

Chemical Stream Hookup Row Should Not Exist
    [Documentation]    Assert ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${TBL}    ${code}

Chemical Stream Hookup Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} persisted in OV_CHEM_STRM_HOOKUP.
    [Arguments]    ${code}
    Code Should Be Present In View    OV_CHEM_STRM_HOOKUP    ${code}

Chemical Stream Hookup Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} deleted from OV_CHEM_STRM_HOOKUP.
    [Arguments]    ${code}
    Code Should Be Absent In View    OV_CHEM_STRM_HOOKUP    ${code}

Chemical Stream Hookup Row Should Show Name
    [Documentation]    Assert the row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    Object Row Should Show Name    ${TBL}    ${code}    ${name}

Insert Chemical Stream Hookup Record
    [Documentation]    Insert (all fields BY LABEL), gate-check for empty mandatory fields BEFORE
    ...    Save, then Save + reload (inlines Save And Refresh List's own GO-or-Refresh logic).
    [Arguments]    ${code}    ${name}    ${start_date}
    Open New Object Form
    Fill OV Field By Label       objectForm    Chemical Stream Hookup Code    ${code}
    Fill OV Field By Label       objectForm    Chemical Stream Hookup Name    ${name}
    Fill OV Date By Label        objectForm    Start Date    ${start_date}
    Assert No Empty Mandatory Field    tab:tabPanel:objectForm:form    Save (insert)
    Save
    ${has_go}=    Get Element Count
    ...    css=button[id="button:form:B"]:visible, a[id="button:form:B"]:visible
    IF    ${has_go} > 0    Apply Navigator    ELSE    Refresh Screen

Update Chemical Stream Hookup Name
    [Documentation]    Select the row, edit Name (by label), gate-check, save + reload.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${TBL}    ${code}
    Fill OV Field By Label    updateAttributes    Chemical Stream Hookup Name    ${new_name}
    Assert No Empty Mandatory Field    tab:tabPanel:updateAttributes:form    Save (update)
    Save
    ${has_go}=    Get Element Count
    ...    css=button[id="button:form:B"]:visible, a[id="button:form:B"]:visible
    IF    ${has_go} > 0    Apply Navigator    ELSE    Refresh Screen

Delete Chemical Stream Hookup
    [Documentation]    Delete via End Date = Start Date (EC true delete), save + reload.
    [Arguments]    ${code}    ${date}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    Apply Navigator
