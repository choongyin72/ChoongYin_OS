# Reporting — Context (as of 2026-06-02)

## Current focus
- **ECPR-31034** (active): Email functionality from ECaaS for Scarborough Upstream Monthly Production Allocation Report. Known bug: user entered space in message code type for R_BLP_DAILY_PROD_ALLOC_SCA — being resolved.
- **ECPR-31024** (merged): ENERGY_MMBTU_LA in lifting section for Burrup LNG Park Monthly Allocation

## Architecture debt — open
- `R_BLP_MONTHLY_ALLOC_PLUTO` was querying `ZWP_V_REP_BLP_MTH_ALLOC` directly
- Simon Lee directive (2026-05-19): create CLASS on top — no direct customer view queries
- **Status: Open — needs ECPR ticket raised**

## Wave delivery status
- Wave 01: ST done, Woodside in UAT
- Wave 02: Active development
- Wave 03: UAT fix bundle — Pluto Scarborough Daily Asset Report fixes included here (not shipped separately)

## Test data needed
- Wave 2 test data: SCA + T2 data required, including Pluto Wells + Pluto data for June
- Grant Hewton requested Cato Johansen + Simon Lee to prepare — check if ready

## Sources
- Teams: Pluto SuperFriends Extended (architecture direction from Simon Lee)
- SharePoint: Weekly SteerCo delivery progress decks
