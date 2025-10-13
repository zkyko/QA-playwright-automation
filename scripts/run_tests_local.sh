#!/bin/bash

# Run Tests Locally - Four Hands QA Automation
# Usage: ./scripts/run_tests_local.sh [test_suite]
# Examples:
#   ./scripts/run_tests_local.sh smoke
#   ./scripts/run_tests_local.sh e2e
#   ./scripts/run_tests_local.sh d365

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Four Hands QA Automation - Local Tests${NC}"
echo -e "${BLUE}========================================${NC}"

# Default test suite
TEST_SUITE="${1:-smoke}"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Install Playwright browsers
echo -e "${GREEN}Installing Playwright browsers...${NC}"
playwright install chromium

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo -e "${BLUE}Please copy .env.example to .env and configure your credentials.${NC}"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Clean previous reports
echo -e "${GREEN}Cleaning previous reports...${NC}"
rm -rf reports/allure-results
rm -rf test-results
mkdir -p reports/allure-results

# Run tests
echo -e "${GREEN}Running ${TEST_SUITE} tests...${NC}"
if [ "$TEST_SUITE" = "all" ]; then
    pytest tests/ -v \
        --headed \
        --alluredir=reports/allure-results \
        --tb=short
else
    pytest tests/ -m "$TEST_SUITE" -v \
        --headed \
        --alluredir=reports/allure-results \
        --tb=short
fi

# Generate Allure report
echo -e "${GREEN}Generating Allure report...${NC}"
if command -v allure &> /dev/null; then
    allure generate reports/allure-results -o reports/allure-report --clean
    echo -e "${GREEN}Opening Allure report...${NC}"
    allure open reports/allure-report
else
    echo -e "${RED}Allure CLI not installed. Install with: npm install -g allure-commandline${NC}"
    echo -e "${BLUE}You can still view results in: reports/allure-results${NC}"
fi

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Tests completed!${NC}"
echo -e "${GREEN}========================================${NC}"
