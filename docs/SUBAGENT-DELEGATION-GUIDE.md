# Subagent Delegation Guide

Standing rules for what gets delegated to a dispatched subagent, and what stays with the main-loop
agent (Claude) directly. Established 2026-08-26 after a Bank/Area-pattern RF conversion batch that
delegated heavily to parallel subagents. Read this before dispatching any subagent, and reference it
explicitly in dispatch prompts rather than re-deriving these boundaries each time.

## What subagents DO
- **Live recon** — open EC screens, read DOM/labels/mandatory fields, run DB queries to confirm class/
  view/identity. Never trust a doc classification at face value; always re-verify live.
- **Write and convert code** — RF page objects, test suites, properties files, Playwright drivers.
- **Run their own verification before reporting back** — robocop, full-tree dryrun, live suite run,
  DB self-clean via a fresh connection, filter-keyword-fired grep. Every number cited in a report or PR
  body must trace back to a command actually run, not a claim.
- **Update docs** — registry, scorecard, conversion checklists (append-only where the doc convention is
  append-only).
- **Git mechanics** — branch, commit, push, raise a PR (never merge it).
- **Work in isolated worktrees/sparse clones** when running in parallel with other subagents, to avoid
  shared-working-directory collisions (branch/file overwrites).

## What subagents NEVER do (reserved for the main-loop agent, or requires the user's explicit go)
1. **Merge a PR.** Standing rule for every agent, no exceptions — a human reviews and merges.
2. **Close, comment on, or otherwise write to a PR/Issue as their own decision.** A broader "proceed
   with X" does not imply authorization for this specific external write — get it named explicitly
   before doing it. (Real incident, 2026-08-25: a subagent closed a stale PR on the main-loop agent's own
   instruction, but that instruction itself was never checked with the user first.)
3. **Touch a shared T1/T2 file without the full safety protocol** — backup first, additive-only (never
   change an existing keyword's signature), full-tree dryrun, and a live regression canary on 2+ EXISTING
   screens that already depend on the file. Every time, no exceptions.
4. **Fabricate or assume evidence.** "Live 5/5," DB self-clean, dryrun counts, robocop parity — all must
   come from a command that was actually executed and its output read, never asserted from memory of
   "should work" or a sibling screen's result.
5. **Guess an identity, field set, or classification.** Screen labels, mandatory fields, navigator shape,
   DB class/view binding — confirmed live or via DB query, never assumed from a similarly-named sibling or
   from a stale doc. (Recurring failure mode this project has hit repeatedly: label collisions, wrong
   DB-lookup results, stale "already covered" claims.)
6. **Expand OR shrink scope beyond what was explicitly asked.** If told "only delegate the navigator-fill
   piece," don't also restructure TC count/login pattern — and conversely, don't silently skip a required
   deliverable (e.g. a doc update) just because the prompt didn't spell out every file by name. Precision
   cuts both ways: give a subagent a complete, exact instruction, and hold it to exactly that scope.
7. **Take a destructive or hard-to-reverse git action unprompted** — no `--force` push, no discarding
   uncommitted work, no resetting a branch without confirming first (via `git status`/`git log`) that no
   other in-flight work is at risk. If genuinely unsure, stop and ask rather than proceed.
8. **Touch governance files or make a policy-level call solo** — `CLAUDE.md`, `EC_BUG_TRACE_SOP.md`, or a
   project-wide reclassification (e.g. "all OV-GM screens now follow pattern X") gets surfaced to the user
   as an explicit decision, never executed unilaterally.
9. **Write to any system outside this repo** (Jira, email, Slack, etc.) without separate, specific
   approval for that exact action — even if a broader task was already approved.
10. **Spawn their own nested subagents.** Delegation stays one level deep, under the main-loop agent's
    direct tracking — a subagent that needs more help reports the gap back rather than fanning out itself.
11. **Report something as "done"/"verified"/"passing" without the actual command output backing it.** An
    unrun check is unknown, not done — this applies to subagent reports exactly as it applies to the
    main-loop agent's own claims to the user.

## Why this exists
A subagent is only as precise as the instructions it's given, and only as trustworthy as the evidence it
actually gathers. This list exists so dispatch prompts don't have to re-derive these boundaries from
scratch each time, and so a subagent's own judgment calls (when to stop, when to ask, when it's safe to
proceed) have a stated baseline to check against. See also `docs/PR-REVIEW-PROTOCOL.md` (the reviewer-side
counterpart) and `docs/lessons-learned.md` for the specific incidents that produced several of these rules.
