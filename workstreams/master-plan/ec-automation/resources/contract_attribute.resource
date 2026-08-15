*** Settings ***
Documentation       T2 pattern — Contract Attribute screen family (Sale/Revenue/Transport Contract
...                 Attributes are the SAME JSF component: com.ec.tran.co.screens/contract_attribute,
...                 differing only by URL ACCESS_COLUMN=SALE_CODE|REVN_CODE|TRAN_CODE). Verified
...                 cross-screen and cross-environment (CLP ECaaS TEST + this repo's local sandbox)
...                 2026-08-09. Ported from the validated Playwright module
...                 ../libraries/contract_attribute_helpers.py — see that file's docstring for the
...                 full mechanism writeup, and ec-ui-knowledge/screens/contract-attributes-family.md
...                 for the cross-screen doc. Screen-specific nav values/row indices live in the T3
...                 page object; this layer is the shared attribute-grid mechanics.

Library             Browser
Resource            common.resource


*** Variables ***
${CA_GRID_ID}           attribute:form:T_data
${CA_MENUBAR_ID}        screenToolbar:form:menuBar
${CA_VALUE_IN}          version:form:T:0:C1_in
${CA_VALUE_CB}          version:form:T:0:C1_cb
${CA_VALUE_DD_BTN}      version:form:T:0:C1_dd_button
${CA_VALUE_DD_PANEL}    version:form:T:0:C1_dd_panel
${CA_DAYTIME_IN}        version:form:T:0:C0_da_input
${CA_PROTECTED_TEXT}    Not allowed to insert protected attributes


*** Keywords ***
Set Contract Attribute Navigator
    [Documentation]    Set Business Unit / Contract Area / Contract on any Contract Attribute
    ...    screen (Sale/Revenue/Transport share the same nav shape: group G:0, columns C:1/C:2/C:3)
    ...    then click Go.
    [Arguments]    ${business_unit}    ${contract_area}    ${contract}
    Set Contract Attribute Nav Field    C:1    ${business_unit}
    Set Contract Attribute Nav Field    C:2    ${contract_area}
    Set Contract Attribute Nav Field    C:3    ${contract}
    Apply Navigator

Set Contract Attribute Nav Field
    [Documentation]    Set one cascading nav dropdown at nav:form:G:0:R:1:${column}:dd by exact
    ...    data-item-label match (mirrors Set Navigator Filter, but that keyword hardcodes C:0 —
    ...    this screen's fields sit at C:1/C:2/C:3).
    [Arguments]    ${column}    ${value}
    VAR    ${dd}=    nav:form:G:0:R:1:${column}:dd
    Click    css=[id="${dd}_button"]
    VAR    ${item}=    xpath=//*[@id='${dd}_panel']//tr[normalize-space(@data-item-label)='${value}']
    Wait For Elements State    ${item} >> nth=0    visible    timeout=10s
    Click    ${item} >> nth=0
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.6s

Click Contract Attribute Row
    [Documentation]    Click the value cell (td index 1) of grid row ${row_idx} (0-based) to
    ...    select it. On a never-before-set attribute this selects the row but does NOT reveal an
    ...    edit field — check Contract Attribute Edit Field Kind afterwards.
    [Arguments]    ${row_idx}
    Evaluate JavaScript    css=[id="${CA_GRID_ID}"]
    ...    (el) => { const row = el.querySelectorAll('tr')[${row_idx}]; if(row){ const tds = row.querySelectorAll('td'); if(tds[1]) tds[1].click(); } }
    Sleep    0.7s

Get Contract Attribute Row Label
    [Documentation]    Return grid row ${row_idx}'s label (td index 0 text).
    [Arguments]    ${row_idx}
    ${label}=    Evaluate JavaScript    css=[id="${CA_GRID_ID}"]
    ...    (el) => { const row = el.querySelectorAll('tr')[${row_idx}]; return row ? (row.querySelectorAll('td')[0].textContent||'').trim() : ''; }
    RETURN    ${label}

Get Contract Attribute Row Value
    [Documentation]    Return grid row ${row_idx}'s current value (td index 1 text) — read this
    ...    AFTER Save Contract Attribute to verify persistence (ground truth, not the optimistic
    ...    client state).
    [Arguments]    ${row_idx}
    ${value}=    Evaluate JavaScript    css=[id="${CA_GRID_ID}"]
    ...    (el) => { const row = el.querySelectorAll('tr')[${row_idx}]; return row ? (row.querySelectorAll('td')[1].textContent||'').trim() : ''; }
    RETURN    ${value}

Contract Attribute Edit Field Kind
    [Documentation]    Return which edit-field kind is present at the fixed version:form:T:0:C1_
    ...    id: 'in' (plain input), 'dd' (dropdown), 'cb' (checkbox), or 'none' (never-set — needs
    ...    Insert Contract Attribute Version first).
    ${n_in}=    Get Element Count    css=[id="${CA_VALUE_IN}"]
    IF    ${n_in} > 0    RETURN    in
    ${n_cb}=    Get Element Count    css=[id="${CA_VALUE_CB}"]
    IF    ${n_cb} > 0    RETURN    cb
    ${n_dd}=    Get Element Count    css=[id="${CA_VALUE_DD_BTN}"]
    IF    ${n_dd} > 0    RETURN    dd
    RETURN    none

Click Text If Present
    [Documentation]    Click a dialog button matched by ${text} (Browser library's text= engine is
    ...    case-insensitive, unlike an xpath contains() check) if it's present, else no-op. Shared
    ...    by Insert/Delete Contract Attribute Version for their respective confirm/error dialogs.
    [Arguments]    ${text}
    ${n}=    Get Element Count    text=${text}
    IF    ${n} > 0
        Click    text=${text}
        Sleep    0.5s
    END
    RETURN    ${n} > 0

Insert Contract Attribute Version
    [Documentation]    Toolbar Insert(+) -> "Attribute Version" submenu (menuBar link index 2 ->
    ...    hover -> index 3 -> click), for a row that has never had a value. Returns PROTECTED if
    ...    EC refuses ("Not allowed to insert protected attributes" — a real per-attribute business
    ...    rule, not a bug; dismisses the dialog via OK), else OK.
    VAR    ${links}=    css=[id="${CA_MENUBAR_ID}"] a
    Hover    ${links} >> nth=2
    Sleep    0.4s
    Click    ${links} >> nth=3
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.7s
    ${n}=    Get Element Count    text=${CA_PROTECTED_TEXT}
    IF    ${n} > 0
        Click Text If Present    Ok
        RETURN    PROTECTED
    END
    RETURN    OK

Set Contract Attribute Daytime
    [Documentation]    Fill the new version row's Daytime field if it's currently blank —
    ...    MANDATORY for a first-time version, or Save silently no-ops (no error, but the value
    ...    never actually persists — only caught by a later Refresh throwing an unsaved-changes
    ...    modal). No-op if the field already has a date.
    [Arguments]    ${date}
    ${n}=    Get Element Count    css=[id="${CA_DAYTIME_IN}"]
    IF    ${n} == 0    RETURN
    ${cur}=    Get Property    css=[id="${CA_DAYTIME_IN}"]    value
    IF    '${cur}' == '${EMPTY}'
        Click    css=[id="${CA_DAYTIME_IN}"]
        Keyboard Key    press    Control+A
        Type Text    css=[id="${CA_DAYTIME_IN}"]    ${date}
        Keyboard Key    press    Tab
        Sleep    0.5s
    END

Set Contract Attribute Checkbox
    [Documentation]    Set the boolean attribute checkbox to match ${value} ('Y'/'Yes'/${TRUE} =
    ...    checked, anything else = unchecked).
    [Arguments]    ${value}
    ${want}=    Evaluate    str("""${value}""").upper() in ('Y', 'YES', 'TRUE')
    ${checked}=    Get Property    css=[id="${CA_VALUE_CB}"]    checked
    IF    "${checked}" != "${want}"    Click    css=[id="${CA_VALUE_CB}"]
    Sleep    0.3s

Select Contract Attribute Dropdown
    [Documentation]    Pick the option in the value dropdown whose data-item-label contains
    ...    ${value} (substring match — labels can carry odd dash characters).
    [Arguments]    ${value}
    Click    css=[id="${CA_VALUE_DD_BTN}"]
    Sleep    0.7s
    VAR    ${item}=    xpath=//*[@id='${CA_VALUE_DD_PANEL}']//tr[contains(@data-item-label, '${value}')]
    Wait For Elements State    ${item} >> nth=0    visible    timeout=10s
    Click    ${item} >> nth=0
    Sleep    0.5s

Save Contract Attribute
    [Documentation]    Save via the toolbar menuBar link index 0. The shared Save keyword's
    ...    title-based xpath is unreliable on THIS toolbar — use position instead.
    Click    css=[id="${CA_MENUBAR_ID}"] a >> nth=0
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

Ensure Contract Attribute Editable
    [Documentation]    Select row ${row_idx} and, if it has never had a value, auto-insert a version
    ...    so an edit field exists. Returns the resulting edit-field kind ('in'/'cb'/'dd'), or
    ...    'PROTECTED' if EC refused the auto-insert - callers must check for that before editing.
    [Arguments]    ${row_idx}
    Click Contract Attribute Row    ${row_idx}
    ${kind}=    Contract Attribute Edit Field Kind
    IF    '${kind}' != 'none'    RETURN    ${kind}
    ${status}=    Insert Contract Attribute Version
    IF    '${status}' == 'PROTECTED'    RETURN    PROTECTED
    ${kind}=    Contract Attribute Edit Field Kind
    RETURN    ${kind}

Set Contract Attribute Value
    [Documentation]    Set the value of the attribute at grid row ${row_idx}. For a plain/numeric
    ...    attribute pass the text value; for a checkbox pass Y/N; for a dropdown/object-reference
    ...    attribute pass the label substring to match. ${daytime} (YYYY-MM-DD) is required the
    ...    first time an attribute is ever set on this contract — harmless to always pass it.
    ...    Returns OK (and saves), or PROTECTED (no save attempted) if EC refuses the insert —
    ...    callers should assert on this return value rather than assume success.
    [Arguments]    ${row_idx}    ${value}    ${daytime}=${EMPTY}
    ${kind}=    Ensure Contract Attribute Editable    ${row_idx}
    IF    '${kind}' == 'PROTECTED'    RETURN    PROTECTED
    IF    '${daytime}' != '${EMPTY}'
        Set Contract Attribute Daytime    ${daytime}
    END
    IF    '${kind}' == 'in'
        Type Cell By Id    ${CA_VALUE_IN}    ${value}
    ELSE IF    '${kind}' == 'cb'
        Set Contract Attribute Checkbox    ${value}
    ELSE IF    '${kind}' == 'dd'
        Select Contract Attribute Dropdown    ${value}
    END
    Save Contract Attribute
    RETURN    OK

Hover And Click Enabled Menu Item
    [Documentation]    Hover the toolbar link at ${hover_idx} (opens its submenu), assert the
    ...    submenu link at ${click_idx} is NOT disabled (real msg on failure), then click it.
    [Arguments]    ${hover_idx}    ${click_idx}    ${disabled_msg}
    VAR    ${links}=    css=[id="${CA_MENUBAR_ID}"] a
    Hover    ${links} >> nth=${hover_idx}
    Sleep    0.4s
    ${cls}=    Get Attribute    ${links} >> nth=${click_idx}    class
    Should Not Contain    ${cls}    ui-state-disabled    msg=${disabled_msg}
    Click    ${links} >> nth=${click_idx}

Delete Contract Attribute Value
    [Documentation]    Delete the version at grid row ${row_idx}, restoring it to never-set/blank
    ...    — the exact inverse of Set Contract Attribute Value, for self-cleaning test data. Fails
    ...    loudly if the row has no existing version to remove (Delete->Attribute Version is
    ...    disabled in that case — a real guard, not a flake).
    [Arguments]    ${row_idx}
    Click Contract Attribute Row    ${row_idx}
    Hover And Click Enabled Menu Item    6    7
    ...    Delete->Attribute Version is disabled -- row ${row_idx} has no existing version to remove
    Wait For Load State    networkidle    timeout=12s
    Sleep    0.7s
    # this confirm dialog wasn't observed live in testing (SS1_Contract_A row 13 deleted with
    # none appearing) but is kept defensively in case a different attribute type shows one
    Click Text If Present    Yes
    Save Contract Attribute
