# ChoongYin_OS Improvement Plan
**Created:** 2026-06-06 · **Owner:** Choong-Yin Lee + Claude · **Mode:** clear one item at a time

Grounded in the 2026-06-06 health snapshot (`tmp/scripts/os_health_review.py`).
Each item has a clear **Definition of Done (DoD)**. Work top-to-bottom; check off as we go.

---

## P1 — Restore the OS operational heartbeat  🔴 highest
*The OS's own job (keeping you briefed) has gone 4 days stale; briefing automation paused on OAuth.*

- [x] **A1.1 Diagnose the briefing/status blocker** ✅ 2026-06-06. **Finding:** 3 separate issues, NOT one. (1) `ClaudeOS-AutoAttach` scheduled task fails every run (last_result `-2147024629`) → approved tasks like `daily-status-reconcile` never get armed → **this is why STATUS is stale, and it needs no OAuth.** (2) `DailyMorningBriefing` task has never run (`SCHED_S_TASK_HAS_NOT_RUN`). (3) MS Graph OAuth consent (Mail/Calendar, app `060468f7…`, Quorum tenant) — only blocks *live-email/calendar content*; no `token_cache.json` = never authed. **Decision:** STATUS → local workaround (A1.2), no OAuth. OAuth/live-briefing **deferred to next week** (user routing via IT help desk).
- [ ] **A1.2 Build a no-OAuth local STATUS generator** — a `py` tool that reads local sources (git log, recent commits, workstreams mtimes, `gh pr list` if available) and regenerates `STATUS.md`. DoD: `tools/status-refresh/` script that produces a current STATUS.md without OAuth.
- [ ] **A1.3 Refresh STATUS.md to today** — run A1.2; reconcile the stale Woodside items (ECPR-31034 PCI rework, 2 UAT blockers, PRs #603–606). DoD: STATUS.md dated today, reflects real current state.

## P2 — Shared `ec_automation/` module (DRY)  🟠 high
*login copied in 28/61 scripts, `ignore_https_errors` in 29, save logic in 14, oracledb in 10.*

- [ ] **A2.1 Design the module API** — list functions + signatures (login, navigate_to_screen, set_nav_dropdown, manage_object insert/update/delete, save, go, db_verify). DoD: 1-page design note.
- [ ] **A2.2 Implement `ec_automation/`** — importable package under the repo. DoD: module importable, unit-smoke runs.
- [ ] **A2.3 Refactor bank-iud + equipment-iud to use it** — prove the DRY win. DoD: both suites still PASS, duplicated helpers removed.

## P3 — Structure hygiene  🟡 medium
*22 loose files at root (18 `ec_doc_*.txt`); tmp/ has 18 scripts + 16 logs, no scratch/deliverable boundary; no root README.*

- [ ] **A3.1 Relocate EC reference docs** — move 18 `ec_doc_*.txt` → `docs/ec-reference/`. DoD: root clean, any references updated.
- [ ] **A3.2 Define the `tmp/` boundary** — gitignore true scratch; promote keepers to a real home. DoD: short policy + `.gitignore`, tmp tidied.
- [ ] **A3.3 Add a top-level `README.md`** — map what each top dir is for. DoD: README at repo root.

## P4 — Knowledge consolidation  🟡 medium
- [ ] **A4.1 `docs/EC/ec-screen-patterns.md`** — one reference: Manage Object / data grid / master-detail, element-ID conventions, DB-view discovery (`OV_`/probe). DoD: single consolidated doc.
- [ ] **A4.2 Fix stale SOW spots** — bank SOW author line, "v2.0"/"to be committed", Role Maintenance mis-typed as NAVIGATOR+TABLE. DoD: corrected.

## P5 — EC learning track (continues in parallel; best after P2)  🟢
- [ ] **A5.1 Data-grid IUD** — Daily Equipment Status (confirms pattern #2). DoD: IUD + DB-verified, deliverable folder.
- [ ] **A5.2 Master-detail IUD** — Role Maintenance (confirms pattern #3). DoD: IUD + DB-verified, deliverable folder.
- [ ] **A5.3 Crystallize the EC-IUD skill** — once 3 types confirmed. DoD: skill authored from `ec_automation/` + the 3 deliverables.

---

### Suggested order
**P1 first** (revive the OS) → **P2** (DRY foundation) → **P3/P4** (hygiene, low-risk) → **P5** (more screens, then the skill).
P5 items reuse P2, so doing P2 before A5.1 pays off.

### Progress log
| Date | Item | Result |
|---|---|---|
| 2026-06-06 | A1.1 | ✅ Diagnosed. STATUS staleness = AutoAttach failing (not OAuth). Decision: local STATUS generator (A1.2). OAuth/live-briefing deferred to next week (IT help desk). |
