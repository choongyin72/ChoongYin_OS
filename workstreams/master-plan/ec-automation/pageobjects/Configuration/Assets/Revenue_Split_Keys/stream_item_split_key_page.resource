*** Settings ***
Documentation       T3 (screen) — Stream Item Split Key page object.
...                 Screen: Configuration > Assets > Revenue_Split_Keys > Stream Item Split Key
...                 (BF_CODE CD.0156). Manage-Object (OV) screen, class SPLIT_KEY,
...                 SPLIT_TYPE=STREAM_ITEM_SPLIT, view OV_SPLIT_KEY. Holds Stream Item Split
...                 Key's locators + thin IUD wrappers that delegate to T2 (manage_object) and
...                 T1 (common).
...                 One of 6 sibling "* Split Key" screens (Product/Company/Field/Stream Item
...                 Category/Other/Stream Item) that ALL share the SAME base view OV_SPLIT_KEY,
...                 differentiated only by SPLIT_TYPE (set server-side from the URL/menu entry,
...                 not user-entered). Live-verified 2026-08-25 via the real treeview click
...                 (search "Split" -> exact-text tv-link "Stream Item Split Key", DISTINCT from
...                 the similarly-named sibling entries "Stream Item Split Key Shares" and
...                 "Stream Item Category Split Key"): URL =
...                 manage_object_split_key/CLASS_NAME/SPLIT_KEY/SPLIT_TYPE/STREAM_ITEM_SPLIT,
...                 grid id = nav:form:T_data (this split_key URL family's OWN grid id - NOT the
...                 shared ${OV_MANAGE_OBJECT_TABLE} constant used by the manage_object_nav
...                 family, e.g. Split Item Other), navigator GO button id = navButton:form:B
...                 (also NOT the standard button:form:B - Save And Refresh List's existing
...                 button:form:B-absent fallback to the toolbar Refresh already handles this
...                 with zero changes needed to shared T1/T2).
...                 OV object-config (live recon 2026-08-25, New Object form): mandatory
...                 "Split Key Code" / "Split Key Name" / "Start Date" only - Description /
...                 Comments / Value Method / Shares add to 100% / Rounding Rule / Number of
...                 Rounding Decimals / Number Display Format are all optional (no mandatory
...                 dropdown to fill). Labels use the class's own GENERIC "Split Key" prefix,
...                 not a "Stream Item"-prefixed label.
...                 Uses a distinctly-scoped fixed test code AUTOTEST_SPLITKEY_STREAMITEM (NOT
...                 the generic AUTOTEST_SPLIT_KEY) so this screen's IUD run can never collide
...                 with the 5 sibling Split Key screens being built in parallel against the
...                 same OV_SPLIT_KEY view.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${STREAM_ITEM_SPLIT_KEY_SCREEN}          Stream Item Split Key
${STREAM_ITEM_SPLIT_KEY_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_item_split_key_insert.properties
${STREAM_ITEM_SPLIT_KEY_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_item_split_key_update.properties
${STREAM_ITEM_SPLIT_KEY_FORM_VERIFY_PROPS}    ${CURDIR}/../../../../testdata/stream_item_split_key_form_verify.properties
${STREAM_ITEM_SPLIT_KEY_GRID_VERIFY_PROPS}    ${CURDIR}/../../../../testdata/stream_item_split_key_grid_verify.properties
# Grid id: THIS screen's OWN id (manage_object_split_key URL family) - confirmed live 2026-08-25,
# distinct from the manage_object_nav family's shared ${OV_MANAGE_OBJECT_TABLE} constant.
${STREAM_ITEM_SPLIT_KEY_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention.
${STREAM_ITEM_SPLIT_KEY_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Stream Item Split Key's own form-field label set - both Code and Name use the class's GENERIC
# "Split Key" prefix (confirmed via live recon 2026-08-25), not a "Stream Item"-prefixed label.
# Start Date deliberately excluded - Insert-only, not present in updateAttributes (same as
# Bank/Berth). Defined ONCE here so both Verify Stream Item Split Key Record Exists (TC02) and
# Verify Stream Item Split Key Record Found (TC04) share the same list.
@{STREAM_ITEM_SPLIT_KEY_FORM_LABELS}    Split Key Code    Split Key Name


*** Keywords ***
Find Stream Item Split Key Row By Filter
    [Documentation]    Explicitly filter the Stream Item Split Key grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Bank/Berth/Split Item Other's own explicit filter usage rather than relying
    ...    only on Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${STREAM_ITEM_SPLIT_KEY_TABLE}    ${code}

Clear Stream Item Split Key Row Filter
    [Documentation]    Clear the Code column filter (see Find Stream Item Split Key Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${STREAM_ITEM_SPLIT_KEY_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Stream Item Split Key's OWN credentials
    ...    (${STREAM_ITEM_SPLIT_KEY_EC_USER}/${STREAM_ITEM_SPLIT_KEY_EC_PASS} from
    ...    credentials.py) on the current page. Standing decision (owner, 2026-08-22): every EC
    ...    screen gets its own dedicated credential pair. Zero-argument wrapper so
    ...    stream_item_split_key_iud.robot's test cases read as a plain business step; supplies
    ...    Stream Item Split Key's own credential defaults to the shared T1 Login To EC Screen
    ...    (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${STREAM_ITEM_SPLIT_KEY_EC_USER}    ${STREAM_ITEM_SPLIT_KEY_EC_PASS}

Open Stream Item Split Key Screen
    [Documentation]    Navigate to the Stream Item Split Key screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    ...    Live-verified 2026-08-25: typing the full exact string "Stream Item Split Key" into
    ...    the treeview search surfaces the exact-text tv-link within the standard 10s wait
    ...    (distinct from the sibling "Stream Item Split Key Shares" / "Stream Item Category
    ...    Split Key" entries) - no special-casing needed here.
    Open EC Screen    ${STREAM_ITEM_SPLIT_KEY_SCREEN}

Insert Stream Item Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so stream_item_split_key_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Berth.
    [Arguments]    ${properties_path}=${STREAM_ITEM_SPLIT_KEY_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Split Key Code
    RETURN    ${code}

Verify Stream Item Split Key Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Split Key Code/Split Key
    ...    Name only - Start Date is grid/insert-only, not present in updateAttributes).
    ...    Delegates the full sequence (row-check, select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Insert Exists. Filters via Find Stream Item Split Key Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream Item Split Key Row By Filter    ${code}
    Verify Object Insert Exists    ${STREAM_ITEM_SPLIT_KEY_TABLE}    ${code}    Stream Item Split Key
    ...    ${STREAM_ITEM_SPLIT_KEY_INSERT_PROPERTIES}    @{STREAM_ITEM_SPLIT_KEY_FORM_LABELS}    code_label=Split Key Code
    Clear Stream Item Split Key Row Filter

Update Stream Item Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked, matching Bank/Berth. Filters via
    ...    Find Stream Item Split Key Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${STREAM_ITEM_SPLIT_KEY_UPDATE_PROPERTIES}
    Find Stream Item Split Key Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${STREAM_ITEM_SPLIT_KEY_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Split Key Code
    Clear Stream Item Split Key Row Filter
    RETURN    ${data}

Verify Stream Item Split Key Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated Split
    ...    Key Name. Delegates the full sequence (select, form-compare, screenshot) to the
    ...    shared T2 Verify Object Form Record. Filters via Find Stream Item Split Key Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream Item Split Key Row By Filter    ${code}
    Verify Object Form Record    ${STREAM_ITEM_SPLIT_KEY_TABLE}    ${code}    Stream Item Split Key
    ...    ${STREAM_ITEM_SPLIT_KEY_UPDATE_PROPERTIES}    Split Key Name    code_label=Split Key Code
    Clear Stream Item Split Key Row Filter

Find Stream Item Split Key Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Stream Item Split Key Row By Filter
    ...    first. Deliberately does NOT clear the filter afterward - Verify Stream Item Split
    ...    Key Record Found (called right after, same TC) needs the grid still filtered to
    ...    ${code} for its own grid-check, since it doesn't re-select the row itself; it clears
    ...    the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream Item Split Key Row By Filter    ${code}
    Find Object Record    ${STREAM_ITEM_SPLIT_KEY_TABLE}    ${code}    Stream Item Split Key    code_label=Split Key Code

Verify Stream Item Split Key Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Stream Item
    ...    Split Key Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${STREAM_ITEM_SPLIT_KEY_TABLE}    ${code}    ${STREAM_ITEM_SPLIT_KEY_GRID_VERIFY_PROPS}
    ...    ${STREAM_ITEM_SPLIT_KEY_FORM_VERIFY_PROPS}    @{STREAM_ITEM_SPLIT_KEY_FORM_LABELS}
    Clear Stream Item Split Key Row Filter

Delete Stream Item Split Key Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the record, set End Date = Start Date (true delete), Save. Captures the TC05
    ...    evidence screenshot right after the End Date is filled but BEFORE Save is clicked,
    ...    matching Bank/Berth. Filters via Find Stream Item Split Key Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Stream Item Split Key Row By Filter    ${code}
    Delete Object Via End Date    ${STREAM_ITEM_SPLIT_KEY_TABLE}    ${STREAM_ITEM_SPLIT_KEY_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Stream Item Split Key Row Filter

Verify Stream Item Split Key Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database (OV_SPLIT_KEY, scoped to this screen's own
    ...    test code so a sibling Split Key screen's rows are never touched).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${STREAM_ITEM_SPLIT_KEY_TABLE}    OV_SPLIT_KEY    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Stream Item Split Key Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${STREAM_ITEM_SPLIT_KEY_TABLE}    ${code}
