"""
Morning Briefing — SMTP Setup (run once)
Saves your email password securely in Windows Credential Manager.
Password never stored in plain text.
"""
import sys, keyring, getpass
sys.stdout.reconfigure(encoding='utf-8')

EMAIL = 'choong-yin.lee@quorumsoftware.com'

print('=' * 50)
print('Morning Briefing — SMTP Password Setup')
print('=' * 50)
print(f'Email: {EMAIL}')
print('Your password will be saved in Windows Credential Manager.')
print('It is NOT stored in any file.')
print()

pwd = getpass.getpass('Enter your Quorum email password: ')
keyring.set_password('morning_briefing_smtp', EMAIL, pwd)

print()
print('✅ Password saved securely in Windows Credential Manager.')
print('You can now run morning_briefing_smtp.py')
