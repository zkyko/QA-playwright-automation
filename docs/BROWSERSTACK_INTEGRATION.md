# BrowserStack Integration Guide
## Four Hands QA Automation Framework

Complete guide for integrating BrowserStack Automate with the Four Hands QA automation framework.

---

## 📋 Overview

BrowserStack Automate allows you to run Playwright tests on real browsers and devices in the cloud, enabling:

- Cross-browser testing (Chrome, Firefox, Safari, Edge)
- Cross-platform testing (Windows, macOS, mobile)
- Parallel test execution
- Video recordings and logs
- No local browser setup required

---

## 🔐 Step 1: BrowserStack Account Setup

### 1.1 Get BrowserStack Credentials

1. Sign up at: https://www.browserstack.com
2. Go to **Account** → **Settings**
3. Copy your:
   - **Username**: `your_username`
   - **Access Key**: `your_access_key`

### 1.2 Add Credentials to Environment

**Local Development (.env file):**
```bash
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
```

**Azure DevOps (Key Vault):**
```bash
az keyvault secret set \
  --vault-name fourhands-qa-keyvault \
  --name "BROWSERSTACK-USERNAME" \
  --value "your_username"

az keyvault secret set \
  --vault-name fourhands-qa-keyvault \
  --name "BROWSERSTACK-ACCESS-KEY" \
  --value "your_access_key"
```

---

## ⚙️ Step 2: Configuration

### 2.1 BrowserStack YAML Configuration

The `browserstack.yml` file defines your test configuration:

```yaml
userName: ${BROWSERSTACK_USERNAME}
accessKey: ${BROWSERSTACK_ACCESS_KEY}

framework: playwright-pytest

platforms:
  - browserName: playwright-chromium
    os: Windows
    osVersion: "11"
  
  - browserName: playwright-chromium
    os: OS X
    osVersion: Monterey
  
  - browserName: playwright-webkit
    os: OS X
    osVersion: Monterey

buildName: "FourHands QA Automation"
projectName: "Playwright Automation"
parallelsPerPlatform: 3
maxDuration: 3600

debug: true
networkLogs: true
consoleLogs: info
video: true
screenshots: true
```

### 2.2 Python Configuration

The `configs/browserstack_config.py` handles connection:

**Key Functions:**
- `get_cdp_url()`: Generates BrowserStack CDP WebSocket URL
- `get_browserstack_capabilities()`: Defines browser capabilities
- `is_browserstack_enabled()`: Checks if BrowserStack mode is enabled

**Example Usage:**
```python
from configs.browserstack_config import get_cdp_url, is_browserstack_enabled

if is_browserstack_enabled():
    browser = playwright.chromium.connect_over_cdp(get_cdp_url())
```

---

## 🚀 Step 3: Running Tests on BrowserStack

### 3.1 Local Execution

**Run with helper script:**
```bash
./scripts/run_tests_browserstack.sh smoke
./scripts/run_tests_browserstack.sh e2e
./scripts/run_tests_browserstack.sh all
```

**Manual execution:**
```bash
# Activate virtual environment
source venv/bin/activate

# Set BrowserStack environment
export USE_BROWSERSTACK=true
export BROWSERSTACK_USERNAME=your_username
export BROWSERSTACK_ACCESS_KEY=your_access_key

# Run tests
pytest tests/ -m smoke -v --alluredir=reports/allure-results
```

### 3.2 Azure Pipeline Execution

**Trigger BrowserStack pipeline:**

1. **Via Azure DevOps UI:**
   - Go to **Pipelines** → `azure-pipelines-browserstack.yml`
   - Click **Run pipeline**
   - Select parameters:
     - Test Suite: `smoke` | `e2e` | `all`
     - Browsers: `chrome,edge,safari`
     - OS: `Windows` | `OS X` | `Both`
   - Click **Run**

2. **Via scheduled trigger:**
   - Runs automatically at 2 AM UTC daily (configured in YAML)

