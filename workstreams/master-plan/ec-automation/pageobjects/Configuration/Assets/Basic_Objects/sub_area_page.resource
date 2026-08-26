*** Settings ***
Documentation       T3 (screen) — Sub Area page object.
...                 Screen: Configuration > Assets > Basic Objects > Sub Area.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Production Unit -> Area navigator cascade (2-level, C:1/C:2 same
...                 row - confirmed live 2026-08-26, matches Facility Class 1's proven shape) is
...                 set + GO. Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify
...                 STRUCTURE (owner standing rule 2026-08-26: any EC screen with a navigator
...                 matching Area's layout MUST follow Area's FULL pattern) - Sub Area remains
...                 OV-GM, its genuine 2-level PU->Area cascade + GO is KEPT exactly as the prior
...                 build left it (Apply Navigator From Properties, EXPLICIT values from
...                 testdata/sub_area_navigator.properties: Op Production Unit=Production Unit,
...                 Op Area=Offshore area - user-approved 2026-06-11, unchanged). This is a
...                 STRUCTURAL conversion, not a reclassification of the screen as plain
...                 Bank-shaped.
...                 Real labels confirmed live (2026-08-26, objectForm label scan): objectForm/
...                 updateAttributes use SCREEN-PREFIXED "Sub Area Code"/"Sub Area Name" (like
...                 Area's "Area Code"/"Area Name"), NOT the generic "Code"/"Name" Bank/Object
...                 List use - every T2 call below passes code_label=Sub Area Code accordingly.
...                 Grid columns confirmed live (manageObject:form:T_head scan): Sub Area Code /
...                 Sub Area Name / Start Date / End Date - same 4-column shape as Area/Facility
...                 Class 1.
...                 objectForm exposes "Op Production Unit"/"Op Area" fields which the pre-existing
...                 driver (playwright/ec_iud_sub_area.py, sub_area_sow.md "insert sets Op PU +
...                 Op Area") ALREADY fills on insert (matching the navigator context) - unlike
...                 Facility Class 1 where they're proven to work blank, Sub Area's own proven
...                 driver fills them, so testdata/sub_area_insert.properties keeps that behavior
...                 unchanged rather than guessing a different requirement.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${SUB_AREA_SCREEN}          Sub Area
${SUB_AREA_TABLE}            manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area 2-level cascade — MANDATORY before the grid
# loads. The fill goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/sub_area_navigator.properties.
${SUB_AREA_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/sub_area_navigator.properties
${SUB_AREA_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/sub_area_insert.properties
${SUB_AREA_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/sub_area_update.properties
${SUB_AREA_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/sub_area_form_verify.properties
${SUB_AREA_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/sub_area_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Facility Class 1's own del-enddate constant: this row packs
# Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# Playwright driver (playwright/ec_iud_sub_area.py: del_end).
${SUB_AREA_DEL_ENDDATE}      tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Sub Area's own form-field label set (Start Date/End Date deliberately excluded - they live only
# in objectdates, not updateAttributes/objectForm's fill-once trio; Op Production Unit/Op Area
# deliberately excluded from round-trip comparison - filled via a resolved reference value which
# can re-render different display text after reload, same caveat as every other converted
# screen's dropdown fields).
@{SUB_AREA_FORM_LABELS}      Sub Area Code    Sub Area Name


*** Keywords ***
Find Sub Area Row By Filter
    [Documentation]    Explicitly filter the Sub Area grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching every
    ...    other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${SUB_AREA_TABLE}    ${code}

Clear Sub Area Row Filter
    [Documentation]    Clear the Code column filter (see Find Sub Area Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${SUB_AREA_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Sub Area's OWN credentials (${SUB_AREA_EC_USER}/
    ...    ${SUB_AREA_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application (same login form, not a
    ...    new page/tab).
    Login To EC Screen    ${SUB_AREA_EC_USER}    ${SUB_AREA_EC_PASS}

Open Sub Area Screen With Navigator Values Populated
    [Documentation]    Navigate to the Sub Area screen, THEN fill + submit the mandatory 2-level
    ...    Production Unit -> Area navigator (dropdowns + GO) - the grid stays empty until this
    ...    happens, so this single keyword bundles both steps for the test case (Area's exact
    ...    skeleton calls this as ONE line per TC, not two). Assumes the caller already logged in
    ...    this test case (via Login To EC Application). Navigator fill delegates to the shared
    ...    T2 "Apply Navigator From Properties" (resources/manage_object.resource), driven by
    ...    testdata/sub_area_navigator.properties.
    Open EC Screen    ${SUB_AREA_SCREEN}
    Apply Navigator From Properties    ${SUB_AREA_NAVIGATOR_PROPERTIES}

Insert Sub Area Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so sub_area_iud.robot's test case body reads as a
    ...    plain business step. Also owns the integrity check that the inserted Sub Area Code
    ...    matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${SUB_AREA_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Sub Area Code
    RETURN    ${code}

Verify Sub Area Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Sub Area Code/Sub Area Name's LIVE SCREEN value is compared to
    ...    testdata/sub_area_insert.properties. Filters via Find Sub Area Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Sub Area Row By Filter    ${code}
    Verify Object Insert Exists    ${SUB_AREA_TABLE}    ${code}    Sub Area
    ...    ${SUB_AREA_INSERT_PROPERTIES}    @{SUB_AREA_FORM_LABELS}    code_label=Sub Area Code
    Clear Sub Area Row Filter

Update Sub Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only Sub
    ...    Area Name is listed in testdata/sub_area_update.properties - Sub Area Code is read-only
    ...    in updateAttributes. Filters via Find Sub Area Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${SUB_AREA_UPDATE_PROPERTIES}
    Find Sub Area Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${SUB_AREA_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Sub Area Code
    Clear Sub Area Row Filter
    RETURN    ${data}

Verify Sub Area Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Sub Area Name's LIVE SCREEN value to
    ...    testdata/sub_area_update.properties. Filters via Find Sub Area Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Sub Area Row By Filter    ${code}
    Verify Object Form Record    ${SUB_AREA_TABLE}    ${code}    Sub Area
    ...    ${SUB_AREA_UPDATE_PROPERTIES}    Sub Area Name    code_label=Sub Area Code
    Clear Sub Area Row Filter

Find Sub Area Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Sub
    ...    Area Row By Filter first. Deliberately does NOT clear the filter afterward - Verify Sub
    ...    Area Record Found (called right after, same TC) needs the grid still filtered to
    ...    ${code} for its own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Sub Area Row By Filter    ${code}
    Find Object Record    ${SUB_AREA_TABLE}    ${code}    Sub Area    code_label=Sub Area Code

Verify Sub Area Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Sub Area Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${SUB_AREA_TABLE}    ${code}    ${SUB_AREA_GRID_VERIFY_PROPERTIES}
    ...    ${SUB_AREA_FORM_VERIFY_PROPERTIES}    @{SUB_AREA_FORM_LABELS}
    Clear Sub Area Row Filter

Delete Sub Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the sub area, set End Date = Start Date (EC true delete for OV_SUB_AREA), Save.
    ...    Versioned groupmodel grids redraw lazily after a delete - Save And Refresh List (inside
    ...    T2) already re-applies the navigator, so the assertion reads a fresh list. Filters via
    ...    Find Sub Area Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Sub Area Row By Filter    ${code}
    Delete Object Via End Date    ${SUB_AREA_TABLE}    ${SUB_AREA_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Sub Area Row Filter

Verify Sub Area Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_SUB_AREA) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${SUB_AREA_TABLE}    OV_SUB_AREA    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Sub Area Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${SUB_AREA_TABLE}    ${code}
