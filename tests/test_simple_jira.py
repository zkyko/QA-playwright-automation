"""
Simple test linked to Jira - WAP-T201
This test will update Jira/Zephyr when executed
"""
import pytest
from playwright.sync_api import Page


@pytest.mark.smoke
@pytest.mark.jira('WAP-T201')  # Links to Jira test case WAP-T201
def test_login_simple(page: Page):
    """
    Playwright: LoginTest
    
    Linked to Jira Test Case: WAP-T201
    This is a simple test to verify Jira integration works
    """
    # Navigate to FourHands login page
    page.goto("https://fh-test-fourhandscom.azurewebsites.net/account/login")
    
    # Verify page loaded
    assert "login" in page.url.lower(), "Should be on login page"
    
    # Verify login form exists
    email_input = page.locator('input[name="email"], input[type="email"]').first
    assert email_input.is_visible(), "Email input should be visible"
    
    print("✓ Login page loaded successfully")
    print("✓ Test case WAP-T201 executed")
