# RF-02: Layered POM Architecture Guide

## The 5-Layer Architecture

```
Layer 1: tests/           ← WHAT to test (pure business steps, no selectors)
Layer 2: keywords/        ← business operations (calls page layer)
Layer 3: pages/           ← screen interactions (calls Browser Library with variables)
Layer 4: variables/       ← ALL selectors and values (never in layers 1-3)
Layer 5: libraries/       ← Python utilities (DB queries, generators, parsers)
```

## Layer Rules (MANDATORY — violations break maintainability)

### Layer 1 — tests/
✅ Contains ONLY test cases  
✅ Imports from keywords/ layer  
✅ Uses ${VARIABLES} not selectors  
❌ NEVER: `Click    id=button` or `Fill Text    xpath=//input` — that is layer 3  
❌ NEVER: inline locator strings  

### Layer 2 — keywords/
✅ Business-readable keyword names: "Insert Role For Operator"  
✅ Calls page layer keywords  
✅ Contains idempotency helpers: "Ensure Role Does Not Exist"  
❌ NEVER: direct Browser Library calls  
❌ NEVER: locator strings  

### Layer 3 — pages/
✅ Screen-specific implementation  
✅ Uses ${VARIABLE} selectors from variables/ — never inline strings  
✅ Calls Browser Library directly  
✅ Named after screen: LoginPage.resource, ObjectPartitionPage.resource  
❌ NEVER: hardcoded selector strings — all must come from variables/  

### Layer 4 — variables/
✅ ALL locator strings defined here  
✅ Naming: `${SCREEN_ELEMENT_TYPE}` e.g. `${OP_INSERT_BTN}`  
✅ Comments above each screen section  
❌ NEVER: business logic here — only data  

### Layer 5 — libraries/
✅ Python utilities (DB queries, parsers)  
✅ ROBOT_LIBRARY_SCOPE = 'SUITE'  
✅ @keyword decorator on all public methods  

## When to Add a New Keyword vs Reuse
1. Search all .resource files for similar keyword first
2. If similar exists: extend it with optional argument
3. If none exists: add to the correct layer
4. Rule: keyword appearing in 2+ tests → move to keywords/ layer

## Anti-Patterns to Avoid

| Anti-pattern | Correct pattern |
|---|---|
| `Click    id=saveButton` in test case | Move to page layer |
| Same selector in 3 different files | Move to variables/ |
| 40-line keyword | Split into sub-keywords |
| `Sleep    5s` | `Wait For Load State    networkidle` |
| Hardcoded URL in .robot | `${EC_URL}` from variable file |
| Test depends on test order | Idempotent setup/teardown |
