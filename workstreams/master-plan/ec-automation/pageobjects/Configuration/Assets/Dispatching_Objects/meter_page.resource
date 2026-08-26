*** Settings ***
Documentation       T3 (screen) — Meter page object.
...                 Screen: Configuration > Assets > Dispatching Objects > Meter (OV_METER).
...                 OV-GM (BU-gated) with TWO mandatory references on insert: Meter Type (dd)
...                 and Delivery Point Name (the GENERIC T1 "Pick From EC Object Popup",
...                 resources/popup.resource - NOT a screen-local popup like Chemical Stream's
...                 From Connection; Meter's popup is the plain pin/pinB object_popup covered by
...                 the shared "Pick OV Popup By Label" resolver in manage_object.resource).
...                 Converted to the full Area-pattern STRUCTURE (owner standing rule 2026-08-26:
...                 any EC screen with a navigator matching Area's layout MUST follow Area's FULL
...                 pattern). Meter's navigator was re-confirmed live (2026-08-26, corrects an
...                 earlier wrong "DOES NOT FIT" classification that conflated the insert form's
...                 Delivery Point POPUP with the navigator): the navigator itself is a single
...                 mandatory Business Unit dropdown at nav:form:G:0:R:1:C:1:dd - the SAME
...                 single-dropdown shape as Area's own Production Unit navigator. A second
...                 dropdown at nav:form:G:0:R:1:C:2:dd (labelled "Delivery Point", an optional
...                 grid filter) exists but is NOT mandatory - GO succeeds with only C:1 filled
...                 (live-confirmed). This conversion is structural only - the genuine BU
...                 navigator gesture and the genuine Delivery Point popup on the insert form are
...                 both kept exactly as they behave; the popup itself is entirely INSIDE the
...                 insert form, orthogonal to the outer navigator, same situation as Chemical
...                 Stream's own From Connection popup (which did not block that conversion).
...                 Field labels confirmed live (2026-08-26): objectForm/updateAttributes use
...                 SCREEN-PREFIXED "Meter Code"/"Meter Name" (like Area's "Area Code"/"Area
...                 Name"), NOT the generic "Code"/"Name" Bank/Object List use - every T2 call
...                 below passes code_label=Meter Code accordingly. DELETE = End Date = Start
...                 Date (true delete in OV_METER).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Resource            ../../../../resources/popup.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${METER_SCREEN}          Meter
${METER_TABLE}           manageObject:form:T_data
# navigator (OV-GM): Business Unit dropdown — MANDATORY before the grid loads. The fill itself
# now goes through the shared T2 "Apply Navigator From Properties" (resources/manage_object.
# resource), driven by testdata/meter_navigator.properties. ${METER_NAV_BU} is kept only as
# documentation of the DOM id (row 1, C:1) - the properties-driven fill resolves to the same
# id/value, not a different one.
${METER_NAV_BU}          nav:form:G:0:R:1:C:1:dd
${METER_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/meter_navigator.properties
${METER_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/meter_insert.properties
${METER_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/meter_update.properties
${METER_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/meter_form_verify.properties
${METER_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/meter_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented rationale as Area's/Bank's own ${..._DEL_ENDDATE}: this row
# packs Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# meter_page.resource ("Delete Meter" keyword, live 2026-06-13).
${METER_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Meter's own form-field label set (Start Date/Meter Type/Delivery Point Name deliberately
# excluded from the live-DOM round-trip compare - Start Date lives only in objectdates, Meter
# Type is a dropdown and Delivery Point Name a popup pin, both of which can re-render different
# display text after reload, same caveat as every other converted screen's dropdown/popup
# fields).
@{METER_FORM_LABELS}    Meter Code    Meter Name


*** Keywords ***
Find Meter Row By Filter
    [Documentation]    Explicitly filter the Meter grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching every other
    ...    Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${METER_TABLE}    ${code}

Clear Meter Row Filter
    [Documentation]    Clear the Code column filter (see Find Meter Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${METER_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Meter's OWN credentials (${METER_EC_USER}/${METER_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${METER_EC_USER}    ${METER_EC_PASS}

Open Meter Screen With Navigator Values Populated
    [Documentation]    Navigate to the Meter screen, THEN fill + submit the mandatory Business
    ...    Unit navigator (dropdown + GO) - the grid AND the Delivery Point popup's source list
    ...    are both scoped by it, so this single keyword bundles both steps for the test case
    ...    (Area's exact skeleton calls this as ONE line per TC, not two). Assumes the caller
    ...    already logged in this test case (via Login To EC Application). Navigator fill
    ...    delegates to the shared T2 "Apply Navigator From Properties" (resources/
    ...    manage_object.resource), driven by testdata/meter_navigator.properties, instead of
    ...    inlining "Select EC Dropdown Option + Apply Navigator" here.
    Open EC Screen    ${METER_SCREEN}
    Apply Navigator From Properties    ${METER_NAVIGATOR_PROPERTIES}

Insert Meter Record And Save
    [Documentation]    Friendly-narrative wrapper (Area-pattern shape, ZERO arguments) around a
    ...    properties-file-driven insert: fills every field named in
    ...    testdata/meter_insert.properties, in FILE ORDER, auto-detecting each field's kind by
    ...    label (the shared T2 "Insert Object From Properties" via "Fill OV Field By Label Any
    ...    Kind" - no screen-local popup special-casing needed, unlike Chemical Stream, because
    ...    Meter's Delivery Point Name is the GENERIC pin/pinB popup already covered by "Pick OV
    ...    Popup By Label"). The file's order (Start Date, Delivery Point Name, Meter Code,
    ...    Meter Name, Meter Type) preserves the load-bearing sequence proven live 2026-06-13:
    ...    the popup pick must happen BEFORE Code/Name/Type are filled, or its close callback
    ...    silently resets Save to a no-op. Also owns the integrity check that the inserted
    ...    Meter Code matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${METER_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Meter Code
    RETURN    ${code}

Verify Meter Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the
    ...    grid, then Meter Code/Meter Name's LIVE SCREEN value is compared to
    ...    testdata/meter_insert.properties. Filters via Find Meter Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Meter Row By Filter    ${code}
    Verify Object Insert Exists    ${METER_TABLE}    ${code}    Meter    ${METER_INSERT_PROPERTIES}
    ...    @{METER_FORM_LABELS}    code_label=Meter Code
    Clear Meter Row Filter

Update Meter Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Meter
    ...    Name is listed in testdata/meter_update.properties - Meter Code is read-only in
    ...    updateAttributes (confirmed live 2026-08-26). Filters via Find Meter Row By Filter
    ...    first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${METER_UPDATE_PROPERTIES}
    Find Meter Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${METER_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Meter Code
    Clear Meter Row Filter
    RETURN    ${data}

Verify Meter Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Meter Name's LIVE SCREEN value to
    ...    testdata/meter_update.properties. Filters via Find Meter Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Meter Row By Filter    ${code}
    Verify Object Form Record    ${METER_TABLE}    ${code}    Meter    ${METER_UPDATE_PROPERTIES}
    ...    Meter Name    code_label=Meter Code
    Clear Meter Row Filter

Find Meter Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Meter
    ...    Row By Filter first. Deliberately does NOT clear the filter afterward - Verify Meter
    ...    Record Found (called right after, same TC) needs the grid still filtered to ${code}
    ...    for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Meter Row By Filter    ${code}
    Find Object Record    ${METER_TABLE}    ${code}    Meter    code_label=Meter Code

Verify Meter Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Meter Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${METER_TABLE}    ${code}    ${METER_GRID_VERIFY_PROPERTIES}
    ...    ${METER_FORM_VERIFY_PROPERTIES}    @{METER_FORM_LABELS}
    Clear Meter Row Filter

Delete Meter Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the meter, set End Date = Start Date (EC true delete for OV_METER), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List
    ...    (inside T2) already re-applies the navigator, so the assertion reads a fresh list.
    ...    Filters via Find Meter Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Meter Row By Filter    ${code}
    Delete Object Via End Date    ${METER_TABLE}    ${METER_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Meter Row Filter

Verify Meter Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_METER) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword (that
    ...    pattern was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${METER_TABLE}    OV_METER    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Meter Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${METER_TABLE}    ${code}
