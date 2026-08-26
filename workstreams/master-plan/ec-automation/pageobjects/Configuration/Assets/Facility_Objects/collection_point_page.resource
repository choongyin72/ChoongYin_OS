*** Settings ***
Documentation       T3 (screen) — Collection Point page object.
...                 Screen: Configuration > Assets > Facility_Objects > Collection Point.
...                 OV-GM (groupmodel manage-object) screen: the grid loads ONLY after the
...                 mandatory Production Unit -> Area -> Operator Route navigator cascade
...                 (3-level, C:1/C:2/C:3 same row, C:4 absent - confirmed live 2026-08-26,
...                 tmp/recon_cp_navigator_cascade.py) is set + GO. Converted to the Area-pattern
...                 5-TC/per-TC-login/pure-screen-verify STRUCTURE (owner standing rule: any EC
...                 screen with a navigator matching Area's layout MUST follow Area's FULL
...                 pattern) - Collection Point remains OV-GM, its genuine 3-level PU->Area->
...                 Operator Route cascade + GO is KEPT exactly as the prior bespoke driver used
...                 it (now delegated to the shared T2 "Apply Navigator From Properties",
...                 EXPLICIT values from testdata/collection_point_navigator.properties: Op
...                 Production Unit=P3 Production Unit, Op Area=P3 Area, Op Operator Route=Oper
...                 Route 1). This is a STRUCTURAL conversion, not a reclassification of the
...                 screen as plain Bank-shaped.
...                 Real labels confirmed live (2026-08-26, matches the pre-existing driver's own
...                 field labels): objectForm/updateAttributes use SCREEN-PREFIXED "Collection
...                 Point Code"/"Collection Point Name" (like Area's "Area Code"/"Area Name"), NOT
...                 the generic "Code"/"Name" Bank/Object List use - every T2 call below passes
...                 code_label=Collection Point Code accordingly. Grid columns confirmed live
...                 (manageObject:form:T_head scan, 2026-08-26): Collection Point Code / Collection
...                 Point Name / Start Date / End Date - same 4-column shape as Area/Facility
...                 Class 1.
...                 3-LEVEL CASCADE TIMING: confirmed live 2026-08-26 that the shared keyword's
...                 flat 0.7s sleep between levels is SUFFICIENT for this screen's redraw timing
...                 at both the PU->Area and Area->Operator Route transitions - no shared-file
...                 change needed, no per-screen extra Sleep added.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CP_SCREEN}            Collection Point
${CP_TABLE}              manageObject:form:T_data
# navigator (groupmodel): Production Unit -> Area -> Operator Route 3-level SAME-ROW cascade —
# MANDATORY before the grid loads. The fill goes through the shared T2 "Apply Navigator From
# Properties" (resources/manage_object.resource), driven by
# testdata/collection_point_navigator.properties.
${CP_NAVIGATOR_PROPERTIES}    ${CURDIR}/../../../../testdata/collection_point_navigator.properties
${CP_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/collection_point_insert.properties
${CP_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/collection_point_update.properties
${CP_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/collection_point_form_verify.properties
${CP_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/collection_point_grid_verify.properties
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented rationale as Area's/Facility Class 1's own del-enddate constant: this row packs
# Start Date (C:1) and End Date (C:3) together with the End Date label at C:2, a shape the
# one-field-per-row label scan cannot safely resolve. Value confirmed live via the pre-existing
# bespoke driver's own ${DEL_ENDDATE} constant (unchanged by this conversion).
${CP_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Collection Point's own form-field label set (Start Date/End Date deliberately excluded - they
# live only in objectdates, not updateAttributes/objectForm's fill-once trio).
@{CP_FORM_LABELS}       Collection Point Code    Collection Point Name


*** Keywords ***
Find Collection Point Row By Filter
    [Documentation]    Explicitly filter the Collection Point grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    every other Area-pattern-converted screen's explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CP_TABLE}    ${code}

Clear Collection Point Row Filter
    [Documentation]    Clear the Code column filter (see Find Collection Point Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${CP_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Collection Point's OWN credentials
    ...    (${COLLECTION_POINT_EC_USER}/${COLLECTION_POINT_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab).
    Login To EC Screen    ${COLLECTION_POINT_EC_USER}    ${COLLECTION_POINT_EC_PASS}

Open Collection Point Screen With Navigator Values Populated
    [Documentation]    Navigate to the Collection Point screen, THEN fill + submit the mandatory
    ...    3-level Production Unit -> Area -> Operator Route navigator (dropdowns + GO) - the grid
    ...    stays empty until this happens, so this single keyword bundles both steps for the test
    ...    case (Area's exact skeleton calls this as ONE line per TC, not two). Assumes the caller
    ...    already logged in this test case (via Login To EC Application). Navigator fill
    ...    delegates to the shared T2 "Apply Navigator From Properties"
    ...    (resources/manage_object.resource), driven by
    ...    testdata/collection_point_navigator.properties, instead of inlining
    ...    "Select EC Dropdown Option + Apply Navigator" three times here.
    Open EC Screen    ${CP_SCREEN}
    Apply Navigator From Properties    ${CP_NAVIGATOR_PROPERTIES}

Insert Collection Point Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And Verify
    ...    Code, called with ZERO arguments so collection_point_iud.robot's test case body reads
    ...    as a plain business step. Also owns the integrity check that the inserted Collection
    ...    Point Code matches the suite's ${TEST_CODE}.
    [Arguments]    ${properties_path}=${CP_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Collection Point Code
    RETURN    ${code}

Verify Collection Point Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification (no
    ...    DB check here - that's TC02's own separate DbVerify assertion): row exists in the grid,
    ...    then Collection Point Code/Collection Point Name's LIVE SCREEN value is compared to
    ...    testdata/collection_point_insert.properties. Filters via Find Collection Point Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Collection Point Row By Filter    ${code}
    Verify Object Insert Exists    ${CP_TABLE}    ${code}    Collection Point
    ...    ${CP_INSERT_PROPERTIES}    @{CP_FORM_LABELS}    code_label=Collection Point Code
    Clear Collection Point Row Filter

Update Collection Point Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Only
    ...    Collection Point Name is listed in testdata/collection_point_update.properties -
    ...    Collection Point Code is read-only in updateAttributes. Filters via Find Collection
    ...    Point Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CP_UPDATE_PROPERTIES}
    Find Collection Point Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CP_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Collection Point Code
    Clear Collection Point Row Filter
    RETURN    ${data}

Verify Collection Point Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row, compares Collection Point Name's LIVE SCREEN value to
    ...    testdata/collection_point_update.properties. Filters via Find Collection Point Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Collection Point Row By Filter    ${code}
    Verify Object Form Record    ${CP_TABLE}    ${code}    Collection Point
    ...    ${CP_UPDATE_PROPERTIES}    Collection Point Name    code_label=Collection Point Code
    Clear Collection Point Row Filter

Find Collection Point Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find
    ...    Collection Point Row By Filter first. Deliberately does NOT clear the filter afterward -
    ...    Verify Collection Point Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Collection Point Row By Filter    ${code}
    Find Object Record    ${CP_TABLE}    ${code}    Collection Point    code_label=Collection Point Code

Verify Collection Point Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Collection Point Record before this) AND left the Code filter
    ...    active - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CP_TABLE}    ${code}    ${CP_GRID_VERIFY_PROPERTIES}
    ...    ${CP_FORM_VERIFY_PROPERTIES}    @{CP_FORM_LABELS}
    Clear Collection Point Row Filter

Delete Collection Point Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the object, set End Date = Start Date (EC true delete for
    ...    OV_COLLECTION_POINT), Save. Versioned groupmodel grids redraw lazily after a delete -
    ...    Save And Refresh List (inside T2) already re-applies the navigator, so the assertion
    ...    reads a fresh list. Filters via Find Collection Point Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Collection Point Row By Filter    ${code}
    Delete Object Via End Date    ${CP_TABLE}    ${CP_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Collection Point Row Filter

Verify Collection Point Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_COLLECTION_POINT) - the DB check lives here, in
    ...    the shared T2 Verify Object Removed, NOT as a separate screen-local wrapper keyword
    ...    (that pattern was removed by this conversion - see Documentation above).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CP_TABLE}    OV_COLLECTION_POINT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Collection Point Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification
    ...    (grid-only check) - delegates to the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CP_TABLE}    ${code}
