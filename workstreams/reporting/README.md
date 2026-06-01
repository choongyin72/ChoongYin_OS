# Workstream: Reporting

LNG allocation and production reporting suite for Woodside Pluto / Scarborough.

## Delivery waves
- **Wave 01** — ST complete, Woodside in UAT
- **Wave 02** — MVP Uplift, in development (`Reporting, MVP_Uplift, WAVE02, PLUTO_ST`)
- **Wave 03** — UAT fix bundle (includes Pluto Scarborough Daily Asset Report fixes)

## Architecture rules (Simon Lee — MANDATORY)
1. **Never query directly from customer views** (e.g. `ZWP_V_REP_BLP_MTH_ALLOC`)
2. **Always use a CLASS on top of a custom view** — `TV_ZWP_R_*` classes are correct
3. Direct view queries must be refactored ASAP — raise ECPR ticket if found

## Key contacts
- **Simon Lee** — reporting architecture owner, gives direction
- **Tahura Anjum Shaikh** — delivery / UAT coordination
- **Grant Hewton** — technical oversight

## Reports catalogue
| Report ID | Name | Status |
|-----------|------|--------|
| R_BLP_MONTHLY_ALLOC_PLUTO | Burrup LNG Park Monthly Allocation (Pluto) | Live — architecture fix needed |
| R_BLP_DAILY_PROD_ALLOC_SCA | Daily Production Allocation Scarborough | Active dev (ECPR-31034) |
| — | Scarborough Upstream Monthly Production Allocation | Email feature in dev (ECPR-31034) |
| — | Pluto Upstream Daily Partner Report | ETA was 20 May — check status |
| — | Pluto Scarborough Daily Asset Report | UAT fixes in Wave 03 |
| — | Mass Balance (Pluto) | Live |
| — | Interim reports (Pluto) | Woodside UAT underway |
