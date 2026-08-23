*** Settings ***
Documentation       T3 (screen) — Bank Account page object.
...                 Screen: Configuration > Assets > Financial Objects > Bank Account.
...                 Manage-Object (OV) screen. Holds Bank Account's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 11, bigger lift than Batch 7-10) from the OLDER
...                 hardcoded-field-id (`Fill New Object Form ${BANK_ACCOUNT_INS_CODE} ...`)
...                 pattern to Bank/Berth's label-driven, properties-file-driven,
...                 T2-consolidated pattern (see `tmp/batch11_shared_findings.md`).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${BANK_ACCOUNT_SCREEN}    Bank Account
${BANK_ACCOUNT_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/bank_account_insert.properties
${BANK_ACCOUNT_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/bank_account_update.properties
${BANK_ACCOUNT_FORM_VERIFY_PROPS}    ${CURDIR}/../../../../testdata/bank_account_form_verify.properties
${BANK_ACCOUNT_GRID_VERIFY_PROPS}    ${CURDIR}/../../../../testdata/bank_account_grid_verify.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal string.
${BANK_ACCOUNT_TABLE}    ${OV_MANAGE_OBJECT_TABLE}
# Code field is SCREEN-PREFIXED "Bank Account Code" (NOT generic "Code" like Bank) - confirmed
# live 2026-08-23 via a fresh objectForm/updateAttributes ECCell label dump
# (tmp/recon_bankaccount_labels.robot + tmp/recon_bankaccount_upd.robot).
${BANK_ACCOUNT_CODE_LABEL}    Bank Account Code
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented precedent as Bank's own ${BANK_DEL_ENDDATE} (this row packs
# TWO fields, Start Date C:1 + End Date C:3, with the End Date LABEL at C:2 - a shape the
# one-field-per-row label scan cannot safely resolve). Confirmed identical row/col shape live
# via the already-proven Playwright driver's `del_end` locator
# (screens/.../Bank_Account/playwright/ec_iud_bank_account.py).
${BANK_ACCOUNT_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Bank Account's own form-field label set for the round-trip compare (Start Date excluded - it
# lives only in objectdates, not updateAttributes, same as Bank; Bank/Customer/Currency
# reference dropdowns excluded too - __FIRST__ never resolves back to literal display text on
# reload, Storage Flow Batch-10 precedent).
@{BANK_ACCOUNT_FORM_LABELS}    ${BANK_ACCOUNT_CODE_LABEL}    Name    Sort Code


*** Keywords ***
Find Bank Account Row By Filter
    [Documentation]    Explicitly filter the Bank Account grid's Code column to ${code} via the
    ...    shared T2 Find Object Row By Filter (resources/manage_object.resource), matching
    ...    Bank/Berth's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${BANK_ACCOUNT_TABLE}    ${code}

Clear Bank Account Row Filter
    [Documentation]    Clear the Code column filter (see Find Bank Account Row By Filter) via
    ...    the shared T2 Clear Object Row Filter, restoring the grid's normal unfiltered view.
    Clear Object Row Filter    ${BANK_ACCOUNT_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Bank Account's OWN credentials (${BANK_ACCOUNT_EC_USER}/
    ...    ${BANK_ACCOUNT_EC_PASS} from credentials.py) on the current page - works whether this
    ...    is the very first login or a re-login after Logout From EC Application. Screen-specific
    ...    wrapper (bank_account_iud.robot's test cases call this with ZERO arguments) that
    ...    supplies Bank Account's own credential defaults to the shared T1 Login To EC Screen
    ...    (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${BANK_ACCOUNT_EC_USER}    ${BANK_ACCOUNT_EC_PASS}

Open Bank Account Screen
    [Documentation]    Navigate to the Bank Account screen. Assumes the caller already logged in
    ...    this test case (via Login To EC Application) - this keyword ONLY navigates. Delegates
    ...    to the shared T1 Open EC Screen (common.resource) for the actual mechanics.
    Open EC Screen    ${BANK_ACCOUNT_SCREEN}

Insert Bank Account Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties And
    ...    Verify Code, so bank_account_iud.robot's test case body reads as a plain business step
    ...    with ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE}. The TC02 evidence screenshot is captured BEFORE Save is clicked.
    [Arguments]    ${properties_path}=${BANK_ACCOUNT_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action    code_label=${BANK_ACCOUNT_CODE_LABEL}
    RETURN    ${code}

Verify Bank Account Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification: row
    ...    exists in the grid, then every field's LIVE SCREEN value (via Get OV Field Value By
    ...    Label) is compared to testdata/bank_account_insert.properties for
    ...    @{BANK_ACCOUNT_FORM_LABELS} (Bank Account Code, Name, Sort Code). Filters via Find
    ...    Bank Account Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Bank Account Row By Filter    ${code}
    Verify Object Insert Exists    ${BANK_ACCOUNT_TABLE}    ${code}    Bank Account
    ...    ${BANK_ACCOUNT_INSERT_PROPERTIES}    @{BANK_ACCOUNT_FORM_LABELS}
    ...    code_label=${BANK_ACCOUNT_CODE_LABEL}
    Clear Bank Account Row Filter

Update Bank Account Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns the
    ...    applied {label: value} dict so the caller can DB-verify against exactly what was set.
    ...    The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via Find Bank
    ...    Account Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${BANK_ACCOUNT_UPDATE_PROPERTIES}
    Find Bank Account Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${BANK_ACCOUNT_TABLE}    ${code}    ${properties_path}
    ...    ${TEST NAME}_action    code_label=${BANK_ACCOUNT_CODE_LABEL}
    Clear Bank Account Row Filter
    RETURN    ${data}

Verify Bank Account Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}). PURE SCREEN verification:
    ...    selects the row (loading updateAttributes), then compares Name/Sort Code's LIVE SCREEN
    ...    value to testdata/bank_account_update.properties. Filters via Find Bank Account Row By
    ...    Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Bank Account Row By Filter    ${code}
    Verify Object Form Record    ${BANK_ACCOUNT_TABLE}    ${code}    Bank Account
    ...    ${BANK_ACCOUNT_UPDATE_PROPERTIES}    Name    Sort Code
    ...    code_label=${BANK_ACCOUNT_CODE_LABEL}
    Clear Bank Account Row Filter

Find Bank Account Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record, called
    ...    with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Calls Find Bank
    ...    Account Row By Filter first. Deliberately does NOT clear the filter afterward - Verify
    ...    Bank Account Record Found (called right after, same TC) needs the grid still filtered.
    [Arguments]    ${code}=${TEST_CODE}
    Find Bank Account Row By Filter    ${code}
    Find Object Record    ${BANK_ACCOUNT_TABLE}    ${code}    Bank Account    ${BANK_ACCOUNT_CODE_LABEL}

Verify Bank Account Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid AND
    ...    the full form record match the expected data. Caller must already have selected the
    ...    row (TC04 does, via Find Bank Account Record before this) AND left the Code filter
    ...    active from that same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${BANK_ACCOUNT_TABLE}    ${code}    ${BANK_ACCOUNT_GRID_VERIFY_PROPS}
    ...    ${BANK_ACCOUNT_FORM_VERIFY_PROPS}    @{BANK_ACCOUNT_FORM_LABELS}
    Clear Bank Account Row Filter

Delete Bank Account Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the bank account, set End Date = Start Date (true delete), Save. Captures the
    ...    TC05 evidence screenshot right after the End Date is filled but BEFORE Save is clicked.
    ...    Filters via Find Bank Account Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Bank Account Row By Filter    ${code}
    Delete Object Via End Date    ${BANK_ACCOUNT_TABLE}    ${BANK_ACCOUNT_DEL_ENDDATE}    ${code}    ${date}
    ...    ${TEST NAME}_action
    Clear Bank Account Row Filter

Verify Bank Account Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with ZERO
    ...    arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is absent
    ...    from BOTH the grid and the database (OV_BANK_ACCOUNT).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${BANK_ACCOUNT_TABLE}    ov_bank_account    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Bank Account Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}).
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${BANK_ACCOUNT_TABLE}    ${code}
