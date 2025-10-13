# Run Tests on BrowserStack - Four Hands QA Automation (Windows)
# Usage: .\run_tests_browserstack.ps1 [test_suite]
# Examples:
#   .\run_tests_browserstack.ps1 smoke
#   .\run_tests_browserstack.ps1 e2e
#   .\run_tests_browserstack.ps1 all

param(
    [string]$TestSuite = "smoke"
)

Write-Host "================================================" -ForegroundColor Blue
Write-Host "Four Hands QA - BrowserStack Cross-Browser Tests" -ForegroundColor Blue
Write-Host "================================================" -ForegroundColor Blue
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Virtual environment not found. Creating..." -ForegroundColor Red
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& "venv\Scripts\Activate.ps1"

# Install/update dependencies
Write-Host "Installing dependencies..." -ForegroundColor Green
python -m pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "Error: .env file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.example to .env and configure your credentials." -ForegroundColor Blue
    exit 1
}

# Load .env file and check BrowserStack credentials
$envContent = Get-Content .env
$bsUsername = ($envContent | Select-String "BROWSERSTACK_USERNAME=").ToString().Split("=")[1]
$bsAccessKey = ($envContent | Select-String "BROWSERSTACK_ACCESS_KEY=").ToString().Split("=")[1]

if ([string]::IsNullOrEmpty($bsUsername) -or [string]::IsNullOrEmpty($bsAccessKey)) {
    Write-Host "Error: BrowserStack credentials not found in .env file!" -ForegroundColor Red
    Write-Host "Please add BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY to .env" -ForegroundColor Blue
    exit 1
}

# Enable BrowserStack
$env:USE_BROWSERSTACK = "true"
$env:BS_PROJECT = "FourHands-QA-Automation"
$env:BS_BUILD = "Local-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Clean previous reports
Write-Host "Cleaning previous reports..." -ForegroundColor Green
if (Test-Path "reports\allure-results") {
    Remove-Item -Path "reports\allure-results" -Recurse -Force
}
if (Test-Path "test-results") {
    Remove-Item -Path "test-results" -Recurse -Force
}
New-Item -ItemType Directory -Force -Path "reports\allure-results" | Out-Null

# Run tests
Write-Host "Running $TestSuite tests on BrowserStack..." -ForegroundColor Green
Write-Host "Note: Tests will run on BrowserStack cloud browsers" -ForegroundColor Yellow
Write-Host "Visit: https://automate.browserstack.com/dashboard/v2" -ForegroundColor Yellow
Write-Host ""

if ($TestSuite -eq "all") {
    pytest tests/ -v --alluredir=reports/allure-results --tb=short
} else {
    pytest tests/ -m $TestSuite -v --alluredir=reports/allure-results --tb=short
}

# Generate Allure report
Write-Host "Generating Allure report..." -ForegroundColor Green
if (Get-Command allure -ErrorAction SilentlyContinue) {
    allure generate reports/allure-results -o reports/allure-report --clean
    Write-Host "Opening Allure report..." -ForegroundColor Green
    allure open reports/allure-report
} else {
    Write-Host "Allure CLI not installed. Install with: npm install -g allure-commandline" -ForegroundColor Red
    Write-Host "You can still view results in: reports\allure-results" -ForegroundColor Blue
}

Write-Host "================================================" -ForegroundColor Green
Write-Host "BrowserStack tests completed!" -ForegroundColor Green
Write-Host "View recordings: https://automate.browserstack.com/dashboard/v2" -ForegroundColor Blue
Write-Host "================================================" -ForegroundColor Green
