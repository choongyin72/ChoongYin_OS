"""
EC Deep Dive Session Runner
Runs a deep dive session via Claude CLI non-interactively.
Called by Windows Task Scheduler.
"""
import subprocess, sys, os, json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(r'C:\Projects\ChoongYin_OS\tools\deep-dive-scheduler\session_log.txt')

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{timestamp}] {msg}'
    print(line)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def run_session(session_name, prompt):
    log(f'Starting {session_name}')

    claude_cmd = r'C:\Users\choong-yin.lee\AppData\Roaming\npm\claude.cmd'
    project_dir = r'C:\Projects\ChoongYin_OS'

    result = subprocess.run(
        [claude_cmd, '--print', '--dangerously-skip-permissions', prompt],
        cwd=project_dir,
        capture_output=False,
        text=True,
        timeout=7200  # 2-hour timeout
    )

    if result.returncode == 0:
        log(f'{session_name} completed successfully')
    else:
        log(f'{session_name} failed with code {result.returncode}')

    return result.returncode

if __name__ == '__main__':
    if len(sys.argv) < 2:
        log('ERROR: No session name provided')
        sys.exit(1)

    session = sys.argv[1]

    prompts = {
        'D': """EC Deep Dive Session D — Woodside Extensions.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ec-application-deep-dive.md to reload context.
Deep dive 3 items:
#19 Extension DB migration (7->9): Read EC Tech Docs technical-documentation/frmw/ec-extensions/db-migration.html (auth: choong-yin.lee@tieto.com/Xinyee!20090330), read ec-application source frmw-extensions folder, understand Flyway in extensions.
#20 Creating extension classes (5->9): Read EC Tech Docs development/ pages, read actual Woodside extension at C:\\DEV\\GIT\\woodside_impl_pluto_12839\\extensions\\ and understand ZWP_ class creation.
#21 ZWP_/ZWT_ Woodside extension patterns (7->9): Deep read C:\\DEV\\GIT\\woodside_impl_pluto_12839\\extensions\\ folder structure, read actual extension XML/SQL files, understand naming conventions and patterns.
After each item: update ec-application-deep-dive.md, git add + commit + push with descriptive message.
After all items: append Session D summary to C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\session-summary-2026-06-05.md, git commit + push.""",

        'E': """EC Deep Dive Session E — Business Domain Production.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ec-application-deep-dive.md to reload context.
Deep dive 3 items:
#22 Production Well/Stream/Tank concepts (7->9): Read EC Tech Docs technical-documentation/prod/object_configuration/ pages (Well, Stream, Tank), read ECpedia Upstream page and Well and reservoir page, read ec-application prod module.
#23 Hydrocarbon accounting (5->9): Read EC Tech Docs technical-documentation/prod/prod_hydrocarbon_accounting.html, read ECpedia Production allocation page (374800386) and Allocation flowchart (374800622).
#24 Daily+Monthly Allocation BPM (5->9): Read EC Tech Docs technical-documentation/prod/bpm/ pages, read ECpedia Daily/Monthly Allocation BPM Workflow pages.
After each item: update ec-application-deep-dive.md, git add + commit + push.
After all items: append Session E summary to session-summary-2026-06-05.md, git commit + push.""",

        'F': """EC Deep Dive Session F — Architecture and Database.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ec-application-deep-dive.md to reload context.
Deep dive 4 items:
#9 JSF/PrimeFaces rendering (7->9): Read frmw-pf module source, understand p:dataTable, p:ajax, f:ajax event flow, PrimeFaces component lifecycle.
#10 Screen template structure (7->9): Read ec-web/src/main/webapp/xhtml/screen/ files fully, understand toolbar/status area/splitter/WebSocket.
#11 Flyway migrations deep (7->9): Read EC Tech Docs ec_flyway_developer_handbook.html, read actual migration files in ec-db-migration-oc-0.
#12 Journal tables _JN mechanics (7->9): Read data_modelling_guideline section on journal tables, find JN_xxx trigger examples in source.
After each item: update ec-application-deep-dive.md, git add + commit + push.
After all items: append Session F summary to session-summary-2026-06-05.md, git commit + push.""",

        'G': """EC Deep Dive Session G — Calculation Engine.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ec-application-deep-dive.md to reload context.
Deep dive 5 items:
#13 Calculation framework process diagrams (7->9): Read EC Tech Docs calculation_framework.html, read ECpedia Calculation Design (279511052).
#14 Library calculations (6->9): Read ECpedia Library Calculations (290881537), Library Calculation Basics (290881778), Working with Library Calculations (290882495).
#15 Calculation execution engine (6->9): Read frmw-calc module source, understand CalculationObject, CalculationValue, rule execution sequence.
#16 AGA3/AGA8 standards (5->9): Read EC Tech Docs prod_api_measurement_standards.html, understand gas volume calculations.
#18 jBPM workflow (5->9): Read EC Tech Docs frmw/bpm/ pages, ECpedia JBPM (546472090), understand allocation workflow execution.
After each item: update ec-application-deep-dive.md, git add + commit + push.
After all items: append Session G summary to session-summary-2026-06-05.md, git commit + push.""",

        'H': """EC Deep Dive Session H — PVT Properties.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ec-application-deep-dive.md to reload context.
Deep dive 1 item:
#17 PVT properties (4->9): Read EC Tech Docs prod_prod_test_result_preprocessing_and_calculate_pvt.html, read prod module PVT calculation source, understand density/viscosity/compressibility calculations in EC context.
After item: update ec-application-deep-dive.md, git add + commit + push.
After all items: append Session H summary to session-summary-2026-06-05.md, git commit + push.""",

        'I': """EC Deep Dive Session I — Business Domain Revenue/Chemistry/Transport.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ec-application-deep-dive.md to reload context.
Deep dive 3 items:
#25 Revenue module (3->9): Read EC Tech Docs technical-documentation/revn/ pages, ECpedia Revenue pages.
#26 Chemistry module (3->9): Read EC Tech Docs prod_ec_chemistry.html, ECpedia Chemical management (453869801).
#27 Transport/Cargo module (2->9): Read EC Tech Docs technical-documentation/transport/ pages, ECpedia Cargo operations (453837019), Terminal Operations (453836999).
After each item: update ec-application-deep-dive.md, git add + commit + push.
After all items: append Session I + full EC deep dive completion summary to session-summary-2026-06-05.md, git commit + push.""",

        'ET-A': """ectestautomation Deep Dive ET-A — Core utilities.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ectestautomation-deep-dive.md to reload context.
Deep dive 4 items:
#ET06 ectest-core base utilities (4->9): Read C:\\DEV\\GIT\\ecaas_clp_hongkong\\ectestautomation\\ectest-core module fully.
#ET07 screenletmapping.properties (5->9): Read the file, understand how screenlet keys map to EC screen elements.
#ET12 Checkbox and complex cell handling (7->9): Read ECCheckboxCell, ECDropdownCell classes in ectest-pages.
#RF01 Navigation pattern translation RF vs Java (8->9): Compare GenericSteps.java navigation with our Robot Framework ec_navigation.robot keyword.
After each item: update ectestautomation-deep-dive.md, git add + commit + push.
After all items: append ET-A summary to session-summary-2026-06-05.md, git commit + push.""",

        'ET-B': """ectestautomation Deep Dive ET-B — Page objects and steps.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ectestautomation-deep-dive.md to reload context.
Deep dive 2 items:
#ET05 113 page objects full coverage (5->9): Read ALL page objects in ectest-pages/src/main/java/com/ec/selenium/. Group by domain. Extract key locators and interaction patterns.
#ET08/#ET09 90+ step definition classes (6->9): Read all step classes in ectest-ecpa/src/main/java/com/ec/storysteps/. Extract patterns, GenericSteps, domain-specific steps.
After each item: update ectestautomation-deep-dive.md, git add + commit + push.
After all items: append ET-B summary to session-summary-2026-06-05.md, git commit + push.""",

        'ET-C': """ectestautomation Deep Dive ET-C — Framework internals.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ectestautomation-deep-dive.md to reload context.
Deep dive 4 items:
#ET01 Arquillian+Graphene integration (7->9): Read arquillian.xml fully, understand Graphene WebDriver extensions, injection patterns.
#ET04 Docker test environment (5->9): Read ectest-ecpa/src/docker/ folder, understand docker-compose test setup.
#ET10 Multi-user workflow patterns (7->9): Read Coal and LNG multi-user feature files, extract the login/logout/action patterns.
#ET11 Date resolution edge cases (7->9): Read TestHelper.resolveDate() implementation, all SYS.DATE patterns.
After each item: update ectestautomation-deep-dive.md, git add + commit + push.
After all items: append ET-C summary to session-summary-2026-06-05.md, git commit + push.""",

        'ET-D': """ectestautomation Deep Dive ET-D — Business domains.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ectestautomation-deep-dive.md to reload context.
Deep dive 6 items:
#ET15 LNG cargo lifecycle (7->9): Read all LNG feature files and page objects.
#ET16 Document workflow (7->9): Read procurementfinance steps and pages (Transfer, Booking, Invoice).
#ET17 Planning and Scheduling screens (6->9): Read planningandscheduling/ folder fully.
#ET18 Pricing calculations (6->9): Read pricing/ steps and pages.
#ET19 Terminal operations (5->9): Read terminalservices/ folder.
#ET20 Invoice verification variants (5->9): Read InvoiceVerification*.java classes for all variants.
After each item: update ectestautomation-deep-dive.md, git add + commit + push.
After all items: append ET-D summary to session-summary-2026-06-05.md, git commit + push.""",

        'ET-E': """ectestautomation Deep Dive ET-E — Infrastructure.
Read C:\\Projects\\ChoongYin_OS\\workstreams\\master-plan\\drafts\\ectestautomation-deep-dive.md to reload context.
Deep dive 4 items:
#ET02 Java 11 module system (6->9): Understand --add-opens requirements and why they are needed.
#ET03 Maven Failsafe vs Surefire (7->9): Read pom.xml configurations, understand integration vs unit test execution.
#ET13 Selenium Grid setup (6->9): Read arquillian.xml grid config, understand GridHub usage.
#ET14 Extent Reports configuration (7->9): Read test runner classes reporting config, understand HTML report generation.
After each item: update ectestautomation-deep-dive.md, git add + commit + push.
After all items: append ET-E summary + FULL completion summary of all sessions to session-summary-2026-06-05.md, git commit + push. This is the final session.""",
    }

    if session not in prompts:
        log(f'ERROR: Unknown session {session}')
        sys.exit(1)

    exit_code = run_session(f'Session {session}', prompts[session])
    sys.exit(exit_code)
