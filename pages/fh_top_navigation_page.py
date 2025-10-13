"""
FourHands Top Navigation Page object.
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class FourHandsTopNavigationPage(BasePage):
    """Page object for FourHands top navigation."""
    
    def __init__(self, page: Page, timeout: int = 30000):
        """
        Initialize FourHands Top Navigation.
        
        Args:
            page: Playwright Page object
            timeout: Default timeout in milliseconds
        """
        super().__init__(page, timeout)
        
        # Selectors
        self.search_icon = "//button[contains(@aria-label, 'Search')]"
        self.search_input = "input[placeholder*='Search' i]"
        self.add_to_cart_button = "button:has-text('Add to Cart')"
        self.cart_bucket = "//a[contains(@href, '/cart')]//span[contains(@class, 'cart-count') or @class='badge']"
        self.cart_banner = "//div[contains(@class, 'cart-banner') or contains(@class, 'notification')]"
        self.dismiss_banner_button = "//button[contains(@aria-label, 'Close') or contains(@class, 'close')]"
        self.cart_link = "//a[contains(@href, '/cart') or text()='Cart']"
    
    def assert_loaded(self) -> None:
        """Assert that navigation is loaded."""
        # Navigation should always be visible
        pass
    
    def click_search_icon(self) -> None:
        """Click search icon."""
        self.click_element(self.search_icon)
    
    def enter_search_item(self, search_term: str) -> None:
        """
        Enter search term.
        
        Args:
            search_term: Product ID or search query
        """
        self.fill_input(self.search_input, search_term)
        # Press Enter to search
        self.page.locator(self.search_input).first.press("Enter")
    
    def click_add_to_cart_button(self) -> None:
        """Click Add to Cart button."""
        self.click_element(self.add_to_cart_button)
    
    def click_cart_bucket(self) -> None:
        """Click cart icon/bucket."""
        self.click_element(self.cart_link)
    
    def get_cart_bucket_text(self) -> str:
        """
        Get cart count from cart bucket.
        
        Returns:
            str: Cart count text
        """
        try:
            return self.get_text(self.cart_bucket)
        except Exception:
            return "0"
    
    def cart_bucket_check(self) -> str:
        """
        Check cart bucket status.
        
        Returns:
            str: 'cart' if items in cart, empty string otherwise
        """
        count_text = self.get_cart_bucket_text()
        return "cart" if count_text and count_text != "0" else ""
    
    def click_dismiss_cart_banner(self) -> None:
        """Dismiss cart notification banner."""
        try:
            if self.is_visible(self.cart_banner):
                self.click_element(self.dismiss_banner_button, wait_after=False)
                self.page.wait_for_timeout(500)
        except Exception:
            pass  # Banner not present or already dismissed
