# Playwright Locator Reference

## Locator Priority (use highest available)

| Priority | Strategy | TS Syntax | Python Syntax | Use when | Avoid when |
|---|---|---|---|---|---|
| 1 | ARIA Role | `getByRole('button', {name:'Login'})` | `get_by_role('button', name='Login')` | Interactive elements with semantic role | Non-semantic elements |
| 2 | Label | `getByLabel('Username')` | `get_by_label('Username')` | Form inputs with `<label>` | Elements without labels |
| 3 | Placeholder | `getByPlaceholder('Search...')` | `get_by_placeholder('Search...')` | Input fields with placeholder | General elements |
| 4 | Text | `getByText('Go...')` | `get_by_text('Go...')` | Buttons/links with visible text | Dynamic text that changes |
| 5 | Test ID | `getByTestId('submit')` | `get_by_test_id('submit')` | When `data-testid` attr is added | Most EC elements (no test IDs) |
| 6 | CSS | `locator('#id')` `locator('css=.class')` | `locator('#id')` | Stable unique IDs | Generic classes shared by many elements |
| 7 | XPath | `locator('xpath=//tag[@attr]')` | `locator('xpath=//tag')` | Complex conditions, text matching | Simple selections (use CSS instead) |

## EC-Specific Examples

| Element | Locator | Notes |
|---|---|---|
| Keycloak username | `#username` | Stable ID |
| Keycloak password | `#password` | Stable ID |
| Keycloak login btn | `#kc-login` | Stable ID |
| Sidebar search | `xpath=//input[@id='menu:searchForm:searchTxt']` | PrimeFaces ID |
| Treeview link | `xpath=//label[contains(@class,'tv-link') and normalize-space(.)='${NAME}']` | Dynamic |
| EC pagination last | `css=span.ui-icon-seek-end` | PrimeFaces icon class |
| EC table row | `tr[data-rk]` | EC data row attribute |
| Screenlet filter field | `#check_rules\\:form\\:T\\:sfilter0_ft_filter` | Escape colons in CSS |
| EC toolbar save | `xpath=//button[contains(@id,'saveButton')]` | Toolbar pattern |
| EC screenlet minimize | `#screenToolbar\\:form\\:minmaxMenu` | Screen toolbar |

## Key Chaining Patterns
```typescript
// First matching element
page.locator('.ui-datatable tr').first()

// Nth element (0-indexed)
page.locator('tr[data-rk]').nth(2)

// Filter by text
page.locator('tr').filter({ hasText: 'PHD_STRM_COMP' })

// Child element
page.locator('#form').locator('button')
```

## `type()` vs `fill()` in EC
| Keyword | Use for | Why |
|---|---|---|
| `fill()` | Most input fields | Clears then sets — reliable |
| `type()` with delay | PrimeFaces search fields, autocomplete | PrimeFaces listens to keyup events — fill() doesn't trigger them |
