*** Settings ***
Documentation       T3 (screen) — Inventory Area page object.
...                 Screen: Configuration > Assets > Inventory_Objects > Inventory Area (CD.0115).
...                 Manage-Object (OV) screen. Holds Inventory Area's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 8) to mirror Bank/Berth exactly - replaces the
...                 older label-driven-only pattern (no properties-file-driven insert/update,
...                 no explicit grid-filter wiring) with the full properties-file-driven,
...                 grid-filter-wired, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${INVENTORY_AREA_SCREEN}         Inventory Area
${INVENTORY_AREA_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/inventory_area_insert.properties
${INVENTORY_AREA_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/inventory_area_update.properties
${INVENTORY_AREA_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/inventory_area_form_verify.properties
${INVENTORY_AREA_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/inventory_area_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${INVENTORY_AREA_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention.
${INVENTORY_AREA_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Inventory Area's own form-field label set. Labels are "Inventory Area Code"/"Inventory
# Area Name" (screen-prefixed) - confirmed live via the pre-existing RF page object and the
# already-proven Playwright driver py/inventory_area_iud.py (INSERT_FIELDS/UPDATE_FIELDS),
# re-confirmed via a fresh live run 2026-08-23. Start Date deliberately excluded - Insert-only,
# not present in updateAttributes (same as Bank/Berth). Defined ONCE here so both Verify
# Inventory Area Record Exists (TC02) and Verify Inventory Area Record Found (TC04) share the
# same list.
@{INVENTORY_AREA_FORM_LABELS}    Inventory Area Code    Inventory Area Name


*** Keywords ***
Find Inventory Area Row By Filter
    [Documentation]    Explicitly filter the Inventory Area grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Account/Bank/Berth's own explicit filter usage (owner, 2026-08-22: "others
    ...    (Bank, State, List_Object) should follow Account... utilise same filter feature"),
    ...    rather than relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${INVENTORY_AREA_TABLE}    ${code}

Clear Inventory Area Row Filter
    [Documentation]    Clear the Code column filter (see Find Inventory Area Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered
    ...    view.
    Clear Object Row Filter    ${INVENTORY_AREA_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Inventory Area's OWN credentials
    ...    (${INVENTORY_AREA_EC_USER}/${INVENTORY_AREA_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so inventory_area_iud.robot's test
    ...    cases read as a plain business step; supplies Inventory Area's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${INVENTORY_AREA_EC_USER}    ${INVENTORY_AREA_EC_PASS}

Open Inventory Area Screen
    [Documentation]    Navigate to the Inventory Area screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${INVENTORY_AREA_SCREEN}

Insert Inventory Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so inventory_area_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth.
    [Arguments]    ${properties_path}=${INVENTORY_AREA_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Inventory Area Code
    RETURN    ${code}

Verify Inventory Area Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Inventory Area
    ...    Code/Inventory Area Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists. Filters via Find
    ...    Inventory Area Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Inventory Area Row By Filter    ${code}
    Verify Object Insert Exists    ${INVENTORY_AREA_TABLE}    ${code}    Inventory Area
    ...    ${INVENTORY_AREA_INSERT_PROPERTIES}    @{INVENTORY_AREA_FORM_LABELS}
    ...    code_label=Inventory Area Code
    Clear Inventory Area Row Filter

Update Inventory Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Inventory Area Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${INVENTORY_AREA_UPDATE_PROPERTIES}
    Find Inventory Area Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${INVENTORY_AREA_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Inventory Area Code
    Clear Inventory Area Row Filter
    RETURN    ${data}

Verify Inventory Area Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Inventory Area Name. Delegates the full sequence (select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Form Record. Filters via Find Inventory Area Row By
    ...    Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Inventory Area Row By Filter    ${code}
    Verify Object Form Record    ${INVENTORY_AREA_TABLE}    ${code}    Inventory Area
    ...    ${INVENTORY_AREA_UPDATE_PROPERTIES}    Inventory Area Name    code_label=Inventory Area Code
    Clear Inventory Area Row Filter

Find Inventory Area Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Inventory Area Row By
    ...    Filter first (2026-08-22 standardisation). Deliberately does NOT clear the filter
    ...    afterward - Verify Inventory Area Record Found (called right after, same TC) needs
    ...    the grid still filtered to ${code} for its own grid-check, since it doesn't
    ...    re-select the row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Inventory Area Row By Filter    ${code}
    Find Object Record    ${INVENTORY_AREA_TABLE}    ${code}    Inventory Area    code_label=Inventory Area Code

Verify Inventory Area Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Inventory
    ...    Area Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${INVENTORY_AREA_TABLE}    ${code}    ${INVENTORY_AREA_GRID_VERIFY_PROPERTIES}
    ...    ${INVENTORY_AREA_FORM_VERIFY_PROPERTIES}    @{INVENTORY_AREA_FORM_LABELS}
    Clear Inventory Area Row Filter

Delete Inventory Area Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the inventory_area, set End Date = Start Date
    ...    (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked, matching Bank/Berth. Filters via Find
    ...    Inventory Area Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Inventory Area Row By Filter    ${code}
    Delete Object Via End Date    ${INVENTORY_AREA_TABLE}    ${INVENTORY_AREA_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Inventory Area Row Filter

Verify Inventory Area Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${INVENTORY_AREA_TABLE}    OV_INVENTORY_AREA    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Inventory Area Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${INVENTORY_AREA_TABLE}    ${code}
