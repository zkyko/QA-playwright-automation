"""
Conftest for D365 tests with BrowserStack support.
"""
import pytest
from playwright.sync_api import Page, BrowserContext
from pathlib import Path
import os


def is_browserstack():
    """Check if running on BrowserStack."""
    # Only return True if actually running through BrowserStack SDK
    return os.getenv("BROWSERSTACK_BUILD_NAME") is not None or os.getenv("BROWSERSTACK_LOCAL") is not None


@pytest.fixture
def d365_authenticated_context(playwright_browser):
    """
    Provide D365 authenticated context.
    
    - Locally: Uses storage state (faster)
    - BrowserStack: Uses programmatic login (works on cloud)
    """
    storage_path = Path("storage_state/d365_session.json")
    
    # On BrowserStack, create fresh context (will login programmatically)
    if is_browserstack():
        print("\n🌐 Running on BrowserStack - will login programmatically")
        context = playwright_browser.new_context()
    # Locally, use storage state if available
    elif storage_path.exists():
        print("\n💾 Using local storage state")
        context = playwright_browser.new_context(storage_state=str(storage_path))
    else:
        print("\n⚠️  No storage state found - will need to login")
        context = playwright_browser.new_context()
    
    yield context
    context.close()


@pytest.fixture
def d365_authenticated_page(d365_authenticated_context):
    """
    Provide authenticated D365 page.
    
    Automatically handles login if needed.
    """
    from utils.auth_helper import D365Auth
    
    page = d365_authenticated_context.new_page()
    
    # On BrowserStack or when no storage state, login programmatically
    if is_browserstack() or not Path("storage_state/d365_session.json").exists():
        auth = D365Auth(page)
        
        # Get credentials from environment
        username = os.getenv("D365_USERNAME")
        password = os.getenv("D365_PASSWORD")
        
        if username and password:
            try:
                auth.login(username, password)
            except Exception as e:
                print(f"⚠️  Login failed: {e}")
                print("   Tests requiring authentication will be skipped")
        else:
            print("⚠️  D365_USERNAME and D365_PASSWORD not set")
            print("   Set these environment variables to run authenticated tests on BrowserStack")
    
    yield page
    page.close()
