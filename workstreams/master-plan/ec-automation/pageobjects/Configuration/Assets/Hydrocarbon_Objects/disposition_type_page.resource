*** Settings ***
Documentation       T3 (screen) — Disposition Type page object.
...                 Screen: Configuration > Assets > Hydrocarbon Objects > Disposition Type (CO.0208).
...                 Manage-Object (OV) screen. Holds Disposition Type's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common). Plain OV (no
...                 mandatory dropdowns) - grid needs GO to populate (no default rows on open),
...                 unlike Bank which auto-loads (see ec-ui-knowledge/screens/disposition_type.md).
...                 Converted to the full Bank-pattern shape (2026-08-24): was previously an OLD
...                 hardcoded-field-id build (Fill EC Field with raw R:n:C:n ids, unique
...                 AUTOTEST_DISP_<timestamp> code, one shared Suite Setup login, inline DB-verify
...                 calls in the test file, 4 TCs / no Find). Now matches bank_page.resource/
...                 berth_page.resource exactly: properties-file-driven insert/update/verify,
...                 explicit grid-filter wiring, fixed test code, per-TC Login/Logout, 5 TCs,
...                 PURE SCREEN verification (no inline DB-verify in the T3/test file).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${DISP_SCREEN}          Disposition Type
${DISP_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/disposition_type_insert.properties
${DISP_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/disposition_type_update.properties
${DISP_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/disposition_type_form_verify.properties
${DISP_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/disposition_type_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${DISP_TABLE}           ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT label-driven
# — same documented precedent as Bank's own BANK_DEL_ENDDATE (the objectdates row packs TWO fields,
# Start Date C:1 / End Date C:3, a shape the one-field-per-row label scan cannot safely resolve).
${DISP_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Disposition Type's own form-field label set (Start Date deliberately excluded - it lives only in
# objectForm/objectdates, not updateAttributes - confirmed by ec-ui-knowledge/screens/
# disposition_type.md's Update tab layout: R2 Disposition Code (read-only) / R3 Disposition Name /
# R5 Description). Labels are screen-prefixed ("Disposition Code"/"Disposition Name"), NOT the
# generic "Code"/"Name" Bank uses. Defined ONCE here so both Verify Disposition Type Record Exists
# (TC02) and Verify Disposition Type Record Found (TC04) share the same list.
@{DISP_FORM_LABELS}    Disposition Code    Disposition Name    Description


*** Keywords ***
Find Disposition Type Row By Filter
    [Documentation]    Explicitly filter the Disposition Type grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank's/Account's own explicit filter usage, rather than relying only on Select Object
    ...    Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${DISP_TABLE}    ${code}

Clear Disposition Type Row Filter
    [Documentation]    Clear the Code column filter (see Find Disposition Type Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${DISP_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Disposition Type's OWN credentials
    ...    (${DISPOSITION_TYPE_EC_USER}/${DISPOSITION_TYPE_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application (same login form, not a new page/tab). Screen-specific wrapper (matches
    ...    Bank's convention: disposition_type_iud.robot's test cases call this with ZERO
    ...    arguments) that supplies Disposition Type's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${DISPOSITION_TYPE_EC_USER}    ${DISPOSITION_TYPE_EC_PASS}

Open Disposition Type Screen
    [Documentation]    Navigate to the Disposition Type screen, then click GO to populate the
    ...    grid (this screen has NO default rows on open, unlike Bank). Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY navigates,
    ...    matching Bank's per-TC Login/Open/action/Logout convention.
    Open EC Screen    ${DISP_SCREEN}
    Apply Navigator

Insert Disposition Type Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Disposition Type From Properties,
    ...    purely so disposition_type_iud.robot's test case body reads as a plain business step
    ...    with ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE}. The TC02 evidence screenshot is captured BEFORE Save is clicked (passed
    ...    through to Insert Object From Properties, which fills every field first).
    [Arguments]    ${properties_path}=${DISP_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Disposition Code
    RETURN    ${code}

Verify Disposition Type Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/disposition_type_insert.properties (the file used to
    ...    insert, not the post-update disposition_type_form_verify.properties) - Disposition
    ...    Code, Disposition Name, Description (${DISP_FORM_LABELS}). NOTE: Start Date is NOT
    ...    verified here - it only exists as a grid column / objectForm-objectdates field, not an
    ...    updateAttributes field (matches Bank's own convention). Delegates the full sequence
    ...    (row-check, select, form-compare, screenshot) to the shared T2 Verify Object Insert
    ...    Exists. Filters via Find Disposition Type Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Disposition Type Row By Filter    ${code}
    Verify Object Insert Exists    ${DISP_TABLE}    ${code}    Disposition Type
    ...    ${DISP_INSERT_PROPERTIES}    @{DISP_FORM_LABELS}    code_label=Disposition Code
    Clear Disposition Type Row Filter

Update Disposition Type Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the
    ...    applied {label: value} dict so the caller can DB-verify against exactly what was set.
    ...    The TC03 evidence screenshot is captured BEFORE Save is clicked (passed through to
    ...    Update Object From Properties, which fills every field first). Filters via Find
    ...    Disposition Type Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${DISP_UPDATE_PROPERTIES}
    Find Disposition Type Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${DISP_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Disposition Code
    Clear Disposition Type Row Filter
    RETURN    ${data}

Verify Disposition Type Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares Disposition Name/
    ...    Description's LIVE SCREEN value (via Get OV Field Value By Label) to testdata/
    ...    disposition_type_update.properties - only those two labels, since that's the only
    ...    fields that file has. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Disposition Type Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Disposition Type Row By Filter    ${code}
    Verify Object Form Record    ${DISP_TABLE}    ${code}    Disposition Type
    ...    ${DISP_UPDATE_PROPERTIES}    Disposition Name    Description    code_label=Disposition Code
    Clear Disposition Type Row Filter

Find Disposition Type Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates the full
    ...    select+capture sequence. Calls Find Disposition Type Row By Filter first. Deliberately
    ...    does NOT clear the filter afterward - Verify Disposition Type Record Found (called
    ...    right after, same TC) needs the grid still filtered to ${code} for its own grid-check,
    ...    since it doesn't re-select the row itself; it clears the filter once both checks are
    ...    done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Disposition Type Row By Filter    ${code}
    Find Object Record    ${DISP_TABLE}    ${code}    Disposition Type    code_label=Disposition Code

Verify Disposition Type Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to the
    ...    shared T2 Verify Object Found. Caller must already have selected the row (TC04 does,
    ...    via Find Disposition Type Record before this) AND left the Code filter active from that
    ...    same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${DISP_TABLE}    ${code}    ${DISP_GRID_VERIFY_PROPERTIES}
    ...    ${DISP_FORM_VERIFY_PROPERTIES}    @{DISP_FORM_LABELS}
    Clear Disposition Type Row Filter

Delete Disposition Type Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the disposition type, set End Date = Start Date (true delete), Save. Captures
    ...    the TC05 evidence screenshot right after the End Date is filled but BEFORE Save is
    ...    clicked - showing the data as entered, not the after-save/reloaded-grid state. Filters
    ...    via Find Disposition Type Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Disposition Type Row By Filter    ${code}
    Delete Object Via End Date    ${DISP_TABLE}    ${DISP_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Disposition Type Row Filter

Verify Disposition Type Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database - the SAME two existing DB-ground-truth keywords,
    ...    just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${DISP_TABLE}    OV_DISPOSITION_TYPE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Disposition Type Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${DISP_TABLE}    ${code}
