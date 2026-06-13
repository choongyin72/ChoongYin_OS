# ECpedia / EC Knowledge (EFK) — Deep-Dive Self-Learning Series
**Set up 2026-06-13 (user-directed).** Source: **EC Knowledge Home** =
`https://energycomponents.atlassian.net/wiki/spaces/EFK/overview?homepageId=1835010`
(space key **EFK**, home page id **1835010**; cloudId `energycomponents.atlassian.net`).
Access: Confluence MCP (search-first then fetch individual pages — [[feedback_atlassian_confluence_pattern]]).
Run during IDLE time per the standing protocol ([[feedback_never_idle_deep_dive]]); synthesize each
item to a local note here; **commit ONLY inside C:\Projects\ChoongYin_OS** (anything else → ask first,
never silent — user, 2026-06-13).

## Calibration (why the phasing is by value, not by tree order)
EFK is a mixed-age space (2014–2026). Many top-level pages are **empty section containers** or
**links out** to other spaces; several are dated training/ops notes. So this series targets the
**current + domain-rich** pages first and treats the dated/ops/product-internal ones as reference.
(Sampled 2026-06-13: EC Test Automation Framework = EC's *product-internal* Java/Arquillian/Cucumber
stack, not our client RF/Playwright; Hydrocarbon Accounting = concise allocation-network overview.)

## Full inventory — 33 top-level pages (id · last-modified · relevance)
### Phase 1 — Business/domain modules (fills the "what makes a test meaningful" gap) ★ highest
- [~] EC Production `1842679` (2015) — READ: parent is just a DIAGRAM image, no text; value is in children (enumerate later for the production KB)
- [x] Hydrocarbon Accounting `1839786` (2021) — allocation network (fields→wells, custody transfer, fiscal flare metering). READ 2026-06-13 → grounds the N2/HA.0002 allocation track.
- [x] EC Sales `1838256` (2020) — gas sales contracts, nominations/re-nominations, availability. READ 2026-06-13 → `sales-revenue.md`. Thin overview; delivery-attribution = a rules+priority engine (sales analogue of allocation).
- [x] EC Revenue `1840867` (2018) — quantities → monetary value. READ 2026-06-13 → `sales-revenue.md`. BAs CD/IN/FT/QTY/FC/RTY/FI (child ids captured). Oracle ideas: invoice=Σ(qty×price), take-or-pay roll-over, JV/royalty splits=100%.
- [ ] EC Regulatory Reporting `1845940` (2014) — SOX / SEC governance reporting
- [ ] EC Chemistry Management `1853912` (2020) — (link page)
- [ ] EC Environment Management `1851143` (2021) — (link to ECpedia/IH space)
- [ ] EC IAM `1850998` (2020) — Integrated Asset Modelling (link)

### Phase 2 — Calculation / framework depth ★ high (ties to allocation + EC internals)
- [ ] VCF Calculation in EC `1853432` (2023) — tank volume correction, API Ch.12.1 (5-step GSV); recent + concrete
- [x] The calculation engine is in dire need of enhancements `1843903` (2017) — READ → calc-engine-insights.md. GOLD: variable-cache model, DIMENSIONED variables (stream×day×PC×company×product, day/mth) mapping to STRM_DAY_*_ALLOC tables, prorate/rollup/round/recombine ops, IsValid/IsZero hazard, AND the allocation TEST ORACLE (sum-to-total / no-neg / rounding tolerance / multi-grain roll-up) for N2.
- [ ] EC Framework `1854410` (2015) — framework KB parent
- [ ] EC Technology `1853250` (2021) — CTO-team architecture info

### Phase 3 — Reference (consult, don't deep-read)
- [ ] EC Vocabulary `1844980` (2022) — abbreviations/acronyms (ACQ, ACL, …) — cross-check vs my GLOSSARY
- [ ] EC Talks `1837692` (2026.03 — NEWEST) — cross-unit knowledge-sharing talks; scan for current topics
- [ ] EC Product Trainings `1853607` (2021) — training index
- [ ] EC Releases and live assets `1853526` (2024) — version/asset matrix
- [ ] EC Extensions Compatibility Matrix `1851205` (updated ~daily) — extension↔EC compat (CPD-maintained)

### Phase 4 — Operational / how-to (read on-demand when I hit the matching problem)
- [ ] How to Script and Enable a Schedule Job in EC 11.2 `1841913` (2017) — ⭐ relevant to ECIS/scheduler + the stall I hit
- [ ] Stopping a "stuck" EC Service `1841576` (2017) — ⭐ relevant to the scheduler-stall restart
- [ ] How-To Articles `1870006` (2014) · Troubleshooting Articles `1874268` (2015) · Knowledge Sharing `1876514` (2015)
- [ ] Configuring SSL in EC10.X `1835012` (2017) · Improve EC screen performance w/ HTTP compression `1837329` (2015)
- [ ] EC Configuration `1863396` (2014) · Upwards Merge Process `1853137` (2022)

### Phase 5 — Lower value for our goals (skim/skip; reference only)
- [ ] EC Test Automation Framework `1853923` (2020) — EC product-internal Java/Arquillian/Cucumber (not our client RF) — SAMPLED, skip deep read
- [ ] Java Technical Knowledge `1850379` (2023) — Java training (generic)
- [ ] Coding Guidelines - Revised `449708144` (2025) — EC dev coding standards (relevant only if I touch ZWP PL/SQL)
- [ ] Energy Components Footprints `1850480` (2015, video) · Oil and Gas: from exploration to production `1861453` (2015, MOOC) — industry primers (covered via As-Built)
- [ ] Energy Components - Well Profitability `1868866` (2016, video-on-request)
- [ ] Archive `1853319` — outdated by definition

## Execution order (idle sessions)
P1 EC Production (+ children) → EC Sales → EC Revenue → EC Regulatory Reporting → the 3 link pages.
Then P2 VCF + calc-engine critique + EC Framework/Technology. Then P3 reference cross-checks.
P4/P5 only when a matching real problem arises (e.g. read the "stuck service" + "schedule job"
pages next time the scheduler misbehaves). One synthesized note per substantive page; update the
[ ]→[x] boxes + leave a 1-line takeaway. Stop a page if it's an empty container/link-out (note it).

## Progress log
- 2026-06-13: Series set up (this file). Enumerated 33 EFK home children via CQL `parent=1835010`.
  Read Hydrocarbon Accounting (allocation-network frame). Kicked off P1 (see notes below / commits).
- 2026-06-13: P1 EC Sales + EC Revenue read → `sales-revenue.md`. Completes the downstream half of
  the reservoir→revenue chain (Production→Allocation→Sales→Revenue). Both thin overview parents;
  captured capability sets + Revenue BA child ids (CD/IN/FT/QTY/FC/RTY/FI) for on-demand drilling.
  Key learning: sales delivery-attribution + revenue valuation are CALCULATION engines (like N2
  allocation), so meaningful tests are conservation/priority/Σ(qty×price) oracles, not CRUD — and
  all three are contract-driven (need a configured contract as fixture). Next: EC Regulatory Reporting
  `1845940`, then the 3 link pages.
