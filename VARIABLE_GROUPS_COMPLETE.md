# Azure DevOps Variable Groups - Complete Configuration

## 📋 Overview

This document lists ALL variables needed for Azure DevOps Variable Groups and local development.

---

## 🔐 Variable Group 1: `QA-Automation-Config`

This group contains existing application and test configuration.

### Variables to Add:

| Variable Name | Value | Secret? | Notes |
|---------------|-------|---------|-------|
| `BROWSERSTACK_USERNAME` | `nbhandari_KMkNq9` | No | BrowserStack account username |
| `BROWSERSTACK_ACCESS_KEY` | `1tnaMGT6bqxfiTNX9zd7` | **Yes** ⚠️ | BrowserStack access key |
| `FH_BASE_URL` | `https://fh-test-fourhandscom.azurewebsites.net` | No | Four Hands test environment URL |
| `FH_USERNAME` | `your_fh_email@example.com` | No | Four Hands test account email |
| `FH_PASSWORD` | `your_fh_password` | **Yes** ⚠️ | Four Hands test account password |
| `D365_BASE_URL` | `https://fourhands-test.sandbox.operations.dynamics.com` | No | D365 test environment URL |
| `D365_COMPANY` | `FH` | No | D365 company code |
| `D365_USERNAME` | `nbhandari@austin.fourhands.com` | No | D365 test account username |
| `D365_PASSWORD` | `Kathmandu1` | **Yes** ⚠️ | D365 test account password |
| `HEADED` | `false` | No | Run tests in headless mode |
| `TIMEOUT` | `30000` | No | Default timeout in milliseconds |

---

## 🎯 Variable Group 2: `Jira-Zephyr-Config` (NEW)

This group contains Jira/Zephyr integration configuration.

### Variables to Add:

| Variable Name | Value | Secret? | Notes |
|---------------|-------|---------|-------|
| `JIRA_BASE_URL` | `https://yourcompany.atlassian.net` | No | Your Jira instance URL (no trailing slash) |
| `JIRA_EMAIL` | `nbhandari@austin.fourhands.com` | No | Email for Jira API authentication |
| `JIRA_API_TOKEN` | `ATATT3xFfGF0BxUlEOAQG-AWfFM1_93IEf8OKMIPgxBDPzlTeR5MmPAnOg_7unFzVOW7MsGukdrpbWw05eouwbYDtyIp2SWCpnQPjeZqU4CqzXk25tHv0T6RUouvZoK3-oBmfjO-3lGm5QD7omsEeCDx2X0gdLT9gDqn1i34TVWaVaGo=C852BE5A` | **Yes** ⚠️ | Jira API token (provided) |
| `JIRA_PROJECT_KEY` | `QA` | No | Your Jira project key (uppercase) |
| `JIRA_VERSION` | `v1.0.0` | No | Optional: Version/Release name for test cycles |

---

## 📝 Step-by-Step: Create Variable Groups in Azure DevOps

### For Group 1: `QA-Automation-Config`

1. Navigate to **Azure DevOps** → **Pipelines** → **Library**
2. Click **"+ Variable group"**
3. Name: `QA-Automation-Config`
4. Add each variable from the table above
5. For variables marked **Yes** in "Secret?" column:
   - Click the **lock icon** 🔒 next to the value field
   - This will hide the value from logs
6. Click **"Save"**
7. Go to **"Pipeline permissions"** tab
8. Add your pipeline to allow access

### For Group 2: `Jira-Zephyr-Config`

1. Click **"+ Variable group"** again
2. Name: `Jira-Zephyr-Config`
3. Add each variable from the Jira table above
4. **CRITICAL:** Mark `JIRA_API_TOKEN` as **SECRET** 🔒
5. Click **"Save"**
6. Add pipeline permissions

---

## 💻 Local Development: `.env` File

Update your local `.env` file for testing:

### Complete `.env` File Contents:

```bash
# ============================================================================
# BROWSERSTACK CONFIGURATION
# ============================================================================
BROWSERSTACK_USERNAME=nbhandari_KMkNq9
BROWSERSTACK_ACCESS_KEY=1tnaMGT6bqxfiTNX9zd7

# ============================================================================
# FOURHANDS CONFIGURATION
# ============================================================================
FH_BASE_URL=https://fh-test-fourhandscom.azurewebsites.net
FH_USERNAME=your_fh_email@example.com
FH_PASSWORD=your_fh_password

# ============================================================================
# D365 CONFIGURATION
# ============================================================================
D365_BASE_URL=https://fourhands-test.sandbox.operations.dynamics.com
D365_COMPANY=FH
D365_USERNAME=nbhandari@austin.fourhands.com
D365_PASSWORD=Kathmandu1

# ============================================================================
# TEST CONFIGURATION
# ============================================================================
HEADED=false
TIMEOUT=30000

# ============================================================================
# JIRA/ZEPHYR CONFIGURATION (NEW)
# ============================================================================
# Your Jira instance URL (no trailing slash)
JIRA_BASE_URL=https://yourcompany.atlassian.net

# Email for Jira API authentication (replace with your actual Jira URL and details)
JIRA_EMAIL=nbhandari@austin.fourhands.com

# Jira API Token (provided by Nischal)
JIRA_API_TOKEN=ATATT3xFfGF0BxUlEOAQG-AWfFM1_93IEf8OKMIPgxBDPzlTeR5MmPAnOg_7unFzVOW7MsGukdrpbWw05eouwbYDtyIp2SWCpnQPjeZqU4CqzXk25tHv0T6RUouvZoK3-oBmfjO-3lGm5QD7omsEeCDx2X0gdLT9gDqn1i34TVWaVaGo=C852BE5A

# Your Jira project key (uppercase, e.g., QA, TEST, PROJ)
JIRA_PROJECT_KEY=QA

# Optional: Version/Release name for test cycles
# JIRA_VERSION=v1.0.0

# Optional: Test Cycle Key (usually set automatically by pipeline)
# ZEPHYR_CYCLE_KEY=TEST-RUN-123

# ============================================================================
# NOTES
# ============================================================================
# 1. DO NOT commit this file to version control
# 2. This file should be in .gitignore
# 3. Update JIRA_BASE_URL with your actual Jira instance URL
# 4. Generate new API token if needed at:
#    https://id.atlassian.com/manage-profile/security/api-tokens
```

