"""
D365 Sales Order Page Object - Using Playwright Codegen selectors
"""
from playwright.sync_api import Page
from pages.d365 import D365BasePage


class D365SalesOrderPage(D365BasePage):
    """Page object for D365 Sales Order functionality."""
    
    def __init__(self, page: Page):
        """Initialize Sales Order page."""
        super().__init__(page)
        
        # Navigation labels (use with get_by_label)
        self.nav_expand_label = "Expand the navigation pane"
        self.modules_label = "Modules"
        
        # Treeitem names (use with get_by_role)
        self.accounts_receivable_name = "Accounts receivable"
        
        # Text labels (use with get_by_text)
        self.all_sales_orders_text = "All sales orders"
        
        # Button names (use with get_by_role)
        self.new_button_name = "New"
        self.ok_button_name = "OK"
        
        # Form field IDs (use with locator)
        self.customer_account_id = "#SalesCreateOrder_5_SalesTable_CustAccount"
        self.delivery_mode_id = "#SalesCreateOrder_5_SalesTable_DlvMode"
        self.item_number_id = "#SalesLine_ItemId_2023_0_0"
    
    def navigate_to_sales_orders(self):
        """Navigate to All Sales Orders page."""
        print("📍 Navigating to Sales Orders...")
        
        # Expand navigation pane
        self.page.get_by_label(self.nav_expand_label).click()
        self.guard.wait_until_idle()
        
        # Click Modules
        self.page.get_by_label(self.modules_label).click()
        self.guard.wait_until_idle()
        
        # Click Accounts Receivable
        self.page.get_by_role("treeitem", name=self.accounts_receivable_name).click()
        self.guard.wait_until_idle()
        
        # Click All Sales Orders
        self.page.get_by_text(self.all_sales_orders_text).click()
        self.guard.wait_until_idle()
        
        print("✅ Successfully navigated to Sales Orders")
    
    def click_new_sales_order(self):
        """Click the New button to create sales order."""
        print("➕ Creating new sales order...")
        # Note: Button has icon, so we filter by name containing "New"
        self.page.get_by_role("button", name=self.new_button_name).click()
        self.guard.wait_until_idle()
    
    def select_customer(self, customer_account: str = "100001"):
        """
        Select customer account.
        
        Args:
            customer_account: Customer account number (default: 100001)
        """
        print(f"👤 Selecting customer: {customer_account}")
        
        # Click customer account dropdown
        self.page.locator(f"{self.customer_account_id} div").nth(1).click()
        self.guard.wait_until_idle()
        
        self.guard.wait_until_idle()  # Extra wait for dropdown
        
        # Select customer from grid
        self.page.get_by_role("gridcell", name=customer_account).get_by_label("Customer account").first.click()
        self.guard.wait_until_idle()
        
        print(f"✅ Customer {customer_account} selected")
    
    def select_delivery_mode(self, mode: str = "ZEFL-B2B"):
        """
        Select delivery mode.
        
        Args:
            mode: Delivery mode code (default: ZEFL-B2B)
        """
        print(f"🚚 Selecting delivery mode: {mode}")
        
        # Click delivery mode dropdown
        self.page.locator(f"{self.delivery_mode_id} div").nth(1).click()
        self.guard.wait_until_idle()
        
        # Select mode from list (row has mode twice in name)
        self.page.get_by_role("row", name=f"{mode} {mode}").get_by_label("Mode of delivery").click()
        self.guard.wait_until_idle()
        
        print(f"✅ Delivery mode {mode} selected")
    
    def click_ok(self):
        """Click OK button to confirm."""
        print("✔️ Clicking OK...")
        self.page.get_by_role("button", name=self.ok_button_name).click()
        self.guard.wait_until_idle()
    
    def select_item(self, item_number: str = "000022-"):
        """
        Select item to add to sales order.
        
        Args:
            item_number: Item number (default: 000022-)
        """
        print(f"📦 Selecting item: {item_number}")
        
        # Open item dropdown
        self.page.locator(self.item_number_id).get_by_role("button", name="Open").click()
        self.guard.wait_until_idle()
        
        # Select item from grid
        self.page.get_by_role("gridcell", name=item_number).get_by_label("Item number").click()
        self.guard.wait_until_idle()
        
        print(f"✅ Item {item_number} selected")
    
    def cancel_order(self):
        """Cancel the order creation."""
        print("❌ Cancelling order...")
        self.page.get_by_label("Sales order summary").get_by_role("button", name="Cancel").click()
        self.guard.wait_until_idle()
        print("✅ Order cancelled")
