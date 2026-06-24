# ECSR-35263 & ECSR-35264 — SCA email enablement (analysis)

_Read-only recon vs `plutodev` (COPSDEV), 2026-06-23. Build in ChoongYin_OS; CY delivers to Pluto repo (develop). Model = `workstreams/ecsr-35329-35330-nopta-email/sql`._

## Tickets (both Critical / UAT_BLOCKER / SCA_STARTUP, reporter Ruchi Doval, assignee CY)
- **ECSR-35263 (Issue_1044A)** — enable ECaaS email for **Scarborough Upstream Daily Partner Report**; reuse subject/template/distribution from **Pluto Upstream Daily Partner Report**. Bug (22-Jun): sent for 18-Jun then 12-Jun separately → email subject/body/date show 18-Jun but the **attached report is 12-Jun** (stale envelope vs attachment).
- **ECSR-35264 (Issue_1044B)** — enable ECaaS email for **Burrup LNG Park Daily Production Report (Scarborough)**; reuse from Pluto Burrup report. Ruchi: "incomplete config — no separate ACTOR Maintenance for Scarborough." **Decision (Ruchi 23-Jun): 2 SEPARATE contact groups** (Scarborough vs Pluto). CY plan: fix the **Pluto** set first (`R_BLP_DAILY_PROD_ALLOC_PLUTO`), then **clone** to a new **Scarborough** set (`R_BLP_DAILY_PROD_ALLOC_SCA`).

## MHM config chain (per NOPTA template ECPR-31089) — idempotent update-insert + REV_TEXT
`OV_CONTACT_GROUP_SET` → `OV_CONTACT_GROUP` (ACTOR Maintenance) → `OV_MESSAGE_CONTACT` (FROM/TO/CC) →
`OV_MESSAGE_DEFINITION` (subject, TEXT format) → `DV_MESSAGE_FORMAT` (TEXT default) →
`DV_MSG_FREE_TEXT_TEMPLATE` (**subject/body with `{production_day}` placeholder**) → `TV_DISTRIBUTION_SET` →
`TV_DISTRIBUTION_SET_CONTACT` (FROM/TO/CC) → `DV_MESSAGE_DISTRIBUTION` → `TV_MESSAGE_DISTR_PARAM` (Report Name) →
`TV_MESSAGE_DISTR_CONN`.

## RECON — current state on plutodev

### ECSR-35264 (Burrup Daily Production) — messy SHARED config + data defects
- `OV_MESSAGE_DEFINITION`: `R_BLP_DAILY_PROD_ALLOC_PLUTO` = **clean reference** (subject "Burrup LNG Park Daily Allocation Statement for Production Date"; free-text subject has `{production_day}`; body "...(Pluto)..."). `R_BLP_ DAILY_PROD_ALLOC_SCA` = **BROKEN**: ⚠️ embedded **space in CODE & NAME**; free-text subject **missing `{production_day}`**; body says generic **"Pluto Hub - Daily Asset Report"** (wrong); shares `COMPANY_CONTACT_CODE = DMS_R_BLP_DAILY_PROD_ALLOC` with Pluto.
- `OV_CONTACT_GROUP_SET`: only ONE — `R_BLP_DAILY_PROD_ALLOC_PLU` (note `_PLU`, generic name "Burrup LNG Park Daily Production Report"). **No Scarborough set** ← Ruchi's complaint.
- `OV_CONTACT_GROUP` (ACTOR Maintenance): only ONE — `R_BLP_DAILY_ALLOC` (name `PHBR-R_BLP_DAIY_PROD_ALLOC_PLU` — ⚠️ "DAIY" typo; set `R_BLP_DAILY_PROD_ALLOC_PLU`).
- `TV_DISTRIBUTION_SET`: only ONE — `R_BLP_DAILY_PROD_ALLOC`.
- `TV_DISTRIBUTION_SET_CONTACT` (R_BLP_DAILY_PROD_ALLOC): CC=INT_R_BLP_DAILY_PROD_ALLOC; FROM=DMS_R_BLP_DAILY_PROD_ALLOC; TO=`INT_R_BLP_DAILY_PROD_ALLOC 1` (⚠️ space); TO=EXT_R_BLP_DAILY_PROD_ALLOC.
- `OV_MESSAGE_CONTACT` (group R_BLP_DAILY_ALLOC): FROM `DMS_...` = WBOperator@woodside.com.au; INT = prodreporting@woodside.com; `INT_..._ALLOC 1` (⚠️ space) = PASReportPJVInternal@woodside.com; EXT = PASReportPJV@woodside.com; EXT_1 = pluto@kepha.au; EXT_2 = PlutoOperationsReport@midoceanenergy.com.
- **Data defects to fix in rebuild:** space-in-code (`R_BLP_ DAILY_PROD_ALLOC_SCA`, `INT_..._ALLOC 1`); `_PLU` vs `_PLUTO` inconsistency; `DAIY` typo; SCA missing `{production_day}` + wrong body.

