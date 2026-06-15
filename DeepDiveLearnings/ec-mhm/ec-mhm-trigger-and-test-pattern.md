# EC Notification / MHM — Trigger/Delivery Layer + Test-Pattern Blueprint (SME, 2026-06-15)

Phase-1b of the MHM SME deep-dive — the side `ec-mhm-sme.md` was thin on: **how a notification
actually fires and gets delivered**, and **how EC itself tests MHM** (the authoritative blueprint for
my own suite). Sources: EC tech-docs KB (`ec-docs/DOC-03`, `DOC-07`), and **EC's own Selenium test
automation** (`C:\DEV\GIT\ec-application\ectestautomation\...\com\ec\messaging\*`). Companion to
`ec-mhm-sme.md` (model + config→table map + `MHM_MSG` journal oracle).

## 1. The send/delivery engine (DOC-03)
EC ↔ external broker via the **EC MHM adapter** (project-implemented; JDBC/web-services; EC
pushes/pulls because firewalls block broker-initiated). **Send flow:**
`Actors (sender/receiver in contact groups) → Distribution Lists (MHM.0001) → Message Definition
(CO.0142; handling = manual / semi / auto) → Message Distribution → SEND`. Formats: Text / XML / EDI /
Body Text. Free-text body templates (CO.0144). This is the engine behind the morning-briefing email.

## 2. The THREE trigger paths (how a message gets sent)
1. **Manual / semi** — the **Send Freetext Message** screen (page object `SendFreetextMessagePage`:
   `nav` form + `template` form + **`SendButton`**). A human composes + sends; lands in the journal.
2. **Scheduled / automatic** — a **schedule** wired with the **`MessagesSend` + `SendMail` business
   actions**. This runs on the **ec-worker scheduler node** — the *same executor* I cracked for N3
   (status processes). So an auto-notification depends on ec-worker RUNNING, exactly like N3.
3. **Event-driven** — **Event Route Configuration (CO.1081)** / **Schedules → Event Subscriptions
   (CO.0130)**: filter on event params (e.g. `className=…`) → fire an outbound bridge / mail. SMTP via
   **Remote Endpoint Configuration** (secret stored write-only). This is the JSF event-route layer
   (DOC-07), not a classic OV screen. `N_R_D_VALIDATION_REVIEW` is this kind (validation event → notify).

## 3. EC's own MHM test blueprint (authoritative — mirror this)
EC ships Selenium tests for MHM (`ectest-ui/.../com/ec/messaging/`), which ARE the canonical pattern:
- **`OutgoingMessagesFreeText`** (test steps) — the end-to-end gesture: `createMessageType` (CO.0142:
  Code/Name/Subject/Handling/Internal Format/Frequency/Direction/Functional Area/Default Sender) →
  `createMessageFormat` (CO.0143) → `createMessageSubject` → **send** via `SendFreetextMessagePage`
  (`SendButton`) → **verify** via `MessageJournalPage`.
- **`MessageJournalPage`** (the oracle surface): grid id **`journal`**; buttons View Original /
  Converted / Attachment / Log; **`viewMessageAndVerifyContent(original, content)`** opens a journal
  message and asserts the page source contains the expected content. → UI oracle = the journal grid;
  **DB oracle = a new `MHM_MSG` row** (DIRECTION/MSG_TYPE/STATUS/SUBJECT/RECIPIENT).
- Siblings: `OutgoingMessagesReportTest`, `IncomingMessagesProcessingTest`, `MessageJournalTest` (iud).

## 4. ✅ Upgraded feasibility — the GENERIC pattern IS buildable here
`ec-mhm-sme.md` found the *Pluto* notification (`N_R_D_VALIDATION_REVIEW`) absent from this sandbox.
But the **generic MHM send→journal flow is fully present + testable** here: the config screens
(Message Type/Format/Template/Distribution), the **Send Freetext** screen, and the **`MHM_MSG`
journal** all exist (EC's own tests exercise exactly this). So I can build a **provable "N-notify"
pattern** now, on generic/free-text config, and **swap in the client's Message Type when a client env
is available** — the mechanism (send → journal-delta oracle) is identical.

## 5. Build-ready "N-notify" pattern (next increment)
- **T2** `resources/message_send.resource`: set Send-Freetext nav + template, click `SendButton`, wait.
- **T3** page object: Send-Freetext screen + the Message Journal (`journal` grid) for the scope.
- **Suite**: baseline `MHM_MSG` count for the Message Type → send a free-text message → assert a NEW
  `MHM_MSG` row (delta +1) with the expected SUBJECT/RECIPIENT/STATUS (+ UI: journal shows it). Append-
  only audit table → scope by delta, no destructive clean (mirrors `STAT_PROCESS_STATUS`).
- **DbVerify**: `message_journal_count(msg_type)` + `message_journal_latest(msg_type)`.
- ⚠️ If using an **auto/scheduled** send, it needs **ec-worker RUNNING** (same as N3); the **manual
  Send-Freetext** path avoids that and is the cleanest first build.

## 6. SME status — Notification/MHM now END-TO-END
Model + config→table map + **3 trigger paths** + the **`MHM_MSG` journal oracle** + EC's own test
blueprint = expert-level. Buildable generic pattern identified; client-specific notification swaps in
at the client env. This is the reusable answer for any future SOW notification requirement.
