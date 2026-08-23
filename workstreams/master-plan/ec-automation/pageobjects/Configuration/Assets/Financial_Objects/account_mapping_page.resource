*** Settings ***
Documentation       T3 (screen) — Account Mapping page object.
...                 Screen: Configuration > Assets > Financial Objects > Account Mapping.
...                 Manage-Object (OV) screen. Holds Account Mapping's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).
...                 Rebuilt 2026-08-23 (Batch 6) to mirror Bank/Customer/Cost Object Mapping
...                 exactly - replaces the older hardcoded-field-id pattern with the
...                 label-driven, properties-file-driven, T2-consolidated pattern.
...                 Live-confirmed 2026-08-23 (tmp/recon_am*.py - deleted before final commit):
...                 objectForm order is Code, Alternative Code, Name, Start Date, End Date,
...                 Description, Product, Line Item Type, Financial Code, Company Category,
...                 Company, Status, Debit / Credit, Debit PK, Credit PK, Account Category,
...                 Financial Account. EIGHT mandatory reference dropdowns beyond Code/Name
...                 (confirmed via the same MandatoryCellStyle-on-the-input/dd-span technique
...                 documented on VAT Code/Customer/Cost Object Mapping - note this screen puts
...                 the mandatory class on the INPUT/dd-span itself, not a wrapping tableCell
...                 div, so the detection had to walk one level deeper than usual): Line Item
...                 Type, Financial Code, Company Category, Status, Debit / Credit, Debit PK,
...                 Credit PK, Financial Account. Account Category is statically
...                 mandatory:false but is functionally required as a CASCADE dependency for
...                 Financial Account (Financial Account's option list is scoped by Account
...                 Category) - same cascade pattern as Cost Object Mapping's Object
...                 Type->Cost Object, so it is listed BEFORE Financial Account in
...                 testdata/account_mapping_insert.properties. Product/Alternative
...                 Code/Company are NOT mandatory and are omitted (IUD fills only needed
...                 fields). All 8+1 dropdown values are the REAL literal option text (NOT
...                 __FIRST__ - Batch 2 VAT Code gotcha), reusing the EXACT combination this
...                 screen's OWN prior Playwright IUD bundle already proved live-PASS on
...                 2026-06-12 (screens/.../Account_Mapping/account_mapping_sow.md,
...                 evidence/account_mapping_results.json): Line Item Type="All Line Item
...                 Types", Financial Code="Journal Entry", Company Category="All",
...                 Status="Accrual", Debit / Credit="Credit", Debit PK="Debit General Ledger
...                 (40)", Credit PK="Credit General Ledger (50)", Account Category="Revenue",
...                 Financial Account="ACCRUAL CR Acct" - the combination (not any single
...                 dropdown) is this screen's real unique key (ALT_CODE =
...                 LineItemType_FinancialCode_CompanyCategory_Status_DebitCredit pattern);
...                 a fresh DB check 2026-08-23 confirms no existing OV_FIN_ACCOUNT_MAPPING row
...                 uses this combination (still free). GRID is a 75-row custom grid showing
...                 MANY columns (Code, Name, Product, Line Item Type, Financial Code, Company
...                 Category, Company, Status, Debit / Credit, Debit PK, Credit PK, Account
...                 Category, Financial Account) - notably NO Start Date column, unlike Bank/
...                 Cost Object Mapping's simpler 3-column grid (same documented variant as
...                 Regulatory Permits, Batch 2) - so
...                 testdata/account_mapping_grid_verify.properties only checks Code/Name (the
...                 two columns guaranteed present and unambiguous as plain text).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${ACCOUNT_MAPPING_SCREEN}          Account Mapping
${ACCOUNT_MAPPING_INSERT_PROPERTIES}    ${CURDIR}/../../../../testdata/account_mapping_insert.properties
${ACCOUNT_MAPPING_UPDATE_PROPERTIES}    ${CURDIR}/../../../../testdata/account_mapping_update.properties
${ACCOUNT_MAPPING_FORM_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/account_mapping_form_verify.properties
${ACCOUNT_MAPPING_GRID_VERIFY_PROPERTIES}    ${CURDIR}/../../../../testdata/account_mapping_grid_verify.properties
# Grid id: this screen does NOT use the manage_object_nav_nav navigator-based grid id that
# ${OV_MANAGE_OBJECT_TABLE} (manage_object.resource) represents - Account Mapping is a
# CUSTOM-URL / no-navigator OV screen (confirmed live 2026-08-23: GO-button locator
# button:form:B has zero matches on this screen, and the grid genuinely renders under
# manageObject:form:T_data, unchanged from this screen's own PRIOR page object/SOW). Kept as
# its own local constant, NOT the shared T2 one, to avoid silently pointing at the wrong grid.
${ACCOUNT_MAPPING_TABLE}           manageObject:form:T_data
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven - same documented shape as Bank's/Customer's/Cost Object Mapping's own
# DEL_ENDDATE (single row, Start Date C:1 / End Date label C:2 / End Date input C:3) -
# confirmed unchanged live 2026-08-23.
${ACCOUNT_MAPPING_DEL_ENDDATE}    tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input
# Account Mapping's own form-field label set (Start Date deliberately excluded - it lives
# only in objectForm/objectdates, not updateAttributes, same convention as Bank/Customer/
# Cost Object Mapping). Defined ONCE here so both Verify Account Mapping Record Exists (TC02,
# against account_mapping_insert.properties) and Verify Account Mapping Record Found (TC04,
# against account_mapping_form_verify.properties) share the same list.
# Line Item Type is DELIBERATELY excluded from this list - a live run 2026-08-23 proved it
# re-renders as the short internal code 'ALL' after a form reload/select instead of the
# literal option text 'All Line Item Types' that was picked at Insert time (exact live
# failure: "Field 'Line Item Type' shows 'ALL' in updateAttributes, expected 'All Line Item
# Types'") - the SAME documented re-render gotcha as DOA Credit Limit's Role Name (Batch 4):
# excluded from the live-DOM round-trip check, relying on DB ground-truth
# (Code Should Be Present In View / TC02's DbVerify) for that field instead.
@{ACCOUNT_MAPPING_FORM_LABELS}    Code    Name    Description    Financial Code
...    Company Category    Status    Debit / Credit    Debit PK    Credit PK
...    Account Category    Financial Account


*** Keywords ***
Find Account Mapping Row By Filter
    [Documentation]    Explicitly filter the Account Mapping grid's Code column to ${code}
    ...    via the shared T2 Find Object Row By Filter (resources/manage_object.resource) -
    ...    matches Bank's/Customer's/Cost Object Mapping's own explicit filter usage.
    [Arguments]    ${code}
    Find Object Row By Filter    ${ACCOUNT_MAPPING_TABLE}    ${code}

Clear Account Mapping Row Filter
    [Documentation]    Clear the Code column filter set by Find Account Mapping Row By
    ...    Filter, via the shared T2 Clear Object Row Filter, restoring the grid's normal
    ...    unfiltered view.
    Clear Object Row Filter    ${ACCOUNT_MAPPING_TABLE}

Login To EC Application
    [Documentation]    Authenticate as Account Mapping's OWN credentials
    ...    (${ACCOUNT_MAPPING_EC_USER}/${ACCOUNT_MAPPING_EC_PASS} from credentials.py)
    ...    on the current page - works whether this is the very first login (page freshly
    ...    loaded on the login form via the shared T1 Open EC Application) or a re-login after
    ...    Logout From EC Application. Screen-specific wrapper (matches Bank's/Customer's own
    ...    pattern) that supplies Account Mapping's own credential defaults to the shared T1
    ...    Login To EC Screen (common.resource), which owns the actual login mechanics.
    Login To EC Screen    ${ACCOUNT_MAPPING_EC_USER}    ${ACCOUNT_MAPPING_EC_PASS}

Open Account Mapping Screen
    [Documentation]    Navigate to the Account Mapping screen. Assumes the caller already
    ...    logged in this test case (via Login To EC Application) - this keyword ONLY
    ...    navigates. Delegates to the shared T1 Open EC Screen (common.resource) for the
    ...    actual mechanics.
    Open EC Screen    ${ACCOUNT_MAPPING_SCREEN}

Insert Account Mapping Record And Save
    [Documentation]    Friendly-narrative wrapper around Insert Object From Properties, so
    ...    account_mapping_iud.robot's test case body reads as a plain business step with
    ...    ZERO arguments - the underlying mechanics (properties-file-driven insert) are
    ...    UNCHANGED. Also owns the integrity check that the inserted Code matches the suite's
    ...    ${TEST_CODE} - this keyword fails on its own if
    ...    testdata/account_mapping_insert.properties' Code ever drifts out of sync with the
    ...    suite variable. The TC02 evidence screenshot is captured BEFORE Save is clicked,
    ...    passed through to Insert Object From Properties, which fills every field first (in
    ...    file order - Account Category BEFORE Financial Account, required for the cascade).
    [Arguments]    ${properties_path}=${ACCOUNT_MAPPING_INSERT_PROPERTIES}
    ${code}=    Insert Object From Properties And Verify Code    ${properties_path}    ${TEST_CODE}
    ...    ${TEST NAME}_action
    RETURN    ${code}

Verify Account Mapping Record Exists
    [Documentation]    Friendly-narrative wrapper around the TC02 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check here): row exists in the grid, then every field's LIVE
    ...    SCREEN value (via Get OV Field Value By Label) is compared to
    ...    testdata/account_mapping_insert.properties (the file used to insert, not the
    ...    post-update account_mapping_form_verify.properties) - Code, Name, Description, Line
    ...    Item Type, Financial Code, Company Category, Status, Debit / Credit, Debit PK,
    ...    Credit PK, Account Category, Financial Account (${ACCOUNT_MAPPING_FORM_LABELS}). Start Date is
    ...    NOT verified here - it only exists as an objectdates field, not an updateAttributes
    ...    field (and is not a grid column on this screen either). Delegates the full sequence
    ...    (row-check, select, form-compare, screenshot) to the shared T2 Verify Object Insert
    ...    Exists. Filters via Find Account Mapping Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Account Mapping Row By Filter    ${code}
    Verify Object Insert Exists    ${ACCOUNT_MAPPING_TABLE}    ${code}    Account Mapping
    ...    ${ACCOUNT_MAPPING_INSERT_PROPERTIES}    @{ACCOUNT_MAPPING_FORM_LABELS}
    Clear Account Mapping Row Filter

