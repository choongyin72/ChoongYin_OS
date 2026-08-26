*** Settings ***
Documentation       T3 (screen) — Tank page object.
...                 Screen: Configuration > Assets > Tank and Storage Objects > Tank
...                 (confirmed live 2026-08-26: treeview expand of Configuration > Assets >
...                 "Tank and Storage Objects" lists Tank/Storage/Manage Tank/Maintain Tanks
...                 etc. as siblings). OV-GM (groupmodel manage-object) screen: the grid loads
...                 ONLY after the mandatory 3-level Production Unit -> Area -> Facility
...                 Class 1 navigator cascade + GO (same shape as Well - see well_page.resource
...                 "Apply Well Navigator"). A 4th navigator column (Date, at C:0, to the LEFT
...                 of the cascade) exists but has a working default and is NOT filled by this
...                 build - confirmed live: leaving it untouched and filling only the C:1..C:3
...                 cascade via GO successfully loads the grid.
...                 Built from scratch as a lean RF-only Area-pattern suite (2026-08-26) per
...                 the ec-area-pattern-new-screen skill - 5-TC/per-TC-login/pure-screen-verify
...                 structure, properties-file-driven, T2-consolidated, matching
...                 area_page.resource exactly. Real labels confirmed live (2026-08-26):
...                 objectForm/updateAttributes use SCREEN-PREFIXED "Tank Code"/"Tank Name"
...                 (like Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name" -
...                 every T2 call below passes code_label=Tank Code accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${TANK_SCREEN}          Tank
${TANK_TABLE}           manageObject:form:T_data
# navigator (groupmodel): 3-level Production Unit -> Area -> Facility Class 1 cascade, filled
# via the shared T2 "Apply Navigator From Properties" (resources/manage_object.resource),
# driven by testdata/tank_navigator.properties. Values confirmed live/selectable 2026-08-26
# (same P1 taxonomy as Well's own navigator).
${TANK_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/tank_navigator.properties
${TANK_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/tank_insert.properties
${TANK_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/tank_update.properties
${TANK_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/tank_form_verify.properties
${TANK_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/tank_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's ${AREA_DEL_ENDDATE}. Value confirmed live 2026-08-26 via a
# self-cleaning probe insert/update/delete (AUTOTEST_TANK_RECON, never AUTOTEST_TANK itself).
${TANK_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Tank's own form-field label set (Start Date/End Date deliberately excluded - they live only
# in objectdates, not updateAttributes/objectForm's fill-once trio; Op Production Unit/Op Area/
# Op Facility Class 1 deliberately excluded from round-trip comparison - they're filled via a
# resolved reference value which can re-render different display text after reload, same
# caveat as every other converted screen's dropdown fields; Tank Meter Freq./Use in BF
# deliberately excluded too - filled via __FIRST__, so the resolved display text is not a
# fixed expected value to compare against).
@{TANK_FORM_LABELS}    Tank Code    Tank Name


*** Keywords ***
Find Tank Row By Filter
    [Documentation]    Explicitly filter the Tank grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource), matching every other
    ...    Bank-pattern-converted/Area-pattern screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${TANK_TABLE}    ${code}

Clear Tank Row Filter
    [Documentation]    Clear the Code column filter (see Find Tank Row By Filter) via the shared
    ...    T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${TANK_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Tank's OWN credentials (${TANK_EC_USER}/${TANK_EC_PASS}
    ...    from credentials.py) on the current page - works whether this is the very first login
    ...    (page freshly loaded on the login form via the shared T1 Open EC Application) or a
    ...    re-login after Logout From EC Application (same login form, not a new page/tab).
    Login To EC Screen    ${TANK_EC_USER}    ${TANK_EC_PASS}

Open Tank Screen With Navigator Values Populated
    [Documentation]    Navigate to the Tank screen, THEN fill + submit the mandatory
    ...    Production Unit -> Area -> Facility Class 1 navigator cascade (dropdowns + GO) -
    ...    Tank's grid stays empty until this happens, so this single keyword bundles both
    ...    steps for the test case (owner's exact skeleton calls this as ONE line per TC, not
    ...    two). Assumes the caller already logged in this test case (via Login To EC
    ...    Application) - matches every other Area-pattern screen's "Open <Screen> Screen"
    ...    convention. Navigator fill delegates to the shared T2 "Apply Navigator From
    ...    Properties" (resources/manage_object.resource), driven by
    ...    testdata/tank_navigator.properties - reuses the SAME shared keyword Area/Well use,
    ...    not a bespoke inline "Select EC Dropdown Option + Apply Navigator" call.
    Open EC Screen    ${TANK_SCREEN}
    Apply Navigator From Properties    ${TANK_NAVIGATOR_PROPERTIES}

Insert Tank Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, called with ZERO arguments so tank_iud.robot's test case body reads as
    ...    a plain business step. Also owns the integrity check that the inserted Tank Code
    ...    matches the suite's ${TEST_CODE}. ${TANK_INSERT_PROPERTIES}'s Op Production
    ...    Unit/Op Area/Op Facility Class 1 values MUST equal the navigator's own P1
    ...    Production Unit/P1 Area/P1 Facility 1 scope or the new row is not visible under
    ...    this navigator scope (OV-GM constraint, confirmed live via a probe insert).
    [Arguments]    ${properties_path}=${TANK_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Tank Code
    RETURN    ${code}

Verify Tank Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Tank Code/Tank Name's LIVE SCREEN value is compared to testdata/tank_insert.properties.
    ...    Filters via Find Tank Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Tank Row By Filter    ${code}
    Verify Object Insert Exists    ${TANK_TABLE}    ${code}    Tank    ${TANK_INSERT_PROPERTIES}
    ...    @{TANK_FORM_LABELS}    code_label=Tank Code
    Clear Tank Row Filter

Update Tank Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Tank
    ...    Name is listed in testdata/tank_update.properties - Tank Code is read-only in
    ...    updateAttributes and Start Date lives only in objectdates. Filters via Find Tank Row
    ...    By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${TANK_UPDATE_PROPERTIES}
    Find Tank Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${TANK_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Tank Code
    Clear Tank Row Filter
    RETURN    ${data}

Verify Tank Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Tank Name's LIVE SCREEN value to testdata/tank_update.properties.
    ...    Filters via Find Tank Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Tank Row By Filter    ${code}
    Verify Object Form Record    ${TANK_TABLE}    ${code}    Tank    ${TANK_UPDATE_PROPERTIES}
    ...    Tank Name    code_label=Tank Code
    Clear Tank Row Filter

Find Tank Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Tank Row
    ...    By Filter first. Deliberately does NOT clear the filter afterward - Verify Tank Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for its
    ...    own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Tank Row By Filter    ${code}
    Find Object Record    ${TANK_TABLE}    ${code}    Tank    code_label=Tank Code

Verify Tank Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Tank Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${TANK_TABLE}    ${code}    ${TANK_GRID_VERIFY_PROPERTIES}
    ...    ${TANK_FORM_VERIFY_PROPERTIES}    @{TANK_FORM_LABELS}
    Clear Tank Row Filter

Delete Tank Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the tank, set End Date = Start Date (EC true delete for OV_TANK), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Tank Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Tank Row By Filter    ${code}
    Delete Object Via End Date    ${TANK_TABLE}    ${TANK_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Tank Row Filter

Verify Tank Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid AND the database (OV_TANK) - the DB check lives here, in the shared
    ...    T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${TANK_TABLE}    OV_TANK    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Tank Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${TANK_TABLE}    ${code}
