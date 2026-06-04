"""
Morning Briefing — SMTP Version
Sends daily briefing email via Quorum SMTP (smtp.office365.com).
Runs via Windows Task Scheduler at 08:30 AWST daily.
NOTE: Live email/calendar data will be added once IT approves OAuth app.
"""
import sys, smtplib, keyring
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sys.stdout.reconfigure(encoding='utf-8')

EMAIL  = 'choong-yin.lee@quorumsoftware.com'
SMTP_HOST = 'smtp.office365.com'
SMTP_PORT = 587
MY8    = timezone(timedelta(hours=8))


def get_password():
    pwd = keyring.get_password('morning_briefing_smtp', EMAIL)
    if not pwd:
        print('❌ Password not found. Run smtp_setup.py first.')
        sys.exit(1)
    return pwd


def build_html(now):
    date_str    = now.strftime('%A, %d %B %Y')
    time_str    = now.strftime('%H:%M')
    day_of_week = now.strftime('%A')

    # Pending tasks
    tasks = [
        ('🔴', 'BLP Offtake Report — overdue'),
        ('🔴', 'Daniel Perez UAT blockers — overdue since 1 Jun'),
        ('🟡', 'Reply to Grant — Issue_1052 (ST vs UAT + Phase 1 results)'),
        ('🟡', 'Add Issue_1052 to v1.0.38 tab (after Grant confirms)'),
        ('🟡', 'Verify 1.0.37 changes in ECaaS TEST environment'),
        ('🟡', 'Raise ECPR for R_BLP_MONTHLY_ALLOC_PLUTO fix'),
        ('🔵', 'PRs #603–606 — monitor release team, alert Grant if not done'),
        ('🔵', 'Rebase ECPR-31030/31/32/34 — monitor release team'),
    ]

    task_rows = ''
    for icon, task in tasks:
        colour = '#C00' if '🔴' in icon else ('#C07000' if '🟡' in icon else '#1F497D')
        task_rows += f'''
        <tr>
          <td style="padding:6px 10px;border-bottom:1px solid #eee;font-size:18px;width:30px">{icon}</td>
          <td style="padding:6px 10px;border-bottom:1px solid #eee;font-size:13px;color:{colour}">{task}</td>
        </tr>'''

    # Woodside project quick links
    links = [
        ('EC Web App (COPS DEV)', 'https://app-plutodev.woodside-pluto.tieto-og.cloud/'),
        ('EC JIRA', 'https://energycomponents.atlassian.net'),
        ('Woodside SharePoint', 'https://woodsideenergy.sharepoint.com/sites/PHBRQuorum'),
        ('EC Hub (Nexus)', 'https://hub.energycomponents.com/'),
    ]
    link_html = ' &nbsp;|&nbsp; '.join(
        f'<a href="{url}" style="color:#548DD4;text-decoration:none">{name}</a>'
        for name, url in links
    )

    # Upcoming reminder based on day
    day_tips = {
        'Monday':    '📋 Start of week — check project weekly digest and plan the week.',
        'Tuesday':   '💻 Mid-week push — good day for deep development work.',
        'Wednesday': '📅 Weekly Project Meeting today — prepare your updates.',
        'Thursday':  '🔍 Review progress — check if tasks are on track for week close.',
        'Friday':    '✅ End of week — close open items, update JIRAs, commit code.',
    }
    day_tip = day_tips.get(day_of_week, '☀️ Have a productive day.')

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;max-width:750px;margin:0 auto;padding:20px;background:#f5f5f5">

  <!-- HEADER -->
  <div style="background:#1F497D;color:#fff;padding:20px 24px;border-radius:6px 6px 0 0">
    <div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;opacity:0.7">Good Morning, Choong Yin</div>
    <div style="font-size:22px;font-weight:bold;margin:4px 0">☀️ Daily Briefing</div>
    <div style="font-size:14px;opacity:0.85">{date_str} &nbsp;|&nbsp; Woodside Pluto — Quorum</div>
  </div>

  <!-- DAY TIP -->
  <div style="background:#548DD4;color:#fff;padding:10px 24px;font-size:13px">
    {day_tip}
  </div>

  <!-- LIVE DATA NOTE -->
  <div style="background:#FFF2CC;padding:12px 24px;border-left:4px solid #C07000;font-size:12px;color:#7A5000">
    📌 <b>Live emails and calendar coming soon</b> — pending IT admin approval for Microsoft Graph access.
    In the meantime, open Claude Code and type <b>"status update"</b> for a full live briefing.
  </div>

  <!-- PENDING TASKS -->
  <div style="background:#fff;padding:20px 24px;margin-top:2px">
    <div style="font-size:14px;font-weight:bold;color:#1F497D;margin-bottom:12px">
      🚨 Pending Action Items — Woodside Pluto
    </div>
    <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse">
      {task_rows}
    </table>
  </div>

  <!-- ISSUE 1052 STATUS -->
  <div style="background:#fff;padding:20px 24px;margin-top:2px">
    <div style="font-size:14px;font-weight:bold;color:#1F497D;margin-bottom:8px">
      📊 Issue_1052 — PHD Tag Validation Status
    </div>
    <table width="100%" cellpadding="0" cellspacing="0"
           style="border-collapse:collapse;font-size:12px">
      <tr style="background:#1F497D;color:#fff">
        <th style="padding:7px 10px;text-align:left">Phase</th>
        <th style="padding:7px 10px;text-align:left">Status</th>
        <th style="padding:7px 10px;text-align:left">Notes</th>
      </tr>
      <tr style="background:#E2EFDA">
        <td style="padding:6px 10px;border-bottom:1px solid #eee">Phase 1 Unit Tests</td>
        <td style="padding:6px 10px;border-bottom:1px solid #eee;color:#00B050;font-weight:bold">✅ COMPLETE</td>
        <td style="padding:6px 10px;border-bottom:1px solid #eee">220/220 PASS — Evidence doc v1.3</td>
      </tr>
      <tr>
        <td style="padding:6px 10px;border-bottom:1px solid #eee">Phase 2 System Test</td>
        <td style="padding:6px 10px;border-bottom:1px solid #eee;color:#C07000;font-weight:bold">⏳ PENDING</td>
        <td style="padding:6px 10px;border-bottom:1px solid #eee">Robot Framework — plan to be enhanced</td>
      </tr>
      <tr style="background:#EEF3FB">
        <td style="padding:6px 10px">Reply to Grant</td>
        <td style="padding:6px 10px;color:#C00;font-weight:bold">🔴 ACTION NEEDED</td>
        <td style="padding:6px 10px">Blocks v1.0.38 planning + ECPR drafts</td>
      </tr>
    </table>
  </div>

  <!-- QUICK LINKS -->
  <div style="background:#fff;padding:14px 24px;margin-top:2px;font-size:12px;text-align:center">
    🔗 Quick Links: {link_html}
  </div>

  <!-- FOOTER -->
  <div style="background:#ddd;padding:10px 24px;border-radius:0 0 6px 6px;
              font-size:11px;color:#888;text-align:center">
    Auto-generated by ChoongYin OS Morning Briefing (SMTP) &nbsp;|&nbsp; {time_str} MY &nbsp;|&nbsp;
    Full live briefing: open Claude Code → type "status update"
  </div>

</body>
</html>"""


def send_email(html, now):
    subject = f'☀️ Morning Briefing — {now.strftime("%a %d %b %Y")}'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = EMAIL
    msg['To']      = EMAIL
    msg.attach(MIMEText(html, 'html', 'utf-8'))

    pwd = get_password()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL, pwd)
        server.sendmail(EMAIL, EMAIL, msg.as_string())


if __name__ == '__main__':
    now = datetime.now(MY8)
    print(f'Morning Briefing (SMTP) — {now.strftime("%Y-%m-%d %H:%M")} MY')
    html = build_html(now)
    send_email(html, now)
    print(f'✅ Briefing sent to {EMAIL}')