3. **Via API/CLI:**
```bash
az pipelines run \
  --name azure-pipelines-browserstack \
  --parameters testSuite=smoke browsers=chrome,edge
```

---

## 📊 Step 4: Viewing Results

### 4.1 BrowserStack Dashboard

**Access:** https://automate.browserstack.com/dashboard/v2

**Features:**
- ✅ Real-time test execution
- 🎬 Video recordings of every test
- 📸 Screenshots at each step
- 📋 Network logs and console logs
- 🐛 Debug information
- 📊 Test trends and analytics

### 4.2 Test Session Details

Each test creates a BrowserStack session with:
- **Session Name**: Test name from pytest
- **Build Name**: From `BS_BUILD` environment variable
- **Project Name**: From `BS_PROJECT` environment variable
- **Tags**: From pytest markers (smoke, e2e, etc.)

**Session URL format:**
```
https://automate.browserstack.com/dashboard/v2/builds/<build-id>/sessions/<session-id>
```

### 4.3 Allure Reports

BrowserStack sessions are linked in Allure reports:

1. Run tests
2. Generate Allure report:
```bash
./scripts/generate_allure_report.sh
```
3. View BrowserStack links in test details

---

## 🔧 Step 5: Advanced Configuration

### 5.1 Parallel Execution

Run tests in parallel across multiple browsers:

```yaml
# browserstack.yml
parallelsPerPlatform: 5  # Number of parallel tests per platform
```

**Pytest parallel execution:**
```bash
pytest tests/ -n auto --dist loadfile
```

### 5.2 Custom Capabilities

Add custom capabilities in `configs/browserstack_config.py`:

```python
def get_browserstack_capabilities():
    capabilities = {
        "browser": "chrome",
        "browser_version": "latest",
        "os": "Windows",
        "os_version": "11",
        "resolution": "1920x1080",
        "project": "FourHands QA",
        "build": f"Build-{os.getenv('BUILD_NUMBER', 'local')}",
        "name": "Test Name",
        
        # Advanced options
        "browserstack.local": "false",
        "browserstack.debug": "true",
        "browserstack.networkLogs": "true",
        "browserstack.console": "errors",
        "browserstack.selenium_version": "4.0.0",
        "browserstack.idleTimeout": "300",
        "browserstack.video": "true",
        "acceptSslCerts": "true",
        "timezone": "America/Chicago"
    }
    return capabilities
```

### 5.3 Local Testing

Test internal/staging environments using BrowserStack Local:

```bash
# Download BrowserStack Local binary
wget https://www.browserstack.com/browserstack-local/BrowserStackLocal-linux-x64.zip
unzip BrowserStackLocal-linux-x64.zip

# Start local tunnel
./BrowserStackLocal --key YOUR_ACCESS_KEY

# Set in configuration
export BS_LOCAL=true
```

**Python configuration:**
```python
capabilities = {
    "browserstack.local": "true",
    "browserstack.localIdentifier": "local-tunnel-1"
}
```

### 5.4 Mobile Browser Testing

Test on mobile devices:

```yaml
# browserstack.yml
platforms:
  - browserName: playwright-chromium
    os: android
    osVersion: "13.0"
    device: Samsung Galaxy S23
  
  - browserName: playwright-webkit
    os: ios
    osVersion: "16"
    device: iPhone 14 Pro
```

---

## 📈 Step 6: Best Practices

### 6.1 Naming Conventions

**Build Names:**
```python
# Include date and build number
BS_BUILD = f"FourHands-QA-{datetime.now().strftime('%Y%m%d')}-Build-{build_number}"
```

**Test Names:**
```python
# Use descriptive names
@pytest.mark.smoke
def test_login_with_valid_credentials():
    """Test: Login with valid user credentials"""
    pass
```

### 6.2 Cost Optimization

**Strategies to reduce BrowserStack usage:**

1. **Run smoke tests locally**, full E2E on BrowserStack
2. **Use scheduled runs** instead of every commit
3. **Limit parallel sessions** based on plan
4. **Enable only necessary logs** (reduce storage)
5. **Set appropriate timeouts** to avoid hanging sessions

