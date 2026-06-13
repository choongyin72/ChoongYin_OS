# ECpedia "EC Knowledge" (EFK space) — Full Deep-Dive Plan
User directive (2026-06-13): full deep dive of the EFK space
(https://energycomponents.atlassian.net/wiki/spaces/EFK/overview, homepage 1835010);
"do planning accordingly". Output base folder: `DeepDiveLearnings/ecpedia-efk/`.

> What EFK is: the **EC Knowledge Hub** — Quorum/Tieto's internal functional + domain +
> framework knowledge for the EC PRODUCT (generic, multi-client), distinct from the Pluto
> As-Built (client-specific). Homepage last touched 2018 → treat as FOUNDATIONAL product
> knowledge; cross-check version specifics against EC Tech Docs 14.2.5 + the As-Built.

## Hard rules (carry from the curriculum)
- Confluence access pattern: **search-first / fetch pages individually**; NEVER
  getPagesInConfluenceSpace with contentFormat on this large space ([[feedback_atlassian_confluence_pattern]]).
- Token-aware: synthesize, never transcribe; one section per work block; checkpoint status here.
- No deletes outside the project folder; no commits to remote without explicit OK; sandbox read-only.
- Leave a written artifact per section ([[feedback_never_idle_deep_dive]]).

## Space structure (mapped 2026-06-13, depth 2 — ~100 pages, 12 top sections)
| # | Section (pageId) | Children (highlights) |
|---|---|---|
| 1 | **EC Framework** (1854410) | Calculation Framework, ECIS, BPM, Reporting, Messaging, Logging, EC Core, JSF, Jboss, EC Timezone, Database Sanity |
| 2 | **EC Production** (1842679) | Hydrocarbon Accounting, Assets:Streams, Assets:Wells/Reservoirs, Deferment, Forecast, Operations, Testing, Field Data Capture, AGA 3/8, "Learn about the Oil & Gas Industry", Configurations, Dashboards |
| 3 | **EC Test Automation Framework** (1853923) | TAF Competency trainings |
| 4 | **EC Sales** (1838256) | Sales Allocation, Price Determination, Oil/Gas Sales, Sales Dispatching, training |
| 5 | **VCF Calculation in EC** (1853432) | (volume correction factor) |
| 6 | **EC Revenue** (1840867) | Quantity, Inventory, Financial Transaction, Forecasting, Royalty, Cost Mapping, Financial Item, Scenario Tester, EC-Calculations, Revenue BFs |
| 7 | **EC Regulatory Reporting** (1845940) | — |
| 8 | **EC Chemistry Management** (1853912) | — |
| 9 | **EC Environment Management** (1851143) | EC Calculation training (GHG/NGER — ties to As-Built XEM!) |
| 10 | **EC IAM** (1850998) | identity & access |
| 11 | **EC Support Tools** (1853622) | status sharing |
| 12 | **How-To Articles** (1870006) | ~30 ops/dev how-tos incl. "How to Set up PI DAS and ECIS", treeview SQL, screens, users, Docker/WSL2 |

## Phased reading order (relevance to live work + knowledge gaps first)
**Phase A — directly amplifies my current work**
1. **EC Test Automation Framework** (TAF) — could sharpen my own RF/Playwright framework; small. → `taf.md`
2. **EC Framework › Calculation Framework** — the calc engine behind every allocation/validation; underpins Issue_1052 + As-Built 06. → `framework-calculation.md`
3. **EC Framework › ECIS** + How-To "Set up PI DAS and ECIS" — the real ECIS task's product basis. → `framework-ecis.md`
4. **EC Environment Management › EC Calculation training** — GHG/NGER calc methods (new As-Built scope). → `environment-ghg.md`

**Phase B — product-knowledge backing for my domain syntheses**
5. EC Production (Hydrocarbon Accounting, Deferment, Testing, Field Data Capture). → extend `production.md`
6. EC Sales (Allocation, Price, Dispatching) + VCF Calculation. → extend `sales.md`
7. EC Revenue (Quantity, Inventory, Financial Transaction, Royalty). → extend `revenue.md`

**Phase C — framework breadth + ops**
8. EC Framework remainder (BPM, Reporting, Messaging, EC Core, Logging, JSF). → `framework-misc.md`
9. EC Regulatory Reporting · EC Chemistry · EC IAM · EC Support Tools. → `misc-modules.md`
10. How-To Articles — index + read on demand (reference, not cover-to-cover). → `how-to-index.md`
11. "Learn more about the Oil and Gas Industry" — industry grounding (feeds GLOSSARY). → GLOSSARY update

## Per-section method (lightweight 3-step)
recon (getConfluencePageDescendants on the section → child list) → read key child pages
individually (getConfluencePage markdown) → synthesize 1 notes file + update GLOSSARY/
TEST-CASE-BACKLOG + cross-link to As-Built/domain docs. Checkpoint the table below.

## Status
| Phase | Section | State |
|---|---|---|
| A1 | TAF | ✅ done — STUB pages; signal: EC TAF = Arquillian/Cucumber/Jenkins/Docker (backend) → taf.md |
| A2 | Calculation Framework | ✅ done — allocation recipe + engine model → framework-calculation.md |
| A3 | ECIS + PI DAS | ✅ done — ECIS pluggable source adapters (PI JDBC / OPC UA / Excel / REST) → framework-ecis.md |
| A4 | Environment/GHG | ✅ done — EFK page = legacy external link (unreachable); REDIRECTED to As-Built 14 §2.4 + 06 → environment-ghg.md |
| B5-7 | Production/Sales/Revenue | ✅ sampled — EFK domain pages are THIN intros linking to RD130 release-docs; depth already held in my As-Built + domain syntheses. Captured HCA allocation rationale → GLOSSARY. Low marginal value; not exhausting page-by-page. |
| C8-11 | Framework misc / modules / how-tos / industry | ☐ (industry page = empty stub, skipped) |

**Phase B finding (2026-06-13):** EFK = light knowledge hub; for product depth the real sources
are **RD130 "Release Documentation"** Confluence space (substantive — e.g. the ECIS Advanced File
Import page) + the Pluto **As-Built**. Decision: stop exhausting thin EFK pages; pull RD130 pages
on-demand when a specific topic needs product depth. EFK deep dive effectively COMPLETE for value.

**Phase A COMPLETE (2026-06-13).** Net: EFK is strong on the allocation recipe + ECIS adapter
architecture; weak (stubs/legacy links) on TAF + Environment — those redirect to ec-docs/DOC-*
+ Pluto As-Built. Next idle block: Phase B (read EFK Production/Sales/Revenue substantive pages
to deepen domain syntheses) OR the higher-payoff As-Built 06 Calculations / 09 Validations
(Issue_1052) per SELF-LEARNING-BACKLOG self-pick logic.

Findings so far: EFK training pages are often thin wrappers (slide images, little body text) —
extract the concrete how-tos/recipes, cross-check depth against ec-docs/DOC-* + As-Built, don't
churn on stubs. 2026-06-13.
