#!/bin/bash

# Run Tests on BrowserStack - Four Hands QA Automation
# Usage: ./scripts/run_tests_browserstack.sh [test_suite]
# Examples:
#   ./scripts/run_tests_browserstack.sh smoke
#   ./scripts/run_tests_browserstack.sh e2e
#   ./scripts/run_tests_browserstack.sh all

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}Four Hands QA - BrowserStack Cross-Browser Tests${NC}"
echo -e "${BLUE}================================================${NC}"

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

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo -e "${BLUE}Please copy .env.example to .env and configure your credentials.${NC}"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Verify BrowserStack credentials
if [ -z "$BROWSERSTACK_USERNAME" ] || [ -z "$BROWSERSTACK_ACCESS_KEY" ]; then
    echo -e "${RED}Error: BrowserStack credentials not found in .env file!${NC}"
    echo -e "${BLUE}Please add BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY to .env${NC}"
    exit 1
fi

# Enable BrowserStack
export USE_BROWSERSTACK=true
export BS_PROJECT="FourHands-QA-Automation"
export BS_BUILD="Local-$(date +%Y%m%d-%H%M%S)"

# Clean previous reports
echo -e "${GREEN}Cleaning previous reports...${NC}"
rm -rf reports/allure-results
rm -rf test-results
mkdir -p reports/allure-results

# Run tests
echo -e "${GREEN}Running ${TEST_SUITE} tests on BrowserStack...${NC}"
echo -e "${YELLOW}Note: Tests will run on BrowserStack cloud browsers${NC}"
echo -e "${YELLOW}Visit: https://automate.browserstack.com/dashboard/v2${NC}"

if [ "$TEST_SUITE" = "all" ]; then
    pytest tests/ -v \
        --alluredir=reports/allure-results \
        --tb=short
else
    pytest tests/ -m "$TEST_SUITE" -v \
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

echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}BrowserStack tests completed!${NC}"
echo -e "${BLUE}View recordings: https://automate.browserstack.com/dashboard/v2${NC}"
echo -e "${GREEN}================================================${NC}"
