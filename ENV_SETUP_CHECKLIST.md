# 🔑 Environment Setup Checklist - Local Testing

## ✅ Pre-Testing Configuration

Before running tests locally, you need to configure these environment variables in your `.env` file.

---

## 📋 Required Configuration Steps

### 1️⃣ **FourHands Credentials** ⚠️ REQUIRED

```bash
FH_USERNAME=your_fh_email@example.com     # ❌ TODO: Update this
FH_PASSWORD=your_fh_password               # ❌ TODO: Update this
```

**Action Required:**
- [ ] Replace with valid FourHands test account credentials
- [ ] Test login at: https://fh-test-fourhandscom.azurewebsites.net/account/login

---

### 2️⃣ **Jira Configuration** ⚠️ REQUIRED for Jira Integration

```bash
JIRA_BASE_URL=https://yourcompany.atlassian.net   # ❌ TODO: Update this
JIRA_PROJECT_KEY=QA                                # ❌ TODO: Update if different
```

**Action Required:**
- [ ] Update `JIRA_BASE_URL` with your company's Jira instance URL
  - Format: `https://yourcompany.atlassian.net`
  - No trailing slash!
  
- [ ] Update `JIRA_PROJECT_KEY` with your project key
  - Examples: `QA`, `TEST`, `PROJ`, `FHQA`
  - Must be uppercase
  - Find it in Jira: Project Settings → Details → Project Key

---

### 3️⃣ **Jira API Token** ✅ Already Configured

```bash
JIRA_EMAIL=nbhandari@austin.fourhands.com         # ✅ Already set
JIRA_API_TOKEN=ATATT3xFfGF0BxUlEOAQG...           # ✅ Already set
```

**Status:** ✅ Token is already in the `.env` file

**If you need to regenerate:**
1. Go to: https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a name (e.g., "QA Automation")
4. Copy the token
5. Replace `JIRA_API_TOKEN` in `.env`

---

### 4️⃣ **D365 Configuration** ✅ Already Configured

```bash
D365_BASE_URL=https://fourhands-test.sandbox.operations.dynamics.com  # ✅ Set
D365_USERNAME=nbhandari@austin.fourhands.com                          # ✅ Set
D365_PASSWORD=Kathmandu1                                              # ✅ Set
```

**Status:** ✅ Already configured

---

### 5️⃣ **Test Execution Settings** ✅ Already Configured

```bash
HEADED=false          # ✅ Set to false (headless mode)
TIMEOUT=30000         # ✅ 30 seconds
BROWSER=chromium      # ✅ Chrome-based browser
USE_BROWSERSTACK=false # ✅ Disabled for local testing
```

**Status:** ✅ Good defaults for local testing

**Optional Adjustments:**
- Set `HEADED=true` if you want to see the browser during tests (helpful for debugging)
- Increase `TIMEOUT` if tests timeout frequently

---

## 🎯 Quick Configuration Summary

| Setting | Status | Action Needed |
|---------|--------|---------------|
| FH_USERNAME | ❌ | Update with valid email |
| FH_PASSWORD | ❌ | Update with valid password |
| JIRA_BASE_URL | ❌ | Update with your Jira URL |
| JIRA_PROJECT_KEY | ⚠️ | Verify it's correct (currently: QA) |
| JIRA_EMAIL | ✅ | Already set |
| JIRA_API_TOKEN | ✅ | Already set |
| D365_* | ✅ | Already configured |
| Test Settings | ✅ | Already configured |

---

## 🧪 Test Your Configuration

### Step 1: Test Jira Connection

```bash
# Navigate to project directory
cd "C:\Users\Timmy\Downloads\QA-PlayWright-Automation-w-jira-automate\QA-PlayWright-Automation w-jira"

# Run the Jira setup wizard
python scripts/setup_jira.py
```

**Expected Output:**
```
✓ Jira connection successful
✓ Project 'QA' found
✓ Zephyr Scale is installed
```

If you see errors:
- Check `JIRA_BASE_URL` format (no trailing slash)
- Verify `JIRA_PROJECT_KEY` exists in your Jira
- Confirm `JIRA_API_TOKEN` is valid

---

### Step 2: Test Basic Playwright Setup

```bash
# Activate virtual environment (if not already activated)
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

---

### Step 3: Run a Simple Test

```bash
# Run a simple smoke test (no Jira integration yet)
pytest tests/fh/test_fh_cart.py::test_cart_empty_message -v --headed
```

**Note:** This test might fail due to authentication, which is expected. We'll set that up next.

---

## 🔐 Authentication Setup

### FourHands Authentication

Before running FourHands tests, you need to save an authenticated session:

1. **Create auth script** (if not exists):
   ```bash
   # Create storage_state directory
   mkdir -p storage_state
   ```

2. **Option A: Manual login to save session**
   - Update `FH_USERNAME` and `FH_PASSWORD` in `.env`
   - Run a test with `--headed` to login manually
   - The session will be saved automatically

3. **Option B: Check if auth script exists**
   ```bash
   # Look for scripts/save_fh_auth.py or similar
   python scripts/save_fh_auth.py  # If it exists
   ```

---

## 📋 Final Checklist

Before running Jira-integrated tests:

- [ ] Updated `FH_USERNAME` and `FH_PASSWORD` in `.env`
- [ ] Updated `JIRA_BASE_URL` in `.env`
- [ ] Verified `JIRA_PROJECT_KEY` is correct
- [ ] Ran `python scripts/setup_jira.py` successfully
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Installed Playwright: `playwright install chromium`
- [ ] Created FourHands authenticated session
- [ ] Virtual environment is activated

---

## 🚀 Ready to Test!

Once all items are checked off:

```bash
# Run smoke tests with Jira integration
pytest tests/ -m smoke -v --junitxml=reports/junit/results.xml

# Create a test cycle in Jira
python utils/jira_integration.py create-cycle \
  --name "Local Test Run $(date +%Y%m%d)" \
  --project "QA"

# Update Jira with results
python utils/jira_integration.py update-results \
  --cycle "TEST-RUN-XXX" \
  --results "reports/junit/results.xml"
```

---

## ❓ Need Help?

**Common Issues:**

1. **Jira Connection Failed:**
   - Verify URL format: `https://company.atlassian.net` (no trailing slash)
   - Check API token is not expired
   - Confirm email matches Jira account

2. **Project Not Found:**
   - Verify project key is correct (uppercase)
   - Check you have access to the project in Jira

3. **Zephyr Scale Not Found:**
   - Ensure Zephyr Scale is installed in your Jira instance
   - Contact Jira admin if needed

4. **Test Failures:**
   - Check `FH_USERNAME` and `FH_PASSWORD` are correct
   - Verify FourHands test site is accessible
   - Try with `--headed` flag to see what's happening

---

## 📞 Contact

If you encounter issues:
- Check documentation: `JIRA_QUICKSTART.md`
- Review logs: `pytest -v` output
- Run setup wizard again: `python scripts/setup_jira.py`

---

**Last Updated:** October 2025  
**Status:** Ready for local testing configuration
