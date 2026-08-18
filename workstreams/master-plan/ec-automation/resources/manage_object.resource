*** Settings ***
Documentation       T2 (pattern) — Manage-Object (OV) screen mechanics, shared by
...                 date-effective object screens (e.g. Bank, Equipment).
...                 DELETE here = End Date set equal to Start Date (zero-length
...                 effective window) which EC treats as a TRUE delete (object
...                 removed from its OV view). The toolbar "-" button is disabled
...                 for these screens by design.

Library             Browser
Resource            common.resource
Resource            popup.resource


*** Variables ***
# The OV manage-object list grid id is INVARIANT across every manage_object_nav screen (framework
# constant, verified). Defined ONCE here so no T3 hardcodes it; T3s reference ${OV_MANAGE_OBJECT_TABLE}.
${OV_MANAGE_OBJECT_TABLE}       manage_object_nav_nav:form:T_data


*** Keywords ***
Open New Object Form
    [Documentation]    Hover the Insert toolbar menu and choose "New Object".
    ...    Wait for the submenu item to be visible before clicking (robust vs a fixed sleep).
    Hover    xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]
    Wait For Elements State
    ...    xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']
    ...    visible    timeout=10s
    Click    xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

Select Object Row
    [Documentation]    Select an object row by its code (text lives in a span child).
    [Arguments]    ${table_id}    ${code}
    Click    xpath=//tbody[@id='${table_id}']//span[normalize-space(text())='${code}']
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

Delete Object By Zero-Length Window
    [Documentation]    Set End Date = Start Date -> zero-length window -> EC true delete.
    [Arguments]    ${enddate_id}    ${date}
    Fill EC Date    ${enddate_id}    ${date}

Fill New Object Form
    [Documentation]    Open the New Object form and fill the universal trio
    ...    (Code / Name / Start Date). Screen-specific mandatory extras (e.g. a
    ...    dropdown) are filled by the caller BEFORE it calls Save And Refresh List.
    # 3 locator ids + their 3 values belong together - splitting hurts readability
    [Arguments]    ${code_id}    ${name_id}    ${date_id}    ${code}    ${name}    ${start_date}    # robocop: off=LEN07
    Open New Object Form
    Fill EC Field    ${code_id}    ${code}
    Fill EC Field    ${name_id}    ${name}
    Fill EC Date    ${date_id}    ${start_date}

Save And Refresh List
    [Documentation]    Save the form, then reload the list from the DB: Apply Navigator
    ...    (GO) where the screen has one, else the toolbar Refresh — some custom-URL OV
    ...    screens (Account, Cost Centre, Revenue Order, WBS…) have NO navigator GO.
    Save
    ${has_go}=    Get Element Count    css=button[id="button:form:B"]:visible, a[id="button:form:B"]:visible
    IF    ${has_go} > 0    Apply Navigator    ELSE    Refresh Screen

Update Object Name
    [Documentation]    Select the object row by code, prove the row actually loaded
    ...    (guards against silent mis-select), edit the Name attribute, save + reload.
    [Arguments]    ${table_id}    ${upd_code_id}    ${upd_name_id}    ${code}    ${new_name}
    Select Object Row    ${table_id}    ${code}
    ${loaded}=    Get Property    css=[id="${upd_code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill EC Field    ${upd_name_id}    ${new_name}
    Save And Refresh List

Delete Object Via End Date
    [Documentation]    Select the object row, set End Date = Start Date (EC true
    ...    delete for date-effective objects), save + reload.
    [Arguments]    ${table_id}    ${enddate_id}    ${code}    ${date}
    Select Object Row    ${table_id}    ${code}
    Delete Object By Zero-Length Window    ${enddate_id}    ${date}
    Save And Refresh List

Object Row Should Show Name
    [Documentation]    Assert the grid row holding ${code} displays ${name}.
    [Arguments]    ${table_id}    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${table_id}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Row ${code} does not show name ${name}

# --- Label-driven field resolution (NO hardcoded row/column ids) -------------------------------
# A field's label span (ECCell) and its input sit in ADJACENT tableCells of the same tableRow. So a
# field is located by its LABEL, not a hardcoded R:<n>:C:<n> id - robust to per-screen row shifts
# (e.g. Start Date at R2 on Choke vs R4 on Choke Model) and to the objectdates End Date (C:2 label ->
# C:3 input). Browser locators auto-pierce the EC iframe. ${form} = objectForm | updateAttributes | objectdates.

OV Field Id By Label
    [Documentation]    Resolve the input id for a field by its LABEL in ${form} (no hardcoded row/column).
    [Arguments]    ${form}    ${label}
    ${id}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':${form}:form:') and normalize-space(text())='${label}']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input
    ...    id
    RETURN    ${id}

