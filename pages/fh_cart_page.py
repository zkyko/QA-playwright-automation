"""
FourHands Cart Page object - Enhanced with Save for Later functionality.
"""
from typing import List
from playwright.sync_api import Page
from pages.base_page import BasePage


class FourHandsCartPage(BasePage):
    """Page object for FourHands Cart page."""
    
    def __init__(self, page: Page, timeout: int = 30000):
        """Initialize FourHands Cart page."""
        super().__init__(page, timeout)
        
        # Main cart selectors
        self.shopping_cart_title = "//h1[text()='Shopping Cart']"
        self.proceed_to_checkout_button = "//button[text()='Proceed to Checkout']"
        self.cart_empty_text = "//div[@class='text-body-xl mb-f10 text-neutral-50']"
        self.cart_products = "//img[contains(@src,'cloudfront.net/image/')]"
        self.cart_item_prices = "//div[@class='text-f-base-2xl md:w-[6.5em] md:min-w-min md:text-right']"
        self.summary_subtotal = "//div[@class='flex items-center justify-between']//span[contains(text(), '$')]"
        self.summary_total = "//div[@class='text-f-lg-3xl']"
        
        # Cart action buttons
        self.remove_button = "//button[@type='button'][normalize-space()='Remove']"
        self.save_for_later_button = "//button[text()='Save for Later']"
        
        # Saved for Later selectors
        self.saved_for_later_section = "//div[contains(@class, 'saved-for-later') or .//h2[contains(text(), 'Saved for Later')]]"
        self.saved_for_later_title = "//h2[contains(text(), 'Saved for Later')]"
        self.saved_for_later_empty_message = "//p[contains(text(), 'No saved items') or contains(text(), 'saved for later is empty')]"
        self.saved_for_later_items = "//div[contains(@class, 'saved-item')]"
        self.move_to_cart_button = "//button[text()='Move to Cart']"
        self.move_all_to_cart_button = "//button[text()='Move All to Cart']"
        self.remove_from_saved_button = "//button[contains(text(), 'Remove')]"
    
    def assert_loaded(self) -> None:
        """Assert that cart page is loaded."""
        self.wait_for_element_visible(self.shopping_cart_title)
    
    # ==================== Cart Actions ====================
    
    def click_proceed_to_checkout(self) -> None:
        """Click Proceed to Checkout button."""
        self.click_element(self.proceed_to_checkout_button)
    
    def remove_all_products(self) -> None:
        """Remove all products from cart."""
        print("🗑️ Removing all products from cart...")
        while True:
            remove_buttons = self.page.locator(self.remove_button).all()
            
            if not remove_buttons or len(remove_buttons) == 0:
                break
            
            # Click first remove button
            remove_buttons[0].click()
            self.page.wait_for_timeout(1000)
        print("✅ Cart cleared")
    
    def get_cart_item_count(self) -> int:
        """
        Get number of items in cart.
        
        Returns:
            int: Number of products in cart
        """
        return self.page.locator(self.cart_products).count()
    
    def is_cart_empty(self) -> bool:
        """Check if cart is empty."""
        return self.is_visible(self.cart_empty_text)
    
    def verify_product_in_cart(self, product_id: str) -> bool:
        """
        Check if specific product is in cart.
        
        Args:
            product_id: Product ID to check
            
        Returns:
            bool: True if product is in cart
        """
        product_selector = f"//div[contains(@class,'truncate')]//span[text()='{product_id}']"
        return self.is_visible(product_selector)
    
    # ==================== Save for Later Actions ====================
    
    def click_save_for_later_from_cart(self) -> None:
        """Click 'Save for Later' button on first cart item."""
        print("💾 Saving item for later...")
        self.click_element(self.save_for_later_button)
        self.page.wait_for_timeout(1500)  # Wait for animation
    
    def click_move_to_cart_from_saved(self) -> None:
        """Click 'Move to Cart' button on first saved item."""
        print("🛒 Moving saved item to cart...")
        self.click_element(self.move_to_cart_button)
        self.page.wait_for_timeout(1500)
    
    def click_move_all_to_cart(self) -> None:
        """Click 'Move All to Cart' button."""
        print("🛒 Moving all saved items to cart...")
        self.click_element(self.move_all_to_cart_button)
        self.page.wait_for_timeout(2000)
    
    def remove_all_saved_for_later(self) -> None:
        """Remove all items from Saved for Later."""
        print("🗑️ Removing all saved items...")
        while True:
            remove_buttons = self.page.locator(self.remove_from_saved_button).all()
            
            if not remove_buttons or len(remove_buttons) == 0:
                break
            
            remove_buttons[0].click()
            self.page.wait_for_timeout(1000)
        print("✅ Saved items cleared")
    
    def get_saved_for_later_count(self) -> int:
        """
        Get number of items in Saved for Later.
        
        Returns:
            int: Number of saved items
        """
        return self.page.locator(self.saved_for_later_items).count()
    
    def verify_one_item_moved_to_saved_for_later(self) -> bool:
        """
        Verify that at least one item is in Saved for Later section.
        
        Returns:
            bool: True if Saved for Later has items
        """
        # Wait for section to appear
        self.page.wait_for_timeout(1000)
        
        # Check if Saved for Later section is visible
        if not self.is_visible(self.saved_for_later_section):
            return False
        
        # Check if it has items
        saved_count = self.get_saved_for_later_count()
        return saved_count > 0
    
    def verify_saved_for_later_empty(self) -> bool:
        """
        Verify Saved for Later section is empty.
        
        Returns:
            bool: True if empty
        """
        # Check for empty message or zero items
        has_empty_message = self.is_visible(self.saved_for_later_empty_message)
        item_count = self.get_saved_for_later_count()
        
        return has_empty_message or item_count == 0
    
    # ==================== Cart Summary ====================
    
    def get_cart_subtotal(self) -> str:
        """Get cart subtotal."""
        return self.get_text(self.summary_subtotal)
    
    def get_cart_total(self) -> str:
        """Get cart total."""
        return self.get_text(self.summary_total)
    
    def verify_shopping_cart_displayed(self) -> bool:
        """Verify Shopping Cart page is displayed."""
        return self.is_visible(self.shopping_cart_title)
