"""
Pytest plugin for Jira test case integration
Allows marking tests with Jira test case keys
"""

import pytest
import os
from typing import Optional


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers",
        "jira(key): Mark test with Jira test case key (e.g., @pytest.mark.jira('TEST-123'))"
    )
    config.addinivalue_line(
        "markers",
        "jira_issue(key): Link test to Jira issue/story (e.g., @pytest.mark.jira_issue('PROJ-456'))"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test items to add Jira test case information
    """
    for item in items:
        # Get Jira test case key from marker
        jira_marker = item.get_closest_marker('jira')
        if jira_marker and jira_marker.args:
            test_case_key = jira_marker.args[0]
            # Add to test properties for JUnit XML reporting
            item.user_properties.append(('jira_test_case', test_case_key))
            
            # Also modify the nodeid to include Jira key
            # This helps with identification in reports
            item._nodeid = f"{item.nodeid} [{test_case_key}]"
        
        # Get Jira issue key from marker
        jira_issue_marker = item.get_closest_marker('jira_issue')
        if jira_issue_marker and jira_issue_marker.args:
            issue_key = jira_issue_marker.args[0]
            item.user_properties.append(('jira_issue', issue_key))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Add Jira information to test reports
    """
    outcome = yield
    report = outcome.get_result()
    
    # Add Jira test case key to report
    jira_marker = item.get_closest_marker('jira')
    if jira_marker and jira_marker.args:
        report.jira_test_case = jira_marker.args[0]
    
    # Add Jira issue key to report
    jira_issue_marker = item.get_closest_marker('jira_issue')
    if jira_issue_marker and jira_issue_marker.args:
        report.jira_issue = jira_issue_marker.args[0]
    
    # Store test cycle key from environment
    zephyr_cycle = os.getenv('ZEPHYR_CYCLE_KEY')
    if zephyr_cycle:
        report.zephyr_cycle = zephyr_cycle


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Add Jira integration summary to terminal output
    """
    jira_enabled = os.getenv('JIRA_BASE_URL') and os.getenv('JIRA_API_TOKEN')
    cycle_key = os.getenv('ZEPHYR_CYCLE_KEY')
    
    if jira_enabled and cycle_key:
        terminalreporter.write_sep("=", "Jira/Zephyr Integration")
        terminalreporter.write_line(f"Test Cycle: {cycle_key}")
        terminalreporter.write_line(f"Jira URL: {os.getenv('JIRA_BASE_URL')}")
        
        # Count tests with Jira markers
        jira_test_count = 0
        for item in terminalreporter.stats.get('passed', []) + \
                   terminalreporter.stats.get('failed', []) + \
                   terminalreporter.stats.get('skipped', []):
            if hasattr(item, 'jira_test_case'):
                jira_test_count += 1
        
        terminalreporter.write_line(f"Tests linked to Jira: {jira_test_count}")


# Custom JUnit XML processing for Jira integration
@pytest.hookimpl(optionalhook=True)
def pytest_junit_modify_testcase(testcase, report):
    """
    Modify JUnit XML test case to include Jira information
    """
    if hasattr(report, 'jira_test_case'):
        testcase.add_property('jira_test_case', report.jira_test_case)
    
    if hasattr(report, 'jira_issue'):
        testcase.add_property('jira_issue', report.jira_issue)
    
    if hasattr(report, 'zephyr_cycle'):
        testcase.add_property('zephyr_cycle', report.zephyr_cycle)