Update Account Mapping Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Update Object From Properties,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Returns
    ...    the applied {label: value} dict so the caller can DB-verify against exactly what was
    ...    set. The TC03 evidence screenshot is captured BEFORE Save is clicked. Filters via
    ...    Find Account Mapping Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}    ${properties_path}=${ACCOUNT_MAPPING_UPDATE_PROPERTIES}
    Find Account Mapping Row By Filter    ${code}
    ${data}=    Update Object From Properties    ${ACCOUNT_MAPPING_TABLE}    ${code}
    ...    ${properties_path}    ${TEST NAME}_action
    Clear Account Mapping Row Filter
    RETURN    ${data}

Verify Account Mapping Record Updated
    [Documentation]    Friendly-narrative wrapper around the TC03 verification, called with
    ...    ZERO arguments: defaults ${code} to the suite's ${TEST_CODE}. PURE SCREEN
    ...    verification (no DB check): selects the row (loading updateAttributes), then compares
    ...    Name/Description's LIVE SCREEN value (via Get OV Field Value By Label) to
    ...    testdata/account_mapping_update.properties - only those two labels, since that's
    ...    the only fields that file has. Delegates the full sequence (select, form-compare,
    ...    screenshot) to the shared T2 Verify Object Form Record. Filters via Find Account
    ...    Mapping Row By Filter first, clears after.
    [Arguments]    ${code}=${TEST_CODE}
    Find Account Mapping Row By Filter    ${code}
    Verify Object Form Record    ${ACCOUNT_MAPPING_TABLE}    ${code}    Account Mapping
    ...    ${ACCOUNT_MAPPING_UPDATE_PROPERTIES}    Name    Description
    Clear Account Mapping Row Filter

