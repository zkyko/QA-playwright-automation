"""
FourHands Product Detail Page (PDP) object.
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class FourHandsProductDetailPage(BasePage):
    """Page object for FourHands Product Detail Page."""
    
    def __init__(self, page: Page, timeout: int = 30000):
        """
        Initialize FourHands PDP.
        
        Args:
            page: Playwright Page object
            timeout: Default timeout in milliseconds
        """
        super().__init__(page, timeout)
        
        # Selectors
        self.add_to_cart_button = "button:has-text('Add to Cart')"
        self.quantity_input = "//input[@type='number' or contains(@class, 'quantity')]"
        self.increment_button = "//button[contains(@aria-label, 'Increase') or contains(@class, 'increment')]"
        self.decrement_button = "//button[contains(@aria-label, 'Decrease') or contains(@class, 'decrement')]"
        self.product_title = "h1"
        self.product_price = "text=/\$\d+/"
        self.availability_message = "//div[contains(@class, 'availability') or contains(text(), 'Available') or contains(text(), 'Arriving')]"
    
    def assert_loaded(self) -> None:
        """Assert that PDP is loaded."""
        # Wait for key elements
        self.wait_for_element_visible(self.product_title)
        self.wait_for_element_visible(self.add_to_cart_button)
    
    def navigate_to_product(self, product_id: str) -> None:
        """
        Navigate directly to a product detail page.
        
        Args:
            product_id: Product SKU/ID
        """
        base_url = self.page.context.browser.options.get('base_url', 'https://fh-test-fourhandscom.azurewebsites.net')
        product_url = f"{base_url}/product/{product_id}"
        self.page.goto(product_url)
        self.assert_loaded()
    
    def click_add_to_cart(self) -> None:
        """Click Add to Cart button."""
        self.click_element(self.add_to_cart_button)
    
    def get_quantity(self) -> int:
        """
        Get current quantity value.
        
        Returns:
            int: Current quantity
        """
        quantity_text = self.get_text(self.quantity_input)
        return int(quantity_text) if quantity_text else 1
    
    def click_increment_button(self, num_clicks: int = 1) -> None:
        """
        Click increment button specified number of times.
        
        Args:
            num_clicks: Number of times to click increment
        """
        for _ in range(num_clicks):
            self.click_element(self.increment_button, wait_after=False)
            self.page.wait_for_timeout(300)  # Small wait between clicks
    
    def click_decrement_button(self, num_clicks: int = 1) -> None:
        """
        Click decrement button specified number of times.
        
        Args:
            num_clicks: Number of times to click decrement
        """
        for _ in range(num_clicks):
            self.click_element(self.decrement_button, wait_after=False)
            self.page.wait_for_timeout(300)
    
    def set_quantity(self, quantity: int) -> None:
        """
        Set product quantity.
        
        Args:
            quantity: Desired quantity
        """
        self.fill_input(self.quantity_input, str(quantity))
    
    def get_product_title(self) -> str:
        """
        Get product title.
        
        Returns:
            str: Product title
        """
        return self.get_text(self.product_title)
    
    def get_product_price(self) -> str:
        """
        Get product price.
        
        Returns:
            str: Product price
        """
        return self.get_text(self.product_price)
    
    def get_availability_message(self) -> str:
        """
        Get availability/ATP message.
        
        Returns:
            str: Availability message
        """
        try:
            return self.get_text(self.availability_message)
        except Exception:
            return "N/A"
    
    def is_add_to_cart_enabled(self) -> bool:
        """
        Check if Add to Cart button is enabled.
        
        Returns:
            bool: True if enabled, False otherwise
        """
        try:
            button = self.page.locator(self.add_to_cart_button).first
            return button.is_enabled()
        except Exception:
            return False