### ECSR-35263 (SCA Upstream Daily Partner) — ⚠️ NOT on plutodev
- Search for SCA/Scarborough/PARTNER returned only: `R_PLU_DAILY_PARTNER` (clean reference), `R_PLU_SCA_DAILY_ASSET` (different report — "Pluto/Scarborough Daily Asset"), `R_SCA_NOPTA`, and the broken `R_BLP_ DAILY_PROD_ALLOC_SCA`.
- **There is NO `R_SCA_DAILY_PARTNER` (or any SCA Upstream Daily Partner) message definition on plutodev.** The config Ruchi tested (and the 18-Jun/12-Jun bug) is likely on **ECaaS TEST only**, OR under a code not yet identified. **BLOCKER — need to confirm the env/code before fixing 35263.**
- Reference `R_PLU_DAILY_PARTNER`: subject "Pluto Upstream Daily Partner Report for Production Date"; free-text subject "Pluto Upstream Daily Partner Report {production_day}"; FROM=WBOperator; recipients INT (prodreporting), INT_1 (PASReportPJVInternal), EXT (PASReportPJV), EXT_1 (pluto@kepha.au), EXT_2 (midoceanenergy).

## Plan
**35264 (buildable now):** (a) clean/normalise the **Pluto** set (`R_BLP_DAILY_PROD_ALLOC_PLUTO` def + a properly-named Pluto contact-group-set / ACTOR Maintenance / distribution); (b) **clone** to a new **Scarborough** set `R_BLP_DAILY_PROD_ALLOC_SCA` (fix space-in-code, add `{production_day}`, correct body to "Burrup LNG Park Daily Production Report (Scarborough)", own contact-group-set + ACTOR Maintenance + distribution + recipients). Idempotent update-insert + REV_TEXT, non-destructive to PROD.
**35263 (blocked):** confirm where the SCA Upstream Daily Partner config lives + its code; then clone `R_PLU_DAILY_PARTNER` and fix the production-date binding so subject/body match the attachment per send.

## RECON — ECaaS TEST (QDB) — AUTHORITATIVE (where Ruchi tested)
_Envs diverge: plutodev is broken/stale; ECaaS TEST is the cleaner, current state._

### ECSR-35263 — config is CORRECT on TEST -> the bug is NOT config
- `R_SCA_DAILY_PARTNER` message def EXISTS; `OV_CONTACT_GROUP_SET` has its OWN `R_SCA_DAILY_PARTNER` set (separate from Pluto).
- `DV_MSG_FREE_TEXT_TEMPLATE`: subject = "Scarborough Upstream Daily Partner Report for Production Date - {production_day}"; body has `{production_day}` too. **Placeholder present & correct.**
- => The 18/12-Jun "email date vs attachment date" mismatch on sequential sends is a **report/message-GENERATION behaviour** (stale `{production_day}` binding vs the generated attachment), **NOT a config defect**. A config SQL will NOT fix it. Needs generation-side investigation + an ECaaS TEST repro. **Do NOT rush into tomorrow's config deploy.**

