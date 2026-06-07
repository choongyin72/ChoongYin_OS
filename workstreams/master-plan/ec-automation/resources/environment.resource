*** Settings ***
Documentation       T1 (shared) — environment configuration for all EC suites.
...                 Local sandbox values. For real CI, override via env vars / secrets.


*** Variables ***
${EC_URL}       https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
${EC_USER}      sysadmin
${EC_PASS}      sysadmin
${HEADLESS}     ${TRUE}
${HOLD}         0s
${DB_DSN}       localhost:1521/ORCL