```python
# pytest.ini
[pytest]
addopts = --tb=short --maxfail=10  # Stop after 10 failures
```

### 6.3 Debugging Failed Tests

**Steps to debug BrowserStack failures:**

1. **Check video recording** in BrowserStack dashboard
2. **Review console logs** for JavaScript errors
3. **Check network logs** for API failures
4. **Download screenshots** from test steps
5. **Review Playwright trace** if available

**Enable Playwright tracing on BrowserStack:**
```python
context.tracing.start(screenshots=True, snapshots=True, sources=True)
# ... run test ...
context.tracing.stop(path="trace.zip")
```

### 6.4 Managing Test Data

**Avoid hard-coded test data:**

```python
# Good: Use environment-specific config
test_user = {
    "email": os.getenv("TEST_USER_EMAIL"),
    "password": os.getenv("TEST_USER_PASSWORD")
}

# Bad: Hard-coded credentials
test_user = {
    "email": "test@example.com",
    "password": "password123"
}
```

---

## 🐛 Step 7: Troubleshooting

### Common Issues

#### Issue 1: Connection Timeout

**Symptoms:**
```
TimeoutError: connect_over_cdp: Timeout 30000ms exceeded
```

**Solutions:**
- Check BrowserStack credentials
- Verify account has available sessions
- Check network/firewall settings
- Increase timeout in configuration

#### Issue 2: Authentication Failure

**Symptoms:**
```
Authentication failed. Please check your credentials.
```

**Solutions:**
```bash
# Verify credentials
echo $BROWSERSTACK_USERNAME
echo $BROWSERSTACK_ACCESS_KEY

# Test connection
curl -u "$BROWSERSTACK_USERNAME:$BROWSERSTACK_ACCESS_KEY" \
  https://api.browserstack.com/automate/plan.json
```

#### Issue 3: Session Not Starting

**Symptoms:**
- Tests hang indefinitely
- No session visible in dashboard

**Solutions:**
- Check parallel session limit
- Verify platform/browser compatibility
- Review capability configuration
- Check BrowserStack service status

#### Issue 4: Tests Pass Locally but Fail on BrowserStack

**Common causes:**
- Timing issues (network latency)
- Different screen resolution
- Browser differences
- Missing wait conditions

**Solutions:**
```python
# Add explicit waits
page.wait_for_load_state("networkidle")
page.wait_for_selector("button:visible")

# Increase timeouts
page.set_default_timeout(60000)  # 60 seconds
```

---

## 📊 Step 8: Reporting & Analytics

### 8.1 BrowserStack REST API

Get test results programmatically:

```python
import requests

# Get builds
response = requests.get(
    "https://api.browserstack.com/automate/builds.json",
    auth=(username, access_key)
)
builds = response.json()

# Get sessions for a build
response = requests.get(
    f"https://api.browserstack.com/automate/builds/{build_id}/sessions.json",
    auth=(username, access_key)
)
sessions = response.json()
```

### 8.2 Custom Reporting

Integrate BrowserStack data into Allure:

```python
import allure

@allure.link(
    url=f"https://automate.browserstack.com/dashboard/v2/builds/{build_id}/sessions/{session_id}",
    name="BrowserStack Session"
)
def test_example():
    pass
```

---

## ✅ Checklist

- [ ] BrowserStack account created
- [ ] Credentials added to .env and Azure Key Vault
- [ ] browserstack.yml configured
- [ ] Local test run successful
- [ ] Azure pipeline configured
- [ ] Dashboard access verified
- [ ] Video recordings enabled
- [ ] Network logs enabled
- [ ] Parallel execution tested
- [ ] Cost optimization implemented

---

## 📞 Support

- **BrowserStack Support**: https://www.browserstack.com/support
- **BrowserStack Docs**: https://www.browserstack.com/docs/automate
- **Playwright + BrowserStack**: https://www.browserstack.com/docs/automate/playwright

**Your BrowserStack integration is complete! 🎉**
