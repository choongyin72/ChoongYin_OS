"""Diagnose the scheduler: (A) which WINDOWS tasks run our scripts (name/schedule/last-run/result/next-run),
(B) the .claude internal cron last-fired time in UTC + AWST. Read-only."""
import csv, json, datetime, pathlib

CSV = r"c:\Projects\ChoongYin_OS\tmp\schtasks_dump.csv"
JSON = r"c:\Projects\ChoongYin_OS\.claude\scheduled_tasks.json"

print("=== (A) WINDOWS Task Scheduler — tasks that run ChoongYin_OS scripts ===")
rows = list(csv.reader(open(CSV, encoding="utf-8", errors="replace")))
hdr = None
seen = set()
for r in rows:
    if not r:
        continue
    if r[0] == "HostName":
        hdr = r
        continue
    if hdr is None or len(r) < len(hdr):
        continue
    d = dict(zip(hdr, r))
    run = d.get("Task To Run", "")
    if "ChoongYin_OS" not in run:
        continue
    name = d.get("TaskName", "")
    if name in seen:
        continue
    seen.add(name)
    print(f"\n  {name}")
    print(f"     Schedule Type : {d.get('Schedule Type')}   Start: {d.get('Start Time')} {d.get('Start Date')}")
    print(f"     Last Run Time : {d.get('Last Run Time')}   Last Result: {d.get('Last Result')}")
    print(f"     Next Run Time : {d.get('Next Run Time')}   Status: {d.get('Status')}   State: {d.get('Scheduled Task State')}")

print("\n=== (B) .claude internal cron (scheduled_tasks.json) ===")
js = json.load(open(JSON, encoding="utf-8"))
for t in js.get("tasks", []):
    def conv(ms):
        if not ms:
            return "(never)"
        u = datetime.datetime.fromtimestamp(ms / 1000, datetime.timezone.utc)
        a = u + datetime.timedelta(hours=8)
        return f"{u:%Y-%m-%d %H:%M:%S} UTC  =  {a:%Y-%m-%d %H:%M:%S} AWST"
    print(f"\n  id={t['id']}  cron='{t.get('cron')}'  recurring={t.get('recurring', False)}")
    print(f"     createdAt   : {conv(t.get('createdAt'))}")
    print(f"     lastFiredAt : {conv(t.get('lastFiredAt'))}")

now = datetime.datetime.now(datetime.timezone.utc)
print(f"\n  NOW = {now:%Y-%m-%d %H:%M:%S} UTC  =  {now + datetime.timedelta(hours=8):%Y-%m-%d %H:%M:%S} AWST")