Fill OV Field By Label
    [Documentation]    Fill a text field found by its LABEL in ${form}; reuses Fill EC Field (change/blur dispatch).
    [Arguments]    ${form}    ${label}    ${value}
    ${id}=    OV Field Id By Label    ${form}    ${label}
    Fill EC Field    ${id}    ${value}

Fill OV Date By Label
    [Documentation]    Fill a date field found by its LABEL in ${form}; reuses Fill EC Date (Tab + change dispatch).
    [Arguments]    ${form}    ${label}    ${value}
    ${id}=    OV Field Id By Label    ${form}    ${label}
    Fill EC Date    ${id}    ${value}

Fill OV Dropdown By Label
    [Documentation]    Select an autocomplete-dropdown option found by its LABEL in ${form} (no hardcoded ids).
    ...    Targets the dd input SPECIFICALLY (contains 'dd_input') - the generic //input matches TWO nodes
    ...    for a dropdown (dd_input + dd_hinput) and trips Browser strict mode. Derives the PrimeFaces widget
    ...    prefix (strip '_input' -> '...:dd'), then reuses Select EC Dropdown Option (chevron -> item row).
    [Arguments]    ${form}    ${label}    ${value}
    ${id}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':${form}:form:') and normalize-space(text())='${label}']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[contains(@id,'dd_input')]
    ...    id
    ${dd}=    Set Variable    ${id.replace('_input', '')}
    IF    '${value}' == '__FIRST__'
        Select First EC Dropdown Option    ${dd}
    ELSE
        Select EC Dropdown Option    ${dd}    ${value}
    END

Pick OV Popup By Label
    [Documentation]    Select a "Pick from EC Object" popup reference found by its LABEL in ${form}
    ...    (${form} = objectForm | updateAttributes | objectdates | nav). Resolves the readonly
    ...    '...:pin' input by label (adjacent tableCell, same as the dropdown resolver but ending ':pin'),
    ...    then reuses Pick From EC Object Popup (or Pick First for __FIRST__). LOCATION-AGNOSTIC: the
    ...    pin/pinB widget is identical in the insert form and the navigator, so the same keyword handles
    ...    both (the id-prefix filter drops the leading colon so 'nav:form:' matches as well as 'objectForm:form:').
    [Arguments]    ${form}    ${label}    ${value}
    ${id}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,'${form}:form:') and normalize-space(text())='${label}']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
    ...    id
    IF    '${value}' == '__FIRST__'
        Pick First EC Object Popup    ${id}
    ELSE
        Pick From EC Object Popup    ${id}    ${value}
    END

# --- Properties-driven read-back / verify (round-trip check, no fixed per-field arguments) -----
# The write-side counterpart to Fill OV Field By Label Any Kind: reads a field's CURRENT value
# instead of setting it, using the same kind-detection order, so a properties file can drive
# VERIFICATION the same way it drives INSERT/UPDATE.

