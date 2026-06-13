# EC Business-Domain Deep-Dive Curriculum (proper plan, 2026-06-13)

User mandate: structured deep-dive LEARNING of EC business domains (production, transport,
sales, revenue, etc.), using ECpedia + EC documentation + EC tech docs + internet research.
**Hard rules:** NEVER delete files outside C:\Projects\ChoongYin_OS · NEVER commit/push
project files to the remote git repo during this work · stay token-aware (synthesize,
don't transcribe) · EC sandbox = read-only recon unless a hands-on exercise is approved.

## Why (the payoff chain)
Domain understanding → design BUSINESS test-case suites (coverage-goal phase 2) → support
real Pluto tasks (ECIS PHD-backup, Issue_1052 validations, future ECPRs) with business
context, not just mechanics.

## Method — 5 phases per domain (one domain ≈ one self-directed session)
| Phase | What | Sources |
|---|---|---|
| **P1 Theory** | Re-read KB chapter; fill gaps from EC Tech Docs 14.2.5; search ECpedia (BPR space) for best-practice pages; web-search the INDUSTRY concepts (what is hydrocarbon allocation / lifting / take-or-pay / demurrage… outside EC) | `ec-docs/DOC-0x`, tech-doc URL map, ECpedia search, web |
| **P2 Screens** | Menu-branch walk (done for all 5) + open 3-5 REPRESENTATIVE screens read-only, screenshot, understand navigator/grain | local EC |
| **P3 Data** | Table families + row counts (done); then FOLLOW ONE REAL RECORD through the flow (e.g. one cargo T→A, one well-day through allocation) via SQL | local DB |
| **P4 Synthesis** | Rewrite `<domain>.md` as the DEEP version: business narrative, flow diagram, glossary of business terms (industry + EC meaning), config↔transaction↔result table map | — |
| **P5 Apply** | Business test-case proposals (DB-verifiable oracles) + self-quiz (10 questions I must answer without notes) + optional HANDS-ON exercise (needs user OK per exercise) | — |

## Domain order (Pluto relevance) & status
| # | Domain | Draft | Deep (P1-P5) | Hands-on candidate |
|---|---|---|---|---|
| 1 | **Production** (allocation core) | ✅ production.md | P3 partial | InitiateDay RUN NOW attempted 2026-06-13 — **BLOCKED: sandbox scheduler executor stalled** (see production.md §5; needs EC app restart; flag before ECIS re-test!) |
| 2 | **Sales** (gas dispatching, price, contract calc) | ✅ sales.md | ☐ | price-calc run (after scheduler revived) |
| 3 | **Transport** (cargo/LNG lifting — Pluto LNG!) | ✅ transport.md | ☐ | follow one cargo record (read-only SQL) |
| 4 | **Revenue** (docs lifecycle, stream items, closing) | ✅ revenue.md | ☐ | trace one document OPEN→BOOKED (read-only) |
| 5 | **Chemistry** (inventory, lab — Issue_1052 ties!) | ✅ chemistry.md | ☐ | — (light) |
| 6 | **Cross-domain spine** (Contract concept · status lifecycles P/V/A + T/R/C/A + OPEN→BOOKED · calc framework · month locking) | ☐ | ☐ | — |

**Hands-on approved by user 2026-06-13 ("hands-on exercises is good approach... think about
it and execute it"); lens = generic EC + Pluto As-Built. As-Built DDS series FOUND on
SharePoint → PLUTO-ASBUILT-INDEX.md (read order: 14 BusinessProcesses → 06 Calculations →
05 Interfaces → 03 ObjectConfig). Next session: read AsBuilt14 + deepen Production.**

## Deliverables
- `<domain>.md` deep version per domain (replaces draft in place)
- `GLOSSARY.md` — cumulative business-term glossary (industry meaning ↔ EC meaning ↔ tables)
- `TEST-CASE-BACKLOG.md` — all proposed business test cases, one list, prioritized,
  each with DB-verifiable oracle (feeds coverage-goal phase 2; user reviews before any build)
- Self-quiz results logged at the end of each domain doc (honesty check)

## Session rhythm (token-aware)
One domain per block; P1 research summarized in ≤1 page of notes per source; NO raw page
dumps into context; checkpoint this PLAN.md status table after each phase so any session
can resume mid-domain. Habit cycle applies to research dead-ends (alternative source).

## Source quick-list
- Local KB: `DeepDiveLearnings/ec-docs/DOC-01..12`
- EC Tech Docs 14.2.5: hub ecindex (see reference_ec_tech_doc_url_map memory)
- ECpedia: energycomponents.atlassian.net BPR space (search-first pattern!)
- Web: industry-concept searches (allocation, entitlement, laytime/demurrage, ToP, royalty)
- Live: local EC app + DB (read-only default)
- Later, with user: Woodside As-Built (SharePoint) for Pluto-specific scope
