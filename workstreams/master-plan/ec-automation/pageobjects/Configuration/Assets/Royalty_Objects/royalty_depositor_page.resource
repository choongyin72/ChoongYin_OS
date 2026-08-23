*** Settings ***
Documentation       T3 (screen) — Royalty Depositor page object.
...                 Screen: Configuration > Assets > Royalty Objects > Royalty Depositor.
...                 Manage-Object (OV) screen — Bank-pattern conversion (Batch 5, 2026-08-23):
...                 label-driven field resolution + properties-file-driven data + T2-consolidated
...                 keywords, replacing the older hardcoded-field-id driver. Live recon (2026-08-23)
...                 confirmed this screen uses SCREEN-PREFIXED labels ("Royalty Depositor Code" /
...                 "Royalty Depositor Name"), not the generic "Code"/"Name" Bank uses — same
...                 shape as State's own "State Code" precedent — so every T2 call below passes
...                 code_label=Royalty Depositor Code. No mandatory navigator/date+GO cascade
...                 beyond the universal as-at-date filter bar every manage-object OV screen has
...                 (confirmed live: NAV_GO_BUTTON_COUNT=1, NAV_DROPDOWN_COUNT=0) — this IS a
...                 standard Bank-pattern manage-object OV, not a scope mismatch.

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${RD_SCREEN}            Royalty Depositor
${RD_CODE_LABEL}        Royalty Depositor Code
${RD_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/royalty_depositor_insert.properties
${RD_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/royalty_depositor_update.properties
${RD_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/royalty_depositor_form_verify.properties
${RD_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/royalty_depositor_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string.
${RD_TABLE}             ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately (matches Bank's
# own documented precedent) — confirmed live 2026-08-23 this row packs Start Date C:1 / End Date
# label C:2 / End Date input C:3, same shape as Bank.
${RD_DEL_ENDDATE}       tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Royalty Depositor's own form-field label set (Start Date deliberately excluded — it lives only
# in objectdates, not updateAttributes, confirmed live 2026-08-23 matching Bank's own exclusion).
# Only Code/Name are mandatory (live MandatoryCellStyle scan) and the only fields the prior
# proven driver ever filled — every other optional objectForm field (Official Name, Comments,
# System Company, Company Number, Registration Details, Interface Sequence Owner, Address Line
# 1-8, Phone, Fax, Email, Original Number, Fin Code, Country) is deliberately out of scope for
# this conversion (no scope expansion — IUD Fill Only Needed Fields).
@{RD_FORM_LABELS}    Royalty Depositor Code    Royalty Depositor Name


*** Keywords ***
Find Royalty Depositor Row By Filter
    [Documentation]    Explicitly filter the Royalty Depositor grid's Code column to ${code} via
    ...    the shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    Bank/Account/State's own explicit filter usage (owner, 2026-08-22 standardisation).
    [Arguments]    ${code}
    Find Object Row By Filter    ${RD_TABLE}    ${code}

Clear Royalty Depositor Row Filter
    [Documentation]    Clear the Code column filter (see Find Royalty Depositor Row By Filter)
    ...    via the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${RD_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Royalty Depositor's OWN credentials
    ...    (${ROYALTY_DEPOSITOR_EC_USER}/${ROYALTY_DEPOSITOR_EC_PASS} from credentials.py) on the
    ...    current page — works whether this is the very first login (page freshly loaded on the
    ...    login form via the shared T1 Open EC Application) or a re-login after Logout From EC
    ...    Application. Screen-specific wrapper (matches Bank's convention: every test case calls
    ...    this with ZERO arguments) — the actual login mechanics live in the shared T1 Login To
    ...    EC Screen (common.resource); kept here only because a shared file should not hardcode
    ...    any screen's credentials.
    Login To EC Screen    ${ROYALTY_DEPOSITOR_EC_USER}    ${ROYALTY_DEPOSITOR_EC_PASS}

Open Royalty Depositor Screen
    [Documentation]    Navigate to the Royalty Depositor screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) — matches Bank's convention
    ...    where each test case gets its own explicit Login/Logout step. Delegates to the shared
    ...    T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${RD_SCREEN}

Insert Royalty Depositor Record And Save
    [Documentation]    Friendly-narrative wrapper (matches Bank's convention) around the shared
    ...    T2 Insert Object From Properties And Verify Code, so the test case body reads as a
    ...    plain business step with ZERO arguments. Also owns the integrity check that the
    ...    inserted Code matches the suite's ${TEST_CODE} — fails on its own if
    ...    testdata/royalty_depositor_insert.properties' Code ever drifts out of sync with the
    ...    suite variable. The TC02 evidence screenshot is captured BEFORE Save is clicked.
    [Arguments]    ${properties_path}=${RD_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${RD_CODE_LABEL}
    RETURN    ${code}

Verify Royalty Depositor Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check here — that is TC02's own separate DbVerify assertion): row exists in the
    ...    grid, then every field's LIVE SCREEN value is compared to
    ...    testdata/royalty_depositor_insert.properties — Royalty Depositor Code, Royalty
    ...    Depositor Name (${RD_FORM_LABELS}). Start Date is NOT verified here (matches Bank) —
    ...    it only exists as a grid column / objectdates field, not an updateAttributes form
    ...    field. Delegates the full sequence to the shared T2 Verify Object Insert Exists.
    ...    Filters via Find Royalty Depositor Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Royalty Depositor Row By Filter    ${code}
    Verify Object Insert Exists    ${RD_TABLE}    ${code}    Royalty Depositor    ${RD_INSERT_PROPERTIES}
    ...    @{RD_FORM_LABELS}    code_label=${RD_CODE_LABEL}
    Clear Royalty Depositor Row Filter

Update Royalty Depositor Record And Save
    [Documentation]    Friendly-narrative wrapper (matches Bank's convention) around T2's Update
    ...    Object From Properties, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Returns the applied {label: value} dict so the caller can DB-verify
    ...    against exactly what was set. The TC03 evidence screenshot is captured BEFORE Save is
    ...    clicked. Filters via Find Royalty Depositor Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${RD_UPDATE_PROPERTIES}
    Find Royalty Depositor Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${RD_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=${RD_CODE_LABEL}
    Clear Royalty Depositor Row Filter
    RETURN    ${data}

Verify Royalty Depositor Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification (no
    ...    DB check): selects the row (loading updateAttributes), then compares Royalty Depositor
    ...    Name's LIVE SCREEN value to testdata/royalty_depositor_update.properties — the only
    ...    field that file has. Delegates the full sequence to the shared T2 Verify Object Form
    ...    Record. Filters via Find Royalty Depositor Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Royalty Depositor Row By Filter    ${code}
    Verify Object Form Record    ${RD_TABLE}    ${code}    Royalty Depositor    ${RD_UPDATE_PROPERTIES}
    ...    Royalty Depositor Name    code_label=${RD_CODE_LABEL}
    Clear Royalty Depositor Row Filter

Find Royalty Depositor Record
    [Documentation]    Friendly-narrative wrapper (matches Bank's convention) around the shared
    ...    T2 Find Object Record, called with ZERO arguments (defaults ${code} to the suite's
    ...    ${TEST_CODE}). Calls Find Royalty Depositor Row By Filter first. Deliberately does NOT
    ...    clear the filter afterward — Verify Royalty Depositor Record Found (called right
    ...    after, same TC) needs the grid still filtered to ${code} for its own grid-check.
    [Arguments]    ${code}=${TEST_CODE}
    Find Royalty Depositor Row By Filter    ${code}
    Find Object Record    ${RD_TABLE}    ${code}    Royalty Depositor    code_label=${RD_CODE_LABEL}

Verify Royalty Depositor Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Delegates the full sequence to the
    ...    shared T2 Verify Object Found. Caller must already have selected the row (TC04 does,
    ...    via Find Royalty Depositor Record before this) AND left the Code filter active from
    ...    that same call — clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${RD_TABLE}    ${code}    ${RD_GRID_VERIFY_PROPERTIES}
    ...    ${RD_FORM_VERIFY_PROPERTIES}    @{RD_FORM_LABELS}
    Clear Royalty Depositor Row Filter

Delete Royalty Depositor Record And Save
    [Documentation]    Friendly-narrative wrapper (matches Bank's convention) around T2's Delete
    ...    Object Via End Date, called with ZERO arguments (defaults ${code}/${date} to the
    ...    suite's ${TEST_CODE}/${END_DATE}). Select the royalty depositor, set End Date = Start
    ...    Date (true delete), Save. Captures the TC05 evidence screenshot right after the End
    ...    Date is filled but BEFORE Save is clicked. Filters via Find Royalty Depositor Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Royalty Depositor Row By Filter    ${code}
    Delete Object Via End Date    ${RD_TABLE}    ${RD_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Royalty Depositor Row Filter

Verify Royalty Depositor Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (ov_royalty_depositor). Also captures the TC05
    ...    evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${RD_TABLE}    ov_royalty_depositor    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Royalty Depositor Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the shared
    ...    T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${RD_TABLE}    ${code}
