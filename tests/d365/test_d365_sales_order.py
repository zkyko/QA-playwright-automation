"""
D365 Sales Order Tests - BrowserStack Compatible

These tests are designed to work both locally (with auth) and on BrowserStack (without auth).
"""
import pytest
import allure
from playwright.sync_api import Page
from pages.d365.sales_order_page import D365SalesOrderPage
from pathlib import Path
import os


pytestmark = [pytest.mark.d365, pytest.mark.smoke]


def is_browserstack():
    """Check if running on BrowserStack."""
    # Only return True if we're actually running through BrowserStack SDK
    return os.getenv("BROWSERSTACK_BUILD_NAME") is not None or os.getenv("BROWSERSTACK_LOCAL") is not None


@pytest.fixture
def d365_authenticated_context(playwright_browser):
    """Provide D365 authenticated context using storage state."""
    storage_path = Path("storage_state/d365_session.json")
    
    # On BrowserStack, skip auth (will test login page instead)
    if is_browserstack():
        print("\n⚠️  Running on BrowserStack - skipping stored auth")
        context = playwright_browser.new_context()
    elif not storage_path.exists():
        pytest.skip("D365 storage state not found. Run: python save_d365_simple.py")
    else:
        context = playwright_browser.new_context(storage_state=str(storage_path))
    
    yield context
    context.close()


@pytest.fixture
def d365_authenticated_page(d365_authenticated_context):
    """Provide D365 authenticated page."""
    page = d365_authenticated_context.new_page()
    yield page
    page.close()


@allure.feature("D365")
@allure.story("Login")
@allure.title("D365 Login Page Loads")
@pytest.mark.smoke
def test_d365_login_page_loads(d365_authenticated_page: Page):
    """
    Test: Verify D365 login page loads correctly.
    
    This test works on BrowserStack without authentication.
    It verifies the D365 URL is accessible and login page appears.
    
    Steps:
        1. Navigate to D365 URL
        2. Wait for page to load
        3. Verify we get login page or dashboard
    
    Expected:
        - Page loads successfully
        - Either Microsoft login or D365 dashboard appears
    """
    page = d365_authenticated_page
    
    with allure.step("Navigate to D365"):
        print("\n📍 Navigating to D365...")
        d365_url = "https://fourhands-test.sandbox.operations.dynamics.com/?cmp=FH&mi=DefaultDashboard"
        page.goto(d365_url)
        page.wait_for_load_state("networkidle", timeout=30000)
    
    with allure.step("Verify page loaded"):
        # Wait a moment for any redirects to complete
        page.wait_for_timeout(2000)
        
        try:
            title = page.title()
            url = page.url
        except Exception as e:
            # If page navigated, get current state
            print(f"⚠️  Page navigated: {e}")
            page.wait_for_load_state("networkidle")
            title = page.title()
            url = page.url
        
        print(f"✅ Page loaded!")
        print(f"📄 Title: {title}")
        print(f"🌐 URL: {url}")
        
        allure.attach(title, name="Page Title", attachment_type=allure.attachment_type.TEXT)
        allure.attach(url, name="Current URL", attachment_type=allure.attachment_type.TEXT)
    
    with allure.step("Verify D365 or Microsoft login"):
        # Check if we're on login or already authenticated
        is_login = "login" in url.lower() or "microsoft" in url.lower()
        is_d365 = "dynamics.com" in url
        
        assert is_login or is_d365, f"Unexpected page: {url}"
        
        if is_login:
            print("✅ Microsoft login page detected")
            print("   (This is expected on BrowserStack without auth)")
        else:
            print("✅ D365 dashboard loaded (already authenticated)")
    
    print("\n✅ D365 page load test completed!")