### ECSR-35264 — precise gap on TEST = no separate SCA contact set
- `OV_MESSAGE_DEFINITION`: BOTH `R_BLP_DAILY_PROD_ALLOC_PLUTO` and `R_BLP_DAILY_PROD_ALLOC_SCA` exist (clean codes on TEST, no space), BUT **both share `COMPANY_CONTACT_CODE = DMS_R_BLP_DAILY_PROD_ALLOC`**.
- `OV_CONTACT_GROUP_SET`: only `R_BLP_DAILY_PROD_ALLOC_PLU` (generic name); **NO `R_BLP_DAILY_PROD_ALLOC_SCA` set** -> exactly Ruchi's "can't find ACTOR Maintenance for Scarborough."
- => Fix = normalise the Pluto set (`_PLU`->`_PLUTO`, name "(Pluto)") + create a **separate** `R_BLP_DAILY_PROD_ALLOC_SCA` contact-group-set + ACTOR Maintenance (OV_CONTACT_GROUP) + sender/recipients (OV_MESSAGE_CONTACT) + distribution set + recipients, and **re-point the SCA message def's COMPANY_CONTACT_CODE + distribution** to the new SCA set. Idempotent, non-destructive. **Fully buildable now.**

## ECSR-35263 ROOT CAUSE (confirmed via code + MESSAGE_OUT data)
- Evidence: 2 consecutive SCA Daily Partner sends on TEST (22-Jun 11:45 & 13:26) BOTH have subject "...18 Jun 26".
- Code: `ZWP_P_MAIL_UTIL.getReportDate(p_message_code)` (R__0500_ZWP_P_MAIL_UTIL_body.sql:459) resolves the date by
  **template TYPE** — `SELECT report_date FROM tv_report_generated WHERE zwp_template_code = p_message_code AND
  send_date IS NOT NULL ORDER BY created_date DESC` (ROWNUM=1) → returns the **most-recent report of that type**.
- `updateMsgOutFromMsgTemplate` (line 429) + `updateMHMFromMsgTemplate` (lines 384-385) loop per message but call
  `getReportDate(msg_type)` → stamp that ONE date into `{production_day}` for the SUBJECT/BODY of EVERY message of
  the type. Attachment keeps its own (correct) date → **subject/body date != attachment date**.
- **FIX:** resolve the date **per message instance**, not per type — e.g. new overload `getReportDate(p_msg_type,
  p_message_no)` that joins the message's OWN attached report (`MESSAGE_ATTACHMENT.REPORT_NO -> tv_report_generated.report_date`
  for that MESSAGE_NO), and call it in both refresh procedures. This is a **base-package (ZWP_P_MAIL_UTIL) code fix**
  delivered via the Pluto repo — it fixes ALL report emails (Pluto/SCA/Burrup/NOPTA), so it needs an ECaaS TEST repro
  (generate 2 dates, confirm distinct subjects) before delivery. NOT a config script.

## Decision (2026-06-23): 35264 = config clone (buildable now). 35263 = ZWP_P_MAIL_UTIL per-message date fix (code, needs TEST repro).

## Open questions for CY
1. **35263:** where is the SCA Upstream Daily Partner email config (ECaaS TEST only? what code?) — or do we create `R_SCA_DAILY_PARTNER` fresh by cloning `R_PLU_DAILY_PARTNER`? And is the 18/12-Jun bug config or a report/message-generation timing issue (may need ECaaS TEST repro)?
2. **35264 cleanup scope:** fix the data defects (space-in-code, `_PLU`→`_PLUTO`, `DAIY` typo) in the rebuild — yes?
3. **New SCA recipients:** seed the Scarborough set's FROM + a placeholder TO and let Woodside set real recipients via ACTOR Maintenance, or clone Pluto's recipient addresses as-is?
