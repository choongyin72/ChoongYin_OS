*** Settings ***
Documentation       T3 (screen) — County page object.
...                 Screen: Configuration > Assets > Basic Objects > County.
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in
...                 OV_COUNTY). Converted 2026-08-23 from the old hardcoded-field-id pattern to
...                 the label-driven, properties-file-driven, T2-consolidated Bank pattern (see
...                 pageobjects/.../Financial_Objects/bank_page.resource for the reference shape).
...                 County Code/County Name are SCREEN-PREFIXED labels (confirmed live, not the
...                 generic "Code"/"Name" - same shape as State), so ${code_label}=County Code is
...                 threaded through every T2 call that accepts it.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${COUNTY_SCREEN}            County
${COUNTY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/county_insert.properties
${COUNTY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/county_update.properties
${COUNTY_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/county_form_verify.properties
${COUNTY_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/county_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string.
${COUNTY_TABLE}         ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven -
# same documented shape as Bank/the old county_page.resource (objectdates packs Start Date C:1 and
# End Date label C:2/input C:3 in ONE row) - live-confirmed 2026-08-23 (county_recon3.robot: a
# probe insert+delete round-trip against this exact id succeeded, row disappeared from the grid).
${COUNTY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# County's own form-field label set (Start Date deliberately excluded - live-confirmed 2026-08-23
# that updateAttributes has no date fields at all; Start Date lives only in objectForm (Insert) and
# objectdates (Delete)). Code label is screen-prefixed "County Code", not generic "Code".
@{COUNTY_FORM_LABELS}    County Code    County Name    Description


*** Keywords ***
Find County Row By Filter
    [Documentation]    Explicitly filter the County grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource) - matches Bank's/
    ...    Account's own explicit filter usage (owner, 2026-08-22: "others... should follow
    ...    Account... utilise same filter feature"), included from day one for this screen
    ...    (2026-08-23 batch-2 conversion, not deferred to a follow-up pass).
    [Arguments]    ${code}
    Find Object Row By Filter    ${COUNTY_TABLE}    ${code}

Clear County Row Filter
    [Documentation]    Clear the Code column filter (see Find County Row By Filter) via the shared
    ...    T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${COUNTY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as County's OWN credentials (${COUNTY_EC_USER}/
    ...    ${COUNTY_EC_PASS} from credentials.py) on the current page - works whether this is the
    ...    very first login (page freshly loaded on the login form via the shared T1 Open EC
    ...    Application) or a re-login after Logout From EC Application. Screen-specific wrapper
    ...    (county_iud.robot's test cases call this with ZERO arguments) that supplies County's own
    ...    credential defaults to the shared T1 Login To EC Screen (common.resource), which owns
    ...    the actual login mechanics.
    Login To EC Screen    ${COUNTY_EC_USER}    ${COUNTY_EC_PASS}

Open County Screen
    [Documentation]    Navigate to the County screen. Assumes the caller already logged in this
    ...    test case (via Login To EC Application) - this keyword ONLY navigates. Delegates to the
    ...    shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${COUNTY_SCREEN}

Insert County Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, so
    ...    county_iud.robot's test case body reads as a plain business step with ZERO arguments -
    ...    the underlying mechanics (properties-file-driven insert) are UNCHANGED. Also owns the
    ...    integrity check that the inserted Code matches the suite's ${TEST_CODE}. The TC02
    ...    evidence screenshot is captured BEFORE Save is clicked, passed through to Insert Object
    ...    From Properties, which fills every field first. ${code_label}=County Code (screen's own
    ...    label, not the generic "Code").
    [Arguments]    ${properties_path}=${COUNTY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=County Code
    RETURN    ${code}

Verify County Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/county_insert.properties - County Code, County Name,
    ...    Description (${COUNTY_FORM_LABELS}). Start Date is NOT verified here - it only exists as
    ...    a grid column/objectForm field, not an updateAttributes form field (live-confirmed).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the shared
    ...    T2 Verify Object Insert Exists. Filters via Find County Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}
    Find County Row By Filter    ${code}
    Verify Object Insert Exists    ${COUNTY_TABLE}    ${code}    County    ${COUNTY_INSERT_PROPERTIES}
    ...    @{COUNTY_FORM_LABELS}    code_label=County Code
    Clear County Row Filter

Update County Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the applied
    ...    {label: value} dict so the caller can DB-verify against exactly what was set. The TC03
    ...    evidence screenshot is captured BEFORE Save is clicked. Filters via Find County Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${COUNTY_UPDATE_PROPERTIES}
    Find County Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${COUNTY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=County Code
    Clear County Row Filter
    RETURN    ${data}

Verify County Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares County Name/Description's LIVE
    ...    SCREEN value to testdata/county_update.properties - only those two labels, since that's
    ...    the only fields that file has. Delegates the full sequence to the shared T2 Verify
    ...    Object Form Record. Filters via Find County Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find County Row By Filter    ${code}
    Verify Object Form Record    ${COUNTY_TABLE}    ${code}    County    ${COUNTY_UPDATE_PROPERTIES}
    ...    County Name    Description    code_label=County Code
    Clear County Row Filter

Find County Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find County Row By Filter first. Deliberately does NOT
    ...    clear the filter afterward - Verify County Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check; it clears the filter
    ...    once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find County Row By Filter    ${code}
    Find Object Record    ${COUNTY_TABLE}    ${code}    County    code_label=County Code

Verify County Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND the
    ...    full form record match the expected data. Also captures the TC04 evidence screenshot.
    ...    Delegates the full sequence to the shared T2 Verify Object Found. Caller must already
    ...    have selected the row (TC04 does, via Find County Record before this) AND left the Code
    ...    filter active from that same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${COUNTY_TABLE}    ${code}    ${COUNTY_GRID_VERIFY_PROPERTIES}
    ...    ${COUNTY_FORM_VERIFY_PROPERTIES}    @{COUNTY_FORM_LABELS}
    Clear County Row Filter

Delete County Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the county, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked.
    ...    Filters via Find County Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find County Row By Filter    ${code}
    Delete Object Via End Date    ${COUNTY_TABLE}    ${COUNTY_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear County Row Filter

Verify County Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_COUNTY).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${COUNTY_TABLE}    ov_county    ${code}
    Capture Step    ${TEST NAME}_verify

Verify County Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${COUNTY_TABLE}    ${code}