@allure.feature("D365")
@allure.story("Navigation")
@allure.title("Navigate to Sales Orders")
@pytest.mark.smoke
def test_d365_navigate_to_sales_orders(d365_authenticated_page: Page):
    """
    Test: Navigate to Sales Orders page in D365
    
    Note: This test requires authentication.
    - Runs locally with saved auth
    - Skips on BrowserStack (requires manual login)
    
    Steps:
        1. Navigate to D365 dashboard
        2. Expand navigation pane
        3. Click Modules
        4. Click Accounts Receivable  
        5. Click All Sales Orders
    
    Expected:
        - Successfully navigates to Sales Orders page
    """
    page = d365_authenticated_page
    
    # Skip on BrowserStack (needs auth)
    if is_browserstack():
        pytest.skip("Skipping authenticated test on BrowserStack")
    
    sales_order_page = D365SalesOrderPage(page)
    
    with allure.step("Navigate to D365 Dashboard"):
        d365_url = "https://fourhands-test.sandbox.operations.dynamics.com/?cmp=FH&mi=DefaultDashboard"
        sales_order_page.navigate_to(d365_url)
    
    with allure.step("Navigate to Sales Orders"):
        sales_order_page.navigate_to_sales_orders()
    
    with allure.step("Verify on Sales Orders page"):
        assert "All sales orders" in page.content(), "Failed to navigate to Sales Orders"
        print("\n✅ Successfully navigated to Sales Orders!")


@allure.feature("D365")
@allure.story("Sales Order Creation")
@allure.title("Create Sales Order")
@pytest.mark.e2e
def test_d365_create_sales_order(d365_authenticated_page: Page):
    """
    Test: Create a new sales order in D365
    
    Note: Requires authentication. Skips on BrowserStack.
    
    Steps:
        1. Navigate to Sales Orders
        2. Create new order
        3. Select customer
        4. Select delivery mode
        5. Add item
        6. Cancel order (cleanup)
    """
    page = d365_authenticated_page
    
    # Skip on BrowserStack
    if is_browserstack():
        pytest.skip("Skipping authenticated test on BrowserStack")
    
    sales_order_page = D365SalesOrderPage(page)
    
    with allure.step("Navigate to Sales Orders"):
        d365_url = "https://fourhands-test.sandbox.operations.dynamics.com/?cmp=FH&mi=DefaultDashboard"
        sales_order_page.navigate_to(d365_url)
        sales_order_page.navigate_to_sales_orders()
    
    with allure.step("Create new sales order"):
        sales_order_page.click_new_sales_order()
    
    with allure.step("Select customer: 100001"):
        sales_order_page.select_customer("100001")
    
    with allure.step("Select delivery mode: ZEFL-B2B"):
        sales_order_page.select_delivery_mode("ZEFL-B2B")
    
    with allure.step("Confirm order details"):
        sales_order_page.click_ok()
    
    with allure.step("Add item: 000022-"):
        sales_order_page.select_item("000022-")
    
    with allure.step("Cancel order (cleanup)"):
        sales_order_page.cancel_order()
    
    print("\n✅ Successfully created and cancelled sales order!")


@allure.feature("D365")
@allure.story("Sales Order Form")
@allure.title("Verify Form Elements")
@pytest.mark.smoke  
def test_d365_sales_order_form_elements(d365_authenticated_page: Page):
    """
    Test: Verify sales order form elements are visible.
    
    Note: Requires authentication. Skips on BrowserStack.
    """
    page = d365_authenticated_page
    
    # Skip on BrowserStack
    if is_browserstack():
        pytest.skip("Skipping authenticated test on BrowserStack")
    
    sales_order_page = D365SalesOrderPage(page)
    
    with allure.step("Navigate and open new order form"):
        d365_url = "https://fourhands-test.sandbox.operations.dynamics.com/?cmp=FH&mi=DefaultDashboard"
        sales_order_page.navigate_to(d365_url)
        sales_order_page.navigate_to_sales_orders()
        sales_order_page.click_new_sales_order()
    
    with allure.step("Verify form elements visible"):
        assert page.locator(sales_order_page.customer_account_input).is_visible(), \
            "Customer account field not visible"
        
        assert page.locator(sales_order_page.delivery_mode_input).is_visible(), \
            "Delivery mode field not visible"
        
        assert page.get_by_role("button", name="OK").is_visible(), \
            "OK button not visible"
        
        print("✅ All form elements are visible!")
    
    with allure.step("Cleanup"):
        page.get_by_role("button", name="Cancel").first.click()
        sales_order_page.guard.wait_until_idle()
    
    print("\n✅ Form validation complete!")
