*** Settings ***
Documentation       T3 (screen) — "Send Freetext Message" (MHM) page object — the N-notify pattern
...                 (the FIRST messaging/notification test, vs the N1/N2/N3 data-grid/run patterns).
...                 Send a freetext message via stock EC MHM, then DB-verify it journaled to MHM_MSG.
...                 Stock-MHM model (present in this sandbox); the same pattern maps to client
...                 implementations by swapping the table/action (AOPA stock MESSAGE_OUT, CLP custom
...                 ZXC_T_NOTIFICATION). See DeepDiveLearnings/ec-mhm/.
...
...                 ⚠️ SAFETY (outbound email): SEND ONLY through a distribution whose recipients are
...                 NON-DELIVERABLE test addresses (an `@example.invalid` test distribution). The stock
...                 FRMW free-text distribution resolves to a REAL domain (@energycomponents.com) — do
...                 NOT use it for a live send. ${SAFE_DISTRIBUTION} below is a placeholder that must be
...                 created (a test distribution with one `.invalid` contact) before the live run.
...                 Oracle = MHM_MSG journal delta (append-only) — see DbVerify message_journal_* .
...                 Layered: this test → this T3 → message_send (T2) + common (T1) + DbVerify.

Library             Browser
Library             ../../libraries/DbVerify.py
Resource            ../../resources/message_send.resource


*** Variables ***
${MSG_SCREEN}             Send Freetext Message
# Scope — a FREETEXT message type exists in the sandbox (MHM13_FREETEXT).
${MSG_TYPE}               MHM13_FREETEXT
# ⚠️ SAFE distribution placeholder — must be a test distribution whose only contact is an
# `@example.invalid` (non-deliverable) address. NOT the stock FRMW set (real @energycomponents.com).
${SAFE_DISTRIBUTION}      AUTOTEST_FREETEXT_INVALID
${MSG_DATE}               2024-02-06
${MSG_SUBJECT}            AUTOTEST N-notify freetext
${MSG_BODY}               Automated MHM journal test — safe, non-deliverable recipient.
${MSG_BASELINE}           ${0}


*** Keywords ***
Open Send Freetext Screen
    [Documentation]    Suite Setup: launch, login, open the Send Freetext Message screen.
    [Arguments]    ${user}=${EC_USER}    ${pass}=${EC_PASS}
    Launch EC And Open Screen    ${MSG_SCREEN}    ${user}    ${pass}

Capture Journal Baseline
    [Documentation]    Record the current MHM_MSG outbound count for the message type (append-only
    ...    journal → a +1 delta after the send proves a fresh message was journaled).
    ${n}=    Message Journal Count    ${MSG_TYPE}    O
    VAR    ${MSG_BASELINE}    ${n}    scope=SUITE

Send Freetext Notification
    [Documentation]    Send a freetext message to the SAFE distribution. ⚠️ Live send only — ensure
    ...    ${SAFE_DISTRIBUTION} resolves to a non-deliverable `.invalid` recipient first.
    Set Message Send Navigator    ${MSG_DATE}    ${MSG_TYPE}    ${SAFE_DISTRIBUTION}
    Fill Freetext Body    ${MSG_SUBJECT}    ${MSG_BODY}
    Send Message

Journal Should Have New Message
    [Documentation]    DB ground truth: MHM_MSG gained a new outbound row for the message type
    ...    (delta over the captured baseline) — the send was journaled.
    Message Journal New Row Should Exist    ${MSG_TYPE}    ${MSG_BASELINE}    O
