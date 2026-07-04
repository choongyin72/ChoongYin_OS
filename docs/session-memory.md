# Session Memory — Owner Chat Notes

_Append a new dated section after each owner chat session. Keep entries concise — decisions, fixes, and context not captured elsewhere._

---

## 2026-06-14 to 2026-07-01 (Earlier sessions — backfilled from compaction summary)

### System architecture decided
- **Two-Claude system:** Worker (Claude Opus 4.8, runs on owner's laptop via VS Code + Claude Code CLI) + Automated Reviewer (cloud Sonnet 4.6, fires via Windows Task Scheduler at 06:00 and 14:00 AWST daily).
- **Three-agent system is sufficient:** Worker + Runner + Reviewer. No additional agents needed for now.
- **Python Runner:** deterministic autopilot (`tools/deep-dive-scheduler/run_ec_screen_learn.py`) runs ~1:30 PM daily, appends EC screen notes to `feature/ec-screen-deepdive`.

### Standing rules set by owner
- **Reviewer does NOT merge PRs autonomously** — reviews and comments only. Owner explicitly requests merges.
- **gstack (Garry Tan's open-source virtual team):** Explored (116k stars), decided NOT to integrate into EC automation pipeline.
- **`/fewer-permission-prompts`:** ON HOLD — Worker analysed and concluded not beneficial for this project.
- **Worker checks GitHub Issues at session start** — CLAUDE.md updated (PR #139, merged) to add step 5: action any open Issues assigned to Worker before starting new work.

### Key rules extracted (R1–R26)
- **R16:** Playwright bundle credentials MUST use env vars (EC_USER/EC_PASS) — never hardcode.
- **R17:** OV-GM T3 MUST have `Wait For Elements State visible 20s` before T1 assert (lazy grid redraw).
- **R18/R20:** Files printed to Windows console or parsed by PowerShell MUST be ASCII-only.
- **R19:** Event-log screens: use marker oracle; prove physical delete in OV AND base table.
- **R23:** Long-lived branch must show zero `-` lines on reviewer-owned docs vs master.
- **R24:** Detached worktree push MUST use `HEAD:refs/heads/<branch>` (not bare branch name).
- **R25:** When any tool/MCP/connection breaks, own the troubleshooting — diagnose and give actionable fix steps; never say "I can't" without a follow-up fix path.
- **R26:** 19-item IUD deliverable checklist is a hard gate — all items green before PR. Introduced with PR #140; `docs/IUD-DELIVERABLE-CHECKLIST.md` is the reference.

### Reviewer upgrade (completed end of June)
- **`docs/ec-domain-reference.md` created** — EC domain knowledge base: 6 screen patterns (OV/Bank, OV-GM/Gated, TV/Language, PC/Parent-Child, Custom-URL OV, Event-Log), view naming, delete patterns, T2 selection, DB assertion cheat sheet, clone error checklist, sandbox safety, rule quick-reference.
- **`.claude/review-prompt.txt` updated** — mandatory first reads (lessons-learned.md + ec-domain-reference.md), step 8d (6 SME review dimensions: pattern correctness, RF design quality, DB assertion quality, better alternatives, clone quality, self-clean rigour), AFTER READING directive, REVIEWER IDENTITY/MINDSET.
- **Goal:** Reviewer acts as EC domain SME + senior peer reviewer, not just a compliance checker. "A passing test on a wrong foundation is a deferred failure."

### PRs merged (major milestones)
- **PR #118:** EC Screen Deep-Dive milestone merge (29/1457 screens). Owner-merged.
- **PR #135:** Next standing draft, accumulated deep-dive notes — owner-merged 2026-07-02.
- **PR #139:** CLAUDE.md — Worker session-start step 5 (check GitHub Issues).
- **PR #140:** 19-item IUD deliverable checklist + R26.
- **PR #141–#145:** Date Objects 5/5 complete (Document Date Term, Document Received Term, Payment Term, Calendar, Calendar Collection) — all live 4/4.
- **PR #146:** Mandatory grid-locator pre-flight guard (prevents wrong grid-id assumption).
- **PR #147, #151:** Automated reviewer feedback PRs — all CLEAR, no MUST-FIX.
- **PR #148:** Date Objects doc-drift fix (clone CHECKLIST/README cited wrong OV view).
- **PR #149:** SME reviewer upgrade (step-8d + ec-domain-reference.md).

### EC screen coverage at end of period
- Royalty Objects: **8/8 COMPLETE** (Owner, Depositor, Product Group, Unit Agreement, Tract, Unit-Well Setup, Tract-Well Setup, Product Group Setup)
- Date Objects: **5/5 COMPLETE** (Document Date Term, Document Received Term, Payment Term, Calendar, Calendar Collection)
- Phase 1 (Config screens) still in progress — remaining sections: Account Mapping, MIME, Equipment, Language, Dispatching, Contract, Cargo, Laboratory Objects

### Lessons from bad moments
- Reviewer wrongly said "I can't" when GitHub MCP connection had issues instead of troubleshooting → led to R25.
- APPROVE on own PRs rejected by GitHub → must use `add_issue_comment` for review comments instead.
- Stacked PR conflict resolution pattern established: `--detach` worktree + `git checkout --ours` + `push HEAD:refs/heads/<branch>` (R24).

### Comms channel: GitHub Issues (not PRs)
- Reviewer leaves task instructions for Worker via **GitHub Issues** (not PR comments).
- Worker checks Issues at session start (CLAUDE.md step 5) and closes them once actioned.

---

## 2026-07-02 (Morning session)

### Decisions made
- **Phased coverage strategy agreed:** Phase 1 (Config screens) → Phase 2 (Operation screens) → Phase 3 (Transaction screens). Captured in `docs/automation-scorecard.md`.
- **Runner batch size:** Increase default from 8 → 25 screens/day, configurable via `EC_LEARN_MAX_SCREENS`. Issue #150 raised for Worker.
- **gstack (Garry Tan's open-source team):** Explored, decided NOT to integrate into EC automation pipeline.
- **`/fewer-permission-prompts`:** ON HOLD — Worker analysed, not beneficial for this project.
- **Standing rule:** Reviewer does NOT merge PRs unless owner explicitly asks. Reviewer reviews and comments only.

### Fixes applied this session
- **GitHub Actions permission:** Enabled "Allow GitHub Actions to create and approve pull requests" in repo Settings → Actions → General → Workflow permissions. Required for `reopen-deepdive-draft-pr.yml` to auto-reopen standing draft PR after milestone merges.
- **PR #158** (scorecard phased coverage) — raised and merged manually (had conflict; master's batch-size wording kept as Worker had already actioned #150).
- **PR #135** (deep-dive standing draft) — milestone-merged by owner request. Auto-reopen workflow fired and created **PR #159** successfully.

### Reviewer upgrade (merged PR #149 + #151)
- `docs/ec-domain-reference.md` created — EC domain knowledge base for reviewer (6 screen patterns, view naming, delete patterns, T2 selection, DB assertions, clone checklist, sandbox safety, rule quick-reference).
- `.claude/review-prompt.txt` updated — added step 8d (6 SME review dimensions), AFTER READING directive, REVIEWER IDENTITY/MINDSET statements.
- First post-upgrade review (2026-06-29 06:00) only saw docs PRs — SME dimensions not yet exercised on real IUD code. **Watch next IUD batch PR.**

### Reviewer maturity assessment
- Rules grown from R1–R5 (seed) → R26 in ~2 weeks.
- Self-corrects process bugs (caught + fixed step 18 R24 refspec violation).
- Recurring gap: clone doc-drift (wrong OV view in CHECKLIST/README) flagged 3× as NICE-TO-HAVE — consider escalating to MUST-FIX after 3rd recurrence.
- SME upgrade untested on real code yet.

### Open items for next session
- Monitor first IUD batch PR after SME upgrade — check if step 8d catches anything new.
- Worker to action Issue #150 (batch size increase to 25/day).
- PR #159 (standing deep-dive draft) accumulating — owner to milestone-merge when ready.

### System state at end of session
- Open PRs: 1 (#159 standing draft, DRAFT)
- Open Issues: #150 (batch size — for Worker)
- All reviewer-owned docs current on master (v26)
- Auto-reopen workflow: ✅ working

---

## 2026-07-02 (Afternoon session — status-update routine gap)

### Problem raised by owner
Asking a fresh session for a "status update" got only a PR/automation-scorecard summary, then only
Jira — the session had no way to know "status update" also means meetings/email/Teams (the format
already used by the scheduled 9am `tools/morning-briefing/run_briefing.py` job) until told twice.
Owner does not want to re-teach this every new session.

### Root cause
The morning-briefing format existed only in `tools/morning-briefing/run_briefing.py`, which nothing
in the mandatory session-start reading list (CLAUDE.md) pointed to. `CLAUDE.md` itself is
auto-injected into every session's context (shown as a system-reminder before any file is read), but
`session-memory.md`/other docs require an explicit Read call — so anything owner needs enforced
with zero re-teaching belongs in `CLAUDE.md`, not just in session-memory.md.

### Fix applied
Added a **"Status update" requests** section directly to `CLAUDE.md` (not just here) defining the
standing behavior: any ad-hoc "status update" / "check PR status" ask pulls all four of GitHub
PRs/Issues + Outlook calendar (today) + Outlook email (today) + Teams messages (today), presented in
the ☀️/📅/📧/💬/🚨 emoji-sectioned format. This is now load-bearing in every session automatically,
no explicit read step required.

### Standing rule for future doc changes
When a behavior must survive a fresh session with **zero re-explanation**, put it in `CLAUDE.md`
(auto-loaded). Reserve `session-memory.md` for narrative/decisions history that's fine to require an
explicit read (it's already mandatory step 5, but CLAUDE.md is the belt-and-suspenders location).