Find Account Mapping Record
    [Documentation]    Friendly-narrative wrapper around the shared T2 Find Object Record,
    ...    called with ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates
    ...    the full select+capture sequence. Calls Find Account Mapping Row By Filter first.
    ...    Deliberately does NOT clear the filter afterward - Verify Account Mapping Record
    ...    Found (called right after, same TC) needs the grid still filtered to ${code} for its
    ...    own grid-check; it clears the filter once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Find Account Mapping Row By Filter    ${code}
    Find Object Record    ${ACCOUNT_MAPPING_TABLE}    ${code}    Account Mapping

Verify Account Mapping Record Found
    [Documentation]    Friendly-narrative wrapper around the TC04 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms BOTH the grid
    ...    AND the full form record match the expected data - the SAME two existing live-DOM
    ...    round-trip keywords, just called under one name. Also captures the TC04 evidence
    ...    screenshot. Delegates the full sequence (grid-compare, form-compare, screenshot) to
    ...    the shared T2 Verify Object Found. Caller must already have selected the row (TC04
    ...    does, via Find Account Mapping Record before this) AND left the Code filter active
    ...    from that same call - clears the filter itself once both checks are done.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Found    ${ACCOUNT_MAPPING_TABLE}    ${code}
    ...    ${ACCOUNT_MAPPING_GRID_VERIFY_PROPERTIES}    ${ACCOUNT_MAPPING_FORM_VERIFY_PROPERTIES}
    ...    @{ACCOUNT_MAPPING_FORM_LABELS}
    Clear Account Mapping Row Filter

