*** Settings ***
Documentation       T2 pattern — N-notify: send a message via the EC MHM "Send Freetext Message"
...                 screen, to be DB-verified in the Message Journal (MHM_MSG). Cross-screen MHM
...                 send mechanics live here; the screen NAME + scope (functional area, message type,
...                 subject, body) + the journal oracle live in the T3.
...
...                 Send gesture (DB-/UI-verified 2026-06-15 against the live screen):
...                 navigator `nav:form` — Date (G:0:R:1:C:0:da_input) + Functional Area
...                 (G:0:R:1:C:1:dd) + Message Type (G:0:R:1:C:2:dd) + Subject (G:0:R:1:C:4:dd) →
...                 GO `button:form:B` → edit the Template body (`template:form:G:0:R:1:C:0:ta`) →
...                 click SEND (`SendButton:form`). The send JOURNALS to MHM_MSG (the oracle).
...
...                 ⚠️ NO DISTRIBUTION SELECTOR: this screen has no recipient/distribution field —
...                 recipients are fixed by the chosen MESSAGE TYPE's wiring (MESSAGE_DISTRIBUTION →
...                 DISTRIBUTION_SET). The stock FRMW free-text type routes to @energycomponents.com
...                 (a REAL domain), so the live SEND is GATED. To send safely, the message type must
...                 first be wired to a non-deliverable (.invalid) distribution. See the T3 + design doc.

Library             Browser
Resource            common.resource


*** Variables ***
${MSG_DATE_FIELD}          nav:form:G:0:R:1:C:0:da_input
${MSG_FA_DD}               nav:form:G:0:R:1:C:1:dd
${MSG_TYPE_DD}             nav:form:G:0:R:1:C:2:dd
${MSG_SUBJECT_DD}          nav:form:G:0:R:1:C:4:dd
${MSG_GO_BUTTON}           button:form:B
${MSG_BODY_FIELD}          template:form:G:0:R:1:C:0:ta
${MSG_SEND_BUTTON}         SendButton:form


*** Keywords ***
Set Message Send Navigator
    [Documentation]    Set the Send-Freetext navigator — Date + Functional Area + Message Type +
    ...    Subject — then GO to render the Template body. Message Type options cascade from the
    ...    Functional Area, so FA is selected first.
    [Arguments]    ${date}    ${functional_area}    ${message_type}    ${subject}
    Fill EC Date    ${MSG_DATE_FIELD}    ${date}
    Select EC Dropdown Option    ${MSG_FA_DD}    ${functional_area}
    Select EC Dropdown Option    ${MSG_TYPE_DD}    ${message_type}
    Select EC Dropdown Option    ${MSG_SUBJECT_DD}    ${subject}
    Apply Navigator

Fill Message Body
    [Documentation]    Replace the Template body textarea with the test body. The textarea renders
    ...    pre-filled with the message-type's template; Fill EC Field clears + sets the value.
    [Arguments]    ${body}
    Fill EC Field    ${MSG_BODY_FIELD}    ${body}

Send Message
    [Documentation]    Click SEND. The message is journaled to MHM_MSG (assert the journal delta next).
    ...    ⚠️ Live SEND only — recipients are the message type's wired distribution; ensure it is a
    ...    non-deliverable (.invalid) set before running live.
    Click    css=[id="${MSG_SEND_BUTTON}"]
    Wait For Load State    networkidle    timeout=30s
    Sleep    1.0s
