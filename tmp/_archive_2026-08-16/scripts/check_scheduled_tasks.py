"""Read-only: list Windows scheduled tasks related to ChoongYin_OS automation (auto-attach, briefing)."""
import subprocess

out = subprocess.run(['schtasks', '/query', '/fo', 'LIST', '/v'],
                     capture_output=True, text=True, errors='ignore').stdout
blocks = out.split('\n\n')
keys = ('attach', 'briefing', 'choong', 'claude', 'reconcile', 'deep-dive', 'deep_dive', 'status')
hits = []
for blk in blocks:
    low = blk.lower()
    if any(k in low for k in keys):
        name = next_run = status = last_run = last_result = ''
        for line in blk.splitlines():
            s = line.strip()
            if s.startswith('TaskName:'):      name = s.split(':', 1)[1].strip()
            elif s.startswith('Next Run Time:'): next_run = s.split(':', 1)[1].strip()
            elif s.startswith('Status:'):        status = s.split(':', 1)[1].strip()
            elif s.startswith('Last Run Time:'):  last_run = s.split(':', 1)[1].strip()
            elif s.startswith('Last Result:'):    last_result = s.split(':', 1)[1].strip()
        hits.append((name, status, next_run, last_run, last_result))

print(f'Automation-related scheduled tasks found: {len(hits)}\n')
for name, status, nxt, last, res in hits:
    print(f'  {name}')
    print(f'    status={status}  next={nxt}  last_run={last}  last_result={res}')
if not hits:
    print('  (none found — no ChoongYin_OS automation tasks registered in Task Scheduler)')
