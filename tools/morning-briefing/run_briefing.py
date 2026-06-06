"""
Morning Briefing Runner — called by Windows Task Scheduler at 9AM weekdays.
Runs Claude CLI to produce daily status update.
"""
import subprocess, sys
from datetime import datetime
from pathlib import Path

LOG = Path(r'C:\Projects\ChoongYin_OS\tools\morning-briefing\briefing_log.txt')

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f'[{ts}] {msg}'
    print(line)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

PROMPT = """Good morning Choong Yin! Producing your daily 9AM status update.

Pull today's information and produce the standard morning briefing:
1. Search today's emails (outlook_email_search after today 00:00)
2. Search today's calendar (outlook_calendar_search for today)
3. Search today's Teams messages (chat_message_search after today 00:00)

Present in this format:
☀️ Morning Briefing — [Day, Date] | Woodside Pluto

📅 MEETINGS TODAY
[List with MY times, cancelled flagged]

📧 EMAILS
[New emails with sender and key points]

💬 TEAMS HIGHLIGHTS
[Key discussions and action items]

🚨 ACTION ITEMS
[Pending/overdue tasks from todo list]

Be concise but complete."""

if __name__ == '__main__':
    log('Starting morning briefing')
    claude = r'C:\Users\choong-yin.lee\AppData\Roaming\npm\claude.cmd'
    r = subprocess.run(
        [claude, '--print', '--dangerously-skip-permissions', PROMPT],
        cwd=r'C:\Projects\ChoongYin_OS',
        capture_output=False, text=True, timeout=300
    )
    log(f'Briefing done. Exit code: {r.returncode}')
