*** Settings ***
Documentation       T3 (screen) — Port page object.
...                 Screen: Configuration > Assets > Transport Objects > Port (CO.2003).
...                 Manage-Object (OV) screen. Holds Port's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 9) to mirror Bank/Berth exactly - replaces the
...                 older arg-based/no-filter pattern with the label-driven,
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.
...                 Port's grid is PAGINATED (2 pages) - Find Port Row By Filter/T2's shared
...                 row-locate keywords already walk all pages (confirmed live 2026-08-23).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${PORT_SCREEN}          Port
${PORT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/port_insert.properties
${PORT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/port_update.properties
${PORT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/port_form_verify.properties
${PORT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/port_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${PORT_TABLE}           ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention.
${PORT_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Port's own form-field label set. Labels are "Port Code"/"Port Name" (screen-prefixed) -
# confirmed via the already-proven Playwright driver py/port_iud.py (INSERT_FIELDS) and the
# pre-existing page object's own recon comment; NOT the generic "Code"/"Name" Bank/Object List
# use. Start Date deliberately excluded - Insert-only, not present in updateAttributes (same
# as Bank/Berth). Defined ONCE here so both Verify Port Record Exists (TC02) and Verify Port
# Record Found (TC04) share the same list.
@{PORT_FORM_LABELS}    Port Code    Port Name


*** Keywords ***
Find Port Row By Filter
    [Documentation]    Explicitly filter the Port grid's Code column to ${code} via the shared
    ...    T2 Find Object Row By Filter (resources/manage_object.resource) - matches Bank/
    ...    Berth's own explicit filter usage. Port's grid is paginated (2 pages); the shared
    ...    T2 filter/row-locate keywords already walk all pages.
    [Arguments]    ${code}
    Find Object Row By Filter    ${PORT_TABLE}    ${code}

Clear Port Row Filter
    [Documentation]    Clear the Code column filter (see Find Port Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${PORT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Port's OWN credentials (${PORT_EC_USER}/
    ...    ${PORT_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so port_iud.robot's test cases read as a plain business
    ...    step; supplies Port's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${PORT_EC_USER}    ${PORT_EC_PASS}

Open Port Screen
    [Documentation]    Navigate to the Port screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${PORT_SCREEN}

Insert Port Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so port_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth.
    [Arguments]    ${properties_path}=${PORT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Port Code
    RETURN    ${code}

Verify Port Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row
    ...    exists in the grid, then the form shows what was just inserted (Port
    ...    Code/Port Name only - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Port Row By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Port Row By Filter    ${code}
    Verify Object Insert Exists    ${PORT_TABLE}    ${code}    Port    ${PORT_INSERT_PROPERTIES}
    ...    @{PORT_FORM_LABELS}    code_label=Port Code
    Clear Port Row Filter

Update Port Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Port Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${PORT_UPDATE_PROPERTIES}
    Find Port Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${PORT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Port Code
    Clear Port Row Filter
    RETURN    ${data}

Verify Port Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Port Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Port Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Port Row By Filter    ${code}
    Verify Object Form Record    ${PORT_TABLE}    ${code}    Port    ${PORT_UPDATE_PROPERTIES}
    ...    Port Name    code_label=Port Code
    Clear Port Row Filter

Find Port Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Port Row By Filter first
    ...    (2026-08-22 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify Port Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row
    ...    itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Port Row By Filter    ${code}
    Find Object Record    ${PORT_TABLE}    ${code}    Port    code_label=Port Code

Verify Port Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Port Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${PORT_TABLE}    ${code}    ${PORT_GRID_VERIFY_PROPERTIES}
    ...    ${PORT_FORM_VERIFY_PROPERTIES}    @{PORT_FORM_LABELS}
    Clear Port Row Filter

Delete Port Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the port, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Berth's convention.
    ...    Filters via Find Port Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Port Row By Filter    ${code}
    Delete Object Via End Date    ${PORT_TABLE}    ${PORT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Port Row Filter

Verify Port Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${PORT_TABLE}    OV_PORT    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Port Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${PORT_TABLE}    ${code}
