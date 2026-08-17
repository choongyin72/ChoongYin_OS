*** Settings ***
Documentation       T3 (screen) — Bank page object.
...                 Screen: Configuration > Assets > Financial Objects > Bank.
...                 Manage-Object (OV) screen. Holds Bank's locators + thin IUD
...                 wrappers that delegate to T2 (manage_object) and T1 (common).

Library             Browser
Library             ../../../../libraries/DbVerify.py
Library             ../../../../libraries/PropertiesReader.py
Resource            ../../../../resources/common.resource
Resource            ../../../../resources/manage_object.resource
Variables           ../../../../resources/credentials.py


*** Variables ***
${BANK_SCREEN}          Bank
${BANK_ENTRY_PROPERTIES}    ${CURDIR}/../../../../testdata/bank_entry.properties
# Grid id: reuse T2's centralized constant instead of re-hardcoding the same literal
# string (manage_object.resource defines this ONCE specifically so no T3 duplicates it).
${BANK_TABLE}           ${OV_MANAGE_OBJECT_TABLE}
# objectdates field ID (Delete — End Date = Start Date). Hardcoded deliberately, NOT
# label-driven: the proven Python driver (py/ec_object_iud.py END_DATE_ID) documents that
# this row packs TWO fields (Start Date C:1, End Date C:3) with the End Date label at C:2 -
# a shape the one-field-per-row label scan cannot safely resolve. TO BE LIVE-VERIFIED
# (2026-08-17) whether OV Field Id By Label's following-sibling lookup agrees with this
# value before relying on it generally - left hardcoded here regardless, matching the
# documented, already-proven precedent rather than a claim not yet checked.
${BANK_DEL_ENDDATE}     tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input


*** Keywords ***
Open Bank Screen
    [Documentation]    Suite Setup: launch, login as ${user} (defaults to Bank's own
    ...    credentials.py, not the shared environment.py), navigate to the Bank screen.
    ...    Pass a different user for role tests.
    [Arguments]    ${user}=${BANK_EC_USER}    ${pass}=${BANK_EC_PASS}
    Launch EC And Open Screen    ${BANK_SCREEN}    ${user}    ${pass}

Bank Row Should Exist
    [Documentation]    Assert a bank with ${code} is present in the list.
    [Arguments]    ${code}
    Row Should Exist    ${BANK_TABLE}    ${code}

Bank Row Should Not Exist
    [Documentation]    Assert a bank with ${code} is absent from the list.
    [Arguments]    ${code}
    Row Should Not Exist    ${BANK_TABLE}    ${code}

Bank Should Exist In DB
    [Documentation]    DB ground-truth: assert ${code} really persisted in ov_bank.
    [Arguments]    ${code}
    Code Should Be Present In View    ov_bank    ${code}

Bank Should Not Exist In DB
    [Documentation]    DB ground-truth: assert ${code} was truly deleted from ov_bank.
    [Arguments]    ${code}
    Code Should Be Absent In View    ov_bank    ${code}

Bank Description Should Equal In DB
    [Documentation]    DB ground-truth: assert ${code}'s DESCRIPTION column equals ${description}
    ...    in ov_bank. Column name + value match the already-proven Python driver
    ...    (py/bank_iud.py: DESC="AUTOTEST desc", DB-verified against ov_bank.DESCRIPTION).
    [Arguments]    ${code}    ${description}
    Field Should Equal In View    ov_bank    ${code}    DESCRIPTION    ${description}

Bank Field Should Equal In DB
    [Documentation]    DB ground-truth: assert ${code}'s ${column} equals ${expected} in ov_bank.
    ...    Generic wrapper for verifying any ov_bank column - real column names confirmed live
    ...    (2026-08-17): ADDRESS_1..ADDRESS_8, BANK_SWIFT_CODE, COUNTRY_CODE, DESCRIPTION,
    ...    COMMENTS. "Address Line 1"/"Swift Code" are the FORM labels, not the column names.
    [Arguments]    ${code}    ${column}    ${expected}
    Field Should Equal In View    ov_bank    ${code}    ${column}    ${expected}

