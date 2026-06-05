# Playwright MCP + Claude Code Integration Guide

## What Playwright MCP Is
`@playwright/mcp` is a Model Context Protocol server that gives Claude Code live browser control. When running, Claude Code can:
- Navigate to URLs
- Click elements
- Fill inputs
- Take screenshots
- Read DOM content
- Execute JavaScript

This enables **live locator discovery** — Claude Code opens the actual EC Web App and finds element selectors by inspecting the real DOM.

## Installation
```bash
npm install -g @playwright/mcp
# Or run without installing:
npx @playwright/mcp@latest
```

## Claude Code settings.json Configuration
```json
{
    "mcpServers": {
        "playwright": {
            "command": "npx",
            "args": [
                "@playwright/mcp@latest",
                "--ignore-https-errors"
            ]
        }
    }
}
```

The `--ignore-https-errors` flag is **critical for EC** — without it, MCP cannot connect to EC's self-signed certificate URL.

Location of settings.json: `C:\Users\choong-yin.lee\.claude\settings.json` (or `~/.claude/settings.json`)

## MCP Tools Available to Claude Code

| Tool | What it does |
|---|---|
| `playwright_navigate` | Navigate to URL |
| `playwright_click` | Click an element by selector or text |
| `playwright_fill` | Fill an input field |
| `playwright_screenshot` | Take screenshot of current page |
| `playwright_get_text` | Get text content of an element |
| `playwright_evaluate` | Execute JavaScript on the page |
| `playwright_select_option` | Select dropdown option |

## Workflow: MCP → Locators → Robot Framework Keywords

```
Step 1: Open EC Web App via MCP
  Claude Code: playwright_navigate to EC URL

Step 2: Navigate to target screen
  Claude Code: playwright_click sidebar search
  Claude Code: playwright_fill search with screen name
  Claude Code: playwright_click screen link

Step 3: Take screenshot for DOM inspection
  Claude Code: playwright_screenshot
  (Review screenshot to identify elements)

Step 4: Discover locators
  Claude Code: playwright_evaluate → document.querySelector('#username').outerHTML
  (Inspect actual element IDs and classes)

Step 5: Propose locator variables
  Claude Code: Generates variables/login_variables.robot with discovered selectors

Step 6: Embed in Robot Framework
  Claude Code: Writes pages/LoginPage.resource using discovered selectors
```

## Limitations

| Limitation | Workaround |
|---|---|
| MCP sessions are ephemeral — browser closes when session ends | Document all discovered locators immediately before session closes |
| MCP cannot access local file system | All locator discovery must be done in the browser session |
| EC self-signed cert may still block some MCP operations | Use `--ignore-https-errors` flag in MCP config |
| Locators found via MCP may differ from test execution timing | Add `waitForLoadState('networkidle')` after each navigation |

## Real Example: Discover EC Login Locators

```
Claude Code runs: playwright_navigate to https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/
Claude Code runs: playwright_screenshot
→ Sees: Keycloak login form

Claude Code runs: playwright_evaluate
  → document.querySelector('input[type="text"]').id
  → Returns: "username"

Claude Code runs: playwright_evaluate  
  → document.querySelector('input[type="password"]').id
  → Returns: "password"

Claude Code runs: playwright_evaluate
  → document.querySelector('[type="submit"]').id
  → Returns: "kc-login"

Result: 3 locators discovered → #username, #password, #kc-login
These are embedded in LoginPage.resource as ${USERNAME_INPUT}  id=username
```
