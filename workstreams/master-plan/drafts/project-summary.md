# Woodside Pluto 12839 — Comprehensive Project Summary
_Generated 2026-06-02 from SteerCo decks, Teams, Git, Email, SharePoint_

---

## 1. What This Project Is

**Woodside Pluto ECaaS Implementation** — Quorum Software implementing Energy Components as a Service (ECaaS) for Woodside Energy's Pluto LNG facility and Scarborough gas field. The system handles:
- **Allocations** — daily/monthly gas allocation calculations (onshore, offshore, commercial)
- **Reports** — 23 production, regulatory, and partner reports
- **Emissions** — Pluto, Scarborough, Burrup LNG Park emissions and discharges
- **Interfaces** — DG Nomination, MMR data, external feeds

**Contract:** T&M. Project IDs: 12839 (original) / 15681 (current). CR28 (High Priority) active as of 1-June-2026 — Woodside has requested Quorum retain current resources.

**Two delivery tracks running in parallel:**

| Track | Branch | Purpose |
|-------|--------|---------|
| PROD | `develop` → `release/PROD_RELEASE_X.X.XX` | Regular production releases (current: 1.0.37-RC1) |
| PCI | `PCI_1.1.0` → `release/PCI_RELEASE_X.X.XX` | PCI swimlane — email notifications and PCI-specific work |

---

## 2. Milestone History (from SteerCo decks)

| Date | Calcs % | Reports % | Key Events |
|------|---------|-----------|-----------|
| 10 Apr 2026 | ~30% | ~20% | Mass Balance dev in CI. On-site Perth collaboration. DDS14 milestone. |
| 23 Apr 2026 | 38% | 25% | 3 interim reports deployed to ECaaS Test. Early UAT for Pluto commenced. SCA data not ready — pushed to Wave02. |
| 01 May 2026 | 48% | 29% | ST-Wave01 near complete (7/9 test cases passed). UAT for 3 interim reports started (10 defects, 5 resolved). |
| 08 May 2026 | ~50% | ~32% | ST-Wave02 reschedule to 11 May. Dedicated focus on Onshore Allocations. |
| 15 May 2026 | ~53% | ~40% | UAT issues prioritised (Simon Lee). PCI Wave 1 UAT in progress. ECSR-35019, 35042 open. |
| 22 May 2026 | 58% | 45% | Combined ST/UAT adopted. Wave04 to mid-July confirmed. Woodside requests CR28 resource retention. RED. |
| 29 May 2026 | 64% | 51% | Wave02 released for UAT (26 May). 1.0.37-RC1 deployed to ECaaS TEST. 37 critical defects, 6 open blockers. |
| 05 Jun 2026 | 64% | 51% | **1 July go-live AT RISK confirmed.** Dev complete 22 June. Wave03 UAT: 7 Jul. Wave04 UAT: 16 Jul. |

---

## 3. Delivery Wave Structure

### Wave 01 — ST complete, UAT in progress
- Offshore/Onshore Daily+Monthly Mass Balance (4 calcs)
- Pluto Upstream Daily Partner Report
- Burrup LNG Park Daily Production Report
- Pluto Scarborough Daily Asset Report

### Wave 02 — Released for UAT (26 May)
- Offshore Daily/Monthly Allocation
- Pluto Upstream Monthly Report
- R_PH_MONTHLY_RAU
- Interface: DG Nomination (testing in PROD WS)

### Wave 03 — Dev target: 8 June, UAT target: 7 July
- Emissions calcs: Pluto, Scarborough, Burrup LNG Park (brought forward from Wave04)
- Onshore Daily Allocation (80% dev)
- Onshore Monthly Allocation (70% dev)
- Burrup LNG Park Monthly Allocation Report (full version)
- BLP LNG Train 1 Manager Report
- Pluto Hub Daily/Monthly Failures Reports
- Burrup LNG Park Offtake Report (**0% — at risk, due 5 Jun**)

### Wave 04 — Dev target: 22 June, UAT target: 16 July
- **Onshore Monthly Commercial Allocation (29%) — CRITICAL PATH**
- BLP Australian Petroleum Statistics Report
- PRRT Report (Pluto)
- Pluto Upstream NOPTA Report
- Daily Offtake Report
- BLP Monthly Allocation Report (Scarborough version)
- Scarborough Upstream NOPTA Report
- Scarborough Upstream Monthly Production Allocation
- BLP LNG Train 2 Manager Report
- Interface: Monthly MMR data (not started — blocked on Commercial Allocation)

---

## 4. Current State (2 June 2026)

```
Delivery Confidence: RED

Calculations:  64% actual vs 82% target  (-18%)
               Dev 92% complete | Testing 23% complete
               Projected at go-live: ~93%

Reports:       51% actual vs 80% target  (-29%)
               Dev 76% complete | Testing 16% complete
               Projected at go-live: ~75%

Go-live:       1 July AT RISK → mid-July increasingly firm
               Wave 03 UAT complete: 7 July
               Wave 04 UAT complete: 16 July
               Exact date: TBC (Woodside + Quorum to align)
```