Bank Fields Should Equal In DB
    [Documentation]    DB ground-truth: assert MULTIPLE ov_bank columns in ONE call, instead of
    ...    one "Bank Field Should Equal In DB" line per column. Pass columns as named arguments,
    ...    e.g.: Bank Fields Should Equal In DB    ${TEST_CODE}    DESCRIPTION=${OBJ_DESC}
    ...    ...    ADDRESS_1=${OBJ_ADDR1}    BANK_SWIFT_CODE=${OBJ_SWIFT}
    [Arguments]    ${code}    &{columns}
    FOR    ${column}    ${expected}    IN    &{columns}
        Bank Field Should Equal In DB    ${code}    ${column}    ${expected}
    END

Bank Row Should Show Name
    [Documentation]    Assert the Bank row for ${code} displays ${name}.
    [Arguments]    ${code}    ${name}
    ${row}=    Get Text    xpath=//tbody[@id='${BANK_TABLE}']//tr[.//span[normalize-space(text())='${code}']]
    Should Contain    ${row}    ${name}    msg=Bank row ${code} does not show name ${name}

Insert Bank Record
    [Documentation]    Insert a new bank: New Object form -> Code/Name/Start Date/Description ->
    ...    Save. Fields resolved BY LABEL (not a hardcoded R:n:C:n id) - robust to a form-layout
    ...    shift, matching manage_object.resource's documented label-driven convention.
    ...    Description is optional on this screen but included here to match the already-proven
    ...    Python driver's own field coverage (py/bank_iud.py INSERT_FIELDS).
    ...    SUPERSEDED for TC02 by "Insert Bank From Properties" (data-driven, owner-requested
    ...    2026-08-17) - kept here as a working fallback, not deleted, in case that needs
    ...    reverting quickly.
    [Arguments]    ${code}    ${name}    ${start_date}    ${description}=${EMPTY}
    Open New Object Form
    Fill OV Field By Label    objectForm    Code    ${code}
    Fill OV Field By Label    objectForm    Name    ${name}
    Fill OV Date By Label    objectForm    Start Date    ${start_date}
    IF    '${description}' != ''
        Fill OV Field By Label    objectForm    Description    ${description}
    END
    Save
    Apply Navigator

Insert Bank From Properties
    [Documentation]    Insert a new bank by reading EVERY column=value entry from
    ...    ${BANK_ENTRY_PROPERTIES} (testdata/bank_entry.properties) and filling each field by
    ...    label, auto-detecting its kind (text/date/dropdown/popup) live - so the fields filled
    ...    and their values live entirely in the properties file, not in this keyword or the
    ...    suite. Returns the Code that was inserted (read back from the properties file).
    [Arguments]    ${properties_path}=${BANK_ENTRY_PROPERTIES}
    ${code}=    Insert Object From Properties    ${properties_path}
    RETURN    ${code}

Update Bank Name
    [Documentation]    Select the bank, confirm it loaded, edit Name, Save. The Code field
    ...    is resolved BY LABEL each call (not a hardcoded id) so a row-load check never
    ...    silently reads the wrong field if the update form's layout ever shifts.
    [Arguments]    ${code}    ${new_name}
    Select Object Row    ${BANK_TABLE}    ${code}
    ${code_id}=    OV Field Id By Label    updateAttributes    Code
    ${loaded}=    Get Property    css=[id="${code_id}"]    value
    Should Be Equal    ${loaded}    ${code}    msg=Row select failed - code not loaded
    Fill OV Field By Label    updateAttributes    Name    ${new_name}
    Save
    Apply Navigator

Delete Bank
    [Documentation]    Select the bank, set End Date = Start Date (true delete), Save.
    [Arguments]    ${code}    ${date}
    Select Object Row    ${BANK_TABLE}    ${code}
    Delete Object By Zero-Length Window    ${BANK_DEL_ENDDATE}    ${date}
    Save
    Apply Navigator
