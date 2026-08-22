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
Resource            grid_menu.resource


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
    [Documentation]    Select an object row by its code (text lives in a span child). Tries a
    ...    direct click first - the exact prior behavior, unchanged - which is the fast path
    ...    for every already-shipped OV screen (all have small/single-page grids where the row
    ...    is always on the current page, so this never triggers the fallback below). If the
    ...    row isn't visible within 3s (the class of failure Account hit 2026-08-22:
    ...    OV_FIN_ACCOUNT has 110+ rows on a 20-row/page grid, and AUTOTEST_ACCOUNT sorted
    ...    alphabetically past every numeric code, landing off page 1), automatically retries by
    ...    filtering the grid's Code column (0, leftmost) to ${code} via the shared
    ...    resources/grid_menu.resource (already proven live on Business Function and Account) -
    ...    this searches the FULL server-side dataset in one call, so no screen has to know or
    ...    declare its own grid size ahead of time (standardised 2026-08-22, superseding
    ...    Account's own one-off T3-local page-walking/filter keywords). Falls back to a bare
    ...    "not found" failure if this grid doesn't expose the hamburger filter toggle at all
    ...    (an older/non-filtering grid) - no worse than the pre-existing behavior for such a
    ...    grid. Clears the filter again right after a successful filtered select, so the grid
    ...    is left unfiltered for any caller that assumes a clean view afterward.
    [Arguments]    ${table_id}    ${code}
    VAR    ${xpath}=    xpath=//tbody[@id='${table_id}']//span[normalize-space(text())='${code}']
    TRY
        Wait For Elements State    ${xpath}    visible    timeout=3s
    EXCEPT
        Select Object Row Via Filter    ${table_id}    ${code}    ${xpath}
        RETURN
    END
    Click    ${xpath}
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s

Select Object Row Via Filter
    [Documentation]    Fallback half of Select Object Row: filter the grid's Code column (0,
    ...    leftmost) to ${code} via resources/grid_menu.resource, then click the now-visible
    ...    row and clear the filter again. Fails loud if this grid has no hamburger filter
    ...    toggle at all (an older/non-filtering grid - no worse than the pre-existing
    ...    behavior for such a grid).
    [Arguments]    ${table_id}    ${code}    ${xpath}
    VAR    ${form}=    ${table_id.rsplit(':T_data', 1)[0]}
    ${supported}=    Get Element Count    css=[id="${form}:T:tfo"]
    IF    ${supported} == 0
        Fail    msg=Row ${code} not found in ${table_id} (grid has no column-filter fallback)
    END
    Filter Grid Text Column By Value    ${form}    0    ${code}
    Wait For Elements State    ${xpath}    visible    timeout=10s
    Click    ${xpath}
    Wait For Load State    networkidle    timeout=15s
    Sleep    1.2s
    Clear Grid Text Column Filter    ${form}    0

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
    ...    If ${pre_save_screenshot} is given, a screenshot is captured right after the End
    ...    Date is filled but BEFORE Save is clicked (added 2026-08-22, consolidating the
    ...    identical pattern previously hand-rolled in Bank's/Object List's own T3 "Delete
    ...    <Screen>" keywords). Optional and backward-compatible - no screenshot at all if
    ...    omitted, so every existing caller (100+ screens) is unaffected.
    [Arguments]    ${table_id}    ${enddate_id}    ${code}    ${date}    ${pre_save_screenshot}=${EMPTY}
    Select Object Row    ${table_id}    ${code}
    Delete Object By Zero-Length Window    ${enddate_id}    ${date}
    IF    '${pre_save_screenshot}' != ''
        Capture Step    ${pre_save_screenshot}
    END
    Save And Refresh List

OV Row Should Exist
    [Documentation]    Assert a row with ${code} exists in ${table_id}. Checks the CURRENT
    ...    page first (T1 Row Exists, unchanged fast path - zero behavior/timing change for
    ...    every already-shipped OV screen, whose grids all fit on one page today). Only if
    ...    not found there AND this grid exposes the EC hamburger column-filter
    ...    (resources/grid_menu.resource) does it retry via a Code-column (0) filter, which
    ...    searches the FULL server-side dataset - the same standardised fallback as Select
    ...    Object Row (2026-08-22), generalised from Account's one-off fix so no future
    ...    large-grid screen needs its own bespoke pagination workaround. Restores the grid
    ...    to its unfiltered state before returning either way.
    [Arguments]    ${table_id}    ${code}
    ${exists}=    Row Exists    ${table_id}    ${code}
    IF    not ${exists}
        VAR    ${form}=    ${table_id.rsplit(':T_data', 1)[0]}
        ${supported}=    Get Element Count    css=[id="${form}:T:tfo"]
        IF    ${supported} > 0
            Filter Grid Text Column By Value    ${form}    0    ${code}
            ${n}=    Grid Data Row Count    ${form}
            ${exists}=    Evaluate    ${n} > 0
            Clear Grid Text Column Filter    ${form}    0
        END
    END
    Should Be True    ${exists}    msg=Expected row ${code} to exist in ${table_id}

OV Row Should Not Exist
    [Documentation]    Assert a row with ${code} is absent from ${table_id} - across the WHOLE
    ...    dataset when this grid supports filtering, not just the current page (2026-08-22
    ...    standardisation, generalised from Account's one-off page-walk fix). Unlike OV Row
    ...    Should Exist, this does NOT try the current page first: a current-page-only absence
    ...    check is unsound on ANY grid, not just a large one - a stale leftover row could sit
    ...    on a later page while page 1 looks clean regardless of grid size. Falls back to the
    ...    original raw current-page-only check only when this grid has no filter toggle at all
    ...    (an older/non-filtering grid keeps its exact prior behavior - nothing to filter,
    ...    nothing lost).
    [Arguments]    ${table_id}    ${code}
    VAR    ${form}=    ${table_id.rsplit(':T_data', 1)[0]}
    ${supported}=    Get Element Count    css=[id="${form}:T:tfo"]
    IF    ${supported} > 0
        Filter Grid Text Column By Value    ${form}    0    ${code}
        ${n}=    Grid Data Row Count    ${form}
        Clear Grid Text Column Filter    ${form}    0
        Should Be Equal    ${n}    ${0}    msg=Row ${code} should NOT exist in ${table_id}
    ELSE
        Row Should Not Exist    ${table_id}    ${code}
    END

Object Row Should Show Name
    [Documentation]    Assert the grid row holding ${code} displays ${name}.
    [Arguments]    ${table_id}    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${table_id}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Row ${code} does not show name ${name}

Find Object By Code
    [Documentation]    Select the object row by ${code} (loads updateAttributes), verifying
    ...    row-identity (Code read back) before returning - the shared core of every screen's
    ...    "Find <Screen>" keyword (added 2026-08-22, consolidating the identical pattern
    ...    previously hand-rolled per-screen in Bank/Object List T3). ${screen_label} is used
    ...    only in the failure message, so a caller's error still names its own screen.
    ...    ${code_label} defaults to "Code" (Bank/Object List's actual label) - added
    ...    2026-08-22 after State's live build proved this is NOT a universal Bank-family
    ...    convention: State's own Code field is labelled "State Code" (screen-prefixed).
    ...    Optional/backward-compatible - every existing caller keeps working unchanged.
    [Arguments]    ${table_id}    ${code}    ${screen_label}=Object    ${code_label}=Code
    Select Object Row    ${table_id}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    ${code_label}
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Find ${screen_label} failed - code not loaded

Find Object Record
    [Documentation]    Select ${code} (loads updateAttributes, via T2 Find Object By Code -
    ...    verifies row-identity before returning) then capture the find-action evidence
    ...    screenshot - the shared core of every screen's "Find <Screen> Record" (TC04
    ...    select-step) keyword (added 2026-08-22, owner: "DONT want repeated codes in all
    ...    screen page.resource files" - consolidating the identical Bank/Object List pattern:
    ...    each screen previously hand-rolled its own single-purpose "Find <Screen>" keyword
    ...    plus an identical select+capture wrapper around it). ${code_label} defaults to
    ...    "Code" - pass a screen's own label (e.g. "State Code") if it differs.
    [Arguments]    ${table_id}    ${code}    ${screen_label}=Object    ${code_label}=Code
    Find Object By Code    ${table_id}    ${code}    ${screen_label}    ${code_label}
    Capture Step    ${TEST NAME}_action

Verify Object Removed
    [Documentation]    Assert ${code} is absent from BOTH the grid (${table_id}) and the
    ...    database (${db_view}) - the shared core of every screen's "Verify <Screen> Record
    ...    Removed" keyword (added 2026-08-22). Caller adds its own Capture Step - screenshot
    ...    naming stays screen-aware, not pulled in here.
    [Arguments]    ${table_id}    ${db_view}    ${code}
    OV Row Should Not Exist    ${table_id}    ${code}
    Code Should Be Absent In View    ${db_view}    ${code}

Verify Object Form Record
    [Documentation]    Select ${code} (loads updateAttributes) and assert ${properties_path}'s
    ...    fields match the live screen (only @{labels} if given, else every key in the file),
    ...    then capture the verify evidence screenshot - the shared core of every screen's
    ...    "Verify <Screen> Record Updated" keyword, and half of "Verify <Screen> Record Exists"
    ...    (added 2026-08-22, consolidating the identical Bank/Object List pattern - owner
    ...    query 2026-08-22: "we want all object ec screen share... code at one place"). The
    ...    sequence (select, compare, capture) is layout-independent; which fields to check
    ...    stays per-screen data (${properties_path}/@{labels}), never assumed here.
    ...    ${code_label} (keyword-only, after @{labels}) defaults to "Code" - pass a screen's
    ...    own label (e.g. "State Code") if it differs (added 2026-08-22, optional/
    ...    backward-compatible, after State's live build proved this isn't a universal label).
    [Arguments]    ${table_id}    ${code}    ${screen_label}    ${properties_path}    @{labels}
    ...    ${code_label}=Code
    Find Object By Code    ${table_id}    ${code}    ${screen_label}    ${code_label}
    Verify Object Form Fields From Properties    updateAttributes    ${properties_path}    @{labels}
    Capture Step    ${TEST NAME}_verify

Verify Object Insert Exists
    [Documentation]    Assert ${code} shows in the grid, THEN assert the form record matches
    ...    ${properties_path} - the shared core of every screen's "Verify <Screen> Record
    ...    Exists" (TC02) keyword (added 2026-08-22, same consolidation as Verify Object Form
    ...    Record above, which this delegates the select/compare/capture half to). PURE SCREEN
    ...    verification - no DB check here (that is TC02's own separate DbVerify assertion).
    ...    ${code_label} (keyword-only, after @{labels}) defaults to "Code" - threaded through
    ...    to Verify Object Form Record (added 2026-08-22, optional/backward-compatible).
    [Arguments]    ${table_id}    ${code}    ${screen_label}    ${properties_path}    @{labels}
    ...    ${code_label}=Code
    OV Row Should Exist    ${table_id}    ${code}
    Verify Object Form Record    ${table_id}    ${code}    ${screen_label}    ${properties_path}
    ...    @{labels}    code_label=${code_label}

Verify Object Does Not Exist
    [Documentation]    Assert ${code} is absent from the grid (${table_id}), then capture the
    ...    verify evidence screenshot - the shared core of every screen's "Verify <Screen>
    ...    Record Does Not Exist" (TC01 clean-state) keyword (added 2026-08-22, same
    ...    consolidation goal as Verify Object Insert Exists/Form Record/Found above).
    [Arguments]    ${table_id}    ${code}
    OV Row Should Not Exist    ${table_id}    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Object Found
    [Documentation]    Assert BOTH the grid row (${grid_properties_path}) AND the form record
    ...    (${form_properties_path}) match - the shared core of every screen's "Verify <Screen>
    ...    Record Found" (TC04) keyword (added 2026-08-22, same consolidation goal as Verify
    ...    Object Insert Exists/Form Record above). Caller must already have selected the row
    ...    when @{form_labels} is empty and the default form-verify file expects a prior Find -
    ...    matching the existing per-screen convention (Bank/Object List TC04 both call their
    ...    own Find <Screen> Record before this).
    [Arguments]    ${table_id}    ${code}    ${grid_properties_path}    ${form_properties_path}
    ...    @{form_labels}
    Verify Object Row Fields From Properties    ${table_id}    ${code}    ${grid_properties_path}
    Verify Object Form Fields From Properties    updateAttributes    ${form_properties_path}
    ...    @{form_labels}
    Capture Step    ${TEST NAME}_verify

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
    ...    (read from the properties file's own ${code_label} entry, defaults to "Code") so
    ...    the caller can assert on it. ${code_label} added 2026-08-22 - State's properties
    ...    file uses "State Code" as the key, not the generic "Code" Bank/Object List use;
    ...    optional/backward-compatible, every existing caller keeps working unchanged.
    ...    If ${pre_save_screenshot} is given, a screenshot is captured right after every field
    ...    is filled but BEFORE Save is clicked (owner-requested 2026-08-18: evidence of what was
    ...    entered, not the after-save/reloaded-grid state). Optional and backward-compatible -
    ...    no screenshot at all if omitted.
    [Arguments]    ${properties_path}    ${pre_save_screenshot}=${EMPTY}    ${code_label}=Code
    ${data}=    Read Properties    ${properties_path}
    Open New Object Form
    FOR    ${label}    IN    @{data.keys()}
        Fill OV Field By Label Any Kind    objectForm    ${label}    ${data}[${label}]
    END
    IF    '${pre_save_screenshot}' != ''
        Capture Step    ${pre_save_screenshot}
    END
    Save And Refresh List
    RETURN    ${data}[${code_label}]

Insert Object From Properties And Verify Code
    [Documentation]    Insert via ${properties_path} (same as Insert Object From Properties),
    ...    then assert the resolved Code matches ${expected_code} - catching a properties-file
    ...    /suite-variable drift immediately instead of silently inserting under the wrong
    ...    code (added 2026-08-22, consolidating the identical pattern previously hand-rolled
    ...    in Bank's/Object List's own "Insert <Screen> Record And Save" keywords).
    ...    ${code_label} defaults to "Code" - pass a screen's own label (e.g. "State Code")
    ...    if it differs (added 2026-08-22, optional/backward-compatible).
    [Arguments]    ${properties_path}    ${expected_code}    ${pre_save_screenshot}=${EMPTY}
    ...    ${code_label}=Code
    ${code}=    Insert Object From Properties    ${properties_path}    ${pre_save_screenshot}
    ...    ${code_label}
    Should Be Equal    ${code}    ${expected_code}
    ...    msg=${properties_path} Code does not match the expected ${expected_code}
    RETURN    ${code}

Update Object From Properties
    [Documentation]    Select the row for ${code}, verify it's really the intended row (read Code
    ...    back from updateAttributes BEFORE writing anything - row-identity check), then fill
    ...    EVERY field named in ${properties_path} into updateAttributes, auto-detecting each
    ...    field's kind by label. Save + reload. Mirrors Insert Object From Properties for the
    ...    Update side. Only list fields that actually exist in updateAttributes in the properties
    ...    file - Code is typically read-only there, and date fields usually live in a separate
    ...    objectdates form, not updateAttributes (confirmed on Bank).
    ...    If ${pre_save_screenshot} is given, a screenshot is captured right after every field
    ...    is filled but BEFORE Save is clicked (owner-requested 2026-08-18: evidence of what was
    ...    entered, not the after-save/reloaded-grid state). Optional and backward-compatible -
    ...    no screenshot at all if omitted. ${code_label} defaults to "Code" - pass a screen's
    ...    own label (e.g. "State Code") if it differs (added 2026-08-22, optional/
    ...    backward-compatible, after State's live build proved this isn't a universal label).
    [Arguments]    ${table_id}    ${code}    ${properties_path}    ${pre_save_screenshot}=${EMPTY}
    ...    ${code_label}=Code
    Select Object Row    ${table_id}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    ${code_label}
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    ${data}=    Read Properties    ${properties_path}
    FOR    ${label}    IN    @{data.keys()}
        Fill OV Field By Label Any Kind    updateAttributes    ${label}    ${data}[${label}]
    END
    IF    '${pre_save_screenshot}' != ''
        Capture Step    ${pre_save_screenshot}
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
