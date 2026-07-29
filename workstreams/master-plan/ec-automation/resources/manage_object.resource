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
