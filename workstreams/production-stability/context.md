# Production Stability — Context (as of 2026-06-02)

## Open issues
| Ticket | Description | Priority | Status |
|--------|-------------|----------|--------|
| ECSR-35019 | Pluto Scarborough Daily Asset Report — UAT issue | P2 | Fix bundled into Wave 03 |
| ECSR-35042 | Burrup LNG Park Monthly Allocation — GHG shows 0 | P2 | Interim fix in ECPR-31019 (merged) |
| (no ticket) | R_BLP_MONTHLY_ALLOC_PLUTO direct customer view query | P2 | **Needs ECPR ticket — Simon Lee flagged ASAP** |

## PCI Wave 1 UAT
- Simon Lee (2026-05-15): UAT issues must be prioritised
- Tahura Anjum Shaikh coordinating — UAT fix bundling in progress

## Architecture rule breach (ATTENTION)
- Simon Lee flagged `R_BLP_MONTHLY_ALLOC_PLUTO` queries `ZWP_V_REP_BLP_MTH_ALLOC` directly
- Must refactor: create CLASS on top of the view, never query customer view directly
- No ECPR ticket raised yet — **action needed**

## Sources
- Teams: Pluto SuperFriends Extended (Simon Lee directives on architecture)
- JIRA: energycomponents.atlassian.net/browse/ECSR-XXXXX
- Email: Bitbucket PR notifications (PR approvals / rejections)
