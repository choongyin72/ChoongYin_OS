*** Settings ***
Documentation       T3 (screen) — Document Sequence page object.
...                 Screen: Configuration > Assets > Revenue Document Objects > Document
...                 Sequence (CD.0109). Custom-URL OV (no navigator/GO at all — reload via
...                 toolbar Refresh, confirmed live via the screen's own prior driver
...                 py/document_sequence_iud.py and re-confirmed live this session: grid id
...                 is nav:form:T_data, renders directly on open, matches Report Context/WBS/
...                 Calendar/Account/Cost Centre/Revenue Order, NOT the manage-object
...                 manage_object_nav_nav:form:T_data + GO variant). Base table
...                 DOC_SEQUENCE/DOC_SEQUENCE_VERSION, view OV_DOC_SEQUENCE.
...                 Bank-pattern conversion (2026-08-25): upgraded from the older
...                 label-driven/timestamped-code shape to the properties-file-driven,
...                 T2-consolidated pattern matching Bank/Report Context - same shape as
...                 Report Context (RP.0007), the precedent for a custom-URL OV screen built
...                 to the full Bank pattern.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${DOCUMENT_SEQUENCE_SCREEN}    Document Sequence
${DOCUMENT_SEQUENCE_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/document_sequence_insert.properties
${DOCUMENT_SEQUENCE_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/document_sequence_update.properties
${DOCUMENT_SEQUENCE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/document_sequence_form_verify.properties
${DOCUMENT_SEQUENCE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/document_sequence_grid_verify.properties
# Grid id: Document Sequence is a custom-URL OV - grid is nav:form:T_data (NOT the
# manage-object manage_object_nav_nav:form:T_data variant) and there is NO navigator/GO
# button at all. T2's Save And Refresh List auto-detects this (falls back to toolbar
# Refresh) - matches Report Context/WBS/Calendar/Account/Cost Centre/Revenue Order.
${DOCUMENT_SEQUENCE_TABLE}    nav:form:T_data
# objectdates field ID (Delete — End Date = Start Date), matching Bank/Report Context's
# convention - framework-invariant objectdates layout (R:0:C:1 = Start Date, R:0:C:3 = End Date).
${DOCUMENT_SEQUENCE_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Document Sequence's own form-field label set. Labels are plain "Code"/"Name" (NOT
# screen-prefixed) - confirmed via the screen's own prior driver/T3 recon. Starting Point
# (a mandatory extra text field, DB column STARTING_POINT) is deliberately excluded here -
# Insert-only, never previously round-trip-verified in updateAttributes, same precedent as
# Bank/Report Context excluding their own Insert-only fields (e.g. Start Date) from this list.
@{DOCUMENT_SEQUENCE_FORM_LABELS}    Code    Name


*** Keywords ***
Find Document Sequence Row By Filter
    [Documentation]    Explicitly filter the Document Sequence grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Bank/Report Context's explicit filter usage, rather than relying only on
    ...    Select Object Row's implicit 3s-timeout fallback.
    [Arguments]    ${code}
    Find Object Row By Filter    ${DOCUMENT_SEQUENCE_TABLE}    ${code}

Clear Document Sequence Row Filter
    [Documentation]    Clear the Code column filter (see Find Document Sequence Row By
    ...    Filter) via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${DOCUMENT_SEQUENCE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Document Sequence's OWN credentials
    ...    (${DOCUMENT_SEQUENCE_EC_USER}/${DOCUMENT_SEQUENCE_EC_PASS} from credentials.py) on
    ...    the current page. Zero-argument wrapper so document_sequence_iud.robot's test
    ...    cases read as a plain business step; supplies Document Sequence's own credential
    ...    defaults to the shared T1 Login To EC Screen (common.resource), which owns the
    ...    actual login mechanics.
    Login To EC Screen    ${DOCUMENT_SEQUENCE_EC_USER}    ${DOCUMENT_SEQUENCE_EC_PASS}

Open Document Sequence Screen
    [Documentation]    Navigate to the Document Sequence screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics. Deliberately does NOT click any GO button or call Apply
    ...    Navigator - this screen has NO navigator at all; the grid (nav:form:T_data)
    ...    renders directly on open, same as Report Context/WBS/Calendar/Account.
    Open EC Screen    ${DOCUMENT_SEQUENCE_SCREEN}

Insert Document Sequence Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Insert Object From Properties
    ...    And Verify Code, so document_sequence_iud.robot's test case body reads as a plain
    ...    business step with ZERO arguments. Also checks the inserted Code matches the
    ...    suite's ${TEST_CODE}. Pre-save evidence screenshot captured before Save is
    ...    clicked, matching Bank/Report Context.
    [Arguments]    ${properties_path}=${DOCUMENT_SEQUENCE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Document Sequence Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check here - matches Bank/Report Context's TC02 convention):
    ...    row exists in the grid, then the form shows what was just inserted (Code/Name
    ...    only). Delegates the full sequence (row-check, select, form-compare, screenshot)
    ...    to the shared T2 Verify Object Insert Exists. Filters via Find Document Sequence
    ...    Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Sequence Row By Filter    ${code}
    Verify Object Insert Exists    ${DOCUMENT_SEQUENCE_TABLE}    ${code}    Document Sequence
    ...    ${DOCUMENT_SEQUENCE_INSERT_PROPERTIES}    @{DOCUMENT_SEQUENCE_FORM_LABELS}
    Clear Document Sequence Row Filter

Update Document Sequence Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Pre-save evidence screenshot captured before Save is clicked, matching
    ...    Bank/Report Context. Filters via Find Document Sequence Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${DOCUMENT_SEQUENCE_UPDATE_PROPERTIES}
    Find Document Sequence Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${DOCUMENT_SEQUENCE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Document Sequence Row Filter
    RETURN    ${data}

Verify Document Sequence Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN
    ...    verification (no DB check), matching Bank/Report Context's TC03 convention: the
    ...    form shows the updated Name. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Document
    ...    Sequence Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Sequence Row By Filter    ${code}
    Verify Object Form Record    ${DOCUMENT_SEQUENCE_TABLE}    ${code}    Document Sequence
    ...    ${DOCUMENT_SEQUENCE_UPDATE_PROPERTIES}    Name
    Clear Document Sequence Row Filter

Find Document Sequence Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    ...    Delegates the full select+capture sequence. Calls Find Document Sequence Row By
    ...    Filter first. Deliberately does NOT clear the filter afterward - Verify Document
    ...    Sequence Record Found (called right after, same TC) needs the grid still filtered
    ...    to ${code} for its own grid-check, since it doesn't re-select the row itself; it
    ...    clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Sequence Row By Filter    ${code}
    Find Object Record    ${DOCUMENT_SEQUENCE_TABLE}    ${code}    Document Sequence

Verify Document Sequence Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the
    ...    grid AND the form record match the expected (post-update) data. Delegates the
    ...    full sequence (grid-compare, form-compare, screenshot) to the shared T2 Verify
    ...    Object Found. Caller must already have selected the row (TC04 does, via Find
    ...    Document Sequence Record before this) AND left the Code filter active from that
    ...    same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${DOCUMENT_SEQUENCE_TABLE}    ${code}    ${DOCUMENT_SEQUENCE_GRID_VERIFY_PROPERTIES}
    ...    ${DOCUMENT_SEQUENCE_FORM_VERIFY_PROPERTIES}    @{DOCUMENT_SEQUENCE_FORM_LABELS}
    Clear Document Sequence Row Filter

Delete Document Sequence Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date,
    ...    called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Select the document sequence, set End Date = Start
    ...    Date (true delete), Save. Captures the TC05 evidence screenshot right after the
    ...    End Date is filled but BEFORE Save is clicked, matching Bank/Report Context.
    ...    Filters via Find Document Sequence Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Document Sequence Row By Filter    ${code}
    Delete Object Via End Date    ${DOCUMENT_SEQUENCE_TABLE}    ${DOCUMENT_SEQUENCE_DEL_ENDDATE}    ${code}
    ...    ${date}    ${TEST NAME}_action
    Clear Document Sequence Row Filter

Verify Document Sequence Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code}
    ...    is absent from BOTH the grid and the database.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${DOCUMENT_SEQUENCE_TABLE}    OV_DOC_SEQUENCE    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Document Sequence Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to
    ...    the shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${DOCUMENT_SEQUENCE_TABLE}    ${code}
