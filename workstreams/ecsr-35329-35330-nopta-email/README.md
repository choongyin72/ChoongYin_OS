# ECSR-35329 / ECSR-35330 — NOPTA Reports Email-Send Enablement

Enable email-send (EC MHM message-distribution) for the two NOPTA reports on **COPSDEV**, for Grant Hewton's
code review + UAT. Built/verified in ChoongYin_OS; **final delivery to the Woodside repo is via the client's
own PR** (never direct-commit; team sets the final Flyway filename under `Pluto_Config/020_Configuration`).

## Contents
| Path | What |
|---|---|
| `sql/V1.0.39.0020.0001__ECPR-31089__R_PLU_NOPTA.sql` | Pluto NOPTA email config — REPORT/XML → **TEXT**, non-destructive (idempotent, REV_TEXT) |
| `sql/V1.0.39.0020.0002__ECPR-31090__R_SCA_NOPTA.sql` | Scarborough NOPTA email config — **fresh build**, clone of 31089 (idempotent, REV_TEXT) |
| `UT/UT_ECPR-31089.docx` | 11-screen UAT evidence (R_PLU_NOPTA) |
| `UT/UT_ECPR-31090.docx` | 11-screen UAT evidence (R_SCA_NOPTA) |
| `UT/screens/`, `UT/screens_sca/` | Source screenshots for the two UT docs |
| `ANALYSIS.md` | Up-front analysis (tickets, MHM mechanism, hypotheses) |
| `RETROSPECTIVE.md` | What was delivered, findings, what went well/wrong, improvements |

## Status (2026-06-22)
Both reports **COMPLETE**: SQL + config applied & DB-verified on COPSDEV + UT docs. Outgoing message reaches
MESSAGE_OUT as TEXT to `prodreporting@woodside.com`, Status ERROR (no SMTP on COPSDEV, by design for UAT).
Ready for hand-off to Grant → Pluto PR. Branch: `feature/ecsr-35329-35330-analysis`.

## Key design points for the reviewer
- **Non-destructive conversion** (R_PLU): keep the legacy XML format row (demoted; pinned by FK_MESSAGE_OUT_4),
  add TEXT as default, flip distribution + recipients FORMAT_CODE to TEXT in place. No DELETEs.
- **Recipients/sender**: R_PLU unchanged (plutohubpas → prodreporting); R_SCA mirrors R_PLU (per user decision).
- **Subjects cleaned**: "Pluto/Scarborough Upstream NOPTA Report for Production Date".
