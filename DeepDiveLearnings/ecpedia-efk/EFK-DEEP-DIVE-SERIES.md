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
- [x] EC Regulatory Reporting `1845940` (2014) — SOX/SEC governance. READ 2026-06-14 → `regulatory-reporting.md`. The *why* behind EC's validation/freeze/audit features (SOX404 internal controls); reporting moved E&P→CFO; ties to CTRL_CHECK_* + Issue_1052.
- [x] EC Chemistry Management `1853912` (2020) — link-out FOLLOWED 2026-06-14 → space **ECCM** (`2326530`) → `link-out-extensions.md`. Chemistry add-on (monitor/report chemical volumes·dosages·performance = N1-family) + Emission Mgmt add-on.
- [x] EC Environment Management `1851143` (2021) — link-out FOLLOWED → space **XEM** (`5734405`) → `link-out-extensions.md`. ⭐ Emission tracking rides EC's **calc+allocation framework** → N2-family target (GHG result screen). Space = mostly dev-admin; calc detail in external SharePoint.
- [x] EC IAM `1850998` (2020) — link-out FOLLOWED → space **ECIAMD** (`4489220`) → `link-out-extensions.md`. EC IAM product manual (TietoEVRY 2020, reservoir-to-surface modelling). Reference only.

**✅ Phase 1 COMPLETE (2026-06-14)** — all 8 domain pages read; reservoir→revenue chain mapped + SOX "why" layered on. Next = Phase 2 (VCF `1853432`).

### Phase 2 — Calculation / framework depth ★ high (ties to allocation + EC internals)
- [x] VCF Calculation in EC `1853432` (2023) — READ 2026-06-14 → `vcf-calculation.md`. Tank volume correction, API MPMS Ch.12.1 8-step chain (GSV→NSV→mass; EC skips mass-in-vacuum). EC 10.4+ = PL/SQL formula (MPMS Ch.11 2004, ITS-90, combined temp+pressure). ⭐ Test oracle: external published standard + the rounding rule (intermediates UNrounded, final VCF=5 dp). Feeds inventory valuation (Revenue IN) + custody transfer.
- [x] The calculation engine is in dire need of enhancements `1843903` (2017) — READ → calc-engine-insights.md. GOLD: variable-cache model, DIMENSIONED variables (stream×day×PC×company×product, day/mth) mapping to STRM_DAY_*_ALLOC tables, prorate/rollup/round/recombine ops, IsValid/IsZero hazard, AND the allocation TEST ORACLE (sum-to-total / no-neg / rounding tolerance / multi-grain roll-up) for N2.
- [x] EC Framework `1854410` (2015) — READ 2026-06-14 → `framework-db-sanity.md`. Thin parent; 13 children mostly 2014 empty stubs (BPM/EC Core/ECIS/JSF/Logging/Messaging/Reporting/Jboss). ⭐ Keeper child = **Database Sanity** `1851734`: unsupported-config rules (object_id unique across classes; group-model loop-free w/ FCTY_CLASS_1/Well_Hookup/Well exceptions; class-trigger discipline; no order/group-by in class DB-where). Calculation Framework `1852084` + EC Timezone `1853989` = empty placeholders.
- [x] EC Technology `1853250` (2021) — READ 2026-06-14. Thin CTO parent; only child = Presentations `1853267` (slide decks, low text value). Noted, skipped.

### Phase 3 — Reference (consult, don't deep-read)
- [x] EC Vocabulary `1844980` (2022) — CROSS-CHECKED 2026-06-14 vs `business-domains/GLOSSARY.md`. Broad industry+EC acronym list; harvested the table/screen-tied + EC-specific terms into GLOSSARY (ACL/Refresh-ACL, Standard vs Normal Conditions=15°C/0°C→VCF, ACQ/DCQ/MDQ, TSA/TSO, PSA, CGR/GOR, Diluent→ALLOC_DILUENT_VOL, Recovery Factor, Lifter/Lifting Account). Left the page as the canonical full industry reference (no duplication).
- [x] EC Talks `1837692` (2026.03) — READ 2026-06-14. Purpose/team stub; "Content" empty (talk recordings in children/SharePoint). Noted, no text value.
- [x] EC Product Trainings `1853607` (2021) — training index. Skipped (index only).
- [x] EC Releases and live assets `1853526` (2024) — READ 2026-06-14. Template with only "test row" placeholder data (no real version/asset counts). Skipped.
- [x] EC Extensions Compatibility Matrix `1851205` (updated daily) — READ 2026-06-14 → `ec-extensions-matrix.md`. ⭐ KEEPER: extension catalog (XEM/XCH/XMS/ECME/XTO/XGH/TAP/reporting XRP*/XRR* by region…) + Pluto EC-14.2.x verified versions (XEM-4.1.2, ECME-1.5.6, XTO-2.0.0…). ⭐ Resolves parked Chemistry Q: **XCH discontinued → Chemistry is an EC CORE MODULE since 13.1.2** (so on Pluto 14.2.x ask "is the module licensed?" not "is XCH installed?").

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
- 2026-06-14: **Phase 1 CLOSED.** Read EC Regulatory Reporting → `regulatory-reporting.md` (SOX404
  governance = the *why* behind EC's validation/freeze/audit machinery; reporting org moves E&P→CFO;
  3 upstream needs = downtime loss / reliable production data / gov+internal control). The 3 remaining
  Phase-1 pages are link-outs (Chemistry→ECCM, Environment→XEM, IAM→ECIAMD) — noted, not chased.
  All 8 Phase-1 domain pages now read; reservoir→revenue value chain mapped with the SOX layer on top,
  explicitly tied back to the validation framework (CTRL_CHECK_*/Issue_1052) + N1/N2 data-integrity
  oracles. Next idle item: Phase 2 — VCF Calculation `1853432`.
