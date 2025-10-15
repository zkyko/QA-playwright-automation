"""
D365 Create Sales Order Test - Complete Flow
Based on Playwright Codegen recording
"""
import pytest
import allure
from playwright.sync_api import Page


pytestmark = [pytest.mark.d365, pytest.mark.e2e]


@allure.feature("D365")
@allure.story("Sales Order Creation")
@allure.title("Create Sales Order - Complete Flow")
@pytest.mark.e2e
def test_d365_create_sales_order_complete(d365_authenticated_page: Page):
    """
    Test: Create a complete sales order in D365
    
    Steps from Playwright Codegen:
    1. Navigate to D365 Dashboard
    2. Expand navigation pane
    3. Go to Modules → Accounts Receivable → Orders → All Sales Orders
    4. Click New
    5. Select Customer: 100001 (Nicole Roby Designs)
    6. Select Delivery Mode: TXQA-B2B
    7. Click OK
    8. Select Item (opens item picker)
    9. Select an item
    10. Save
    11. Go back
    
    Note: Works both locally (with saved auth) and BrowserStack (programmatic login)
    """
    page = d365_authenticated_page
    
    with allure.step("Navigate to D365 Dashboard"):
        print("\n📍 Navigating to D365...")
        page.goto("https://fourhands-test.sandbox.operations.dynamics.com/?cmp=FH&mi=DefaultDashboard")
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(3000)  # Wait for D365 to settle
    
    with allure.step("Expand navigation pane"):
        print("📂 Expanding navigation...")
        page.get_by_role("button", name="Expand the navigation pane").click()
        page.wait_for_timeout(1000)
    
    with allure.step("Navigate to Modules"):
        print("🔍 Navigating to Modules...")
        page.get_by_role("treeitem", name="Modules").click()
        page.wait_for_timeout(1000)
    
    with allure.step("Navigate to Accounts Receivable"):
        print("💰 Opening Accounts Receivable...")
        page.get_by_role("treeitem", name="Accounts receivable").click()
        page.wait_for_timeout(1000)
    
    with allure.step("Navigate to Orders"):
        print("📋 Opening Orders...")
        page.get_by_role("treeitem", name="Orders").click()
        page.wait_for_timeout(1000)
    
    with allure.step("Open All Sales Orders"):
        print("📄 Opening All Sales Orders...")
        page.get_by_text("All sales orders").click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(2000)
    
    with allure.step("Click New to create order"):
        print("➕ Creating new sales order...")
        page.get_by_role("button", name=" New").click()
        page.wait_for_timeout(2000)
    
    with allure.step("Select Customer: 100001"):
        print("👤 Selecting customer...")
        # Click customer dropdown
        page.locator("#SalesCreateOrder_5_SalesTable_CustAccount div").nth(1).click()
        page.wait_for_timeout(1000)
        
        # Select customer from grid
        page.get_by_role("row", name="100001 Nicole Roby Designs").get_by_label("Name", exact=True).click()
        page.wait_for_timeout(1000)
    
    with allure.step("Select Delivery Mode: TXQA-B2B"):
        print("🚚 Selecting delivery mode...")
        # Click delivery mode dropdown
        page.locator("#SalesCreateOrder_5_SalesTable_DlvMode div").nth(1).click()
        page.wait_for_timeout(1000)
        
        # Select mode
        page.get_by_role("row", name="TXQA-B2B TXQA-B2B").get_by_label("Description").click()
        page.wait_for_timeout(1000)
    
    with allure.step("Click OK to create order"):
        print("✔️ Confirming order creation...")
        page.get_by_role("button", name="OK").click()
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(3000)  # Wait for order form to load
    
    with allure.step("Open item picker"):
        print("📦 Opening item picker...")
        page.get_by_role("combobox", name="Item number").click()
        page.wait_for_timeout(500)
        
        # Click Open button
        page.locator("#SalesLine_ItemId_2603_0_0").get_by_role("button", name="Open").click()
        page.wait_for_timeout(2000)
    
    with allure.step("Select item"):
        print("✨ Selecting item...")
        # Select first available item with "Light" in name
        page.get_by_title("LightCameldirectText").click()
        page.wait_for_timeout(1000)
    
    with allure.step("Save the order"):
        print("💾 Saving order...")
        page.get_by_role("button", name=" Save").click()
        page.wait_for_timeout(2000)
        
        # Sometimes need to click Save twice
        try:
            page.get_by_role("button", name=" Save").click(timeout=5000)
            page.wait_for_timeout(1000)
        except:
            pass  # Already saved
    
    with allure.step("Navigate back"):
        print("🔙 Navigating back...")
        page.get_by_role("button", name="Back", exact=True).click()
        page.wait_for_timeout(1000)
    
    print("\n✅ Successfully created sales order!")


@allure.feature("D365")
@allure.story("Sales Order Creation")
@allure.title("Create Sales Order - Verify Form Loads")
@pytest.mark.smoke
def test_d365_sales_order_form_loads(d365_authenticated_page: Page):
    """
    Quick smoke test: Verify sales order form loads
    
    Just navigates and opens the new order form.
    Faster than full creation test.
    """
    page = d365_authenticated_page
    
    # Navigate to dashboard
    page.goto("https://fourhands-test.sandbox.operations.dynamics.com/?cmp=FH&mi=DefaultDashboard")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000)
    
    # Expand navigation
    page.get_by_role("button", name="Expand the navigation pane").click()
    page.wait_for_timeout(1000)
    
    # Navigate to sales orders
    page.get_by_role("treeitem", name="Modules").click()
    page.wait_for_timeout(1000)
    
    page.get_by_role("treeitem", name="Accounts receivable").click()
    page.wait_for_timeout(1000)
    
    page.get_by_role("treeitem", name="Orders").click()
    page.wait_for_timeout(1000)
    
    page.get_by_text("All sales orders").click()
    page.wait_for_timeout(2000)
    
    # Click New
    page.get_by_role("button", name=" New").click()
    page.wait_for_timeout(2000)
    
    # Verify form loaded
    assert page.locator("#SalesCreateOrder_5_SalesTable_CustAccount").is_visible(), \
        "Customer account field should be visible"
    
    print("\n✅ Sales order form loaded successfully!")
