*** Settings ***
Documentation       EC IUD Test - Document Template (Configuration > Assets > Revenue_Document_Objects > Document Template, CD.0013).
...                 Manage-Object (OV) screen. DELETE = End Date = Start Date (true delete in OV_DOC_TEMPLATE).
...                 Layered: this test -> document_template_page (T3) -> manage_object (T2) + common (T1).
...                 NEVER touch existing data. Uses a FIXED test code (AUTOTEST_DOCUMENT_TEMPLATE,
...                 matching this round's fixed-code convention) - confirmed absent from
...                 OV_DOC_TEMPLATE before this was wired in. Every run must complete TC05 (delete)
...                 so the code is free for the next run.
...                 EACH test case does its own real Login/Logout on ONE browser opened once in
...                 Suite Setup - not 5 separate browser launches (matches Bank's own convention).
...                 Bank-pattern conversion (2026-08-24): properties-file-driven insert/update/
...                 verify + explicit grid-filter wiring, upgraded from the prior label-driven-only
...                 shape (see docs/ec_screen_registry.md / docs/automation-scorecard.md - this
...                 MODIFIES that existing row, not a new build).
...                 PURE SCREEN verification (matches bank_iud.robot's owner-requested
...                 2026-08-18 convention: no DB check here) - removed the extra inline
...                 DB-read keywords this suite originally had, to match Bank exactly
...                 (2026-08-25 alignment fix).

Resource            ../../../../pageobjects/Configuration/Assets/Revenue_Document_Objects/document_template_page.resource

Suite Setup         Open EC Application
Suite Teardown      Close EC
Test Teardown        Ensure Logged Out From EC Application

Test Tags           iud    document_template


*** Variables ***
${TEST_CODE}        AUTOTEST_DOCUMENT_TEMPLATE
${OBJ_NAME}         AUTOTEST Document Template
${START_DATE}       2000-01-01
${END_DATE}         ${START_DATE}
${OBJ_NAME_UPD}     AUTOTEST Document Template UPDATED


*** Test Cases ***
TC01 Verify Clean State
    Login To EC Application
    Open Document Template Screen
    Verify Document Template Record Does Not Exist
    Logout From EC Application

TC02 Insert Document Template Data
    Login To EC Application
    Open Document Template Screen
    Insert Document Template Record And Save
    Verify Document Template Record Exists
    Logout From EC Application

TC03 Update Document Template Data
    Login To EC Application
    Open Document Template Screen
    Update Document Template Record And Save
    Verify Document Template Record Updated
    Logout From EC Application

TC04 Find Document Template Data
    Login To EC Application
    Open Document Template Screen
    Find Document Template Record
    Verify Document Template Record Found
    Logout From EC Application

TC05 Delete Document Template Data
    Login To EC Application
    Open Document Template Screen
    Delete Document Template Record And Save
    Verify Document Template Record Removed
    Logout From EC Application
