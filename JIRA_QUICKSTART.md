# Jira/Zephyr Integration - Quick Start

## 🚀 Quick Setup (5 minutes)

### Step 1: Run Setup Wizard

```bash
cd scripts
python setup_jira.py
```

The wizard will:
- ✅ Test your Jira connection
- ✅ Verify project access
- ✅ Check Zephyr Scale installation
- ✅ Create local .env file (optional)
- ✅ Provide Azure DevOps setup instructions
- ✅ Create a test cycle to verify everything works

### Step 2: Configure Azure DevOps

1. Go to **Azure DevOps** → **Pipelines** → **Library**
2. Create a variable group named: `Jira-Zephyr-Config`
3. Add these variables:

```
JIRA_BASE_URL       = https://yourcompany.atlassian.net
JIRA_EMAIL          = your.email@company.com
JIRA_API_TOKEN      = your-api-token (mark as SECRET!)
JIRA_PROJECT_KEY    = QA
JIRA_VERSION        = v1.0.0 (optional)
```

4. **Important:** Mark `JIRA_API_TOKEN` as secret (click the lock icon)

### Step 3: Update Your Tests

Add Jira markers to your test functions:

```python
import pytest

@pytest.mark.jira('TEST-101')  # Your Jira test case key
def test_my_feature(page):
    # Your test code
    pass
```

### Step 4: Run Tests

**Locally:**
```bash
# Load environment variables
source .env  # or use 'set -a; source .env; set +a' on some systems

# Run tests
pytest tests/ -m smoke -v

# Update Jira with results
python utils/jira_integration.py update-results \
  --cycle "YOUR-CYCLE-KEY" \
  --results "reports/junit/results.xml"
```

**Via Azure Pipeline:**
Just push your code - the pipeline handles everything automatically!

## 📚 What Gets Created

### In Azure Pipeline:

1. **Setup Job** - Creates test cycle in Zephyr
2. **Smoke Tests** - Runs tests and updates Jira
3. **E2E Tests** - Runs tests and updates Jira  
4. **Report Job** - Generates Allure reports
5. **Finalize Job** - Updates cycle summary and creates defects

### In Jira:

1. **Test Cycle** - New cycle for this build
2. **Test Executions** - Pass/Fail status for each test
3. **Bugs** - Auto-created for failed tests (optional)

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `azure-pipelines.yml` | Main pipeline with Jira integration |
| `utils/jira_integration.py` | Jira API integration script |
| `conftest_jira.py` | Pytest plugin for Jira markers |
| `scripts/setup_jira.py` | Setup wizard |
| `docs/JIRA_INTEGRATION.md` | Complete documentation |

## 📖 Example Test

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
@pytest.mark.jira('TEST-101')  # Jira test case key
@pytest.mark.jira_issue('PROJ-500')  # User story key
def test_login_success(page: Page, fh_base_url, fh_username, fh_password):
    """Test successful login - linked to TEST-101"""
    page.goto(f"{fh_base_url}/account/login")
    page.fill('input[name="email"]', fh_username)
    page.fill('input[name="password"]', fh_password)
    page.click('button[type="submit"]')
    
    expect(page).to_have_url(f"{fh_base_url}/account/dashboard")
```

## 🎯 Key Features

✅ **Automated Test Cycles** - Created automatically for each build  
✅ **Real-time Updates** - Test results pushed to Jira as they run  
✅ **Defect Creation** - Auto-create bugs for failed tests  
✅ **Full Traceability** - Link tests to user stories and requirements  
✅ **Rich Reporting** - Allure reports + Jira dashboard  

## 🆘 Troubleshooting

### Connection Issues

```bash
# Test your connection
python scripts/setup_jira.py
```

### Test Results Not Updating

**Check:**
- ✓ Test has `@pytest.mark.jira('TEST-XXX')` marker
- ✓ Test case key exists in Jira
- ✓ Test case is in the test cycle
- ✓ Environment variables are set

### Pipeline Errors

**Check:**
- ✓ Variable group `Jira-Zephyr-Config` exists
- ✓ All required variables are set
- ✓ API token is marked as secret
- ✓ Pipeline has access to variable group

## 📞 Getting Help

1. **Check logs:** Pipeline → Failed job → View logs
2. **Review docs:** `docs/JIRA_INTEGRATION.md`
3. **Test locally:** Run `python scripts/setup_jira.py`
4. **Verify access:** Check Jira permissions

## 🎓 Learn More

- Full documentation: `docs/JIRA_INTEGRATION.md`
- Example tests: `tests/test_jira_example.py`
- API reference: See docstrings in `utils/jira_integration.py`

## ✨ Tips

1. **Use descriptive cycle names:** Include build number and date
2. **Link tests properly:** Every automated test should have a Jira key
3. **Review defects regularly:** Auto-created bugs need triage
4. **Keep cycles organized:** Archive old cycles periodically
5. **Test locally first:** Verify Jira integration before pushing

---

**Ready to go!** Push your code and watch the magic happen in Jira! 🎉
