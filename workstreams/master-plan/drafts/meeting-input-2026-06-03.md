# Meeting Input — Woodside Pluto Weekly Project Meeting
**Date:** Wed 3 June 2026, 15:00 AWST
**Organiser:** Kirsten Bransfield-Garth
**Attendees:** Full Woodside Pluto team (Cato, Grant, JP, Simon, Tahura, Daniel, Jamilin, Ricardo, Rizki, Shivani, Tushar, Dinesh, Joey, Wee-Leng, Kenneth, Norzarina, Syazwani, Amy, Akmal, Tomas)

---

## My Update (Workstream H — Reporting)

### Completed since last meeting
- **PRs raised and approved** — PRs #603–607 for ECPR-31030, 31031, 31032, 31034, 31049 all raised and approved by Grant
- **1.0.37-RC1 PROD issue resolutions** — verified my report changes deployed in ECaaS TEST (29 May)
- **ECPR-31034** — Email functionality for Scarborough Upstream Monthly Production Allocation Report: initial commit done, fix version script updated

### In Progress
- **ECPR-31034** — Completing email notification feature on `feature/ECPR-31034`
  - Issue: Feature was built from `develop` branch — need to rebase to `PCI_Release` branch per Jamilin/Ruchi direction (28 May)
  - Plan: Rebase this week before Wave 03 dev deadline (8 June)
- **ECPR-31035, 31036** — Open branches, targeting Wave 03 completion (8 June)

### Blockers / Risks
- **PCI branch rebase** — email notification branches (ECPR-31030/31/32/34) were cut from `develop` but must now go through PCI swimlane. Rebase adds overhead — flagging for awareness
- **BLP Offtake Report** — was at 0% (mapping stage) with a 5 June dev target — need to confirm status with Tahura/team

### Planned this week
- Rebase ECPR-31034 to PCI_Release branch
- Merge PRs #603–606 (all approved)
- Complete ECPR-31035, 31036 for Wave 03
- Reply to Grant on Issue_1052 (PHD validation testing approach)

---

## Questions / Items to raise in meeting

1. **BLP Offtake Report** — Was at 0% dev (report mapping stage) with 5 June target. What is current status? Is it still on track for Wave 03?

2. **PCI branch rebase** — Can the team confirm the exact scope of what needs to go through PCI swimlane? Are ECPR-31030/31/32 also included, or just 31034?

3. **Wave 03 test data** — SCA + T2 test data (including Pluto Wells, Pluto data for June) was requested by Grant from Cato + Simon. Is this ready?

4. **UAT blockers** — Daniel raised 2 open blockers on 1 June. ECSR-35100 reportedly unblocked. What is the second one and does it affect Reporting?

---

## Project-level context (for awareness)
- **Delivery confidence: RED** — Calcs 64% (target 82%), Reports 51% (target 80%)
- **1 July go-live AT RISK** — Mid-July increasingly firm (Wave 03 UAT 7 Jul, Wave 04 UAT 16 Jul)
- **Wave 03 dev deadline: 8 June** — 5 days away
- **Wave 04 dev deadline: 22 June**
- **Co-location:** Cato in Perth 15 Jun–3 Jul; Shivani + Azila 14–24 Jun; JP 12–25 Jul

---
_Prepared: 2026-06-02 | Auto-generated from git, Teams, SharePoint, Calendar_
