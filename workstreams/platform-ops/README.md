# Workstream: Platform Ops

Release management, DB upgrades, CI/CD, deployments, and dev environment for Woodside Pluto ECaaS.

## Release cadence
- Branch flow: `develop` → `release/<tag>` → `master`
- Tags: `PROD_RELEASE_X.X.XX`
- CI: Jenkins (`Jenkinsfile` — Maven + jdk17 on agent)
- Artifact repo: internal Nexus (`repository.releases` / `repository.snapshots`)

## Dev environment
- App: https://app-plutodev.woodside-pluto.tieto-og.cloud/ (user: sysadmin)
- DB: db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev (Oracle, user: ECKERNEL_EC)
- Container-based env in `dev-environment/` folder

## Java version note
- Jenkins agent: **jdk17**
- Local dev: **Java 21 (Zulu)** — be aware of version delta when comparing CI vs local build output

## Key repo folders
- `Jenkinsfile` — CI pipeline definition
- `pom.xml` — aggregator POM (groupId: `com.ec.custom.woodside.plp`)
- `bpm/` — BPM building blocks
- `initial-db-upgrade/upgrade-scripts/` — DB migration scripts
- `initial-dataload/` — seed / reference data
- `dev-environment/` — container + deployment configs
