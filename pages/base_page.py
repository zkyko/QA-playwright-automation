"""
Base page class providing shared functionality for all page objects.
"""
from typing import Optional
from playwright.sync_api import Page, FrameLocator, expect
from utils.waits import WaitConditions


class BasePage:
    """Base page class with common functionality."""
    
    def __init__(self, page: Page, timeout: int = 30000):
        """
        Initialize base page.
        
        Args:
            page: Playwright Page object
            timeout: Default timeout in milliseconds
        """
        self.page = page
        self.timeout = timeout
        self.waits = WaitConditions(page, timeout)
    
    def assert_loaded(self) -> None:
        """
        Assert that the page is loaded.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement assert_loaded()")
    
    def navigate(self, url: str) -> None:
        """
        Navigate to a URL.
        
        Args:
            url: URL to navigate to
        """
        self.page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")
    
    def wait_for_element_visible(
        self, 
        selector: str, 
        frame: Optional[FrameLocator] = None
    ) -> None:
        """
        Wait for element to be visible.
        
        Args:
            selector: Element selector
            frame: Optional frame to search in
        """
        context = frame if frame else self.page
        context.locator(selector).first.wait_for(state="visible", timeout=self.timeout)
    
    def click_element(
        self, 
        selector: str, 
        frame: Optional[FrameLocator] = None,
        wait_after: bool = True
    ) -> None:
        """
        Click an element with optional waiting.
        
        Args:
            selector: Element selector
            frame: Optional frame containing the element
            wait_after: Whether to wait for loading after click
        """
        context = frame if frame else self.page
        element = context.locator(selector).first
        element.wait_for(state="visible", timeout=self.timeout)
        element.click()
        
        if wait_after:
            self.waits.wait_for_no_loading_mask(frame)
            self.waits.wait_for_no_spinner(frame)
    
    def fill_input(
        self, 
        selector: str, 
        value: str, 
        frame: Optional[FrameLocator] = None,
        clear_first: bool = True
    ) -> None:
        """
        Fill an input field.
        
        Args:
            selector: Input selector
            value: Value to fill
            frame: Optional frame containing the input
            clear_first: Whether to clear existing value first
        """
        context = frame if frame else self.page
        element = context.locator(selector).first
        element.wait_for(state="visible", timeout=self.timeout)
        
        if clear_first:
            element.clear()
        
        element.fill(value)
    
    def get_text(self, selector: str, frame: Optional[FrameLocator] = None) -> str:
        """
        Get text content of an element.
        
        Args:
            selector: Element selector
            frame: Optional frame containing the element
            
        Returns:
            str: Element text content
        """
        context = frame if frame else self.page
        element = context.locator(selector).first
        element.wait_for(state="visible", timeout=self.timeout)
        return element.inner_text()
    
    def is_visible(self, selector: str, frame: Optional[FrameLocator] = None) -> bool:
        """
        Check if element is visible.
        
        Args:
            selector: Element selector
            frame: Optional frame containing the element
            
        Returns:
            bool: True if visible, False otherwise
        """
        context = frame if frame else self.page
        try:
            element = context.locator(selector).first
            return element.is_visible()
        except Exception:
            return False
    
    def wait_for_url_contains(self, text: str) -> None:
        """
        Wait until URL contains specific text.
        
        Args:
            text: Text to search for in URL
        """
        self.waits.wait_for_url_contains(text, self.timeout)
    
    def assert_element_visible(
        self, 
        selector: str, 
        frame: Optional[FrameLocator] = None,
        message: Optional[str] = None
    ) -> None:
        """
        Assert that element is visible.
        
        Args:
            selector: Element selector
            frame: Optional frame containing the element
            message: Optional assertion message
        """
        context = frame if frame else self.page
        element = context.locator(selector).first
        
        if message:
            expect(element).to_be_visible(timeout=self.timeout)
        else:
            expect(element).to_be_visible(timeout=self.timeout)
    
    def assert_text_contains(
        self, 
        selector: str, 
        expected_text: str, 
        frame: Optional[FrameLocator] = None
    ) -> None:
        """
        Assert that element contains specific text.
        
        Args:
            selector: Element selector
            expected_text: Expected text content
            frame: Optional frame containing the element
        """
        context = frame if frame else self.page
        element = context.locator(selector).first
        expect(element).to_contain_text(expected_text, timeout=self.timeout)
    
    def take_screenshot(self, name: str) -> bytes:
        """
        Take a screenshot.
        
        Args:
            name: Screenshot name/path
            
        Returns:
            bytes: Screenshot data
        """
        return self.page.screenshot(path=name, full_page=True)
    
    def get_current_url(self) -> str:
        """
        Get current page URL.
        
        Returns:
            str: Current URL
        """
        return self.page.url
