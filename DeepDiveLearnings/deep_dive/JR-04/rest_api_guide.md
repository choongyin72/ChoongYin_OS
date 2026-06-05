# JasperReports REST API Guide — v7.0.3+

## Base URL and Authentication

```
Base: https://{jasper-server}/jasperserver/rest_v2/
Auth: HTTP Basic — Authorization: Basic base64(username:password)
     OR Token: GET /rest_v2/login → returns JSESSIONID cookie
```

## Key Endpoints

### 1. Browse Repository
```bash
# List all resources in a folder
curl -u admin:admin \
  "https://server/jasperserver/rest_v2/resources?folderUri=/reports/EC"

# Response: JSON array of resource descriptors
```

### 2. Run Report to PDF
```bash
curl -X POST -u admin:admin \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"reportParameter": [
    {"name": "P_DAYTIME", "value": ["2025-01-01"]},
    {"name": "P_FACILITY_CODE", "value": ["ALL"]}
  ]}}' \
  "https://server/jasperserver/rest_v2/reports/reports/EC/DailyProduction.pdf" \
  -o output.pdf
```

### 3. Run Report to Excel
```bash
curl -X POST -u admin:admin \
  -H "Content-Type: application/json" \
  -d '{"parameters": {"reportParameter": [{"name": "P_DAYTIME", "value": ["2025-01-01"]}]}}' \
  "https://server/jasperserver/rest_v2/reports/reports/EC/DailyProduction.xlsx" \
  -o output.xlsx
```

### 4. Get Report Input Controls (Parameters)
```bash
curl -u admin:admin \
  "https://server/jasperserver/rest_v2/reports/reports/EC/DailyProduction/inputControls"
# Returns: parameter names, types, default values, allowed values
```

### 5. Upload JRXML to Repository
```bash
curl -X PUT -u admin:admin \
  -H "Content-Type: application/repository.reportUnit+json" \
  -d '{"label":"Daily Production","uri":"/reports/EC/DailyProduction","jrxml":{...}}' \
  "https://server/jasperserver/rest_v2/resources/reports/EC/DailyProduction"
```

### 6. Async Report Execution
```bash
# Step 1: Start execution
curl -X POST -u admin:admin \
  -H "Content-Type: application/json" \
  -d '{"reportUnitUri":"/reports/EC/DailyProduction","async":true,"outputFormat":"pdf"}' \
  "https://server/jasperserver/rest_v2/reportExecutions"
# Returns: {"requestId": "abc123", "status": "queued"}

# Step 2: Poll for status
curl -u admin:admin \
  "https://server/jasperserver/rest_v2/reportExecutions/abc123/status"
# Returns: {"value": "ready"} when done

# Step 3: Download result
curl -u admin:admin \
  "https://server/jasperserver/rest_v2/reportExecutions/abc123/exports/pdf/outputResource" \
  -o result.pdf
```

## EC JasperServices Notes
EC's internal report service (`frmw-report` module) wraps JasperReports directly — not Jasper Server. EC calls `JasperFillManager.fillReport()` in-process with an Oracle connection. The REST API above applies to standalone Jasper Server deployments, not EC embedded reports.
