# ECSR-35329 / ECSR-35330 — Enable Email Send for NOPTA Reports — Analysis

_Analysis only. Woodside repo is READ-ONLY; deliver final product via their PR. Work/branch in ChoongYin_OS._
_Branch: `feature/ecsr-35329-35330-analysis`. Date: 2026-06-21._

## The two tickets (Jira, energycomponents.atlassian.net, project ECSR "ECGS Services")
| Ticket | Summary | Type/Pri | Status | Report |
|---|---|---|---|---|
| **ECSR-35329** | Workstream-HIJ: Enable Email send functionality for **Pluto NOPTA Report** | Bug / **Critical** | New | Pluto NOPTA (`R_PLU_NOPTA`) |
| **ECSR-35330** | Workstream-HIJ: Enable Email send functionality for **SCA NOPTA Report** | Bug / **Critical** | Analysis in progress | SCA = **Scarborough** NOPTA |
- Both: component **EC Reports**, labels `PLUTO_UAT / PLU_REPORTS / UAT_Wave_02`, **assignee Grant Hewton**, reporter Swapnil Thakur. 35330 clones 35329; 35329 clones Test ECSR-35313 (email-send for a Burrup LNG Park report — a precedent).
- Ask (both): users can't email the report; **email-send must be enabled** for it. Env = **COPSDEV**.

## What "email send for a report" means in EC / Woodside Pluto
It's the EC **Message-Distribution** framework (NOT the on-screen-only export). Evidenced by
`Pluto_Testdata/.../V1.0.2.0010.0010__ECPR-30103_EMAIL_DIST.sql`, which wires the **Pluto NOPTA** report's email:
1. `OV_CONTACT_GROUP_SET` / `OV_CONTACT_GROUP` — contact groups.
2. `OV_MESSAGE_CONTACT` — sender (`DEFAULT_MAIL_SENDER`, SMTP) + recipient(s) (`WDS_MAIL_01`).
3. `TV_DISTRIBUTION_SET` + `TV_DISTRIBUTION_SET_CONTACT` — the FROM/TO email list (`DL_WDS_EMAIL`).
4. `OV_MESSAGE_DEFINITION` — CODE `R_PLU_NOPTA`, `INTERNAL_FORMAT_TYPE='REPORT'`, `DIRECTION='OUT'`,
   `MESSAGE_HANDLING='AUTO'`, `COMPANY_CONTACT_CODE='DEFAULT_MAIL_SENDER'`.
5. `DV_MESSAGE_FORMAT` + `DV_MESSAGE_DISTRIBUTION` (object_code `R_PLU_NOPTA`, format XML) +
   `TV_MESSAGE_DISTR_PARAM` (Report Name) + `TV_MESSAGE_DISTR_CONN` → links the report distribution to `DL_WDS_EMAIL`.
6. A send schedule/job (the file leaves "SCHEDULE JOB" as a TODO comment).
The email engine itself: `Pluto_Java .../com/ec/woodside/plp/Email/SendNotifications.java`, plus the
`ECPR-30825` email-template/schedule (`ZWP_SEND_EMAIL` / `ZWP_SENDMAIL`) and BPM `EC_CreateEmailNotification`.

## Leading hypothesis (⚠️ NOT yet verified on COPSDEV — must confirm before building)
The Pluto NOPTA email/distribution config exists **only in `Pluto_Testdata`** (ECPR-30103), which is typically
**not applied to COPSDEV** → the `OV_MESSAGE_DEFINITION` / distribution for the NOPTA report is **missing on
COPSDEV**, so the report can't be emailed. The fix = deliver that Message-Definition + Distribution config as
**`Pluto_Config`** Flyway migration(s) for **both** NOPTA reports (Pluto + Scarborough), so it's on COPSDEV.
**This is a hypothesis** — I have not yet read COPSDEV's actual state. Do not treat as fact until verified.

## Proposed approach (subject to verification + answers below)
1. **Verify COPSDEV** current state for both reports: is `OV_MESSAGE_DEFINITION` / `DV_MESSAGE_DISTRIBUTION` /
   distribution-set present? What's the exact delta to enable email-send?
2. Build **`Pluto_Config`** Flyway migration(s) (EC SQL house style — re-runnable, `REV_TEXT`=the ECPR ticket)
   that configure the Message-Definition + Distribution for `R_PLU_NOPTA` and the Scarborough NOPTA report,
   using the **real** distribution list + sender (not the test-data placeholders), mirroring ECPR-30103's shape.
3. Self-verify on COPSDEV (or a safe env): the report's "send by email" path works; capture evidence.
4. Produce the **code (for Grant's review) + a UAT test-evidence document** (per our demo-deliverables practice).
5. Deliver to the Woodside repo only as the final product, via their PR — never direct commit.

## Open questions / things to confirm (for the user / Grant)
1. **COPSDEV DB access** — I need connection details to verify current state (the local sandbox creds don't
   reach COPSDEV). This is the #1 unblocker.
2. **SCA NOPTA report's exact code** — confirm (e.g. `R_SCA_NOPTA`?) and whether its template already exists.
3. **Real email recipients / distribution list** for each NOPTA report (the test data uses placeholder
   `admin@ / sysadmin@quorumsoftware.com`; production/UAT needs the intended NOPTA distribution + a safe UAT
   recipient so we don't send to a real regulator during testing).
4. **The dev change ticket (ECPR)** to use for `REV_TEXT` + the Flyway file name (ECSR are the UAT issues).
5. **Send trigger** — on-demand "Send by email" from the report screen, or a scheduled send? Is a send job needed?
6. **SMTP enabled on COPSDEV?** (and a non-deliverable test recipient for UAT, per the MHM outbound-email gate.)

## Status
Jira read ✅. Repo recon ✅ (READ-ONLY). COPSDEV verification ⏳ (needs access). No code written yet — analysis only.
