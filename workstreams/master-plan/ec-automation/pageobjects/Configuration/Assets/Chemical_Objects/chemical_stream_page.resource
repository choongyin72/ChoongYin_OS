*** Settings ***
Documentation       T3 (screen) — Chemical Stream page object.
...                 Screen: Configuration > Assets > Chemical_Objects > Chemical Stream (CO.0258).
...                 OV-GM with a mandatory Pick-from-EC-Object POPUP (From Connection). The popup
...                 (stream_node_ref_popup) differs from the standard object_popup: it has its own
...                 inner navigator + an Object Type dd (nav:form:G:4, empty on open) + inner GO,
...                 and its list grid id is manage_object_nav_nav:form:T_data (NOT PopupList) -
...                 hence the screen-local popup keyword below (shared T1 popup.resource untouched).
...                 This popup is ORTHOGONAL to the outer navigator and is preserved EXACTLY AS-IS
...                 by this conversion (Open From Connection Popup List / Pick From Connection
...                 Popup keywords unchanged).
...                 Converted to the full Area-pattern STRUCTURE (owner standing rule 2026-08-26:
...                 any EC screen with a navigator matching Area's layout must follow Area's FULL
...                 pattern) - Chemical Stream remains OV-GM with its genuine 3-level Production
...                 Unit -> Area -> Facility Class 1 navigator cascade (same-row, increasing
...                 column: nav:form:G:0:R:1:C:1/C:2/C:3:dd, confirmed via the pre-conversion
...                 "Apply Chemical Stream Navigator" keyword), now filled via the shared T2
...                 "Apply Navigator From Properties" (resources/manage_object.resource), driven by
...                 testdata/chemical_stream_navigator.properties (SPECIFIC P1 values - the popup
...                 source is EMPTY under the first-available AS1 scope, owner screenshot 2026-07-30
...                 proved the P1 scope populates it). Fields BY LABEL. DELETE = End Date = Start
...                 Date.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/navigator.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${SCR}                  Chemical Stream
${TBL}                  manageObject:form:T_data
${DEL_ENDDATE}          tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
${CHEMICAL_STREAM_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_navigator.properties
${CHEMICAL_STREAM_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_insert.properties
${CHEMICAL_STREAM_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_update.properties
${CHEMICAL_STREAM_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_form_verify.properties
${CHEMICAL_STREAM_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_stream_grid_verify.properties
# Chemical Stream's own form-field label set (Start Date/Chemical Stream Type/From Connection
# deliberately excluded from the live-DOM round-trip compare - Start Date lives only in
# objectdates, Chemical Stream Type is a dropdown and From Connection a popup pin, both of which
# can re-render different display text after reload, same caveat as every other converted
# screen's dropdown/popup fields).
@{CHEMICAL_STREAM_FORM_LABELS}    Chemical Stream Code    Chemical Stream Name
# From Connection popup internals (recon-verified 2026-07-30) - UNCHANGED by this conversion.
${CHS_POPUP_OBJTYPE}    CHEM_TANK
${CHS_POPUP_OBJTYPE_DD}    nav:form:G:4:R:1:C:0:dd
${CHS_POPUP_GRID}       manage_object_nav_nav:form:T_data


*** Keywords ***
Find Chemical Stream Row By Filter
    [Documentation]    Explicitly filter the Chemical Stream grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${TBL}    ${code}

Clear Chemical Stream Row Filter
    [Documentation]    Clear the Code column filter (see Find Chemical Stream Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${TBL}

Login To EC Application
    [Documentation]    Authenticate as Chemical Stream's OWN credentials
    ...    (${CHEMICAL_STREAM_EC_USER}/${CHEMICAL_STREAM_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab).
    Login To EC Screen    ${CHEMICAL_STREAM_EC_USER}    ${CHEMICAL_STREAM_EC_PASS}

Open Chemical Stream Screen With Navigator Values Populated
    [Documentation]    Navigate to the Chemical Stream screen, THEN fill + submit the mandatory
    ...    3-level Production Unit -> Area -> Facility Class 1 navigator cascade (dropdowns + GO)
    ...    - the grid AND the From Connection popup source are scoped by it, so this single
    ...    keyword bundles both steps for the test case (Area's exact skeleton calls this as ONE
    ...    line per TC, not two). Assumes the caller already logged in this test case (via Login
    ...    To EC Application). Navigator fill delegates to the shared T2 "Apply Navigator From
    ...    Properties" (resources/manage_object.resource), driven by
    ...    testdata/chemical_stream_navigator.properties, instead of inlining "Select EC Dropdown
    ...    Option + Apply Navigator" here.
    Open EC Screen    ${SCR}
    Apply Navigator From Properties    ${CHEMICAL_STREAM_NAVIGATOR_PROPERTIES}

Open From Connection Popup List
    [Documentation]    Open the stream_node_ref_popup behind ${pin_prefix} and drive it to the list
    ...    state: select Object Type = CHEM_TANK in the popup's inner dd, click the popup's inner GO,
    ...    wait for the popup grid (manage_object_nav_nav:form:T_data). The generic T1 popup keywords
    ...    do not fit this popup type: they wait for PopupList:form:T_data and drive no inner steps.
    ...    PRESERVED UNCHANGED by the Area-pattern conversion (owner instruction: this popup logic
    ...    is orthogonal to the outer navigator and must not be refactored).
    [Arguments]    ${pin_prefix}
    Evaluate JavaScript    ${None}    () => document.getElementById('${pin_prefix}B').click()
    Wait For Elements State    css=[id="popupIFrame"]    visible    timeout=15s
    Sleep    2s
    Click    css=[id="popupIFrame"] >>> css=[id="${CHS_POPUP_OBJTYPE_DD}_button"]
    Click    css=[id="popupIFrame"] >>> xpath=//*[@id='${CHS_POPUP_OBJTYPE_DD}_panel']//tr[normalize-space(@data-item-label)='${CHS_POPUP_OBJTYPE}']
    Sleep    1s
    Click    css=[id="popupIFrame"] >>> css=[id="button:form:B"]
    Wait For Elements State    css=[id="popupIFrame"] >>> css=[id="${CHS_POPUP_GRID}"]    visible    timeout=15s
    Sleep    1s

Pick From Connection Popup
    [Documentation]    Screen-LOCAL first-available picker: drive the popup to its list state
    ...    (Open From Connection Popup List), click the FIRST row, verify the popup closed and
    ...    the pin input took a value. PRESERVED UNCHANGED by the Area-pattern conversion.
    [Arguments]    ${pin_prefix}
    Open From Connection Popup List    ${pin_prefix}
    ${found}=    Evaluate JavaScript
    ...    css=[id="popupIFrame"] >>> css=[id="${CHS_POPUP_GRID}"]
    ...    (tbody) => { const tr = tbody.querySelector('tr'); const td = tr ? tr.querySelector('td') : null; if (td) { td.click(); return true; } return false; }
    Should Be True    ${found}    msg=From Connection popup has no rows (check the P1 navigator scope)
    Wait For Elements State    css=[id="popupIFrame"]    hidden    timeout=15s
    Sleep    1s
    ${val}=    Get Property    css=[id="${pin_prefix}"]    value
    Should Not Be Empty    ${val}    msg=From Connection pick did not fill the pin field

Insert Chemical Stream Record And Save
    [Documentation]    Friendly-narrative wrapper (Area-pattern shape, ZERO arguments) around a
    ...    properties-file-driven insert: fills every field named in
    ...    testdata/chemical_stream_insert.properties EXCEPT "From Connection" (auto-detected by
    ...    label/kind, same mechanism as the shared T2 Insert Object From Properties), then drives
    ...    the screen-local From Connection popup (Pick From Connection Popup, UNCHANGED) before
    ...    Save. Also owns the integrity check that the inserted Chemical Stream Code matches the
    ...    suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${CHEMICAL_STREAM_INSERT_PROPERTIES}
    ${data}=    Read Properties    ${properties_path}
    Open New Object Form
    FOR    ${label}    IN    @{data.keys()}
        IF    '${label}' != 'From Connection'
            Fill OV Field By Label Any Kind    objectForm    ${label}    ${data}[${label}]
        END
    END
    ${pin}=    Get Attribute
    ...    xpath=//span[contains(@class,'ECCell') and contains(@id,':objectForm:form:') and normalize-space(text())='From Connection']/ancestor::div[contains(@class,'tableCell')][1]/following-sibling::div[contains(@class,'tableCell')][1]//input[substring(@id, string-length(@id) - 3) = ':pin']
    ...    id
    Pick From Connection Popup    ${pin}
    Capture Step    ${TEST NAME}_action
    Save And Refresh List
    Should Be Equal    ${data}[Chemical Stream Code]    ${TEST_CODE}
    ...    msg=${properties_path} Chemical Stream Code does not match the expected ${TEST_CODE}
    RETURN    ${data}[Chemical Stream Code]

Verify Chemical Stream Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Chemical Stream Code/Chemical Stream Name's LIVE SCREEN value is compared to
    ...    testdata/chemical_stream_insert.properties. Filters via Find Chemical Stream Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Stream Row By Filter    ${code}
    Verify Object Insert Exists    ${TBL}    ${code}    Chemical Stream
    ...    ${CHEMICAL_STREAM_INSERT_PROPERTIES}    @{CHEMICAL_STREAM_FORM_LABELS}
    ...    code_label=Chemical Stream Code
    Clear Chemical Stream Row Filter

Update Chemical Stream Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Chemical Stream Name is listed in testdata/chemical_stream_update.properties -
    ...    Chemical Stream Code is read-only in updateAttributes. Filters via Find Chemical
    ...    Stream Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CHEMICAL_STREAM_UPDATE_PROPERTIES}
    Find Chemical Stream Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${TBL}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Chemical Stream Code
    Clear Chemical Stream Row Filter
    RETURN    ${data}

Verify Chemical Stream Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Chemical Stream Name's LIVE SCREEN value to
    ...    testdata/chemical_stream_update.properties. Filters via Find Chemical Stream Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Stream Row By Filter    ${code}
    Verify Object Form Record    ${TBL}    ${code}    Chemical Stream
    ...    ${CHEMICAL_STREAM_UPDATE_PROPERTIES}    Chemical Stream Name
    ...    code_label=Chemical Stream Code
    Clear Chemical Stream Row Filter

Find Chemical Stream Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find
    ...    Chemical Stream Row By Filter first. Deliberately does NOT clear the filter afterward -
    ...    Verify Chemical Stream Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Stream Row By Filter    ${code}
    Find Object Record    ${TBL}    ${code}    Chemical Stream    code_label=Chemical Stream Code

Verify Chemical Stream Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Chemical Stream Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${TBL}    ${code}    ${CHEMICAL_STREAM_GRID_VERIFY_PROPERTIES}
    ...    ${CHEMICAL_STREAM_FORM_VERIFY_PROPERTIES}    @{CHEMICAL_STREAM_FORM_LABELS}
    Clear Chemical Stream Row Filter

Delete Chemical Stream Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the object, set End Date = Start Date (EC true delete for OV_CHEM_STREAM),
    ...    Save. Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List
    ...    (inside T2) already re-applies the navigator, so the assertion reads a fresh list.
    ...    Filters via Find Chemical Stream Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Chemical Stream Row By Filter    ${code}
    Delete Object Via End Date    ${TBL}    ${DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Chemical Stream Row Filter

Verify Chemical Stream Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_CHEM_STREAM) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword (that
    ...    pattern was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${TBL}    OV_CHEM_STREAM    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Chemical Stream Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${TBL}    ${code}
