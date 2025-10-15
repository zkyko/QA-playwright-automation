# 🪟 Windows Quick Start Guide
## Four Hands QA Automation Framework

**For Windows Users** | **PowerShell Commands**

---

## 🚀 Quick Start (Windows)

### Step 1: Run Cleanup Script
```powershell
# Open PowerShell in project directory
cd "C:\Users\Nbhandari\Documents\QA-PlayWright-Automation\QA-PlayWright-Automation"

# Run cleanup script
.\scripts\cleanup_poc_files.ps1
```

### Step 2: Set Up Environment
```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit with your credentials (use notepad or VS Code)
notepad .env
```

### Step 3: Run Tests
```powershell
# Run smoke tests locally
.\scripts\run_tests_local.ps1 smoke

# Run E2E tests
.\scripts\run_tests_local.ps1 e2e

# Run on BrowserStack
.\scripts\run_tests_browserstack.ps1 smoke

# Generate Allure report
.\scripts\generate_allure_report.ps1
```

---

## 📝 PowerShell Execution Policy

If you get an error about script execution:

```powershell
# Check current policy
Get-ExecutionPolicy

# Set policy for current user (recommended)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single script
PowerShell -ExecutionPolicy Bypass -File .\scripts\cleanup_poc_files.ps1
```

---

## 🛠️ Available Scripts

| Script | Command | Purpose |
|--------|---------|---------|
| **Cleanup** | `.\scripts\cleanup_poc_files.ps1` | Remove old POC files |
| **Local Tests** | `.\scripts\run_tests_local.ps1 smoke` | Run tests locally |
| **BrowserStack** | `.\scripts\run_tests_browserstack.ps1 smoke` | Run on BrowserStack |
| **Allure Report** | `.\scripts\generate_allure_report.ps1` | Generate reports |

---

## 🧪 Test Commands (Direct)

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run specific tests
pytest tests\ -m smoke -v --headed
pytest tests\ -m e2e -v --headed
pytest tests\d365\ -v --headed
pytest tests\fh\ -v --headed

# Run with Allure reporting
pytest tests\ -m smoke -v --headed --alluredir=reports\allure-results
```

---

## 📂 Windows-Specific Paths

```powershell
# Project root
C:\Users\Nbhandari\Documents\QA-PlayWright-Automation\QA-PlayWright-Automation

# Scripts folder
C:\Users\Nbhandari\Documents\QA-PlayWright-Automation\QA-PlayWright-Automation\scripts

# Documentation
C:\Users\Nbhandari\Documents\QA-PlayWright-Automation\QA-PlayWright-Automation\docs

# Virtual environment
C:\Users\Nbhandari\Documents\QA-PlayWright-Automation\QA-PlayWright-Automation\venv
```

---

## 🔧 Troubleshooting (Windows)

### Issue: Script not recognized
```powershell
# Make sure you're in the project root
cd "C:\Users\Nbhandari\Documents\QA-PlayWright-Automation\QA-PlayWright-Automation"

# Use .\ prefix
.\scripts\cleanup_poc_files.ps1
```

### Issue: Virtual environment not found
```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
playwright install chromium
```

### Issue: Playwright not found
```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Then install
pip install playwright
playwright install chromium
```

---

## 📚 Documentation Paths (Windows)

```powershell
# View documentation
type START_HERE.md
type QUICK_REFERENCE.md
type docs\AZURE_SETUP.md
type docs\BROWSERSTACK_INTEGRATION.md
type docs\LOCAL_DEVELOPMENT.md

# Or open in notepad
notepad START_HERE.md
notepad docs\AZURE_SETUP.md
```

---

## ✅ Your Next Commands

```powershell
# 1. Navigate to project
cd "C:\Users\Nbhandari\Documents\QA-PlayWright-Automation\QA-PlayWright-Automation"

# 2. Run cleanup
.\scripts\cleanup_poc_files.ps1

# 3. Set up .env file
Copy-Item .env.example .env
notepad .env

# 4. Run smoke tests
.\scripts\run_tests_local.ps1 smoke

# 5. View report
.\scripts\generate_allure_report.ps1
```

---

## 🎯 Summary

**Windows PowerShell commands are ready!**

All scripts are in: `.\scripts\`
- ✅ cleanup_poc_files.ps1
- ✅ run_tests_local.ps1
- ✅ run_tests_browserstack.ps1
- ✅ generate_allure_report.ps1

**Start with:** `.\scripts\cleanup_poc_files.ps1`

---

**💡 Tip:** Use PowerShell (not CMD) for best results!
