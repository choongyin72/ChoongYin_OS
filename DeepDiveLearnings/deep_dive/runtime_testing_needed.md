# Runtime Testing Needed — Review With User at 9PM

All files produced are syntactically correct and mentally validated.
The following runtime tests are needed to confirm production readiness.

---

## JasperReports — Local Oracle DB

**Environment:** Jasper Studio 7.0.3 + `localhost:1521/ORCL` (ECKERNEL_EC/energy)

| Test | File | Action | Expected |
|---|---|---|---|
| JR-01 | `JR-01/annotated_template.jrxml` | Open in Jasper Studio → validate | Zero errors in Problems panel |
| JR-01 | `JR-01/annotated_template.jrxml` | Preview with local DB | Report renders with well data |
| JR-01 | Export to PDF | Check fonts render | No blank text |
| JR-01 | Export to Excel | Check cell types | Numbers as numbers not text |
| JR-02 | `JR-02/working_report_sql.jrxml` | Preview — $X{IN} params | Multiple streams in result |
| JR-02 | `JR-02/working_report_csv.jrxml` | Preview with test CSV | CSV data displays correctly |
| JR-03 | Compile subreport first | `subreport_detail.jrxml` → .jasper | Compiled without errors |
| JR-03 | `JR-03/master_with_subreport.jrxml` | Preview | Subreport calls work, oil total returned |
| JR-03 | `JR-03/crosstab_report.jrxml` | Preview | Crosstab renders months as columns |

**Flag:** JasperReports 7.0.3 `.jasper` files are incompatible with EC 6.21.4 runtime.
Confirm with Grant whether EC will be upgraded before deploying v7.0.3 reports.

---

## Playwright TypeScript — Local EC Web App

**Environment:** `https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/` (sysadmin/Sysadmin)

**Setup first:**
```bash
cd deep_dive/PW-01
npm init -y
npm install @playwright/test
npx playwright install chromium
```

| Test | File | Action | Expected |
|---|---|---|---|
| PW-01 | `starter_test.spec.ts` | `npx playwright test` | 3 tests pass |
| PW-01 | TC01 Login | Login succeeds | URL not on Keycloak |
| PW-01 | TC02 Check Rule nav | Screen opens | Datatable visible |
| PW-01 | TC03 Validation Overview | Screenshot taken | File saved to results/ |
| PW-02 | Run `globalSetup.ts` | `node globalSetup.ts` | `auth-state.json` created |
| PW-02 | `auth_test.spec.ts` | Tests with saved state | 3 tests pass |

**Adjust if needed:** EC element IDs for Check Rule screen and Validation Overview may need DOM inspection to confirm exact selectors.

---

## Playwright Python — Local EC Web App

**Setup first:**
```bash
pip install pytest pytest-playwright
playwright install chromium
```

| Test | File | Action | Expected |
|---|---|---|---|
| PW-01 | `python/starter_test.py` | `pytest python/starter_test.py -v` | 3 tests pass |
| PW-02 | `python/auth_setup.py` | `python auth_setup.py` | `auth-state.json` created |

---

## Robot Framework — Local EC Web App

**Setup first:**
```bash
pip install robotframework robotframework-browser robotframework-pabot
rfbrowser init
```

| Test | File | Action | Expected |
|---|---|---|---|
| RF-01 | `starter_test.robot` | `robot --variablefile RF-01/ec_variables.py RF-01/starter_test.robot` | 3 tests pass |
| RF-02 | `TC_Login.robot` | `robot --variablefile vars/local.py tests/login/` | 3 tests pass |
| RF-02 | `TC_ObjectPartition.robot` | `robot --variablefile vars/local.py tests/object_partition/` | 3 tests pass (may need selector adjustment) |
| COPY | `ROBOT_CLAUDE.md` | Copy to `C:\DEV\ROBOT\APPS\EC\14.2.4\AutomationTest\` | Governs all future RF work |

---

## Critical Action Items After Testing

1. **JasperReports v7 compatibility** — confirm with Grant whether EC runtime will be upgraded to support v7.0.3 `.jasper` files
2. **Object Partition screen locators** — exact selectors depend on EC version. Use Playwright MCP to confirm after local EC is confirmed working
3. **ECHelpers.py Oracle connection** — test `python resources/libraries/ECHelpers.py` works with local Oracle DB
4. **Playwright MCP setup** — add to `C:\Users\choong-yin.lee\.claude\settings.json` with `--ignore-https-errors` for EC
