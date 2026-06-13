# Pluto As-Built 11 — Notifications / MHM (deep dive, 2026-06-11 doc, read 2026-06-13)
Source: `WSPLU_EC_AsBuilt11_Notification_v1.0.docx` (V1.0, 22pp, Grant Hewton + Simon Lee).
The missing module in my map: how EC tells a human "something needs you." Closes the loop on
the daily/monthly flow (As-Built 14) — every QC checkpoint, validation failure, and approval
gate fires a notification through here.

## The two notification types EC generates
1. **Email** — via the **Message Handling Module (MHM)**. Manual or BPM/trigger-fired. Each
   notification type ↔ an EC **Message Type**; each recipient user must be registered in MHM
   (Actor + Message Contact) and added to a **Distribution List** to receive mail.
2. **To-do task** — appears on the **TODO screen** + the **bell icon** in the main menu. Users
   claim / work / create / complete / assign tasks. This is the in-app work-queue half.

Most in-scope notifications are BOTH ("EC screen notification / EC Todo List item / Email") — the
task lands in the assignee's Todo list AND an email goes to their distribution list.

## MHM configuration screens (the email plumbing) — NEW screen codes
| Screen | Code | Role |
|---|---|---|
| User Maintenance | CO.1000 | EC user accounts |
| Maintain Contact Group Set | CO.0225 | "Woodside Pluto Hub Contact Group Set" default |
| Maintain Message Type | CO.0142 | message type + dynamic-param subject (`$shipper$` → "BP") |
| Message Format | CO.0143 | format definition |
| Freetext Message Template | CO.0144 | email **body** template + placeholders (`{production_date}`) |
| Actor Maintenance | MHM.0012 | register each user as a Message Contact (Contact Code **1:1** with User ID — keep them equal) |
| Distribution List | MHM.0001 | role → from/to email mapping |
| Message Distribution | MHM.0004 | bind Message Type → Distribution List / Report |
| Message Journal | MHM.0007 | **audit log of every message handled** (the DB-verify oracle for notification tests) |

**SMTP endpoint**: configured on **Remote Endpoint Configuration** (reached via **Event Route
Configuration** → External Webhook → `endpointconfigcode` dropdown → `default-smtp-endpoint`).
Password write-only (hidden after save). This is the JSF event-route layer, not a classic OV screen.

## Pluto Distribution Lists (Table 1) — role → mailbox routing
8 lists, all FROM `plutopasprod@woodside.com`:
`DL_PLU_DL_01` OPERATOR · `_02` EMISSIONS · `_03` ALLOC_PROC · `_04` SUPERVISOR ·
`_05` SUPPORT_ADMIN · `_06` QMI_ROLE · `_07` TOPSIDE_SURVEIL · `_08` WELLS_SURVEIL.
→ The notification recipients ARE the role taxonomy. Useful for understanding who-does-what in
the daily flow (e.g. ALLOC_PROC owns allocation, WELLS/TOPSIDE_SURVEIL approve monthly results).

## Notification catalog — scope reality (IMPORTANT for test planning)
The doc lists 26 notifications but almost all are **<descoped>** or **<Phase 2>**. Only ONE is
live **<new scope>** for the current build:
- **N_R_D_VALIDATION_REVIEW** `<new scope>` — "EC/PAS – Review Daily Validation Report".
  Fires when a Todo task is created/assigned; emails the assignee. **This is the only active
  notification** → ties directly to Issue_1052 (daily validation → analyst review).

**Descoped** (daily/monthly validation + allocation BPM alerts — built into product but OFF for
Pluto now): N_DAILY_DATA_INVALID, N_MONTHLY_DATA_INVALID, N_SWING_WELL_EVENT,
N_BPM_DAILY_ALLOC_FAIL, N_BPM_MONTH_ALLOC_READY, the 4 N_BPM_*_REVIEW_*_ALLOC, N_BPM_MTH_ALLOC_FAIL.

**Phase 2** (the future approval-workflow stack — verify/approve daily+monthly asset & allocation
reports, lock data, role-based monthly sign-off): N_TASK_OPEN_OPR, N_VER/APP_R_D_PLU(_PA),
N_BPM_DAY_REVIEW (V_SAMPLING_VALIDATION), N_V_ALLOC_RES, N_APP_MTH_PROV/_R_MTH_PROV/_MTH_FINAL,
N_LOCK_DATA, and the role-specific monthly approvals N_QMI/TOP/WEL_APP_MTH, N_REP_EMAIL.

→ The Phase-2 list is effectively a **spec for the monthly governance workflow** (As-Built 14
QC4): data → verify → approve (provisional) → approve (final) by QMI + Topside + Wells surveillance
→ lock. Each step has a named notification waiting to be switched on.

## Update processes (how config is maintained)
- **Add a Distribution List email**: first create the Message Contact in Actor Maintenance
  (MHM.0012), then add it to the list (MHM.0001).
- **Change Message Distribution**: on MHM.0004, bind/rebind the Distribution List or Report to a
  Message Type (every outbound notification/interface/report has a Message Type).
- Subject lines support **dynamic placeholders** (PARAM substitution) — e.g. report name, shipper.
- Body templates (CO.0144) substitute `{production_date}` etc. with the report date.

## Test-case angle (no technical testing planned by project, but for MY suite)
- **N_R_D_VALIDATION_REVIEW is the only testable live notification** → an integration test would:
  trigger a daily validation failure (Issue_1052 rule) → assert a Todo task is created for the
  assignee → assert a row in **Message Journal (MHM.0007)**. DB oracle = the journal table.
- The MHM config screens (MHM.0001/0004/0012, CO.0142/0143/0144) are **OV/TV-style config** →
  reachable with existing patterns if a master-data IUD test is ever wanted; but they're support
  config, low business-test value vs. the N1 status grids.

## Where this fits the capstone chain
Notifications are the **human-in-the-loop signalling layer** that wraps the whole flow:
`VALIDATE → (N_R_D_VALIDATION_REVIEW Todo+email) → analyst fixes → re-run`, and in Phase 2 the
`REPORT → verify → approve → lock` governance gates each fire a notification. MHM Message Journal
is the audit trail. Module deep dive: COMPLETE (reference-grade; only 1 live notification today).