**UAT defects as of 28 May:**
- Wave 01: 28 total, 0 open blockers, 7 closed
- Wave 02: 9 total, 6 open blockers
- Total: 37 critical, 6 open blockers

**Your active work (Workstream H — Reporting):**
- `feature/ECPR-31034` — Email notifications for Scarborough (must rebase to PCI branch)
- `feature/ECPR-31035/36` — Open
- PRs #603, 604, 605, 606 — Approved, awaiting merge

---

## 5. Critical Path

```
Onshore Monthly Commercial Allocation (29% dev — due 5 Jun)
    blocks:
    ├── BLP Monthly Allocation Report (Pluto)
    ├── BLP Australian Petroleum Statistics Report
    ├── PRRT Report (Pluto)
    ├── Pluto Upstream NOPTA Report
    ├── BLP LNG Train 1 + 2 Manager Reports
    ├── Pluto Hub Daily/Monthly Failures Reports
    ├── Onshore Monthly Emissions Allocation
    └── Interface: Monthly MMR data (not started)

Scarborough (SCA) Object Configuration
    blocks:
    ├── R_PH_MONTHLY_RAU (needs re-run)
    ├── Pluto Scarborough Daily Asset Report (UAT fix)
    ├── BLP Monthly Allocation Report (SCA version)
    └── Scarborough Upstream Monthly Production Allocation
```

---

## 6. Key Decisions Made

| Date | Decision | Impact on You |
|------|----------|--------------|
| Late Apr | Combined ST/UAT approach | Faster cycles, more defects expected |
| May | Emissions calcs moved Wave04 → Wave03 | Frontloads testing complexity |
| May | PRRT excluded from MVP | One less dependency |
| May | CR28 high priority — resources retained | You likely stay post-July |
| 28 May | Email notifications → PCI swimlane (Ruchi/Jamilin) | **Your branches need rebasing NOW** |
| Ongoing | No scope changes before July | Protects your delivery window |

---

## 7. Future Plan

### June 2026
| Period | Event |
|--------|-------|
| 2–8 Jun | Wave 03 dev complete. Code drop to Woodside. |
| 14–24 Jun | Shivani + Azila (Reporting team) in Perth. |
| 15 Jun | Cato (Allocations lead) in Perth — through 3 July. |
| 22 Jun | Wave 04 dev complete. All reports finalised. |
| 23 Jun | Wave 04 code drop to Woodside. |

### July 2026
| Date | Event |
|------|-------|
| 7 Jul | Wave 03 UAT complete (target) |
| 12 Jul | Jean-Pierre in Perth (E2E Allocations) through 25 Jul |
| 16 Jul | Wave 04 UAT complete (target) |
| ~Mid-Jul | **GO-LIVE** |

### Post Go-Live (CR28 scope — you are staying)
- SND redesign / post-July reassessment (A-157 document covers this)
- PRRT calculation uplift
- Onshore SND redesign
- Report suite maintenance and enhancements
- CR28 + CR29 planning and scoping

---

## 8. Proposals for Choong-Yin

### Do this week
1. **Rebase email notification branches to PCI_Release** — Grant and Jamilin direction (28 May). Branches ECPR-31030/31/32/34 were cut from `develop`, not PCI branch. Recreate or cherry-pick onto PCI_Release. The longer you wait the messier.
2. **Verify your items in 1.0.37-RC1** — Jamilin deployed to ECaaS TEST on 29 May. Confirm your report changes are working.
3. **Raise ECPR for R_BLP_MONTHLY_ALLOC_PLUTO architecture fix** — Simon Lee flagged ASAP (19 May). Still no ticket. This is an open architecture debt that will resurface post go-live.
4. **Check if BLP Offtake Report is on track** — It is at 0% (report mapping stage) with a dev target of 5 June. That is today. Raise visibility to Tahura/Grant if at risk.

### June delivery
5. **Watch the SCA configuration dependency** — your Scarborough reports are blocked on SCA object configuration. This has caused delays before (Wave01, Wave02). Track Cato and Simon Lee on readiness.
6. **Prepare for Wave 03 testing** — your reports will enter UAT around 9 June. Make sure test data is ready and you understand what Woodside will test.

### Strategic (post July)
7. **Document the Pluto report architecture patterns** — class-over-view rule, JRXML query structure, config patterns. You have built enough to write a one-pager. Invaluable for CR28 onboarding and your own reference.
8. **Think about what you want in CR28** — You are being retained. Start forming a view on which workstreams you want to own vs hand off. Reporting workstream ownership is a natural fit given your current work.

---

_Sources: SteerCo decks (10 Apr – 05 Jun 2026), Teams (Pluto SuperFriends Extended + Daily Standup Workstream H), Git commit log (all branches), Bitbucket PR email notifications, SharePoint (1,725 project documents)_
