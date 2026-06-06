"""Recreate all deep dive tasks without battery restrictions."""
import subprocess, os
from datetime import datetime, timedelta
from pathlib import Path

PY     = r'C:\Tools\python\Python314\python.exe'
SCRIPT = r'C:\Projects\ChoongYin_OS\tools\deep-dive-scheduler\run_session.py'
TASKS  = Path(r'C:\Projects\ChoongYin_OS\tools\deep-dive-scheduler\tasks')
TASKS.mkdir(exist_ok=True)

sessions = [
    ('D',    2.0), ('E',   2.5), ('F',    2.0), ('G',    3.0),
    ('H',    2.0), ('I',   2.5), ('ET-A', 2.5), ('ET-B', 2.5),
    ('ET-C', 2.0), ('ET-D',2.5), ('ET-E', 2.0),
]

# Delete old tasks
for sess, _ in sessions:
    task = f'ECDeepDive_Session_{sess.replace("-","_")}'
    subprocess.run(f'schtasks /Delete /TN "{task}" /F',
                   shell=True, capture_output=True)

# Start Session D in 10 minutes from now
now   = datetime.now().replace(second=0, microsecond=0)
start = now + timedelta(minutes=10)

for sess, hrs in sessions:
    task     = f'ECDeepDive_Session_{sess.replace("-","_")}'
    xml_file = TASKS / f'task_{sess.replace("-","_")}.xml'
    start_ts = start.strftime('%Y-%m-%dT%H:%M:%S')

    xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo><Description>EC Deep Dive Session {sess}</Description></RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <StartBoundary>{start_ts}</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <ExecutionTimeLimit>PT4H</ExecutionTimeLimit>
    <Enabled>true</Enabled>
  </Settings>
  <Actions>
    <Exec>
      <Command>{PY}</Command>
      <Arguments>"{SCRIPT}" {sess}</Arguments>
      <WorkingDirectory>C:\\Projects\\ChoongYin_OS</WorkingDirectory>
    </Exec>
  </Actions>
</Task>'''

    xml_file.write_text(xml, encoding='utf-16')
    r = subprocess.run(
        f'schtasks /Create /F /TN "{task}" /XML "{xml_file}"',
        shell=True, capture_output=True, text=True
    )
    status = 'OK' if r.returncode == 0 else f'FAIL: {r.stderr.strip()[:60]}'
    print(f'Session {sess:5s} @ {start.strftime("%d/%m/%Y %H:%M")} — Battery OK — {status}')
    start += timedelta(hours=hrs, minutes=30)
