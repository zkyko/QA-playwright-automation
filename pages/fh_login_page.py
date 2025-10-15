"""
FourHands Login Page object.
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class FourHandsLoginPage(BasePage):
    """Page object for FourHands login."""
    
    def __init__(self, page: Page, timeout: int = 30000):
        """
        Initialize FourHands Login page.
        
        Args:
            page: Playwright Page object
            timeout: Default timeout in milliseconds
        """
        super().__init__(page, timeout)
        
        # Selectors (from Java code)
        self.username_input = "//input[@placeholder='Enter email or customer number']"
        self.password_input = "//input[@placeholder='Enter password']"
        self.continue_button = "//button[@type='submit' and text()='Continue']"
    
    def assert_loaded(self) -> None:
        """Assert that login page is loaded."""
        self.wait_for_element_visible(self.username_input)
        self.wait_for_element_visible(self.password_input)
    
    def enter_username(self, username: str) -> None:
        """
        Enter username.
        
        Args:
            username: Username or email
        """
        self.fill_input(self.username_input, username, clear_first=False)
    
    def enter_password(self, password: str) -> None:
        """
        Enter password.
        
        Args:
            password: Password
        """
        self.fill_input(self.password_input, password, clear_first=False)
    
    def click_continue(self) -> None:
        """Click continue/login button."""
        self.click_element(self.continue_button)
    
    def login(self, username: str, password: str) -> None:
        """
        Perform login with credentials.
        
        Args:
            username: Username or email
            password: Password
        """
        self.assert_loaded()
        self.enter_username(username)
        self.enter_password(password)
        self.click_continue()
        
        # Wait for navigation after login
        self.page.wait_for_load_state("networkidle", timeout=self.timeout)