- 2026-06-14: Followed the 3 Phase-1 **link-outs** (user-directed) to their real spaces → migrated onto
  energycomponents.atlassian.net: **ECCM** (Chemistry+Emission add-ons), **XEM** (Emission Tracking),
  **ECIAMD** (IAM manual). Note → `link-out-extensions.md`. ⭐ Key find: XEM emissions ride EC's **calc
  +allocation framework** → emissions = an **N2-family** test target (run emission calc → assert Exit
  Status + DB mass-balance/no-neg on the GHG result table); Chemistry = N1-family data entry. Both are
  add-ons → confirm licensed/installed for Woodside before real coverage (open Q for user). Spaces are
  product-dev admin + external SharePoint for calc detail — no deeper crawl.
  ↪ PARKED (user, 2026-06-14): "jump back to Chemistry later" — revisit the ECCM/XEM emission+chemistry
  add-ons as a coverage candidate once licensing/install in the Woodside sandbox is confirmed.
- 2026-06-14: **Phase 2 started.** Read VCF Calculation in EC → `vcf-calculation.md`. Tank volume
  correction (API MPMS Ch.12.1 8-step GSV→NSV→mass; EC omits mass-in-vacuum); EC 10.4+ uses a PL/SQL
  formula (MPMS Ch.11 2004 ed., ITS-90 scale, combined temp+pressure). Strong test-oracle family — has
  an EXTERNAL published standard to check against, and the rounding rule (intermediates unrounded, final
  VCF rounded to 5 dp) is the headline test concern (matches the calc-engine rounding-tolerance hazard).
  Feeds inventory valuation (Revenue IN) + custody transfer → a VCF error hits revenue + SOX numbers.
  Next Phase-2 idle item: EC Framework `1854410` or EC Technology `1853250`.
- 2026-06-14: **Phase 2 framework cohort done** → `framework-db-sanity.md`. EC Framework + EC
  Technology are thin parents (children mostly 2014 empty stubs / slide decks). The keeper = **Database
  Sanity**: a list of EC's *unsupported* config patterns (object_id unique across classes; group-model
  must be loop-free w/ the FCTY_CLASS_1/Well_Hookup/Well exceptions — which explains the N1 nav cascade
  shape; class INSTEAD-OF trigger discipline = High severity; no order/group-by in class DB-where).
  High-value guardrail for any class-config / ZWP-extension / ECPR change. Calculation Framework +
  EC Timezone children are empty placeholders. **Phase 2 effectively complete** (calc+framework depth
  held across calc-engine-insights / vcf-calculation / framework-db-sanity). Next: Phase-3 reference —
  EC Vocabulary `1844980` (cross-check vs business-domains/GLOSSARY.md), then EC Talks `1837692` (newest).
- 2026-06-14: **Phase 3 reference done.** EC Vocabulary → harvested table-tied/EC-specific terms into
  `business-domains/GLOSSARY.md` (left the page as the canonical industry acronym source). EC Talks /
  Product Trainings / Releases = thin stub / index / template-with-test-rows (noted, skipped). **EC
  Extensions Compatibility Matrix** (updated daily) = the keeper → `ec-extensions-matrix.md`: extension
  catalog + Pluto EC-14.2.x verified versions (XEM-4.1.2, ECME-1.5.6, XTO-2.0.0…). ⭐ Resolved the
  parked Chemistry question — **XCH discontinued → Chemistry is an EC CORE MODULE since 13.1.2**, so for
  Woodside it's "is the module licensed?" not "is the extension installed?". **EFK series now
  effectively complete for value** (Phases 1–3 done; Phase-4 ops = on-demand when the scheduler
  misbehaves; Phase-5 = skip). Next idle work returns to the automation track (N3 status-process
  P→V→A) or a held item.
