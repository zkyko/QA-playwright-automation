# Run Tests Locally - Four Hands QA Automation (Windows)
# Usage: .\run_tests_local.ps1 [test_suite]
# Examples:
#   .\run_tests_local.ps1 smoke
#   .\run_tests_local.ps1 e2e
#   .\run_tests_local.ps1 d365

param(
    [string]$TestSuite = "smoke"
)

Write-Host "========================================" -ForegroundColor Blue
Write-Host "Four Hands QA Automation - Local Tests" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
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

# Install Playwright browsers
Write-Host "Installing Playwright browsers..." -ForegroundColor Green
playwright install chromium

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "Error: .env file not found!" -ForegroundColor Red
    Write-Host "Please copy .env.example to .env and configure your credentials." -ForegroundColor Blue
    exit 1
}

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
Write-Host "Running $TestSuite tests..." -ForegroundColor Green
if ($TestSuite -eq "all") {
    pytest tests/ -v --headed --alluredir=reports/allure-results --tb=short
} else {
    pytest tests/ -m $TestSuite -v --headed --alluredir=reports/allure-results --tb=short
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

Write-Host "========================================" -ForegroundColor Green
Write-Host "Tests completed!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
