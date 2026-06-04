"""
Morning Briefing — One-Time Authentication Setup
Run this ONCE to authenticate with Microsoft 365.
A browser window will open — login with your Quorum account.
Token is saved locally for daily reuse.
"""
import sys, json, msal
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

cfg  = json.loads(Path(r'C:\Projects\ChoongYin_OS\tools\morning-briefing\config.json').read_text())
SCOPES = ['Mail.Read', 'Mail.Send', 'Calendars.Read']

cache = msal.SerializableTokenCache()

app = msal.PublicClientApplication(
    client_id  = cfg['client_id'],
    authority  = f'https://login.microsoftonline.com/{cfg["tenant_id"]}',
    token_cache = cache
)

print('Opening browser for Microsoft 365 login...')
print('Login with: choong-yin.lee@quorumsoftware.com')
print()

result = app.acquire_token_interactive(scopes=SCOPES)

if 'access_token' in result:
    # Save token cache
    Path(cfg['token_cache']).write_text(cache.serialize())
    print('✅ Authentication successful!')
    print(f'   Token saved to: {cfg["token_cache"]}')
    print()
    print('You can now run morning_briefing.py daily.')
else:
    print(f'❌ Authentication failed: {result.get("error_description")}')
