"""
Example test file showing Jira/Zephyr integration
Demonstrates how to link tests with Jira test cases
"""

import pytest
from playwright.sync_api import Page, expect


@pytest.mark.smoke
@pytest.mark.jira('TEST-101')  # Link to Jira test case
@pytest.mark.jira_issue('PROJ-500')  # Link to Jira story/issue
def test_login_success_with_jira(page: Page, fh_base_url, fh_username, fh_password):
    """
    Test successful login flow
    
    Linked to:
    - Test Case: TEST-101
    - User Story: PROJ-500
    """
    # Navigate to login page
    page.goto(f"{fh_base_url}/account/login")
    
    # Fill in credentials
    page.fill('input[name="email"]', fh_username)
    page.fill('input[name="password"]', fh_password)
    
    # Click login button
    page.click('button[type="submit"]')
    
    # Verify login success
    expect(page).to_have_url(f"{fh_base_url}/account/dashboard")
    expect(page.locator('.user-welcome')).to_be_visible()


@pytest.mark.smoke
@pytest.mark.jira('TEST-102')
def test_logout_functionality(page: Page, fh_base_url, fh_username, fh_password):
    """
    Test logout functionality
    
    Linked to Test Case: TEST-102
    """
    # Login first
    page.goto(f"{fh_base_url}/account/login")
    page.fill('input[name="email"]', fh_username)
    page.fill('input[name="password"]', fh_password)
    page.click('button[type="submit"]')
    
    # Logout
    page.click('.logout-button')
    
    # Verify redirected to login page
    expect(page).to_have_url(f"{fh_base_url}/account/login")


@pytest.mark.e2e
@pytest.mark.cart
@pytest.mark.jira('TEST-201')
@pytest.mark.jira_issue('PROJ-510')
def test_add_to_cart_flow(page: Page, fh_base_url):
    """
    Test adding product to cart
    
    Linked to:
    - Test Case: TEST-201
    - User Story: PROJ-510
    """
    # Navigate to product page
    page.goto(f"{fh_base_url}/products/sample-product")
    
    # Add to cart
    page.click('button.add-to-cart')
    
    # Verify cart count updated
    cart_count = page.locator('.cart-count').inner_text()
    assert int(cart_count) > 0, "Cart should have at least 1 item"


@pytest.mark.e2e
@pytest.mark.checkout
@pytest.mark.jira('TEST-301')
def test_checkout_process(page: Page, fh_base_url, fh_username, fh_password):
    """
    Test complete checkout process
    
    Linked to Test Case: TEST-301
    """
    # Login
    page.goto(f"{fh_base_url}/account/login")
    page.fill('input[name="email"]', fh_username)
    page.fill('input[name="password"]', fh_password)
    page.click('button[type="submit"]')
    
    # Add product to cart
    page.goto(f"{fh_base_url}/products/sample-product")
    page.click('button.add-to-cart')
    
    # Go to checkout
    page.goto(f"{fh_base_url}/checkout")
    
    # Fill shipping information
    page.fill('input[name="address"]', '123 Test Street')
    page.fill('input[name="city"]', 'Test City')
    page.fill('input[name="zip"]', '12345')
    
    # Proceed to payment
    page.click('button.continue-to-payment')
    
    # Verify on payment page
    expect(page).to_have_url(f"{fh_base_url}/checkout/payment")


@pytest.mark.smoke
@pytest.mark.jira('TEST-103')
def test_search_functionality(page: Page, fh_base_url):
    """
    Test search functionality
    
    Linked to Test Case: TEST-103
    """
    page.goto(fh_base_url)
    
    # Perform search
    search_query = "sofa"
    page.fill('input[name="search"]', search_query)
    page.press('input[name="search"]', 'Enter')
    
    # Verify search results
    expect(page.locator('.search-results')).to_be_visible()
    results_text = page.locator('.results-count').inner_text()
    assert "results" in results_text.lower(), "Should display search results count"


# Example of test without Jira link (will still run but won't update Zephyr)
@pytest.mark.smoke
def test_homepage_load(page: Page, fh_base_url):
    """
    Test homepage loads successfully
    
    No Jira test case linked - for ad-hoc testing
    """
    page.goto(fh_base_url)
    expect(page).to_have_title(pytest.approx("Four Hands", abs=20))
    expect(page.locator('.header-logo')).to_be_visible()
