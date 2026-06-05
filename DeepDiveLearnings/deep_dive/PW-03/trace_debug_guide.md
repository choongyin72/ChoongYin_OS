# Playwright Trace Viewer & Debugging Guide

## Enabling Tracing

### In playwright.config.ts
```typescript
use: {
    trace: 'on-first-retry',    // trace only on test retry (recommended for CI)
    // trace: 'on',              // always trace (large files)
    // trace: 'retain-on-failure', // keep trace only when test fails
}
```

### In Test (Programmatic)
```typescript
await context.tracing.start({ screenshots: true, snapshots: true });
// ... test code ...
await context.tracing.stop({ path: 'trace.zip' });
```

## Opening Trace Viewer
```bash
npx playwright show-trace trace.zip
# Opens browser-based trace viewer at localhost
```

## Trace Viewer UI
- **Timeline** — shows all actions in chronological order
- **Action log** — click any action to jump to that moment
- **DOM snapshot** — exact HTML at that point in time
- **Network panel** — all requests and responses during that action
- **Console panel** — console.log output
- **Screenshot** — what the page looked like

## Playwright Inspector (Step-by-Step Debug)
```bash
# Run tests with inspector
npx playwright test --debug

# Or set env var
PWDEBUG=1 npx playwright test

# Pause at specific point in test
await page.pause();  // opens inspector at this point
```

## VS Code Debugger Configuration
```json
// .vscode/launch.json
{
    "configurations": [
        {
            "name": "Playwright: Debug",
            "type": "node",
            "request": "launch",
            "program": "${workspaceFolder}/node_modules/.bin/playwright",
            "args": ["test", "--debug", "${file}"],
            "env": {
                "EC_URL": "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
                "PWDEBUG": "1"
            }
        }
    ]
}
```

## Slow Motion for Visual Debugging
```typescript
const browser = await chromium.launch({ slowMo: 500 }); // 500ms between actions
```

## Console Log Capture
```typescript
page.on('console', msg => {
    if (msg.type() === 'error') {
        console.log(`Browser ERROR: ${msg.text()}`);
    }
});
```

## Common Debugging Scenarios

| Problem | Debug approach |
|---|---|
| Test clicks wrong element | Inspector → hover over elements → verify locator matches |
| AJAX not waited for | Trace viewer → Network panel → find which request is missing |
| Screenshot differs from expectation | Trace viewer → DOM snapshot at failure point |
| Element not found | `page.pause()` before the failing line → inspect DOM manually |
| Flaky test | Run 5x: `--repeat-each=5` → trace all runs → compare timings |
