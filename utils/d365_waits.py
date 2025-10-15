"""
D365 Busy Watcher Utility
Handles D365-specific loading states and busy indicators.
"""
from playwright.sync_api import Page
import time
import contextlib

# D365-specific busy selectors
BUSY_SELECTORS = [
    "text=/Please wait.*processing your request/i",
    "[aria-busy='true']",
    ".ax-busy-indicator",
    ".loadingMask",
    ".modalBackground",
    ".ms-Spinner",
    ".ms-Dialog-main",  # Modal dialogs
]


class BusyWatcher:
    """
    Watches for D365 busy states and waits until page is idle.
    
    Usage:
        guard = BusyWatcher(page)
        page.click("button")
        guard.wait_until_idle()  # Waits for D365 to finish loading
    """
    
    def __init__(self, page: Page):
        """
        Initialize the busy watcher.
        
        Args:
            page: Playwright Page object
        """
        self.page = page
        self._inflight = 0
        
        # Track network requests
        page.on("request", lambda _: self._bump(1))
        page.on("requestfinished", lambda _: self._bump(-1))
        page.on("requestfailed", lambda _: self._bump(-1))
    
    def _bump(self, delta: int):
        """Update the count of in-flight requests."""
        self._inflight = max(0, self._inflight + delta)
    
    def _busy_visible(self) -> bool:
        """Check if any busy indicators are visible."""
        for sel in BUSY_SELECTORS:
            with contextlib.suppress(Exception):
                if self.page.locator(sel).first.is_visible():
                    return True
        return False
    
    def wait_until_idle(self, timeout: float = 60):
        """
        Wait until D365 is idle (no busy indicators, no pending requests).
        
        Args:
            timeout: Maximum time to wait in seconds (default: 60)
            
        Raises:
            TimeoutError: If D365 stays busy longer than timeout
        """
        start = time.time()
        
        while time.time() - start < timeout:
            # Check if page is idle
            if not self._busy_visible() and self._inflight == 0:
                # Wait a bit to ensure it stays idle (quiet window)
                time.sleep(0.5)
                
                # Double check it's still idle
                if not self._busy_visible() and self._inflight == 0:
                    return
            
            # Still busy, wait a bit and check again
            time.sleep(0.2)
        
        raise TimeoutError(
            f"D365 stayed busy for more than {timeout} seconds. "
            f"Still has {self._inflight} pending requests."
        )
    
    def wait_for_navigation(self, timeout: float = 60):
        """
        Wait for navigation to complete (includes waiting until idle).
        
        Args:
            timeout: Maximum time to wait in seconds (default: 60)
        """
        self.page.wait_for_load_state("networkidle", timeout=timeout * 1000)
        self.wait_until_idle(timeout=timeout)
