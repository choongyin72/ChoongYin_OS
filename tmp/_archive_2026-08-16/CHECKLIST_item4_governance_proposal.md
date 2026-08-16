# CHECKLIST - Item 4: re-raise the step-0 rule as a governance PROPOSAL

## Why this PR exists
- [x] PR #285 landed this rule into `CLAUDE.md` + `EC_BUG_TRACE_SOP.md` WITHOUT asking. The reviewer
      reverted both files before merging, per the owner's decision, and wrote: "Feel free to re-raise the
      rule addition as its own small PR/proposal."
- [x] The tool itself SURVIVED that merge (`scripts/check_known_issue.py` exists on master) but nothing
      references it - verified: `grep -c check_known_issue CLAUDE.md EC_BUG_TRACE_SOP.md` -> 0 and 0.
      So today it is an orphan: a tool I have to remember to run, which is the exact failure it addresses.

## What I did differently this time
- [x] Own branch off master, nothing else bundled with it.
- [x] Both governance files named EXPLICITLY in "Files touched" (the reviewer's specific instruction - last
      time they appeared in the diff but not in the body).
- [x] Text marked "PROPOSED (owner sign-off pending)" in-line, so if it merges by accident it still reads
      as unapproved rather than as an active rule.
- [x] Nothing else in the diff: no tooling, no screens.

## Verification
- [x] Conflict markers from a `git stash apply` were removed by restoring master's version of both files
      and re-adding the text cleanly - `grep -c "<<<<<<<\|>>>>>>>"` -> 0 and 0.
- [x] The referenced path is correct for master: the tool is at `scripts/check_known_issue.py`, not the old
      `tmp/` location.
- [x] `py scripts/check_known_issue.py "Chemical Product"` -> exit 2 (prior record found), so the command
      the rule asks for actually works from the path the rule cites.

## Decision requested
- [ ] OWNER: approve (rule becomes active) or reject (I delete these two edits and, if you prefer, the
      orphaned tool with them). This box is for the owner, not for me to tick.