---

## ⚙️ Quick Setup Commands

### Test Your Configuration

```bash
# Load environment variables
source .env  # On Mac/Linux
# OR
set -a; source .env; set +a  # Alternative for some systems

# Run the setup wizard
python scripts/setup_jira.py

# This will:
# ✓ Test Jira connection
# ✓ Verify project access
# ✓ Check Zephyr Scale installation
# ✓ Create a test cycle
```

### Run Tests Locally with Jira Integration

```bash
# Run smoke tests
pytest tests/ -m smoke -v --junitxml=reports/junit/smoke-results.xml

# Update Jira with results (after creating a test cycle)
python utils/jira_integration.py update-results \
  --cycle "YOUR-CYCLE-KEY" \
  --results "reports/junit/smoke-results.xml" \
  --test-type "smoke"
```

---

## 🔍 Variable Verification Checklist

### Before Pushing to Pipeline:

- [ ] Both variable groups created in Azure DevOps
- [ ] All variables from tables above are added
- [ ] Secret variables are marked with lock icon 🔒
- [ ] Pipeline has permissions to both variable groups
- [ ] Local `.env` file updated with all variables
- [ ] `.env` is in `.gitignore` (verify with `git status`)
- [ ] Setup wizard runs successfully: `python scripts/setup_jira.py`

### Variables that MUST be SECRET:

1. ✅ `BROWSERSTACK_ACCESS_KEY`
2. ✅ `FH_PASSWORD`
3. ✅ `D365_PASSWORD`
4. ✅ `JIRA_API_TOKEN` ⚠️ **MOST IMPORTANT**

---

## 📋 Copy-Paste Ready Values

### For Azure DevOps Variable Groups

**Group 1: QA-Automation-Config**
```
BROWSERSTACK_USERNAME = nbhandari_KMkNq9
BROWSERSTACK_ACCESS_KEY = 1tnaMGT6bqxfiTNX9zd7 [SECRET]
FH_BASE_URL = https://fh-test-fourhandscom.azurewebsites.net
FH_USERNAME = your_fh_email@example.com
FH_PASSWORD = your_fh_password [SECRET]
D365_BASE_URL = https://fourhands-test.sandbox.operations.dynamics.com
D365_COMPANY = FH
D365_USERNAME = nbhandari@austin.fourhands.com
D365_PASSWORD = Kathmandu1 [SECRET]
HEADED = false
TIMEOUT = 30000
```

**Group 2: Jira-Zephyr-Config**
```
JIRA_BASE_URL = https://yourcompany.atlassian.net
JIRA_EMAIL = nbhandari@austin.fourhands.com
JIRA_API_TOKEN = ATATT3xFfGF0BxUlEOAQG-AWfFM1_93IEf8OKMIPgxBDPzlTeR5MmPAnOg_7unFzVOW7MsGukdrpbWw05eouwbYDtyIp2SWCpnQPjeZqU4CqzXk25tHv0T6RUouvZoK3-oBmfjO-3lGm5QD7omsEeCDx2X0gdLT9gDqn1i34TVWaVaGo=C852BE5A [SECRET]
JIRA_PROJECT_KEY = QA
JIRA_VERSION = v1.0.0
```

---

## ⚠️ Important Security Notes

### DO:
✅ Mark all passwords and tokens as SECRET in Azure DevOps
✅ Keep `.env` file in `.gitignore`
✅ Rotate API tokens if they get exposed
✅ Use separate credentials for test environments

### DON'T:
❌ Commit `.env` file to Git
❌ Share API tokens in Slack/Email
❌ Use production credentials in tests
❌ Hardcode secrets in code

---

## 🆘 Troubleshooting

### Issue: Variable group not found in pipeline

**Solution:**
1. Go to Variable Group → Pipeline permissions
2. Add your pipeline explicitly
3. Save and re-run pipeline

### Issue: Secret values showing in logs

**Solution:**
1. Ensure variable is marked with lock icon 🔒
2. Re-save the variable group
3. Clear pipeline cache and re-run

### Issue: Jira connection fails locally

**Solution:**
```bash
# Verify .env is loaded
echo $JIRA_BASE_URL
echo $JIRA_EMAIL

# If empty, reload:
source .env

# Test connection
python scripts/setup_jira.py
```

---

## 📞 Need Help?

**Can't find your Jira URL?**
- Look at your Jira browser URL
- Format: `https://yourcompany.atlassian.net`
- Remove any `/browse/...` or trailing paths

**Don't know your project key?**
- Go to Jira → Projects → Your Project
- Look at the URL: `/projects/QA/...` - "QA" is the key
- Or check issue keys: "QA-123" - "QA" is the project key

**API Token expired?**
- Generate new at: https://id.atlassian.com/manage-profile/security/api-tokens
- Update in both Azure DevOps AND local `.env`

---

**Last Updated:** October 14, 2025  
**Total Variables:** 16 (11 existing + 5 new for Jira)  
**Secret Variables:** 4 (BROWSERSTACK_ACCESS_KEY, FH_PASSWORD, D365_PASSWORD, JIRA_API_TOKEN)
