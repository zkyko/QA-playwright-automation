# Generate Allure Report (Windows)
# Usage: .\generate_allure_report.ps1

Write-Host "========================================" -ForegroundColor Blue
Write-Host "Generating Allure Report" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# Check if allure-results exists
if (-not (Test-Path "reports\allure-results")) {
    Write-Host "Error: reports\allure-results directory not found!" -ForegroundColor Red
    Write-Host "Run tests first to generate results." -ForegroundColor Blue
    exit 1
}

# Check if Allure CLI is installed
if (-not (Get-Command allure -ErrorAction SilentlyContinue)) {
    Write-Host "Allure CLI not found!" -ForegroundColor Red
    Write-Host "Installing Allure CLI..." -ForegroundColor Blue
    
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        npm install -g allure-commandline
    } else {
        Write-Host "npm not found. Please install Node.js first." -ForegroundColor Red
        Write-Host "Visit: https://nodejs.org/" -ForegroundColor Blue
        exit 1
    }
}

# Generate report
Write-Host "Generating Allure report..." -ForegroundColor Green
allure generate reports/allure-results -o reports/allure-report --clean

# Open report
Write-Host "Opening Allure report in browser..." -ForegroundColor Green
allure open reports/allure-report

Write-Host "========================================" -ForegroundColor Green
Write-Host "Report generated successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
