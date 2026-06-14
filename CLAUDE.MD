# WORKER SESSION — READ FIRST

## On session start (mandatory)
Before starting any automation work, read:
- docs/lessons-learned.md  → standing rules from prior reviews (mandatory)
- docs/automation-scorecard.md → current coverage + parked backlog
- STATUS.md → active Jira tickets + blockers

## During a long session (self-check rule)
After every 10 commits OR when resuming after a long pause, re-read
docs/lessons-learned.md to check for new rules added by the reviewer session.
Context compression does NOT re-read this file automatically — you must do it
explicitly. New rules from the reviewer take effect immediately when you read them.

## Why this matters
A reviewer session runs daily at 20:00 AWST and appends new rules to
docs/lessons-learned.md based on analysis of your recent commits. If you are
in a long-running session that started before 20:00, you will miss those rules
unless you re-read the file yourself mid-session.

---

GIT Project Folder   : C:\DEV\GIT\woodside_impl_pluto_12839
EC Web App Url       : https://app-plutodev.woodside-pluto.tieto-og.cloud/
EC WebUser Id        : sysadmin
EC Web User Password : Sysadmin@01
EC DB Url            : db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev
EC DB User Id        : ECKERNEL_EC
EC DB User Password  : energy

Java                 : C:\Tools\java\zulu21.36.17-ca-jdk21.0.4-win_x64
VS Code              : C:\Tools\Microsoft VS Code\Code.exe
Maven                : C:\Tools\maven\apache-maven-3.8.4-bin
Python               : C:\Tools\python\Python314
Notepad++            : C:\Program Files\Notepad++
# Verified Data Sources (2026-06-02)

## Project
- Woodside Git Repo : C:\DEV\GIT\woodside_impl_pluto_12839

## Web & DB
- EC Web App        : https://app-plutodev.woodside-pluto.tieto-og.cloud/ (user: sysadmin)
- EC Database       : db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev (user: ECKERNEL_EC)

## Tools (verified paths)
- Java 21           : C:\Tools\java\zulu21.36.17-ca-jdk21.0.4-win_x64\bin\java.exe
- Maven             : C:\Tools\maven\apache-maven-3.8.4-bin\bin\mvn
- Python 3.14       : C:\Tools\python\Python314\python.exe  (use `py` launcher)
- VS Code           : C:\Tools\Microsoft VS Code\Code.exe
- Notepad++         : C:\Program Files\Notepad++\notepad++.exe

# Client SharePoint (added 2026-06-02)
- Woodside Pluto Client SP : https://woodsideenergy.sharepoint.com/sites/PHBRQuorum

# Additional Verified Sources (added 2026-06-02)
- EC Hub (Nexus Repo) : https://hub.energycomponents.com/ (user: choong-yin.lee@tieto.com)
- EC Tech Docs 14.2.5 : https://hub.energycomponents.com/repository/site-hub/ec-application/14.2.5/documentation/Energy-Components/14.2.5/ecindex.html

# EC Best Practices (added 2026-06-03)
- EC Best Practices Confluence (BPR space): https://energycomponents.atlassian.net/wiki/spaces/BPR
- Cloud ID: energycomponents.atlassian.net
- Space: EC Professional Services - Best Practices & Sandbox
- Nickname: ECpedia | Launched: 1 April 2026 | 50+ pages
