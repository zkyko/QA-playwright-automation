# 🚀 Jira Integration - Quick Reference Card

## ⚡ Quick Commands

```bash
# Setup wizard
python scripts/setup_jira.py

# Create test cycle
python utils/jira_integration.py create-cycle --name "Test Run" --project "QA"

# Update results
python utils/jira_integration.py update-results --cycle "TEST-RUN-123" --results "reports/junit/results.xml"

# Finalize cycle
python utils/jira_integration.py finalize-cycle --cycle "TEST-RUN-123" --build "456"

# Create defects
python utils/jira_integration.py create-defects --cycle "TEST-RUN-123" --build "456"
```

## 🏷️ Test Markers

```python
# Basic test case link
@pytest.mark.jira('TEST-101')
def test_feature(page):
    pass

# Link to test case AND user story
@pytest.mark.jira('TEST-101')
@pytest.mark.jira_issue('PROJ-500')
def test_feature(page):
    pass
```

## ⚙️ Environment Variables

```bash
JIRA_BASE_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your.email@company.com
JIRA_API_TOKEN=your-token
JIRA_PROJECT_KEY=QA
ZEPHYR_CYCLE_KEY=TEST-RUN-123  # Optional
```

## 📋 Azure DevOps Variable Group

**Name:** `Jira-Zephyr-Config`

| Variable | Secret? |
|----------|---------|
| JIRA_BASE_URL | No |
| JIRA_EMAIL | No |
| JIRA_API_TOKEN | **Yes** ⚠️ |
| JIRA_PROJECT_KEY | No |
| JIRA_VERSION | No |

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check API token and email |
| 404 Not Found | Verify base URL and project key |
| Test not updating | Check test has `@pytest.mark.jira()` |
| Pipeline fails | Verify variable group exists and is linked |

## 📚 Documentation

| File | Purpose |
|------|---------|
| `JIRA_QUICKSTART.md` | 5-minute guide |
| `docs/JIRA_INTEGRATION.md` | Complete documentation |
| `DEPLOYMENT_CHECKLIST.md` | Deployment steps |
| `CHANGES_SUMMARY.md` | All changes made |

## 🎯 Key URLs

- **API Token:** https://id.atlassian.com/manage-profile/security/api-tokens
- **Jira API Docs:** https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **Zephyr Docs:** https://support.smartbear.com/zephyr-scale-cloud/api-docs/

## ✅ Deployment Checklist

- [ ] Create variable group in Azure DevOps
- [ ] Add all required variables
- [ ] Mark API token as secret
- [ ] Run `python scripts/setup_jira.py`
- [ ] Add markers to tests
- [ ] Push and monitor pipeline

## 🎓 Quick Test Example

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
@pytest.mark.jira('TEST-101')
def test_login(page: Page, fh_base_url, fh_username, fh_password):
    """Test login functionality - TEST-101"""
    page.goto(f"{fh_base_url}/account/login")
    page.fill('input[name="email"]', fh_username)
    page.fill('input[name="password"]', fh_password)
    page.click('button[type="submit"]')
    expect(page).to_have_url(f"{fh_base_url}/account/dashboard")
```

---

**Need help?** Run: `python scripts/setup_jira.py` or check `JIRA_QUICKSTART.md`
