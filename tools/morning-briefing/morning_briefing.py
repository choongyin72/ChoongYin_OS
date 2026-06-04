"""
Morning Briefing — Daily Email Script
Pulls today's emails, calendar and Teams highlights.
Sends a formatted HTML briefing email to yourself at 08:30 AWST.
Run via Windows Task Scheduler daily.
"""
import sys, json, requests, msal
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# ── Config ────────────────────────────────────────────────────────────────────
cfg    = json.loads(Path(r'C:\Projects\ChoongYin_OS\tools\morning-briefing\config.json').read_text())
SCOPES = ['Mail.Read', 'Mail.Send', 'Calendars.Read']
GRAPH  = 'https://graph.microsoft.com/v1.0'
MY8    = timezone(timedelta(hours=8))   # MY/SGT +8


# ── Auth ──────────────────────────────────────────────────────────────────────
def get_token():
    cache = msal.SerializableTokenCache()
    cache_path = Path(cfg['token_cache'])
    if cache_path.exists():
        cache.deserialize(cache_path.read_text())

    app = msal.PublicClientApplication(
        client_id   = cfg['client_id'],
        authority   = f'https://login.microsoftonline.com/{cfg["tenant_id"]}',
        token_cache = cache
    )

    accounts = app.get_accounts()
    result   = app.acquire_token_silent(SCOPES, account=accounts[0]) if accounts else None

    if not result or 'access_token' not in result:
        print('Token expired or missing — run auth_setup.py first.')
        sys.exit(1)

    # Save refreshed cache
    cache_path.write_text(cache.serialize())
    return result['access_token']


# ── Graph API helpers ─────────────────────────────────────────────────────────
def graph_get(token, path, params=None):
    r = requests.get(f'{GRAPH}{path}', headers={'Authorization': f'Bearer {token}'}, params=params)
    r.raise_for_status()
    return r.json()


def graph_post(token, path, body):
    r = requests.post(f'{GRAPH}{path}',
                      headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
                      json=body)
    r.raise_for_status()


# ── Data fetchers ─────────────────────────────────────────────────────────────
def get_todays_emails(token):
    now   = datetime.now(MY8)
    start = now.replace(hour=0, minute=0, second=0).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    data  = graph_get(token, '/me/mailFolders/inbox/messages', {
        '$filter': f"receivedDateTime ge {start}",
        '$orderby': 'receivedDateTime desc',
        '$top': '20',
        '$select': 'subject,sender,receivedDateTime,isRead,importance'
    })
    return data.get('value', [])


def get_todays_calendar(token):
    now   = datetime.now(MY8)
    start = now.replace(hour=0, minute=0, second=0).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    end   = now.replace(hour=23, minute=59, second=59).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    data  = graph_get(token, '/me/calendarView', {
        'startDateTime': start,
        'endDateTime':   end,
        '$orderby': 'start/dateTime',
        '$top': '20',
        '$select': 'subject,start,end,location,isCancelled,organizer'
    })
    return data.get('value', [])


# ── HTML Email builder ────────────────────────────────────────────────────────
def fmt_time(dt_str):
    """Convert UTC ISO string to MY time HH:MM."""
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00')).astimezone(MY8)
        return dt.strftime('%H:%M')
    except:
        return dt_str[:16]


