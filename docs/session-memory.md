# Session Memory — Owner Chat Notes

_Append a new dated section after each owner chat session. Keep entries concise — decisions, fixes, and context not captured elsewhere._

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
