*** Settings ***
Documentation       T3 (screen) — Functional Area page object.
...                 Screen: Configuration > Assets > Basic Objects > Functional Area.
...                 Manage-Object (OV) screen. Holds Functional Area's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-22 to mirror Bank/Object List/State/Region exactly
...                 (owner: "reflect the current EC screen exactly the same way as the
...                 OV_BANK IUD related task") - replaces the older hardcoded-field-id
...                 pattern with the label-driven, properties-file-driven,
...                 T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${FUNCTIONAL_AREA_SCREEN}    Functional Area
${FUNCTIONAL_AREA_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/functional_area_insert.properties
${FUNCTIONAL_AREA_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/functional_area_update.properties
${FUNCTIONAL_AREA_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/functional_area_form_verify.properties
${FUNCTIONAL_AREA_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/functional_area_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${FUNCTIONAL_AREA_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Object List/State/Region's convention.
${FUNCTIONAL_AREA_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Functional Area's own form-field label set. Labels are "Area Code"/"Area Name" - NOT
# "Functional Area Code"/"Functional Area Name" (the screen name does not match the field
# prefix) - confirmed live 2026-08-22 via RF recon (tmp/recon_fa_labels.robot) BEFORE
# building, same discipline as Region. "Start date" is also lowercase-'d' on this screen
# (case-sensitive live label), unlike Bank/State/Region's "Start Date" - noted here since it
# affects functional_area_insert.properties' key, not this label list (Start date is
# Insert-only, excluded from updateAttributes same as every other screen). Defined ONCE here
# so both Verify Functional Area Record Exists (TC02) and Verify Functional Area Record
# Found (TC04) share the same list.
@{FUNCTIONAL_AREA_FORM_LABELS}    Area Code    Area Name


*** Keywords ***
Find Functional Area Row By Filter
    [Documentation]    Explicitly filter the Functional Area grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Account/Bank/State/Object List's explicit filter usage (owner, 2026-08-22: "same to
    ...    other ec screens"), rather than relying only on Select Object Row's implicit
    ...    3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${FUNCTIONAL_AREA_TABLE}    ${code}

Clear Functional Area Row Filter
    [Documentation]    Clear the Code column filter (see Find Functional Area Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${FUNCTIONAL_AREA_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Functional Area's OWN credentials
    ...    (${FUNCTIONAL_AREA_EC_USER}/${FUNCTIONAL_AREA_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so functional_area_iud.robot's
    ...    test cases read as a plain business step; supplies Functional Area's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${FUNCTIONAL_AREA_EC_USER}    ${FUNCTIONAL_AREA_EC_PASS}

Open Functional Area Screen
    [Documentation]    Navigate to the Functional Area screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${FUNCTIONAL_AREA_SCREEN}

Insert Functional Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so functional_area_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Object List/State/Region. ${code_label}="Area Code" passed through so
    ...    T2 reads the resolved code back from the right properties-file key.
    [Arguments]    ${properties_path}=${FUNCTIONAL_AREA_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Area Code
    RETURN    ${code}

Verify Functional Area Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Object List/State/Region's TC02
    ...    convention): row exists in the grid, then the form shows what was just inserted
    ...    (Area Code/Area Name only - Start date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Functional Area Row By Filter first, clears after (2026-08-23
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Functional Area Row By Filter    ${code}
    Verify Object Insert Exists    ${FUNCTIONAL_AREA_TABLE}    ${code}    Functional Area
    ...    ${FUNCTIONAL_AREA_INSERT_PROPERTIES}    @{FUNCTIONAL_AREA_FORM_LABELS}
    ...    code_label=Area Code
    Clear Functional Area Row Filter

Update Functional Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/
    ...    Object List/State/Region. Filters via Find Functional Area Row By Filter first,
    ...    clears after (2026-08-23 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${FUNCTIONAL_AREA_UPDATE_PROPERTIES}
    Find Functional Area Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${FUNCTIONAL_AREA_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Area Code
    Clear Functional Area Row Filter
    RETURN    ${data}

Verify Functional Area Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Object List/State/Region's TC03 convention: the form
    ...    shows the updated Name. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find
    ...    Functional Area Row By Filter first, clears after (2026-08-23 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Functional Area Row By Filter    ${code}
    Verify Object Form Record    ${FUNCTIONAL_AREA_TABLE}    ${code}    Functional Area
    ...    ${FUNCTIONAL_AREA_UPDATE_PROPERTIES}    Area Name    code_label=Area Code
    Clear Functional Area Row Filter

Find Functional Area Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Functional Area Row By
    ...    Filter first (2026-08-23 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Functional Area Record Found (called right after, same TC)
    ...    needs the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Functional Area Row By Filter    ${code}
    Find Object Record    ${FUNCTIONAL_AREA_TABLE}    ${code}    Functional Area
    ...    code_label=Area Code

Verify Functional Area Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Functional Area Record before this) AND left the Code filter active from that
    ...    same call - clears the filter itself once both checks are done (2026-08-23
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${FUNCTIONAL_AREA_TABLE}    ${code}    ${FUNCTIONAL_AREA_GRID_VERIFY_PROPERTIES}
    ...    ${FUNCTIONAL_AREA_FORM_VERIFY_PROPERTIES}    @{FUNCTIONAL_AREA_FORM_LABELS}
    Clear Functional Area Row Filter

Delete Functional Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the functional area, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/Object List/State/Region's
    ...    convention. Filters via Find Functional Area Row By Filter first, clears after
    ...    (2026-08-23 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Functional Area Row By Filter    ${code}
    Delete Object Via End Date    ${FUNCTIONAL_AREA_TABLE}    ${FUNCTIONAL_AREA_DEL_ENDDATE}    ${code}
    ...    ${date}    ${TEST NAME}_action
    Clear Functional Area Row Filter

Verify Functional Area Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${FUNCTIONAL_AREA_TABLE}    OV_FUNCTIONAL_AREA    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Functional Area Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${FUNCTIONAL_AREA_TABLE}    ${code}
