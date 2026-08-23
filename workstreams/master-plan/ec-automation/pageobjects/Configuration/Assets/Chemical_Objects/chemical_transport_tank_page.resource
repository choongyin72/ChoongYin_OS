*** Settings ***
Documentation       T3 (screen) — Chemical Transport Tank page object.
...                 Screen: Configuration > Assets > Chemical_Objects > Chemical Transport Tank
...                 (CO.0257). Manage-Object (OV) screen. Holds Chemical Transport Tank's
...                 locators + thin IUD wrappers that delegate to T2 (manage_object) and T1
...                 (common).
...                 Rebuilt 2026-08-23 (Batch 8) to mirror Bank/Berth exactly — replaces the
...                 older label-driven-but-not-properties-file-driven pattern with the
...                 properties-file-driven, grid-filter-wired, T2-consolidated pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${CHEMICAL_TRANSPORT_TANK_SCREEN}    Chemical Transport Tank
${CTT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_transport_tank_insert.properties
${CTT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_transport_tank_update.properties
${CTT_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_transport_tank_form_verify.properties
${CTT_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/chemical_transport_tank_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${CTT_TABLE}            ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Same framework-invariant id already
# confirmed live on Bank/State/Berth (identical across those 3 unrelated OV screens' objectdates
# tab) - reused here on the same manage_object framework layout.
${CTT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Chemical Transport Tank's own form-field label set. Labels are "Transport Tank Code"/
# "Transport Tank Name" (screen-prefixed) - confirmed via the already-proven Playwright driver
# py/chemical_transport_tank_iud.py (INSERT_FIELDS/UPDATE_FIELDS), NOT the generic "Code"/"Name"
# Bank/Object List use. Start Date deliberately excluded - Insert-only, not present in
# updateAttributes (same as Bank/Berth/State). Defined ONCE here so both Verify Chemical
# Transport Tank Record Exists (TC02) and Verify Chemical Transport Tank Record Found (TC04)
# share the same list.
@{CTT_FORM_LABELS}    Transport Tank Code    Transport Tank Name


*** Keywords ***
Find Chemical Transport Tank Row By Filter
    [Documentation]    Explicitly filter the Chemical Transport Tank grid's Code column to
    ...    ${code} via the shared T2 Find Object Row By Filter (resources/manage_object.resource)
    ...    - matches Bank/Berth/State's own explicit filter usage (owner, 2026-08-22: "others
    ...    (Bank, State, List_Object) should follow Account... utilise same filter feature"),
    ...    rather than relying only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${CTT_TABLE}    ${code}

Clear Chemical Transport Tank Row Filter
    [Documentation]    Clear the Code column filter (see Find Chemical Transport Tank Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${CTT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Chemical Transport Tank's OWN credentials
    ...    (${CHEMICAL_TRANSPORT_TANK_EC_USER}/${CHEMICAL_TRANSPORT_TANK_EC_PASS} from
    ...    credentials.py) on the current page. Standing decision (owner, 2026-08-22): every EC
    ...    screen gets its own dedicated credential pair. Zero-argument wrapper so
    ...    chemical_transport_tank_iud.robot's test cases read as a plain business step;
    ...    supplies Chemical Transport Tank's own credential defaults to the shared T1 Login To
    ...    EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${CHEMICAL_TRANSPORT_TANK_EC_USER}    ${CHEMICAL_TRANSPORT_TANK_EC_PASS}

Open Chemical Transport Tank Screen
    [Documentation]    Navigate to the Chemical Transport Tank screen and load the list (GO).
    ...    Assumes the caller already logged in this test case (via Login To EC Application).
    [Arguments]    ${user}=${CHEMICAL_TRANSPORT_TANK_EC_USER}    ${pass}=${CHEMICAL_TRANSPORT_TANK_EC_PASS}
    Open EC Screen    ${CHEMICAL_TRANSPORT_TANK_SCREEN}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Insert Chemical Transport Tank Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties And
    ...    Verify Code, so chemical_transport_tank_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Berth.
    [Arguments]    ${properties_path}=${CTT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Transport Tank Code
    RETURN    ${code}

Verify Chemical Transport Tank Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists in
    ...    the grid, then the form shows what was just inserted (Transport Tank Code/Transport
    ...    Tank Name only - Start Date is grid/insert-only, not present in updateAttributes).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find Chemical Transport Tank Row
    ...    By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Transport Tank Row By Filter    ${code}
    Verify Object Insert Exists    ${CTT_TABLE}    ${code}    Chemical Transport Tank
    ...    ${CTT_INSERT_PROPERTIES}    @{CTT_FORM_LABELS}    code_label=Transport Tank Code
    Clear Chemical Transport Tank Row Filter

Update Chemical Transport Tank Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked, matching Bank/Berth. Filters via
    ...    Find Chemical Transport Tank Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${CTT_UPDATE_PROPERTIES}
    Find Chemical Transport Tank Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${CTT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Transport Tank Code
    Clear Chemical Transport Tank Row Filter
    RETURN    ${data}

Verify Chemical Transport Tank Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Transport Tank Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Chemical Transport Tank Row
    ...    By Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Transport Tank Row By Filter    ${code}
    Verify Object Form Record    ${CTT_TABLE}    ${code}    Chemical Transport Tank
    ...    ${CTT_UPDATE_PROPERTIES}    Transport Tank Name    code_label=Transport Tank Code
    Clear Chemical Transport Tank Row Filter

Find Chemical Transport Tank Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Chemical Transport Tank Row By Filter
    ...    first (2026-08-22 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify Chemical Transport Tank Record Found (called right after, same TC) needs the
    ...    grid still filtered to ${code} for its own grid-check, since it doesn't re-select the
    ...    row itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Chemical Transport Tank Row By Filter    ${code}
    Find Object Record    ${CTT_TABLE}    ${code}    Chemical Transport Tank    code_label=Transport Tank Code

Verify Chemical Transport Tank Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid
    ...    AND the form record match the expected (post-update) data. Delegates the full sequence
    ...    (grid-compare, form-compare, screenshot) to the shared T2 Verify Object Found. Caller
    ...    must already have selected the row (TC04 does, via Find Chemical Transport Tank
    ...    Record before this) AND left the Code filter active from that same call - clears the
    ...    filter itself once both checks are done (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${CTT_TABLE}    ${code}    ${CTT_GRID_VERIFY_PROPERTIES}
    ...    ${CTT_FORM_VERIFY_PROPERTIES}    @{CTT_FORM_LABELS}
    Clear Chemical Transport Tank Row Filter

Delete Chemical Transport Tank Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the chemical transport tank, set End Date = Start Date (true delete), Save.
    ...    Captures the TC05 evidence screenshot right after the End Date is filled but BEFORE
    ...    Save is clicked, matching Bank/Berth. Filters via Find Chemical Transport Tank Row By
    ...    Filter first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Chemical Transport Tank Row By Filter    ${code}
    Delete Object Via End Date    ${CTT_TABLE}    ${CTT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Chemical Transport Tank Row Filter

Verify Chemical Transport Tank Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${CTT_TABLE}    OV_CHEM_TRANS_TANK    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Chemical Transport Tank Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${CTT_TABLE}    ${code}
