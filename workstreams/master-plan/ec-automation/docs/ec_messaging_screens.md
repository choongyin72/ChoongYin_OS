# EC Messaging / MHM screen characteristics (learn-once reference)

> **CHECK THIS FIRST before automating any messaging/MHM screen — do NOT trial-and-error.**
> Captured live from `app-plutodev` (COPSDEV), 2026-06-24. Used for the NOPTA + ECSR-35264 UT screenshot capture.
> These are the 11 screens of the standard email-enablement UT doc (model: `workstreams/ecsr-35329-35330-nopta-email/UT/UT_ECPR-31089.docx`).

## Common
- **Login:** `https://app-plutodev.woodside-pluto.tieto-og.cloud/` — user `Sysadmin` / `Sysadmin@01` (fields `#username`,`#password`,`#kc-login`).
- **Open a screen:** type into `#menu:searchForm:searchTxt`, then click `xpath=//*[contains(@class,"tv-link") and normalize-space(text())="<Screen>"]`.
- **Content lives in an iframe** — find the frame containing `[id^="nav:"]` or `[id*="sfilter"]` or `[id*=":form:T:"]`.
- **Navigator (where present):** Date input `nav:form:G:*:R:*:C:*:da_input`; **Functional Area dropdown — find generically** `[id^="nav:"][id$="dd_button"]` (its id VARIES per screen, see table), panel = that id with `_button`→`_panel`, pick `xpath=//*[@id="<panel>"]//tr[normalize-space(@data-item-label)="EC"]`; **GO** = `[id="button:form:B"]`.
- **Column filter:** `<prefix>:form:T:sfilter0_ft_filter` (text filter) — fill the code + press Enter. Some columns are combo filters (`..._cb_filter`).
- **Select a record:** click the grid row `xpath=//tr[.//text()[contains(.,"<code>")]]` → the detail form / recipients load below.

## Per-screen map (verified ids)
| # | Screen | Frame module | FA dropdown button | GO | Primary filter id (column) | Key buttons |
|---|---|---|---|---|---|---|
| 1 | **Maintain Message Type** | `co.screens/manage_object` | `nav:form:G:0:R:1:C:1:dd_button` | `button:form:B` | `manageObject:form:T:sfilter0_ft_filter` (Message Type Code) | NEW VERSION |
| 2 | **Message Format** | `mhm.screens/message_format` | `nav:form:G:0:R:1:C:1:dd_button` | `button:form:B` | **Message Type is a MANDATORY navigator dropdown** `nav:form:G:0:R:1:C:2:dd_button` — set it to the message-def CODE (open dd, pick the row containing the code) BEFORE GO, else "Required fields are empty: Message Type [MESSAGE_TYPE_POPUP]". Grid then shows Format Code=Text | — |
| 3 | **Freetext Message Template** | `mhm.screens/free_text_templ` | `nav:form:G:0:R:1:C:1:dd_button` | `button:form:B` | `subject:form:T:sfilter0_cb_filter` (Message Type, combo) | — |
| 4 | **Maintain Contact Group Set** | `co.screens/manage_object` | `nav:form:G:0:R:1:C:1:dd_button` | `button:form:B` | `manageObject:form:T:sfilter0_ft_filter` (Contact Group Set Code) | NEW VERSION |
| 5 | **Actor Maintenance** | `mhm.screens/actor_maintenance` | `nav:form:G:1:R:1:C:0:dd_button` | `button:form:B` | grid loads after FA+GO (no sfilter pre-load; pick a contact group first) | — |
| 6 | **Distribution List** | `mhm.screens/distribution_list` | `nav:form:G:1:R:1:C:0:dd_button` | `button:form:B` | `list:form:T:sfilter0_ft_filter` (Distribution List Code) | — |
| 7 | **Message Distribution** | `mhm.screens/message_distrib` | `nav:form:G:1:R:1:C:0:dd_button` | `button:form:B` | `manageObject:form:T:sfilter0_ft_filter` (Message Type) [+sfilter1 Format, sfilter2 Subject, col Set] | — |
| 8 | **Report Administration** | `report.screens/report_admin` | `nav:form:G:0:R:1:C:1:dd_button` | (no `button:form:B`; use its own Go/refresh) | `runable_reports:form:T:sfilter0_ft_filter` (Name) | **GENERATE**, **VIEW**, (SEND on the messages tab) |
| 9 | **Schedules** | `co.screens/create_and_maint` | `nav:form:G:0:R:0:C:1:dd_button` (FA optional) | `button:form:B` | `schedule:form:T:sfilter0_ft_filter` (Name) [sfilter1 Description] | **RUN NOW** |
| 10 | **Outgoing Messages** | `mhm.screens/outgoing_messages` | — (no navigator; loads directly) | — | `outmess:form:T:sfilter0_ft_filter` (Message Id) [sfilter1 Type combo, sfilter2 Subject] | SELECT ALL, **VIEW**, VIEW ATTACHMENT, VALIDATE, SEND |
| 11 | **Preview** | (rendered message) | — | — | from Outgoing Messages → select row → **VIEW**; or verbatim from `MESSAGE_OUT.SUBJECT` + `MESSAGE_DRAFT` | — |

## Notes
- FA dropdown grid-index differs by screen family: CO manage-object = `G:0:R:1:C:1`; MHM (actor/dist/msg-dist) = `G:1:R:1:C:0`; Schedules = `G:0:R:0:C:1`. **Find it generically** (`[id^="nav:"][id$="dd_button"]`) rather than hardcoding.
- The grid/column-filter only appears AFTER Functional Area is set + GO is clicked (except Outgoing Messages, which loads directly).
- Verbatim rendered email = `MESSAGE_OUT.SUBJECT` + `MESSAGE_OUT.MESSAGE_DRAFT` (join `REPORT_SEND_LOG`→`TV_REPORT_GENERATED` for the report date).
