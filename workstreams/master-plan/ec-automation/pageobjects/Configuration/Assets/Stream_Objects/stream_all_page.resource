*** Settings ***
Documentation       T3 (screen) — Stream - All page object.
...                 Screen: EC Production > Stream - All (CD.0007), class STREAM, view OV_STREAM.
...                 Manage-Object (OV) screen, manage_object_nav/CLASS_NAME/STREAM URL controller -
...                 the exact Bank layout signature (Date+GO nav, single object grid, one NEW
...                 VERSION detail form). Holds Stream - All's locators + thin IUD wrappers that
...                 delegate to T2 (manage_object) and T1 (common).
...                 Built from scratch 2026-08-24 (genuinely new screen - no prior automation for
...                 class STREAM/view OV_STREAM existed anywhere in the repo; docs/ov-reuse-
...                 targets.md's "Stream-All CD.0007 covered" claim was stale/wrong, corrected in
...                 the same PR). Mirrors bank_page.resource/berth_page.resource exactly.
...                 ⚠️ Unlike Bank/Berth's 3-field baseline (Code/Name/Start Date), this screen's
...                 objectForm has TWO EXTRA mandatory dropdowns confirmed via a live scan:
...                 Stream Type (Measured/Reference/Calculated/Quality/Derived) and Alloc Period
...                 (Daily/Monthly/Yearly/...) - both filled with literal option text (not
...                 __FIRST__, per the VAT Code round-trip gotcha) and both persist into
...                 updateAttributes as still-mandatory fields.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${STREAM_ALL_SCREEN}       Stream - All
${STREAM_ALL_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_all_insert.properties
${STREAM_ALL_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_all_update.properties
${STREAM_ALL_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_all_form_verify.properties
${STREAM_ALL_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/stream_all_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${STREAM_ALL_TABLE}     ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth/State's convention.
${STREAM_ALL_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Stream - All's own form-field label set. Labels are "Stream Code"/"Stream Name" (screen-
# prefixed) - confirmed via a fresh live scan 2026-08-24 (no ec-ui-knowledge/screens/*.md entry
# existed for this screen before this build); NOT the generic "Code"/"Name" Bank/Object List use.
# Start Date deliberately excluded - Insert-only, not present in updateAttributes (same as
# Bank/Berth). Stream Type/Alloc Period ARE included - both live in updateAttributes too (still
# mandatory there, confirmed via a read-only scan of an existing production row) so the TC02/TC04
# round-trip checks also confirm the dropdowns actually persisted. Defined ONCE here so both
# Verify Stream All Record Exists (TC02) and Verify Stream All Record Found (TC04) share the list.
@{STREAM_ALL_FORM_LABELS}    Stream Code    Stream Name    Stream Type    Alloc Period


*** Keywords ***
Find Stream All Row By Filter
    [Documentation]    Explicitly filter the Stream - All grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank/Berth/State's own explicit filter usage (owner, 2026-08-22: "others... should
    ...    follow Account... utilise same filter feature").
    [Arguments]    ${code}
    Find Object Row By Filter    ${STREAM_ALL_TABLE}    ${code}

Clear Stream All Row Filter
    [Documentation]    Clear the Code column filter (see Find Stream All Row By Filter) via the
    ...    shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${STREAM_ALL_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Stream - All's OWN credentials (${STREAM_ALL_EC_USER}/
    ...    ${STREAM_ALL_EC_PASS} from credentials.py) on the current page. Standing decision
    ...    (owner, 2026-08-22): every EC screen gets its own dedicated credential pair.
    ...    Zero-argument wrapper so stream_all_iud.robot's test cases read as a plain business
    ...    step; supplies Stream - All's own credential defaults to the shared T1 Login To EC
    ...    Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${STREAM_ALL_EC_USER}    ${STREAM_ALL_EC_PASS}

Open Stream All Screen
    [Documentation]    Navigate to the Stream - All screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${STREAM_ALL_SCREEN}

Insert Stream All Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so stream_all_iud.robot's test case body reads as a plain business
    ...    step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked,
    ...    matching Bank/Berth.
    [Arguments]    ${properties_path}=${STREAM_ALL_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Stream Code
    RETURN    ${code}

Verify Stream All Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Stream Code/Stream Name/
    ...    Stream Type/Alloc Period - Start Date is grid/insert-only, not present in
    ...    updateAttributes). Delegates the full sequence (row-check, select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Stream All Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream All Row By Filter    ${code}
    Verify Object Insert Exists    ${STREAM_ALL_TABLE}    ${code}    Stream - All
    ...    ${STREAM_ALL_INSERT_PROPERTIES}    @{STREAM_ALL_FORM_LABELS}    code_label=Stream Code
    Clear Stream All Row Filter

Update Stream All Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching Bank/Berth.
    ...    Filters via Find Stream All Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${STREAM_ALL_UPDATE_PROPERTIES}
    Find Stream All Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${STREAM_ALL_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Stream Code
    Clear Stream All Row Filter
    RETURN    ${data}

Verify Stream All Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated
    ...    Stream Name. Delegates the full sequence (select, form-compare, screenshot) to
    ...    the shared T2 Verify Object Form Record. Filters via Find Stream All Row By Filter
    ...    first, clears after (2026-08-22 standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream All Row By Filter    ${code}
    Verify Object Form Record    ${STREAM_ALL_TABLE}    ${code}    Stream - All
    ...    ${STREAM_ALL_UPDATE_PROPERTIES}    Stream Name    code_label=Stream Code
    Clear Stream All Row Filter

Find Stream All Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Stream All Row By Filter
    ...    first (2026-08-22 standardisation). Deliberately does NOT clear the filter afterward -
    ...    Verify Stream All Record Found (called right after, same TC) needs the grid still
    ...    filtered to ${code} for its own grid-check, since it doesn't re-select the row
    ...    itself; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Stream All Row By Filter    ${code}
    Find Object Record    ${STREAM_ALL_TABLE}    ${code}    Stream - All    code_label=Stream Code

Verify Stream All Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Stream All Record before this) AND left the Code filter active from that same
    ...    call - clears the filter itself once both checks are done (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${STREAM_ALL_TABLE}    ${code}    ${STREAM_ALL_GRID_VERIFY_PROPERTIES}
    ...    ${STREAM_ALL_FORM_VERIFY_PROPERTIES}    @{STREAM_ALL_FORM_LABELS}
    Clear Stream All Row Filter

Delete Stream All Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the stream, set End Date = Start Date (true
    ...    delete), Save. Captures the TC05 evidence screenshot right after the End Date is
    ...    filled but BEFORE Save is clicked, matching Bank/Berth's convention.
    ...    Filters via Find Stream All Row By Filter first, clears after (2026-08-22
    ...    standardisation).
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Stream All Row By Filter    ${code}
    Delete Object Via End Date    ${STREAM_ALL_TABLE}    ${STREAM_ALL_DEL_ENDDATE}    ${code}
    ...    ${date}    ${TEST NAME}_action
    Clear Stream All Row Filter

Verify Stream All Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${STREAM_ALL_TABLE}    OV_STREAM    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Stream All Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${STREAM_ALL_TABLE}    ${code}
