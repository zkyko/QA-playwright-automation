"""
FourHands Home Page object.
"""
from typing import Optional
from playwright.sync_api import Page
from pages.base_page import BasePage


class FourHandsHomePage(BasePage):
    """Page object for FourHands home page."""
    
    def __init__(self, page: Page, timeout: int = 30000):
        """
        Initialize FourHands Home page.
        
        Args:
            page: Playwright Page object
            timeout: Default timeout in milliseconds
        """
        super().__init__(page, timeout)
        
        # Selectors
        self.login_button = "//span[text()='Log In']/ancestor::a"
        self.search_icon = "//button[contains(@aria-label, 'Search')]"
        self.search_input = "input[placeholder*='Search' i]"
        self.cart_bucket = "//a[contains(@href, '/cart') or contains(@class, 'cart')]"
        self.logo = "//img[@alt='Four Hands' or contains(@src, 'fourhands')]"
    
    def assert_loaded(self) -> None:
        """Assert that home page is loaded."""
        # Check URL contains fourhands
        assert "fourhands" in self.page.url.lower(), \
            f"Not on FourHands page. Current URL: {self.page.url}"
        
        # Verify logo or key element is visible
        self.wait_for_element_visible(self.logo)
    
    def click_login_button(self) -> None:
        """Click the login button."""
        self.click_element(self.login_button)
    
    def click_search_icon(self) -> None:
        """Click the search icon."""
        self.click_element(self.search_icon)
    
    def enter_search_term(self, search_term: str) -> None:
        """
        Enter search term in search box.
        
        Args:
            search_term: Product ID or search query
        """
        self.fill_input(self.search_input, search_term)
        # Press Enter to search
        self.page.locator(self.search_input).first.press("Enter")
    
    def search_for_product(self, product_id: str) -> None:
        """
        Search for a product by ID.
        
        Args:
            product_id: Product ID to search for
        """
        self.click_search_icon()
        self.enter_search_term(product_id)
    
    def click_searched_item(self, product_id: str) -> None:
        """
        Click on a searched product.
        
        Args:
            product_id: Product ID to click on
        """
        product_link = f"//a[contains(@href, '{product_id}') or contains(text(), '{product_id}')]"
        self.click_element(product_link)
    
    def navigate_to_home(self, base_url: str) -> None:
        """
        Navigate to FourHands home page.
        
        Args:
            base_url: Base URL of FourHands site
        """
        self.navigate(base_url)
        self.assert_loaded()
