"""
D365 Base Page - Parent class for all D365 page objects.
"""
from playwright.sync_api import Page
from utils.d365_waits import BusyWatcher


class D365BasePage:
    """Base page object for D365 pages."""
    
    def __init__(self, page: Page):
        """
        Initialize D365 base page.
        
        Args:
            page: Playwright Page object
        """
        self.page = page
        self.guard = BusyWatcher(page)
    
    def navigate_to(self, url: str):
        """Navigate to URL and wait until idle."""
        self.page.goto(url)
        self.guard.wait_until_idle()
    
    def click_and_wait(self, selector: str):
        """Click element and wait for D365 to be idle."""
        self.page.locator(selector).click()
        self.guard.wait_until_idle()
    
    def fill_and_wait(self, selector: str, text: str):
        """Fill input and wait for D365 to be idle."""
        self.page.locator(selector).fill(text)
        self.guard.wait_until_idle()
    
    def select_and_wait(self, selector: str):
        """Select element and wait for D365 to be idle."""
        self.page.locator(selector).click()
        self.guard.wait_until_idle()
