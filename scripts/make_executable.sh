#!/bin/bash
# Make all helper scripts executable
chmod +x scripts/run_tests_local.sh
chmod +x scripts/run_tests_browserstack.sh
chmod +x scripts/generate_allure_report.sh
chmod +x scripts/cleanup_poc_files.sh
echo "✅ All scripts are now executable!"
echo ""
echo "Available commands:"
echo "  ./scripts/run_tests_local.sh [test_suite]"
echo "  ./scripts/run_tests_browserstack.sh [test_suite]"
echo "  ./scripts/generate_allure_report.sh"
echo "  ./scripts/cleanup_poc_files.sh"
