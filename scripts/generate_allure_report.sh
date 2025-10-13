#!/bin/bash

# Generate Allure Report
# Usage: ./scripts/generate_allure_report.sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Generating Allure Report${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if allure-results exists
if [ ! -d "reports/allure-results" ]; then
    echo -e "${RED}Error: reports/allure-results directory not found!${NC}"
    echo -e "${BLUE}Run tests first to generate results.${NC}"
    exit 1
fi

# Check if Allure CLI is installed
if ! command -v allure &> /dev/null; then
    echo -e "${RED}Allure CLI not found!${NC}"
    echo -e "${BLUE}Installing Allure CLI...${NC}"
    
    if command -v npm &> /dev/null; then
        npm install -g allure-commandline
    else
        echo -e "${RED}npm not found. Please install Node.js first.${NC}"
        echo -e "${BLUE}Visit: https://nodejs.org/${NC}"
        exit 1
    fi
fi

# Generate report
echo -e "${GREEN}Generating Allure report...${NC}"
allure generate reports/allure-results -o reports/allure-report --clean

# Open report
echo -e "${GREEN}Opening Allure report in browser...${NC}"
allure open reports/allure-report

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Report generated successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