Delete Account Mapping Record And Save
    [Documentation]    Friendly-narrative wrapper around T2's Delete Object Via End Date, called
    ...    with ZERO arguments (defaults ${code}/${date} to the suite's ${TEST_CODE}/${END_DATE}).
    ...    Select the account mapping, set End Date = Start Date (true delete), Save.
    ...    Captures the TC05 evidence screenshot right after the End Date is filled but BEFORE
    ...    Save is clicked. Filters via Find Account Mapping Row By Filter first, clears
    ...    after.
    [Arguments]    ${code}=${TEST_CODE}    ${date}=${END_DATE}
    Find Account Mapping Row By Filter    ${code}
    Delete Object Via End Date    ${ACCOUNT_MAPPING_TABLE}    ${ACCOUNT_MAPPING_DEL_ENDDATE}
    ...    ${code}    ${date}    ${TEST NAME}_action
    Clear Account Mapping Row Filter

Verify Account Mapping Record Removed
    [Documentation]    Friendly-narrative wrapper around the TC05 verification, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}): confirms ${code} is
    ...    absent from BOTH the grid and the database - the SAME two existing DB-ground-truth
    ...    keywords, just called under one name. Also captures the TC05 evidence screenshot.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Removed    ${ACCOUNT_MAPPING_TABLE}    OV_FIN_ACCOUNT_MAPPING    ${code}
    Capture Step    ${TEST NAME}_verify

Verify Account Mapping Record Does Not Exist
    [Documentation]    Friendly-narrative wrapper around the TC01 clean-state check, called with
    ...    ZERO arguments (defaults ${code} to the suite's ${TEST_CODE}). Delegates to the
    ...    shared T2 Verify Object Does Not Exist.
    [Arguments]    ${code}=${TEST_CODE}
    Verify Object Does Not Exist    ${ACCOUNT_MAPPING_TABLE}    ${code}
