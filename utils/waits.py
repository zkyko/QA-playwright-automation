"""
Condition-based wait utilities for D365 F&O automation.
Provides resilient waiting mechanisms without using sleep.
"""
from typing import Callable, Optional, Any
from playwright.sync_api import Page, FrameLocator, expect
import time


class WaitConditions:
    """Collection of reusable wait conditions for D365."""
    
    # Common D365 selectors
    LOADING_MASK = ".blockUI, .ms-Spinner, [data-dyn-role='LoadingMask']"
    LOADING_SPINNER = ".ms-Spinner, [data-dyn-role='Spinner']"
    GRID_CONTAINER = "[data-dyn-role='Grid'], .grid-container"
    GRID_ROW = "[data-dyn-role='Row'], .grid-row"
    TOAST_NOTIFICATION = "[data-dyn-role='Toast'], .ms-MessageBar"
    DIALOG_CONTAINER = "[data-dyn-role='Dialog'], .ms-Dialog"
    
    def __init__(self, page: Page, timeout: int = 30000):
        """
        Initialize wait conditions.
        
        Args:
            page: Playwright Page object
            timeout: Default timeout in milliseconds
        """
        self.page = page
        self.timeout = timeout
    
    def wait_for_no_loading_mask(self, frame: Optional[FrameLocator] = None) -> None:
        """
        Wait until loading masks/overlays are gone.
        
        Args:
            frame: Optional frame to search in; uses page if None
        """
        context = frame if frame else self.page
        
        try:
            # Wait for loading mask to appear and then disappear
            mask = context.locator(self.LOADING_MASK)
            if mask.count() > 0:
                mask.first.wait_for(state="hidden", timeout=self.timeout)
        except Exception:
            # If mask never appears, that's fine
            pass
    
    def wait_for_no_spinner(self, frame: Optional[FrameLocator] = None) -> None:
        """
        Wait until loading spinners are gone.
        
        Args:
            frame: Optional frame to search in
        """
        context = frame if frame else self.page
        
        try:
            spinner = context.locator(self.LOADING_SPINNER)
            if spinner.count() > 0:
                spinner.first.wait_for(state="hidden", timeout=self.timeout)
        except Exception:
            pass
    
    def wait_for_grid_ready(self, frame: Optional[FrameLocator] = None) -> None:
        """
        Wait until grid is loaded and ready.
        
        Args:
            frame: Optional frame to search in
        """
        context = frame if frame else self.page
        
        # Wait for grid container to be visible
        grid = context.locator(self.GRID_CONTAINER).first
        grid.wait_for(state="visible", timeout=self.timeout)
        
        # Wait for at least one row to appear (or timeout if empty)
        try:
            context.locator(self.GRID_ROW).first.wait_for(
                state="visible", 
                timeout=5000
            )
        except Exception:
            # Grid might be empty, which is valid
            pass
        
        # Ensure no loading indicators
        self.wait_for_no_loading_mask(frame)
        self.wait_for_no_spinner(frame)
    
    def wait_for_toast_message(self, frame: Optional[FrameLocator] = None) -> str:
        """
        Wait for toast notification and return its text.
        
        Args:
            frame: Optional frame to search in
            
        Returns:
            str: Toast message text
        """
        context = frame if frame else self.page
        
        toast = context.locator(self.TOAST_NOTIFICATION).first
        toast.wait_for(state="visible", timeout=self.timeout)
        text = toast.inner_text()
        
        # Wait for toast to disappear
        try:
            toast.wait_for(state="hidden", timeout=10000)
        except Exception:
            pass
        
        return text
    
    def wait_for_url_contains(self, text: str, timeout: Optional[int] = None) -> None:
        """
        Wait until URL contains specific text.
        
        Args:
            text: Text to search for in URL
            timeout: Optional timeout override
        """
        timeout = timeout or self.timeout
        self.page.wait_for_url(f"**/*{text}*", timeout=timeout)
    
    def wait_for_url_stable(self, stable_duration_ms: int = 1000) -> None:
        """
        Wait until URL hasn't changed for specified duration.
        
        Args:
            stable_duration_ms: Duration in ms that URL must remain stable
        """
        last_url = self.page.url
        start_time = time.time() * 1000
        
        while (time.time() * 1000 - start_time) < stable_duration_ms:
            current_url = self.page.url
            if current_url != last_url:
                # URL changed, reset timer
                last_url = current_url
                start_time = time.time() * 1000
            time.sleep(0.1)
    
    def wait_for_network_idle(self, timeout: Optional[int] = None) -> None:
        """
        Wait for network to be idle (no pending requests).
        
        Args:
            timeout: Optional timeout override
        """
        timeout = timeout or self.timeout
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def wait_for_element_stable(
        self, 
        selector: str, 
        frame: Optional[FrameLocator] = None,
        stable_duration_ms: int = 500
    ) -> None:
        """
        Wait until element position hasn't changed for specified duration.
        Useful for waiting for animations/transitions to complete.
        
        Args:
            selector: Element selector
            frame: Optional frame to search in
            stable_duration_ms: Duration element must remain stable
        """
        context = frame if frame else self.page
        element = context.locator(selector).first
        
        # First ensure element is visible
        element.wait_for(state="visible", timeout=self.timeout)
        
        # Then wait for stability
        last_box = element.bounding_box()
        start_time = time.time() * 1000
        
        while (time.time() * 1000 - start_time) < stable_duration_ms:
            current_box = element.bounding_box()
            if current_box != last_box:
                # Position changed, reset timer
                last_box = current_box
                start_time = time.time() * 1000
            time.sleep(0.05)
    
    def wait_for_condition(
        self, 
        condition: Callable[[], bool], 
        timeout: Optional[int] = None,
        poll_interval_ms: int = 100
    ) -> None:
        """
        Wait until custom condition returns True.
        
        Args:
            condition: Callable that returns bool
            timeout: Optional timeout override in ms
            poll_interval_ms: Polling interval in ms
            
        Raises:
            TimeoutError: If condition not met within timeout
        """
        timeout = timeout or self.timeout
        start_time = time.time() * 1000
        
        while (time.time() * 1000 - start_time) < timeout:
            if condition():
                return
            time.sleep(poll_interval_ms / 1000)
        
        raise TimeoutError(f"Condition not met within {timeout}ms")
    
    def wait_for_dialog(self, frame: Optional[FrameLocator] = None) -> None:
        """
        Wait for dialog/modal to appear.
        
        Args:
            frame: Optional frame to search in
        """
        context = frame if frame else self.page
        dialog = context.locator(self.DIALOG_CONTAINER).first
        dialog.wait_for(state="visible", timeout=self.timeout)


def wait_for_grid_load_complete(
    page: Page, 
    frame: Optional[FrameLocator] = None,
    timeout: int = 30000
) -> None:
    """
    Comprehensive wait for grid to be fully loaded.
    Combines multiple wait conditions for reliability.
    
    Args:
        page: Playwright Page object
        frame: Optional frame containing the grid
        timeout: Timeout in milliseconds
    """
    waits = WaitConditions(page, timeout)
    
    waits.wait_for_no_loading_mask(frame)
    waits.wait_for_no_spinner(frame)
    waits.wait_for_grid_ready(frame)
    waits.wait_for_network_idle()


def wait_for_page_ready(
    page: Page,
    frame: Optional[FrameLocator] = None,
    timeout: int = 30000
) -> None:
    """
    Wait for page to be fully ready (no loading indicators, stable URL).
    
    Args:
        page: Playwright Page object
        frame: Optional frame to check
        timeout: Timeout in milliseconds
    """
    waits = WaitConditions(page, timeout)
    
    waits.wait_for_network_idle()
    waits.wait_for_no_loading_mask(frame)
    waits.wait_for_no_spinner(frame)
    waits.wait_for_url_stable()