def build_html(emails, events, now):
    date_str = now.strftime('%A, %d %B %Y')

    # ── Meetings section ──────────────────────────────────────────────────────
    if events:
        mtg_rows = ''
        for e in events:
            cancelled = e.get('isCancelled', False)
            strike    = 'text-decoration:line-through;color:#999;' if cancelled else ''
            start     = fmt_time(e['start']['dateTime'])
            end       = fmt_time(e['end']['dateTime'])
            loc       = e.get('location', {}).get('displayName', '') or 'Teams'
            status    = '~~Cancelled~~' if cancelled else ''
            mtg_rows += f"""
            <tr>
              <td style="padding:6px 10px;border-bottom:1px solid #eee;color:#555;white-space:nowrap">{start}–{end}</td>
              <td style="padding:6px 10px;border-bottom:1px solid #eee;{strike}">{e['subject']}</td>
              <td style="padding:6px 10px;border-bottom:1px solid #eee;color:#888;font-size:12px">{loc}</td>
            </tr>"""
        meetings_html = f"""
        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px">
          <tr style="background:#1F497D;color:#fff">
            <th style="padding:8px 10px;text-align:left">Time (MY)</th>
            <th style="padding:8px 10px;text-align:left">Meeting</th>
            <th style="padding:8px 10px;text-align:left">Location</th>
          </tr>{mtg_rows}
        </table>"""
    else:
        meetings_html = '<p style="color:#888;font-style:italic">No meetings scheduled today.</p>'

    # ── Emails section ────────────────────────────────────────────────────────
    if emails:
        email_rows = ''
        for em in emails[:10]:
            unread   = not em.get('isRead', True)
            bold     = 'font-weight:bold;' if unread else ''
            imp      = em.get('importance', 'normal')
            imp_tag  = '<span style="color:#C00;font-size:11px">⚠ HIGH</span> ' if imp == 'high' else ''
            sender   = em.get('sender', {}).get('emailAddress', {}).get('name', 'Unknown')
            recv     = fmt_time(em.get('receivedDateTime', ''))
            email_rows += f"""
            <tr>
              <td style="padding:6px 10px;border-bottom:1px solid #eee;color:#555;white-space:nowrap">{recv}</td>
              <td style="padding:6px 10px;border-bottom:1px solid #eee;color:#888;font-size:12px">{sender}</td>
              <td style="padding:6px 10px;border-bottom:1px solid #eee;{bold}">{imp_tag}{em.get('subject','(no subject)')}</td>
            </tr>"""
        emails_html = f"""
        <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;font-size:13px">
          <tr style="background:#1F497D;color:#fff">
            <th style="padding:8px 10px;text-align:left">Time</th>
            <th style="padding:8px 10px;text-align:left">From</th>
            <th style="padding:8px 10px;text-align:left">Subject</th>
          </tr>{email_rows}
        </table>"""
        unread_count = sum(1 for e in emails if not e.get('isRead', True))
        email_count  = f'<span style="color:#548DD4">{len(emails)} received today — {unread_count} unread</span>'
    else:
        emails_html  = '<p style="color:#888;font-style:italic">No new emails today.</p>'
        email_count  = ''

    # ── Pending tasks reminder ────────────────────────────────────────────────
    tasks = [
        '🔴 BLP Offtake Report — overdue',
        '🔴 Daniel Perez UAT blockers — overdue since 1 Jun',
        '🟡 Reply to Grant — Issue_1052 (ST vs UAT + Phase 1 results)',
        '🟡 Add Issue_1052 to v1.0.38 tab (after Grant confirms)',
        '🟡 Verify 1.0.37 changes in ECaaS TEST',
        '🟡 Raise ECPR for R_BLP_MONTHLY_ALLOC_PLUTO fix',
    ]
    task_rows = ''.join(f'<li style="padding:3px 0;font-size:13px">{t}</li>' for t in tasks)

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family:Arial,sans-serif;max-width:800px;margin:0 auto;padding:20px;background:#f5f5f5">

  <!-- HEADER -->
  <div style="background:#1F497D;color:#fff;padding:20px 24px;border-radius:6px 6px 0 0">
    <div style="font-size:11px;text-transform:uppercase;letter-spacing:1px;opacity:0.7">Good Morning, Choong Yin</div>
    <div style="font-size:22px;font-weight:bold;margin:4px 0">☀️ Daily Briefing</div>
    <div style="font-size:14px;opacity:0.85">{date_str} &nbsp;|&nbsp; Woodside Pluto — Quorum</div>
  </div>

  <!-- MEETINGS -->
  <div style="background:#fff;padding:20px 24px;margin-top:2px">
    <div style="font-size:14px;font-weight:bold;color:#1F497D;margin-bottom:12px">📅 Meetings Today</div>
    {meetings_html}
  </div>

  <!-- EMAILS -->
  <div style="background:#fff;padding:20px 24px;margin-top:2px">
    <div style="font-size:14px;font-weight:bold;color:#1F497D;margin-bottom:4px">📧 Emails {email_count}</div>
    {emails_html}
  </div>

  <!-- PENDING TASKS -->
  <div style="background:#fff;padding:20px 24px;margin-top:2px">
    <div style="font-size:14px;font-weight:bold;color:#1F497D;margin-bottom:8px">🚨 Pending Action Items</div>
    <ul style="margin:0;padding-left:20px">{task_rows}</ul>
  </div>

  <!-- FOOTER -->
  <div style="background:#eee;padding:10px 24px;border-radius:0 0 6px 6px;font-size:11px;color:#999;text-align:center">
    Auto-generated by ChoongYin OS Morning Briefing &nbsp;|&nbsp; {now.strftime('%H:%M')} MY time
  </div>

</body>
</html>"""


# ── Send email ────────────────────────────────────────────────────────────────
def send_briefing(token, html, now):
    subject = f'☀️ Morning Briefing — {now.strftime("%a %d %b %Y")}'
    graph_post(token, '/me/sendMail', {
        'message': {
            'subject': subject,
            'body': {'contentType': 'HTML', 'content': html},
            'toRecipients': [{'emailAddress': {'address': cfg['user_email']}}]
        },
        'saveToSentItems': False
    })


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    now = datetime.now(MY8)
    print(f'Morning Briefing — {now.strftime("%Y-%m-%d %H:%M")} MY')

    token  = get_token()
    print('✅ Token acquired')

    emails = get_todays_emails(token)
    print(f'✅ Emails: {len(emails)} fetched')

    events = get_todays_calendar(token)
    print(f'✅ Calendar: {len(events)} events fetched')

    html   = build_html(emails, events, now)
    send_briefing(token, html, now)
    print(f'✅ Briefing sent to {cfg["user_email"]}')
    print('Done.')
