# BrowserStack GitHub Actions Setup Guide

## ✅ What Was Fixed

The tests were being **SKIPPED** instead of running on BrowserStack because:

1. ❌ The workflow was running `pytest` directly (local execution)
2. ❌ No `BROWSERSTACK_BUILD_NAME` environment variable was set
3. ❌ The test fixture checked for BrowserStack environment and skipped when not found

## ✅ Solution Applied

Now the workflow correctly runs tests on BrowserStack using the SDK:

```bash
# Before (Local - doesn't show on BrowserStack)
pytest tests/d365/test_d365_sales_order.py -v

# After (BrowserStack Cloud - shows on dashboard)
browserstack-sdk pytest tests/d365/test_d365_sales_order.py -v
```

## 📁 Updated Files

### 1. `.github/workflows/browserstack-tests.yml`
- ✅ Added Node.js setup (required for BrowserStack SDK)
- ✅ Installs `browserstack-sdk` via npm
- ✅ Uses `browserstack-sdk pytest` command
- ✅ Tests will now appear in BrowserStack Automate dashboard

### 2. `.github/workflows/browserstack-full-suite.yml` (NEW)
- ✅ Comprehensive workflow with multiple test suites
- ✅ Manual trigger with options: smoke, e2e, d365, fh, all
- ✅ Scheduled daily runs at 2 AM UTC
- ✅ Generates Allure reports
- ✅ Prints BrowserStack dashboard link

## 🚀 How to Use

### Run Single Test (Quick Validation)

```bash
# From your local machine
browserstack-sdk pytest tests/d365/test_d365_sales_order.py::test_d365_login_page_loads -v
```

### Run from GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **BrowserStack Cloud Tests** workflow
4. Click **Run workflow**
5. Wait for completion
6. Check BrowserStack dashboard: https://automate.browserstack.com/dashboard

### Run Different Test Suites

Use the **BrowserStack Full Suite** workflow:

1. Go to **Actions** → **BrowserStack Full Suite**
2. Click **Run workflow**
3. Select test suite:
   - **smoke** - Quick validation (default)
   - **e2e** - End-to-end tests
   - **d365** - D365 only
   - **fh** - FourHands only
   - **all** - Everything

## 🔍 Verifying BrowserStack Execution

### How to Know Tests Ran on BrowserStack:

1. **GitHub Actions Log** should show:
   ```
   Running tests on BrowserStack using SDK
   browserstack-sdk pytest ...
   ```

2. **BrowserStack Dashboard** will show:
   - Build name: "FourHands & D365 Playwright Tests"
   - Session with video recording
   - Console logs
   - Network logs

3. **Test Won't Be Skipped** - You'll see:
   ```
   tests/d365/test_d365_sales_order.py::test_d365_login_page_loads PASSED
   ```
   Instead of:
   ```
   tests/d365/test_d365_sales_order.py::test_d365_login_page_loads SKIPPED
   ```

## 🐛 Troubleshooting

### Tests Still Being Skipped?

Check if BrowserStack SDK is actually running:

```bash
# In GitHub Actions logs, look for:
npm install -g browserstack-sdk
# Should complete successfully

browserstack-sdk pytest ...
# Should connect to BrowserStack
```

### Not Showing in BrowserStack Dashboard?

1. Verify credentials in GitHub Secrets:
   - `BROWSERSTACK_USERNAME`
   - `BROWSERSTACK_ACCESS_KEY`

2. Check `browserstack.yml` is in repository root

3. Look for BrowserStack connection logs in Actions output

### Authentication Issues?

The D365 tests need credentials:
- `D365_USERNAME` - Set in GitHub Secrets
- `D365_PASSWORD` - Set in GitHub Secrets

## 📊 BrowserStack Configuration

Your `browserstack.yml` is configured to run on:
- ✅ Windows 10 + Chromium
- ✅ macOS Monterey + Chromium
- ✅ 2 parallel tests per platform
- ✅ Video recording enabled
- ✅ Network logs enabled
- ✅ Console logs enabled

## 🎯 Next Steps

1. **Commit and Push** the updated workflow files:
   ```bash
   git add .github/workflows/
   git commit -m "Fix: Configure BrowserStack SDK in GitHub Actions"
   git push
   ```

2. **Trigger a Test Run**:
   - Go to Actions tab
   - Run **BrowserStack Cloud Tests** workflow
   - Verify it completes without skipping

3. **Check BrowserStack Dashboard**:
   - Visit: https://automate.browserstack.com/dashboard
   - Look for your build: "FourHands & D365 Playwright Tests"
   - Watch the video recording

4. **Set Up Scheduled Runs** (Optional):
   - Already configured to run daily at 2 AM UTC
   - Edit cron schedule if needed

## 📝 Environment Variables Required

Make sure these are set in **GitHub Secrets**:

```
BROWSERSTACK_USERNAME     # Your BrowserStack username
BROWSERSTACK_ACCESS_KEY   # Your BrowserStack access key
D365_USERNAME            # D365 login username
D365_PASSWORD            # D365 login password
```

## ✅ Success Criteria

After running the workflow, you should see:

1. ✅ GitHub Actions workflow completes successfully
2. ✅ No tests skipped (unless intentionally marked)
3. ✅ Build appears in BrowserStack dashboard
4. ✅ Video recording available
5. ✅ Test results and logs visible

---

**Created:** October 16, 2025  
**Status:** ✅ Ready to use  
**BrowserStack Dashboard:** https://automate.browserstack.com/dashboard
