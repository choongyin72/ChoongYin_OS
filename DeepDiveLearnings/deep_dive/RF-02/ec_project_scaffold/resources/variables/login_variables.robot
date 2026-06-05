*** Settings ***
Documentation    Login screen selectors — Keycloak form

*** Variables ***
# ── Keycloak Login Form ───────────────────────────────────────────────────────
${LOGIN_USERNAME_INPUT}     id=username
${LOGIN_PASSWORD_INPUT}     id=password
${LOGIN_SUBMIT_BTN}         id=kc-login
${LOGIN_ERROR_MSG}          css=.kc-feedback-text, .alert-error

# ── Post-login verification ───────────────────────────────────────────────────
${DASHBOARD_INDICATOR}      xpath=//div[contains(@id,'screenToolbar')]
