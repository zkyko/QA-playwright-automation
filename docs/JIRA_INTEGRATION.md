# Jira/Zephyr Integration Guide

## Overview

This project integrates with Jira and Zephyr Scale to provide automated test management, execution tracking, and defect reporting directly from your CI/CD pipeline.

## Features

✅ **Automated Test Cycle Creation** - Creates test cycles in Zephyr Scale for each build
✅ **Real-time Test Execution Updates** - Updates test case status in Jira as tests execute
✅ **Automatic Defect Creation** - Creates Jira bugs for failed test cases
✅ **Test Traceability** - Links automated tests to Jira test cases and user stories
✅ **Comprehensive Reporting** - Generates detailed reports with links to Jira

## Prerequisites

### 1. Jira Setup

1. **Jira Account** with API access
2. **Zephyr Scale** installed and configured in your Jira instance
3. **API Token** generated from Jira (https://id.atlassian.com/manage-profile/security/api-tokens)

### 2. Azure DevOps Variable Groups

Create a variable group named `Jira-Zephyr-Config` with the following variables:

| Variable Name | Description | Example |
|--------------|-------------|---------|
| `JIRA_BASE_URL` | Your Jira instance URL | `https://yourcompany.atlassian.net` |
| `JIRA_EMAIL` | Email associated with Jira account | `your.email@company.com` |
| `JIRA_API_TOKEN` | Jira API token (mark as secret) | `ATATT3xFfGF0B...` |
| `JIRA_PROJECT_KEY` | Your Jira project key | `QA`, `TEST`, etc. |
| `JIRA_VERSION` | Optional: Release version | `v1.0.0`, `Sprint 23` |

**To create the variable group:**
1. Go to Azure DevOps → Pipelines → Library
2. Click "+ Variable group"
3. Name it `Jira-Zephyr-Config`
4. Add all variables listed above
5. Mark `JIRA_API_TOKEN` as secret (lock icon)
6. Save

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## How It Works

### Pipeline Flow

```
1. Setup Jira Test Cycle
   ↓
2. Run Smoke Tests → Update Jira Results
   ↓
3. Run E2E Tests → Update Jira Results
   ↓
4. Generate Reports
   ↓
5. Finalize Test Cycle & Create Defects (if needed)
```

### Test Cycle Lifecycle

1. **Creation**: When pipeline starts, a new test cycle is created in Zephyr Scale
2. **Execution**: As tests run, results are pushed to Jira in real-time
3. **Finalization**: After all tests complete, the cycle is marked as "Done" with summary
4. **Defect Creation**: Failed tests automatically create Jira bugs (optional)

## Linking Tests to Jira

### Method 1: Using Pytest Markers (Recommended)

```python
import pytest
from playwright.sync_api import Page, expect

@pytest.mark.smoke
@pytest.mark.jira('TEST-101')  # Link to Jira test case
@pytest.mark.jira_issue('PROJ-500')  # Link to user story/issue
def test_login_functionality(page: Page):
    """Test login with Jira integration"""
    # Your test code here
    pass
```

### Method 2: Test Name Convention

Include the Jira test case key in your test name:

```python
def test_login_functionality_TEST101(page: Page):
    """The test case key will be extracted automatically"""
    pass
```

### Method 3: Test Docstring

```python
def test_login_functionality(page: Page):
    """
    Test login functionality
    Jira Test Case: TEST-101
    User Story: PROJ-500
    """
    pass
```

## Using the Jira Integration Utility

The `utils/jira_integration.py` script provides CLI commands for Jira operations.

### Create Test Cycle

```bash
python utils/jira_integration.py create-cycle \
  --name "Automated Test Run - Build 123" \
  --project "QA" \
  --version "v1.0.0"
```

### Update Test Results

```bash
python utils/jira_integration.py update-results \
  --cycle "TEST-RUN-456" \
  --results "reports/junit/smoke-results.xml" \
  --test-type "smoke"
```

### Finalize Test Cycle

```bash
python utils/jira_integration.py finalize-cycle \
  --cycle "TEST-RUN-456" \
  --build "123" \
  --build-url "https://dev.azure.com/..."
```

### Create Defects for Failures

```bash
python utils/jira_integration.py create-defects \
  --cycle "TEST-RUN-456" \
  --build "123"
```

## Running Tests with Jira Integration

### Local Execution

```bash
# Set environment variables
export JIRA_BASE_URL="https://yourcompany.atlassian.net"
export JIRA_EMAIL="your.email@company.com"
export JIRA_API_TOKEN="your-token"
export JIRA_PROJECT_KEY="QA"
export ZEPHYR_CYCLE_KEY="TEST-RUN-123"

# Run tests
pytest tests/ -m smoke -v --junitxml=reports/junit/results.xml

# Update Jira with results
python utils/jira_integration.py update-results \
  --cycle "$ZEPHYR_CYCLE_KEY" \
  --results "reports/junit/results.xml" \
  --test-type "smoke"
```

### CI/CD Execution

The integration is automatic when running via Azure Pipelines. Simply push your code and the pipeline will:
1. Create a test cycle
2. Run tests
3. Update Jira with results
4. Finalize the cycle
5. Create defects for failures (if enabled)

## Test Case Mapping

### In Jira/Zephyr

1. Create test cases in Jira with unique keys (e.g., `TEST-101`, `TEST-102`)
2. Add test cases to your test cycle
3. Note the test case keys for use in your automated tests

### In Your Tests

Use the `@pytest.mark.jira()` decorator with the test case key:

```python
@pytest.mark.jira('TEST-101')
def test_my_feature(page: Page):
    pass
```

When this test runs, it will automatically update the execution status of `TEST-101` in Zephyr.

## Viewing Results

### In Jira

1. Navigate to your Jira project
2. Go to Zephyr Scale (usually in the left sidebar)
3. Click on "Test Cycles"
4. Find your test cycle (e.g., "Automated Test Run - Build 123")
5. View detailed test execution results

### In Azure DevOps

1. Go to your pipeline run
2. View the test results tab
3. Download Allure reports artifact
4. Check console output for Jira links

## Defect Management

### Automatic Defect Creation

When tests fail, defects can be automatically created in Jira with:
- Test name and details
- Error message and stack trace
- Link to test cycle
- Build number and timestamp
- Labels: `automated-test`, `test-failure`, `build-{number}`

### Defect Format

```
Title: [Automated] Test Failure: test_login_functionality

Description:
### Test Failure Details
- Test Name: test_login_functionality
- Test Cycle: TEST-RUN-456
- Build Number: 123
- Detected: 2025-10-14 10:30:00

### Error Message
AssertionError: Expected element to be visible
...

### Investigation Required
This defect was automatically created from a failed automated test execution.
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `JIRA_BASE_URL` | Yes | Jira instance URL |
| `JIRA_EMAIL` | Yes | Jira account email |
| `JIRA_API_TOKEN` | Yes | Jira API token |
| `JIRA_PROJECT_KEY` | Yes | Project key for creating issues |
| `ZEPHYR_CYCLE_KEY` | No | Current test cycle key (set by pipeline) |
| `JIRA_VERSION` | No | Version/release name for test cycle |

### Pytest Configuration

Update `conftest.py` to include the Jira plugin:

```python
# Import the Jira integration plugin
pytest_plugins = ['conftest_jira']
```

## Troubleshooting

### Issue: Test cycle not created

**Possible causes:**
- Invalid Jira credentials
- Zephyr Scale not installed in Jira
- Incorrect project key
- API token expired

**Solution:**
```bash
# Test your credentials
python utils/jira_integration.py create-cycle \
  --name "Test Cycle" \
  --project "YOUR_PROJECT_KEY"
```

### Issue: Test results not updating

**Possible causes:**
- Test case key not found in Jira
- Incorrect test case key format
- Test case not added to the test cycle

**Solution:**
- Verify test case keys exist in Jira
- Ensure tests are marked with `@pytest.mark.jira('KEY')`
- Check console output for update errors

### Issue: Defects not created

**Possible causes:**
- Insufficient permissions
- Invalid issue type configuration
- Required fields not provided

**Solution:**
- Verify your Jira user has permission to create bugs
- Check project issue type configuration
- Review console output for specific errors

### Common Error Messages

**"401 Unauthorized"**
```
Solution: Check your API token and email are correct
Verify at: https://id.atlassian.com/manage-profile/security/api-tokens
```

**"404 Not Found"**
```
Solution: Verify your Jira base URL is correct
Should be: https://yourcompany.atlassian.net (no trailing slash)
```

**"Test case not found"**
```
Solution: Ensure the test case key exists in Jira
Format should be: PROJECT-123 (uppercase)
```

## Best Practices

### 1. Test Case Naming

- Use descriptive test case names in Jira
- Keep test case keys consistent with automated test names
- Group related tests in the same test cycle

### 2. Test Markers

```python
# Good: Clear markers with Jira links
@pytest.mark.smoke
@pytest.mark.jira('TEST-101')
@pytest.mark.jira_issue('PROJ-500')
def test_critical_login_flow(page: Page):
    pass

# Avoid: Multiple unrelated markers
@pytest.mark.jira('TEST-101')
@pytest.mark.jira('TEST-102')  # Don't link to multiple test cases
def test_something(page: Page):
    pass
```

### 3. Defect Creation

- Review auto-created defects regularly
- Add additional context manually if needed
- Close duplicate defects
- Link defects to appropriate sprints/epics

### 4. Test Cycles

- Use meaningful cycle names (include build number, date)
- Create separate cycles for different test types (smoke, regression, e2e)
- Archive old test cycles periodically

## Advanced Usage

### Custom Zephyr API Endpoints

If you need to use different Zephyr Scale endpoints, modify `utils/jira_integration.py`:

```python
# For Zephyr Scale Cloud
self.zephyr_base = f"{self.base_url}/rest/atm/1.0"

# For Zephyr Scale Server
self.zephyr_base = f"{self.base_url}/rest/zapi/latest"
```

### Custom Defect Templates

Modify the `create_defect()` method in `jira_integration.py`:

```python
def create_defect(self, test_name: str, error_message: str, 
                 cycle_key: str, build_number: str):
    # Customize the defect payload here
    payload = {
        "fields": {
            "project": {"key": self.project_key},
            "summary": f"[Automated] {test_name}",
            "description": "Your custom description",
            "issuetype": {"name": "Bug"},
            "priority": {"name": "High"},  # Change priority
            "labels": ["automated-test"],
            "customfield_10001": "Custom value"  # Add custom fields
        }
    }
```

### Parallel Test Execution

The pipeline supports parallel test execution with Jira integration:

```yaml
- script: |
    pytest tests/ -n auto --junitxml=reports/junit/results.xml
  displayName: 'Run Tests in Parallel'
```

Results from all parallel tests will be aggregated and pushed to Jira.

## API Reference

### JiraZephyrIntegration Class

**Methods:**

- `create_test_cycle(name, project_key, version)` - Create a new test cycle
- `parse_junit_results(junit_file)` - Parse JUnit XML results
- `update_test_results(cycle_key, junit_file, test_type)` - Update test executions
- `finalize_test_cycle(cycle_key, build_number, build_url)` - Finalize cycle
- `create_defect(test_name, error_message, cycle_key, build_number)` - Create bug
- `create_defects_from_failures(cycle_key, build_number)` - Batch create defects

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Azure Pipeline logs
3. Check Jira/Zephyr Scale documentation
4. Contact your Jira administrator for permissions issues

## References

- [Jira REST API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Zephyr Scale API Documentation](https://support.smartbear.com/zephyr-scale-cloud/api-docs/)
- [Azure DevOps Variable Groups](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/variable-groups)
- [Pytest Markers Documentation](https://docs.pytest.org/en/stable/how-to/mark.html)
