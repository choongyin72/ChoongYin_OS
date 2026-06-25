# ECSR-35264 UT docs — reproducible capture

Regenerates `../UT_ECSR-35264__R_BLP_DAILY_PROD_ALLOC_PLUTO.docx` and `…_SCA.docx`
(the 11-screen MHM email-config evidence) from live COPSDEV/plutodev. Field-ids are
**not discovered here** — they come from the learn-once reference
[`workstreams/master-plan/ec-automation/docs/ec_messaging_screens.md`](../../../master-plan/ec-automation/docs/ec_messaging_screens.md).
Consult that first; do not trial-and-error screen locators.

## Prerequisites
- `py` (Python 3.14), `pip install playwright python-docx oracledb`, `playwright install chromium`
- Credentials via **env vars** (never commit them):
  - Web:  `EC_URL` (default app-plutodev), `EC_USER`, `EC_PASS`
  - DB:   `EC_DB_DSN` (default plutodev), `EC_DB_USER` (default ECKERNEL_EC), `EC_DB_PASS`

## Run order
```bash
# 1. Capture the 10 on-screen screenshots per report (headless)
EC_USER=Sysadmin EC_PASS=*** py capture_ut_screens.py pluto
EC_USER=Sysadmin EC_PASS=*** py capture_ut_screens.py sca

# 2. Pull the verbatim rendered subject/body (section 11) -> content.json
EC_DB_PASS=*** py fetch_message_content.py

# 3. Assemble both .docx into ../
py build_ut_docs.py
```

## Notes
- **SMTP is not configured on COPSDEV** → generated outgoing messages sit at Status=ERROR
  (mail is never despatched). That is the expected, safe state; the message is still built
  correctly with the report-specific type, subject and recipients — which is what the UT proves.
- Section 11 (Preview) uses the verbatim `MESSAGE_OUT.MESSAGE_DRAFT` text rather than a screenshot:
  the Outgoing-Messages **VIEW** button opens the plain-text body, which the browser renders as an
  XML-parse error page (not a usable image).
- `shots/` and `content.json` are run artifacts (git-ignored) — the committed evidence is the two
  `.docx` files in the parent folder.
