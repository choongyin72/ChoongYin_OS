*** Settings ***
Documentation       T3 (screen) — Service page object.
...                 Screen: Configuration > Assets > Service_Objects > Service.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Business Unit navigator dropdown is set + GO (Contract Area/
...                 Contract are further nav columns visible on the screen but are OPTIONAL
...                 filters - confirmed live, 2026-08-26: GO with only Business Unit set already
...                 loads the grid - see screens/.../Service/evidence/SV_02_inserted.png).
...                 Converted to the Area-pattern 5-TC/per-TC-login/pure-screen-verify STRUCTURE
...                 (2026-08-26), matching Area/External Location/Field/Facility Class 1's own
...                 conversions - Service remains OV-GM, this is a structural conversion, not a
...                 reclassification. Real labels confirmed live (pre-existing proven driver,
...                 shipped 2026-08-01, live 8/8): objectForm/updateAttributes use
...                 SCREEN-PREFIXED "Service Code"/"Service Name", NOT the generic "Code"/"Name"
...                 Bank/Object List use - every T2 call below passes code_label=Service Code
...                 accordingly.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${SERVICE_SCREEN}          Service
${SERVICE_TABLE}           manageObject:form:T_data
# navigator (groupmodel): Business Unit dropdown — MANDATORY before the grid loads.
# Value confirmed live (pre-existing proven driver, shipped 2026-08-01): "TS3 BU1" at row 1,
# column 1 (nav:form:G:0:R:1:C:1:dd).
# 2026-08-26: the fill itself now goes through the shared T2 "Apply Navigator From Properties"
# (resources/manage_object.resource), driven by testdata/service_navigator.properties.
# ${SERVICE_NAV_BU} and ${SERVICE_NAV_BU_VALUE} are kept only as documentation of the DOM id
# (row 1, C:1) and the required value - the properties-driven fill resolves to the same id/
# value, not a different one.
${SERVICE_NAV_BU}          nav:form:G:0:R:1:C:1:dd
${SERVICE_NAV_BU_VALUE}    TS3 BU1
${SERVICE_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/service_navigator.properties
${SERVICE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/service_insert.properties
${SERVICE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/service_update.properties
${SERVICE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/service_form_verify.properties
${SERVICE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/service_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented rationale as Area's/Bank's own del-enddate constants: this row
# packs Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape
# the one-field-per-row label scan cannot safely resolve. Value confirmed live via the
# pre-existing proven service_page.resource ${DEL_ENDDATE}.
${SERVICE_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Service's own form-field label set (Start Date/End Date deliberately excluded - they live only
# in objectdates, not updateAttributes/objectForm's fill-once trio; Service Template/Service
# Type/Service Status/Contract/Transport System deliberately excluded from round-trip comparison
# - they are filled via a resolved reference value or __FIRST__ which can re-render different
# display text after reload, same caveat as every other converted screen's dropdown fields).
@{SERVICE_FORM_LABELS}    Service Code    Service Name


*** Keywords ***
Find Service Row By Filter
    [Documentation]    Explicitly filter the Service grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${SERVICE_TABLE}    ${code}

Clear Service Row Filter
    [Documentation]    Clear the Code column filter (see Find Service Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${SERVICE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Service's OWN credentials (${SERVICE_EC_USER}/
    ...    ${SERVICE_EC_PASS} from credentials.py) on the current page - works whether this is
    ...    the very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application (same login form, not a
    ...    new page/tab).
    Login To EC Screen    ${SERVICE_EC_USER}    ${SERVICE_EC_PASS}

Open Service Screen With Navigator Values Populated
    [Documentation]    Navigate to the Service screen, THEN fill + submit the mandatory Business
    ...    Unit navigator (dropdown + GO) - Service's grid stays empty until this happens, so
    ...    this single keyword bundles both steps for the test case (matches Area's exact
    ...    skeleton: called as ONE line per TC, not two). Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - matches every other Area-pattern-
    ...    converted screen's "Open <Screen> Screen" convention. Navigator fill delegates to the
    ...    shared T2 "Apply Navigator From Properties" (resources/manage_object.resource),
    ...    driven by testdata/service_navigator.properties, instead of inlining "Select EC
    ...    Dropdown Option + Apply Navigator" here (which is what the OLD pre-conversion driver
    ...    did) - so this screen now reuses the SAME shared keyword every other converted OV-GM
    ...    screen calls with its own properties file.
    Open EC Screen    ${SERVICE_SCREEN}
    Apply Navigator From Properties    ${SERVICE_NAVIGATOR_PROPERTIES}

Insert Service Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, called with ZERO arguments so service_iud.robot's test case body reads
    ...    as a plain business step. Also owns the integrity check that the inserted Service
    ...    Code matches the suite's ${TEST_CODE}. ${SERVICE_INSERT_PROPERTIES}'s mandatory-field
    ...    set (Service Template/Service Type/Service Status/Contract/Transport System) is
    ...    EXACTLY what the pre-existing proven driver already filled.
    [Arguments]    ${properties_path}=${SERVICE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Service Code
    RETURN    ${code}

Verify Service Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the
    ...    grid, then Service Code/Service Name's LIVE SCREEN value is compared to
    ...    testdata/service_insert.properties. Filters via Find Service Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Service Row By Filter    ${code}
    Verify Object Insert Exists    ${SERVICE_TABLE}    ${code}    Service    ${SERVICE_INSERT_PROPERTIES}
    ...    @{SERVICE_FORM_LABELS}    code_label=Service Code
    Clear Service Row Filter

Update Service Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Service Name is listed in testdata/service_update.properties - Service Code is
    ...    read-only in updateAttributes. Filters via Find Service Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${SERVICE_UPDATE_PROPERTIES}
    Find Service Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${SERVICE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Service Code
    Clear Service Row Filter
    RETURN    ${data}

Verify Service Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Service Name's LIVE SCREEN value to
    ...    testdata/service_update.properties. Filters via Find Service Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Service Row By Filter    ${code}
    Verify Object Form Record    ${SERVICE_TABLE}    ${code}    Service    ${SERVICE_UPDATE_PROPERTIES}
    ...    Service Name    code_label=Service Code
    Clear Service Row Filter

Find Service Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find
    ...    Service Row By Filter first. Deliberately does NOT clear the filter afterward -
    ...    Verify Service Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Service Row By Filter    ${code}
    Find Object Record    ${SERVICE_TABLE}    ${code}    Service    code_label=Service Code

Verify Service Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Service Record before this) AND left the Code filter active -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${SERVICE_TABLE}    ${code}    ${SERVICE_GRID_VERIFY_PROPERTIES}
    ...    ${SERVICE_FORM_VERIFY_PROPERTIES}    @{SERVICE_FORM_LABELS}
    Clear Service Row Filter

Delete Service Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/
    ...    ${END_DATE}). Select the service, set End Date = Start Date (EC true delete for
    ...    OV_SERVICE), Save. Filters via Find Service Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Service Row By Filter    ${code}
    Delete Object Via End Date    ${SERVICE_TABLE}    ${SERVICE_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Service Row Filter

Verify Service Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_SERVICE) - the DB check lives here, in the
    ...    shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${SERVICE_TABLE}    OV_SERVICE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Service Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (grid-only check) - delegates to the shared T2 Verify Object Does Not
    ...    Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${SERVICE_TABLE}    ${code}
