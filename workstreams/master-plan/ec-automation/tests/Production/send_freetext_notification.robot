*** Settings ***
Documentation       EC N-notify Test — "Send Freetext Message" (MHM) → Message Journal oracle. The
...                 first messaging/notification pattern (alongside N1 edit-grids, N2 calc-runs, N3
...                 status-processes). Sends a freetext message via stock EC MHM and DB-verifies it
...                 journaled to MHM_MSG (append-only delta). Stock-MHM mechanism is present in this
...                 sandbox; the same pattern maps to client implementations (AOPA stock MESSAGE_OUT,
...                 CLP custom ZXC_T_NOTIFICATION) by swapping the oracle table. See DeepDiveLearnings/ec-mhm/.
...
...                 ⚠️ STATUS: BUILD-READY, dryrun-green — the LIVE send is GATED on a safe recipient.
...                 The only stock free-text distribution resolves to a REAL domain
...                 (@energycomponents.com); a live run MUST first point ${SAFE_DISTRIBUTION} at a test
...                 distribution whose contact is a non-deliverable `@example.invalid` address (so no
...                 real email can ever be sent). Also confirm the template:form compose field ids live
...                 on first run. Outbound email is an external action — run live only when safe/approved.
...                 Layered: this test → send_freetext_message_page (T3) → message_send (T2) + DbVerify.

Resource            ../../pageobjects/Production/send_freetext_message_page.resource

Suite Setup         Open Send Freetext Screen
Suite Teardown      Close EC

Test Tags           n_notify    mhm    send_freetext


*** Test Cases ***
TC01 Freetext Send Journals To MHM_MSG
    [Documentation]    Capture the MHM_MSG baseline for the message type, send a freetext message to a
    ...    SAFE (non-deliverable) distribution, and DB-verify a NEW outbound journal row appeared
    ...    (delta) — proving the send→journal mechanism end to end. The journal row is the trustworthy
    ...    oracle (the sandbox journals as PREPARED — no real transmission).
    [Tags]    send
    Capture Journal Baseline
    Send Freetext Notification
    Journal Should Have New Message
    Capture Step    nnotify_tc01_freetext_journaled