Get OV Field Value By Label
    [Documentation]    Read back the CURRENT value of a field found by LABEL in ${form}, using the
    ...    SAME kind-detection order as Fill OV Field By Label Any Kind (dropdown dd_input checked
    ...    first to avoid the dd_input/dd_hinput dual-node strict-mode trip, then popup pin, then
    ...    the generic single-input case) so a read-back always targets the same node a fill would
    ...    have written to.
    [Arguments]    ${form}    ${label}
    ${dd_count}=    Get Element Count
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':${form}:form:') and normalize-space(text())='${label}']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[contains(@id,'dd_input')]
    IF    ${dd_count} > 0
        ${id}=    Get Attribute
        ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':${form}:form:') and normalize-space(text())='${label}']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[contains(@id,'dd_input')]
        ...    id
    ELSE
        ${pin_count}=    Get Element Count
        ...    xpath=//span[contains(@class,'ECCell') and contains(@id,'${form}:form:') and normalize-space(text())='${label}']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
        IF    ${pin_count} > 0
            ${id}=    Get Attribute
            ...    xpath=//span[contains(@class,'ECCell') and contains(@id,'${form}:form:') and normalize-space(text())='${label}']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
            ...    id
        ELSE
            ${id}=    OV Field Id By Label    ${form}    ${label}
        END
    END
    ${value}=    Get Property    css=[id="${id}"]    value
    RETURN    ${value}

Verify Object Form Fields From Properties
    [Documentation]    Read fields from ${form} (by label, auto-detecting kind via Get OV Field
    ...    Value By Label) and assert each equals ${properties_path}'s value for that label - a
    ...    live-DOM round-trip check that the UI actually SHOWS what was saved, on top of (not
    ...    instead of) DB verification. Caller must already have the row selected/form loaded.
    ...    If @{labels} is given, only THOSE labels are checked (use this when ${form} doesn't
    ...    contain every field the properties file lists - e.g. updateAttributes has no Start Date,
    ...    that lives only in objectdates). If @{labels} is empty, every key in the file is checked.
    [Arguments]    ${form}    ${properties_path}    @{labels}
    ${data}=    Read Properties    ${properties_path}
    ${keys}=    Set Variable If    ${labels}    ${labels}    ${data.keys()}
    FOR    ${label}    IN    @{keys}
        ${expected}=    Set Variable    ${data}[${label}]
        ${actual}=    Get OV Field Value By Label    ${form}    ${label}
        Should Be Equal    ${actual}    ${expected}
        ...    msg=Field '${label}' shows '${actual}' in ${form}, expected '${expected}'
    END

Verify Object Row Fields From Properties
    [Documentation]    Assert the grid row for ${code} in ${table_id} displays each field named in
    ...    ${properties_path} (grid-column labels only, e.g. Code/Name/Start Date - the grid shows
    ...    far fewer columns than the form, so this should point at a DEDICATED grid-only properties
    ...    file, not the full form-record one). If @{labels} is given, only THOSE labels are checked
    ...    instead of every key in the file. Only pass/list labels that are REAL grid columns on
    ...    this screen (confirmed by a live field-inventory scan) - a form-only field (e.g.
    ...    Description) is never shown in the grid and would always fail here.
    [Arguments]    ${table_id}    ${code}    ${properties_path}    @{labels}
    ${data}=    Read Properties    ${properties_path}
    ${keys}=    Set Variable If    ${labels}    ${labels}    ${data.keys()}
    ${row}=    Get Text    xpath=//tbody[@id='${table_id}']//tr[.//span[normalize-space(text())='${code}']]
    FOR    ${label}    IN    @{keys}
        Should Contain    ${row}    ${data}[${label}]
        ...    msg=Grid row ${code} missing ${label}='${data}[${label}]'
    END

# --- Properties-driven Insert (data-driven form fill, no fixed per-field arguments) ------------
# A properties file (column=value, read via libraries/PropertiesReader.py) drives WHICH fields get
# filled and WITH WHAT, so a screen's insert data lives in a plain text file, not hardcoded RF
# arguments. Each field's INPUT KIND (text/date/dropdown/popup) is auto-detected live from the DOM
# by label - the caller's properties file never has to say what kind a field is.

