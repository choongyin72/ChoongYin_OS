# Network Interception Guide — Playwright

## When to Use Network Interception in EC Testing

| Use case | Technique |
|---|---|
| Test error handling without breaking EC DB | Mock API endpoint to return 500 |
| Test with controlled data (no DB dependency) | Mock API to return fixture JSON |
| Verify EC makes correct API calls | Observe requests, assert URL/headers/body |
| Speed up tests by skipping slow EC reports | Mock JasperServices response |
| Test loading states | Delay API response with `route.fulfill({ delay: 2000 })` |

## Route Pattern Matching
```
**/api/**        — any URL containing /api/
https://*/rest/* — any domain, /rest/ path
**/jasper/**     — JasperReports service calls
**/*.js          — all JavaScript files
```

## EC-Specific: Mock JasperReports Service
```typescript
// Intercept EC's internal Jasper call and return a static PDF fixture
await page.route('**/jasper/rest_v2/reports/**', async route => {
    const pdfBuffer = require('fs').readFileSync('fixtures/test-report.pdf');
    await route.fulfill({
        status: 200,
        contentType: 'application/pdf',
        body: pdfBuffer,
    });
});
```

## Logging All XHR/Fetch Requests (Debug Mode)
```typescript
// Add to test setup for debugging EC's AJAX calls
page.on('request', req => {
    if (['xhr', 'fetch'].includes(req.resourceType())) {
        console.log(`→ ${req.method()} ${req.url()}`);
    }
});
page.on('response', resp => {
    if (['xhr', 'fetch'].includes(resp.request().resourceType())) {
        console.log(`← ${resp.status()} ${resp.url()}`);
    }
});
```

## Python Equivalents
```python
# Route interception
page.route('**/api/**', lambda route: route.fulfill(
    status=200,
    content_type='application/json',
    body='{"status": "ok"}'
))

# Request observation
page.on('request', lambda req: print(f'→ {req.method} {req.url}'))
page.on('response', lambda resp: print(f'← {resp.status} {resp.url}'))

# Wait for response
with page.expect_response('**/api/calc/**') as resp_info:
    page.locator('#runCalcButton').click()
response = resp_info.value
data = response.json()
```
