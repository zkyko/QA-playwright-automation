"""
D365 Authentication Helper for BrowserStack

Handles login flow programmatically so tests can run on BrowserStack.
"""
import os
from playwright.sync_api import Page
from pathlib import Path


class D365Auth:
    """Handle D365 authentication for both local and BrowserStack."""
    
    def __init__(self, page: Page):
        self.page = page
        self.d365_url = "https://fourhands-test.sandbox.operations.dynamics.com/?cmp=FH&mi=DefaultDashboard"
    
    def is_browserstack(self) -> bool:
        """Check if running on BrowserStack."""
        return os.getenv("BROWSERSTACK_USERNAME") is not None
    
    def has_local_storage_state(self) -> bool:
        """Check if local storage state exists."""
        storage_path = Path("storage_state/d365_session.json")
        return storage_path.exists()
    
    def login(self, username: str = None, password: str = None):
        """
        Perform D365 login programmatically.
        
        Args:
            username: D365 username (from env if not provided)
            password: D365 password (from env if not provided)
        """
        # Get credentials from environment if not provided
        username = username or os.getenv("D365_USERNAME")
        password = password or os.getenv("D365_PASSWORD")
        
        if not username or not password:
            raise ValueError(
                "D365 credentials not found. Set D365_USERNAME and D365_PASSWORD environment variables."
            )
        
        print(f"\n🔐 Logging into D365 as: {username}")
        
        # Navigate to D365
        self.page.goto(self.d365_url)
        
        # Wait for Microsoft login page
        print("⏳ Waiting for Microsoft login page...")
        self.page.wait_for_load_state("networkidle")
        
        # Check if already logged in
        if "dynamics.com" in self.page.url and "login" not in self.page.url.lower():
            print("✅ Already logged in!")
            return
        
        # Enter email
        print("📧 Entering email...")
        email_input = self.page.wait_for_selector("input[type='email']", timeout=10000)
        email_input.fill(username)
        email_input.press("Enter")
        
        # Wait for password page
        self.page.wait_for_load_state("networkidle")
        
        # Enter password
        print("🔑 Entering password...")
        password_input = self.page.wait_for_selector("input[type='password']", timeout=10000)
        password_input.fill(password)
        password_input.press("Enter")
        
        # Handle "Stay signed in?" prompt
        print("⏳ Handling post-login prompts...")
        try:
            # Click "Yes" or "No" on "Stay signed in?"
            stay_signed_in = self.page.wait_for_selector("input[type='submit']", timeout=5000)
            stay_signed_in.click()
        except:
            print("   No 'Stay signed in' prompt")
        
        # Wait for D365 to load
        print("⏳ Waiting for D365 dashboard...")
        self.page.wait_for_url("**/dynamics.com/**", timeout=60000)
        self.page.wait_for_load_state("networkidle")
        
        print("✅ Successfully logged into D365!")
    
    def ensure_authenticated(self):
        """
        Ensure user is authenticated.
        Uses local storage if available, otherwise performs login.
        """
        # Navigate to D365
        self.page.goto(self.d365_url)
        self.page.wait_for_load_state("networkidle")
        
        # Check if we're on login page
        if "login" in self.page.url.lower() or "microsoft" in self.page.url.lower():
            print("🔓 Not authenticated. Logging in...")
            self.login()
        else:
            print("✅ Already authenticated!")


class FourHandsAuth:
    """Handle FourHands authentication for BrowserStack."""
    
    def __init__(self, page: Page):
        self.page = page
        self.fh_url = "https://fh-test-fourhandscom.azurewebsites.net"
    
    def login(self, username: str = None, password: str = None):
        """
        Perform FourHands login programmatically.
        
        Args:
            username: FH username (from env if not provided)
            password: FH password (from env if not provided)
        """
        # Get credentials from environment if not provided
        username = username or os.getenv("FH_USERNAME")
        password = password or os.getenv("FH_PASSWORD")
        
        if not username or not password:
            raise ValueError(
                "FourHands credentials not found. Set FH_USERNAME and FH_PASSWORD environment variables."
            )
        
        print(f"\n🔐 Logging into FourHands as: {username}")
        
        # Navigate to FourHands
        self.page.goto(self.fh_url)
        self.page.wait_for_load_state("networkidle")
        
        # Check if already logged in (look for account icon or logout button)
        if self.is_logged_in():
            print("✅ Already logged in!")
            return
        
        # Click login button
        print("🖱️  Clicking login button...")
        login_button = self.page.wait_for_selector("text=Log In", timeout=10000)
        login_button.click()
        
        # Wait for Microsoft login page
        self.page.wait_for_load_state("networkidle")
        
        # Enter email
        print("📧 Entering email...")
        email_input = self.page.wait_for_selector("input[type='email']", timeout=10000)
        email_input.fill(username)
        email_input.press("Enter")
        
        # Wait for password page
        self.page.wait_for_load_state("networkidle")
        
        # Enter password
        print("🔑 Entering password...")
        password_input = self.page.wait_for_selector("input[type='password']", timeout=10000)
        password_input.fill(password)
        password_input.press("Enter")
        
        # Handle "Stay signed in?" prompt
        print("⏳ Handling post-login prompts...")
        try:
            stay_signed_in = self.page.wait_for_selector("input[type='submit']", timeout=5000)
            stay_signed_in.click()
        except:
            print("   No 'Stay signed in' prompt")
        
        # Wait for FourHands to load
        print("⏳ Waiting for FourHands to load...")
        self.page.wait_for_url(f"{self.fh_url}/**", timeout=30000)
        self.page.wait_for_load_state("networkidle")
        
        print("✅ Successfully logged into FourHands!")
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        # Look for logout button or user account icon
        logout_exists = self.page.locator("text=Log Out").count() > 0
        account_exists = self.page.locator("[aria-label*='Account']").count() > 0
        
        return logout_exists or account_exists
    
    def ensure_authenticated(self):
        """Ensure user is authenticated."""
        self.page.goto(self.fh_url)
        self.page.wait_for_load_state("networkidle")
        
        if not self.is_logged_in():
            print("🔓 Not authenticated. Logging in...")
            self.login()
        else:
            print("✅ Already authenticated!")