Fill OV Field By Label Any Kind
    [Documentation]    Fill a field found by LABEL in ${form}, auto-detecting whether it's a
    ...    dropdown, date, popup, or plain text field - so a properties-file-driven caller never
    ...    has to know a field's kind ahead of time. Dropdown is checked FIRST and separately
    ...    (not via the generic OV Field Id By Label) because a dropdown's "following-sibling"
    ...    tableCell holds TWO input nodes (dd_input + dd_hinput) - the generic single-//input
    ...    xpath trips Browser strict mode on those, exactly the gotcha Fill OV Dropdown By Label
    ...    already documents. __FIRST__ picks the first available option for a dropdown/popup.
    [Arguments]    ${form}    ${label}    ${value}
    ${dd_count}=    Get Element Count
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':${form}:form:') and normalize-space(text())='${label}']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[contains(@id,'dd_input')]
    IF    ${dd_count} > 0
        Fill OV Dropdown By Label    ${form}    ${label}    ${value}
    ELSE
        ${pin_count}=    Get Element Count
        ...    xpath=//span[contains(@class,'ECCell') and contains(@id,'${form}:form:') and normalize-space(text())='${label}']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
        IF    ${pin_count} > 0
            Pick OV Popup By Label    ${form}    ${label}    ${value}
        ELSE
            ${id}=    OV Field Id By Label    ${form}    ${label}
            IF    '${id}'[-8:] == 'da_input'
                Fill EC Date    ${id}    ${value}
            ELSE
                Fill EC Field    ${id}    ${value}
            END
        END
    END

Insert Object From Properties
    [Documentation]    Open the New Object form and fill EVERY field named in ${properties_path}
    ...    (a column=value file read via PropertiesReader.Read Properties), auto-detecting each
    ...    field's kind by label. Then Save + reload the list. Returns the resolved Code value
    ...    (read from the properties file's own "Code" entry) so the caller can assert on it.
    [Arguments]    ${properties_path}
    ${data}=    Read Properties    ${properties_path}
    Open New Object Form
    FOR    ${label}    IN    @{data.keys()}
        Fill OV Field By Label Any Kind    objectForm    ${label}    ${data}[${label}]
    END
    Save And Refresh List
    RETURN    ${data}[Code]

Update Object From Properties
    [Documentation]    Select the row for ${code}, verify it's really the intended row (read Code
    ...    back from updateAttributes BEFORE writing anything - row-identity check), then fill
    ...    EVERY field named in ${properties_path} into updateAttributes, auto-detecting each
    ...    field's kind by label. Save + reload. Mirrors Insert Object From Properties for the
    ...    Update side. Only list fields that actually exist in updateAttributes in the properties
    ...    file - Code is typically read-only there, and date fields usually live in a separate
    ...    objectdates form, not updateAttributes (confirmed on Bank).
    [Arguments]    ${table_id}    ${code}    ${properties_path}
    Select Object Row    ${table_id}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    ${data}=    Read Properties    ${properties_path}
    FOR    ${label}    IN    @{data.keys()}
        Fill OV Field By Label Any Kind    updateAttributes    ${label}    ${data}[${label}]
    END
    Save And Refresh List
    RETURN    ${data}

Apply OV-GM Navigator First Available
    [Documentation]    OV-GM (grid manageObject:form:T_data) is navigator-GATED: the grid is empty until a
    ...    cascade of navigator dropdowns is set + GO. Fill nav:form:G:0:R:${row}:C:1..N dd FIRST-AVAILABLE
    ...    parent->child (up to 6 columns; stops at the first absent), click GO, RETURN the C:1 top-parent
    ...    value. The insert form's parent-dd (Op Production Unit / Business Unit Name) MUST be set to it or
    ...    the new row is not visible under this scope. Twin of engine apply_ovgm_navigator (py/ec_object_iud.py).
    [Arguments]    ${row}=1
    ${top}=    Set Variable    ${EMPTY}
    FOR    ${col}    IN RANGE    1    7
        ${dd}=    Set Variable    nav:form:G:0:R:${row}:C:${col}:dd
        ${n}=    Get Element Count    css=[id="${dd}_input"]
        IF    ${n} == 0    BREAK
        Select First EC Dropdown Option    ${dd}
        Sleep    0.7s
        IF    ${col} == 1
            ${top}=    Get Property    css=[id="${dd}_input"]    value
        END
    END
    Apply Navigator
    RETURN    ${top}
