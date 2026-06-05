# Playwright Parallel Execution Guide

## Default Parallelism
Playwright runs tests in parallel by default — one worker per CPU core (limited to 4 for stability).

## Configuration
```typescript
// playwright.config.ts
export default defineConfig({
    workers: process.env.CI ? 4 : 2,     // CI: 4, local: 2
    fullyParallel: false,                  // false = parallel files, not within a file
    // fullyParallel: true,               // true = parallel within a file too
});
```

## Test Isolation Checklist
For parallel execution to work correctly:
- [ ] Each test creates its own BrowserContext (handled by Playwright fixtures automatically)
- [ ] No shared global variables modified during tests
- [ ] Test data uses unique prefixes: `AUTOTEST_<timestamp>` or `AUTOTEST_<workerIndex>`
- [ ] Database cleanup in teardown (not just setup)
- [ ] No `test.only` in committed code

## EC-Specific Isolation
EC tests that create data (insert roles, add check groups) must use unique identifiers:
```typescript
test('Insert role', async ({ page }, testInfo) => {
    // Use worker index to ensure uniqueness in parallel runs
    const uniqueRole = `AUTOTEST_ROLE_${testInfo.workerIndex}`;
    await objectPartitionPage.insertRole(uniqueRole);

    test.afterEach(async () => {
        await objectPartitionPage.ensureRowNotExists(uniqueRole);
    });
});
```

## Force Sequential (When Needed)
```typescript
// If tests in a describe block must run in order:
test.describe.serial('Sequential tests', () => {
    test('Step 1', ...);
    test('Step 2', ...);  // runs after Step 1
});
```

## Sharding for CI
```bash
# Split 100 tests across 4 CI machines
# Machine 1:
npx playwright test --shard=1/4
# Machine 2:
npx playwright test --shard=2/4
# Machine 3:
npx playwright test --shard=3/4
# Machine 4:
npx playwright test --shard=4/4
```

## Recommended Worker Count for EC Test Suite
- Local development: `workers: 1` (single browser, easier to debug)
- CI smoke tests: `workers: 2` (2 parallel, fast)
- CI full regression: `workers: 4` (balanced speed vs stability for EC AJAX)
- Avoid `workers > 4` for EC — Oracle DB connections may saturate
