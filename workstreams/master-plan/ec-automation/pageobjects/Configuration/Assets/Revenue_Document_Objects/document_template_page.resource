*** Settings ***
Documentation       T3 (screen) - Document Template page object.
...                 Screen: Configuration > Assets > Revenue_Document_Objects > Document Template (CD.0013). Manage-Object (OV) screen.
...                 OV object-config: Code / Name / Start Date mandatory + Document Title (de-facto
...                 mandatory - Save silently fails to persist without it, per the already-proven
...                 Python driver py/document_template_iud.py; optional dropdowns skipped).
...                 NO hardcoded field ids: grid = shared T2 ${OV_MANAGE_OBJECT_TABLE};
...                 fields resolved by LABEL via T2 (Fill OV * By Label Any Kind). Bank-pattern:
...                 properties-file-driven insert/update/verify + explicit grid-filter wiring
...                 (upgraded 2026-08-24 from the prior label-driven-only shape, PR body cites the
...                 registry row this MODIFIES).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${DOCUMENT_TEMPLATE_SCREEN}         Document Template
${DOCUMENT_TEMPLATE_INSERT_PROPERTIES}         ${CURDIR}/../../../../testdata/document_template_insert.properties
${DOCUMENT_TEMPLATE_UPDATE_PROPERTIES}         ${CURDIR}/../../../../testdata/document_template_update.properties
${DOCUMENT_TEMPLATE_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/document_template_form_verify.properties
${DOCUMENT_TEMPLATE_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/document_template_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string.
${DOCUMENT_TEMPLATE_TABLE}          ${OV_MANAGE_OBJECT_TABLE}
# Document Template's own form-field label set (Start Date excluded - lives only in objectdates,
# not updateAttributes/objectForm's own compare set, matching Bank's documented precedent).
@{DOCUMENT_TEMPLATE_FORM_LABELS}    Code    Name    Document Title


*** Keywords ***
Find Document Template Row By Filter
    [Documentation]    Explicitly filter the Document Template grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource) - matches
    ...    Bank/Account's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${DOCUMENT_TEMPLATE_TABLE}    ${code}

Clear Document Template Row Filter
    [Documentation]    Clear the Code column filter set by Find Document Template Row By Filter,
    ...    restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${DOCUMENT_TEMPLATE_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Document Template's OWN credentials
    ...    (${DOCUMENT_TEMPLATE_EC_USER}/${DOCUMENT_TEMPLATE_EC_PASS} from credentials.py) on the
    ...    current page - works whether this is the very first login (page freshly loaded on the
    ...    login form) or a re-login after Logout From EC Application.
    Login To EC Screen    ${DOCUMENT_TEMPLATE_EC_USER}    ${DOCUMENT_TEMPLATE_EC_PASS}

Open Document Template Screen
    [Documentation]    Navigate to the Document Template screen and load the list (GO). Assumes
    ...    the caller already logged in this test case (via Login To EC Application).
    Open EC Screen    ${DOCUMENT_TEMPLATE_SCREEN}
    Apply Navigator    # grid needs GO to populate (no default rows on open)

Insert Document Template Record And Save
    [Documentation]    Properties-file-driven insert (Bank pattern) via the shared T2 Insert
    ...    Object From Properties And Verify Code, called with ZERO arguments (defaults ${code}
    ...    to the suite's ${TEST_CODE}). Fails on its own if
    ...    testdata/document_template_insert.properties' Code ever drifts out of sync with the
    ...    suite variable. The TC02 evidence screenshot is captured BEFORE Save is clicked.
    [Arguments]    ${properties_path}=${DOCUMENT_TEMPLATE_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Document Template Record Exists
    [Documentation]    TC02 verification, called with ZERO arguments (defaults ${code} to the
    ...    suite's ${TEST_CODE}). PURE SCREEN verification (no DB check here - that is TC02's own
    ...    separate DbVerify assertion): row exists in the grid, then every field named in
    ...    @{DOCUMENT_TEMPLATE_FORM_LABELS} is compared to testdata/document_template_insert.properties.
    ...    Filters via Find Document Template Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Template Row By Filter    ${code}
    Verify Object Insert Exists    ${DOCUMENT_TEMPLATE_TABLE}    ${code}    Document Template
    ...    ${DOCUMENT_TEMPLATE_INSERT_PROPERTIES}    @{DOCUMENT_TEMPLATE_FORM_LABELS}
    Clear Document Template Row Filter

Update Document Template Record And Save
    [Documentation]    Properties-file-driven update (Bank pattern) via the shared T2 Update
    ...    Object From Properties, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Returns the applied {label: value} dict so the caller can DB-verify
    ...    against exactly what was set. Filters via Find Document Template Row By Filter first,
    ...    clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${DOCUMENT_TEMPLATE_UPDATE_PROPERTIES}
    Find Document Template Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${DOCUMENT_TEMPLATE_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action
    Clear Document Template Row Filter
    RETURN    ${data}

Verify Document Template Record Updated
    [Documentation]    TC03 verification, called with ZERO arguments (defaults ${code} to the
    ...    suite's ${TEST_CODE}). PURE SCREEN verification: selects the row, then compares Name's
    ...    LIVE SCREEN value to testdata/document_template_update.properties. Filters via Find
    ...    Document Template Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Template Row By Filter    ${code}
    Verify Object Form Record    ${DOCUMENT_TEMPLATE_TABLE}    ${code}    Document Template
    ...    ${DOCUMENT_TEMPLATE_UPDATE_PROPERTIES}    Name
    Clear Document Template Row Filter

Find Document Template Record
    [Documentation]    Select ${code} (loads updateAttributes) then capture the find-action
    ...    evidence screenshot, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Calls Find Document Template Row By Filter first - deliberately does
    ...    NOT clear the filter afterward, Verify Document Template Record Found (called right
    ...    after) needs the grid still filtered.
    [Arguments]    ${code}=${TEST_CODE}
    Find Document Template Row By Filter    ${code}
    Find Object Record    ${DOCUMENT_TEMPLATE_TABLE}    ${code}    Document Template

Verify Document Template Record Found
    [Documentation]    TC04 verification, called with ZERO arguments (defaults ${code} to the
    ...    suite's ${TEST_CODE}): confirms BOTH the grid AND the full form record match the
    ...    expected data. Caller must already have selected the row (TC04 does, via Find
    ...    Document Template Record before this) AND left the Code filter active - clears the
    ...    filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${DOCUMENT_TEMPLATE_TABLE}    ${code}    ${DOCUMENT_TEMPLATE_GRID_VERIFY_PROPERTIES}
    ...    ${DOCUMENT_TEMPLATE_FORM_VERIFY_PROPERTIES}    @{DOCUMENT_TEMPLATE_FORM_LABELS}
    Clear Document Template Row Filter

Delete Document Template Record And Save
    [Documentation]    Select the document_template, set End Date = Start Date (true delete),
    ...    Save. Called with ZERO arguments (defaults ${code}/${date} to the suite's
    ...    ${TEST_CODE}/${END_DATE}). Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked. Filters via Find Document Template Row By
    ...    Filter first, clears after. The End Date field id is resolved BY LABEL at runtime
    ...    (OV Field Id By Label) - not hardcoded - matching the prior (pre-conversion) page
    ...    object's own Fill OV Date By Label objectdates "End Date" approach, since no live
    ...    row-shape scan of objectdates has been run this session to safely hardcode an id
    ...    the way Bank's own documented precedent does.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Document Template Row By Filter    ${code}
    Select Object Row    ${DOCUMENT_TEMPLATE_TABLE}    ${code}
    ${enddate_id}=    OV Field Id By Label    objectdates    End Date
    Delete Object By Zero-Length Window    ${enddate_id}    ${date}
    Capture Step    ${TEST NAME}_action
    Save And Refresh List
    Clear Document Template Row Filter

Verify Document Template Record Removed
    [Documentation]    TC05 verification, called with ZERO arguments (defaults ${code} to the
    ...    suite's ${TEST_CODE}): confirms ${code} is absent from BOTH the grid and OV_DOC_TEMPLATE.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${DOCUMENT_TEMPLATE_TABLE}    ov_doc_template    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Document Template Record Does Not Exist
    [Documentation]    TC01 clean-state check, called with ZERO arguments (defaults ${code} to
    ...    the suite's ${TEST_CODE}).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${DOCUMENT_TEMPLATE_TABLE}    ${code}
