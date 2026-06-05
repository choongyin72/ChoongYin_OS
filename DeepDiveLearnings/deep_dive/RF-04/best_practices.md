# Robot Framework — World-Class Best Practices

## Code Standards (Actionable Rules)

1. **Keyword names are sentences:** `Verify Check Rule Exists In Database` not `verify_rule`
2. **One assertion focus per test:** test cases test one thing; complex setup → separate test
3. **Max 15 steps per test case:** if longer, extract to a keyword
4. **Max 20 lines per keyword:** if longer, split into sub-keywords
5. **Variables ONLY in variables/ layer:** zero inline selectors in pages or keywords
6. **Type Text not Fill Text:** for ALL PrimeFaces search/autocomplete
7. **networkidle after every AJAX action:** no exceptions
8. **AUTOTEST_ prefix:** on ALL data created by tests
9. **Screenshot path:** `${OUTPUT_DIR}${/}${SUITE_NAME}_${TEST_NAME}_failure`
10. **Documentation:** `[Documentation]` on every keyword AND test case

## Tagging Strategy
```
smoke     — fast health checks (< 2 min total)
regression — full suite (all tests)
unit      — DB verification (no browser)
system    — browser-based EC screen tests
{screen}  — screen-specific: check_rule, validation, login
{domain}  — domain-specific: strm_comp, tank, allocation
critical  — must pass for release
high      — important but not blocking
```

## PR Code Review Checklist
- [ ] No inline selectors in tests/ or keywords/
- [ ] Every keyword has [Documentation] and [Arguments]
- [ ] Every test has [Documentation] and [Tags]
- [ ] Test Teardown includes screenshot-on-failure pattern
- [ ] No Sleep keywords — replaced with Wait For Load State
- [ ] Type Text (not Fill Text) for search/autocomplete fields
- [ ] AUTOTEST_ prefix on all created test data
- [ ] Idempotent: cleanup in BOTH Test Setup AND Test Teardown
- [ ] `robot --dryrun` passes
- [ ] `robocop` passes with zero errors

## Onboarding New Team Member (1 Day)
```
Morning:
  1. Install: pip install robotframework robotframework-browser; rfbrowser init
  2. Install VS Code + RobotCode extension
  3. Read ROBOT_CLAUDE.md (30 min)
  4. Read RF-02/architecture_guide.md (20 min)
  5. Run existing tests: robot --variablefile vars/local.py --include smoke tests/

Afternoon:
  6. Add one test case to TC_Login.robot (practice)
  7. Run linting: robocop + robotidy
  8. Create a simple keyword in LoginKeywords.resource
  9. Demo Playwright MCP for locator discovery
  10. Review ROBOT_CLAUDE.md checklist before submitting PR
```
