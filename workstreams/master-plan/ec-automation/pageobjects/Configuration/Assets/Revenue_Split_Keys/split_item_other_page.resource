*** Settings ***
Documentation       T3 (screen) — Split Item Other page object.
...                 Screen: Configuration > Assets > Revenue_Split_Keys > Split Item Other (CD.0017).
...                 Manage-Object (OV) screen. Holds Split Item Other's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 10) to mirror Bank/Berth exactly - adds the
...                 properties-file-driven insert/update/verify and explicit grid-filter wiring
...                 that were missing from the earlier label-driven-only pattern.
...                 OV object-config: Split Item Code / Name / Start Date mandatory (optional
...                 dropdowns skipped, confirmed via the already-proven Playwright driver
...                 py/split_item_other_iud.py). Labels: "Split Item Code" (screen-prefixed) but
...                 GENERIC "Name" (not screen-prefixed) - confirmed via direct grep.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${SPLIT_ITEM_OTHER_SCREEN}          Split Item Other
${SPLIT_ITEM_OTHER_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/split_item_other_insert.properties
${SPLIT_ITEM_OTHER_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/split_item_other_update.properties
${SPLIT_ITEM_OTHER_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/split_item_other_form_verify.properties
${SPLIT_ITEM_OTHER_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/split_item_other_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal.
${SPLIT_ITEM_OTHER_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Berth's convention.
${SPLIT_ITEM_OTHER_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Split Item Other's own form-field label set. "Split Item Code" is screen-prefixed but "Name"
# is GENERIC (not screen-prefixed) - confirmed via direct grep, don't assume otherwise.
# Start Date deliberately excluded - Insert-only, not present in updateAttributes (same as
# Bank/Berth). Defined ONCE here so both Verify Split Item Other Record Exists (TC02) and
# Verify Split Item Other Record Found (TC04) share the same list.
@{SPLIT_ITEM_OTHER_FORM_LABELS}    Split Item Code    Name


*** Keywords ***
Find Split Item Other Row By Filter
    [Documentation]    Explicitly filter the Split Item Other grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank/Berth's own explicit filter usage rather than relying only on Select Object
    ...    Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${SPLIT_ITEM_OTHER_TABLE}    ${code}

Clear Split Item Other Row Filter
    [Documentation]    Clear the Code column filter (see Find Split Item Other Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${SPLIT_ITEM_OTHER_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Split Item Other's OWN credentials
    ...    (${SPLIT_ITEM_OTHER_EC_USER}/${SPLIT_ITEM_OTHER_EC_PASS} from credentials.py) on the
    ...    current page. Standing decision (owner, 2026-08-22): every EC screen gets its own
    ...    dedicated credential pair. Zero-argument wrapper so split_item_other_iud.robot's test
    ...    cases read as a plain business step; supplies Split Item Other's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${SPLIT_ITEM_OTHER_EC_USER}    ${SPLIT_ITEM_OTHER_EC_PASS}

Open Split Item Other Screen
    [Documentation]    Navigate to the Split Item Other screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY navigates.
    ...    Delegates to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${SPLIT_ITEM_OTHER_SCREEN}

Insert Split Item Other Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so split_item_other_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the suite's
    ...    ${TEST_CODE}. Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Berth.
    [Arguments]    ${properties_path}=${SPLIT_ITEM_OTHER_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=Split Item Code
    RETURN    ${code}

Verify Split Item Other Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here, matching Bank/Berth's TC02 convention): row exists
    ...    in the grid, then the form shows what was just inserted (Split Item Code/Name only -
    ...    Start Date is grid/insert-only, not present in updateAttributes). Delegates the full
    ...    sequence (row-check, select, form-compare, screenshot) to the shared T2 Verify Object
    ...    Insert Exists. Filters via Find Split Item Other Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Split Item Other Row By Filter    ${code}
    Verify Object Insert Exists    ${SPLIT_ITEM_OTHER_TABLE}    ${code}    Split Item Other
    ...    ${SPLIT_ITEM_OTHER_INSERT_PROPERTIES}    @{SPLIT_ITEM_OTHER_FORM_LABELS}    code_label=Split Item Code
    Clear Split Item Other Row Filter

Update Split Item Other Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Pre-save
    ...    evidence screenshot captured before Save is clicked, matching Bank/Berth. Filters via
    ...    Find Split Item Other Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${SPLIT_ITEM_OTHER_UPDATE_PROPERTIES}
    Find Split Item Other Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${SPLIT_ITEM_OTHER_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=Split Item Code
    Clear Split Item Other Row Filter
    RETURN    ${data}

Verify Split Item Other Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification, matching Bank/Berth's TC03 convention: the form shows the updated Name.
    ...    Delegates the full sequence (select, form-compare, screenshot) to the shared T2
    ...    Verify Object Form Record. Filters via Find Split Item Other Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Split Item Other Row By Filter    ${code}
    Verify Object Form Record    ${SPLIT_ITEM_OTHER_TABLE}    ${code}    Split Item Other
    ...    ${SPLIT_ITEM_OTHER_UPDATE_PROPERTIES}    Name    code_label=Split Item Code
    Clear Split Item Other Row Filter

Find Split Item Other Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Split Item Other Row By Filter first.
    ...    Deliberately does NOT clear the filter afterward - Verify Split Item Other Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for its
    ...    own grid-check, since it doesn't re-select the row itself; it clears the filter once
    ...    both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Split Item Other Row By Filter    ${code}
    Find Object Record    ${SPLIT_ITEM_OTHER_TABLE}    ${code}    Split Item Other    code_label=Split Item Code

Verify Split Item Other Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the full
    ...    sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify Object
    ...    Found. Caller must already have selected the row (TC04 does, via Find Split Item
    ...    Other Record before this) AND left the Code filter active from that same call -
    ...    clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${SPLIT_ITEM_OTHER_TABLE}    ${code}    ${SPLIT_ITEM_OTHER_GRID_VERIFY_PROPERTIES}
    ...    ${SPLIT_ITEM_OTHER_FORM_VERIFY_PROPERTIES}    @{SPLIT_ITEM_OTHER_FORM_LABELS}
    Clear Split Item Other Row Filter

Delete Split Item Other Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the split_item_other, set End Date = Start Date (true delete), Save. Captures
    ...    the TC05 evidence screenshot right after the End Date is filled but BEFORE Save is
    ...    clicked, matching Bank/Berth. Filters via Find Split Item Other Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Split Item Other Row By Filter    ${code}
    Delete Object Via End Date    ${SPLIT_ITEM_OTHER_TABLE}    ${SPLIT_ITEM_OTHER_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Split Item Other Row Filter

Verify Split Item Other Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${SPLIT_ITEM_OTHER_TABLE}    OV_SPLIT_ITEM_OTHER    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Split Item Other Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${SPLIT_ITEM_OTHER_TABLE}    ${code}
