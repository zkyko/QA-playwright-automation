"""
FourHands authentication tests.
Record and manage FourHands authentication sessions.

Usage:
    pytest tests/fh/test_fh_auth.py -k "record" -s --headed
"""
import pytest
from playwright.sync_api import Page
from pathlib import Path

from pages.fh_home_page import FourHandsHomePage
from pages.fh_login_page import FourHandsLoginPage


@pytest.mark.record
@pytest.mark.fourhands
def test_record_fh_authentication(page: Page):
    """
    Record FourHands authentication session.
    
    This test:
    1. Opens FourHands homepage
    2. Clicks login
    3. Enters credentials from environment
    4. Saves authenticated session
    """
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    base_url = os.getenv("FH_BASE_URL")
    username = os.getenv("FH_USERNAME")
    password = os.getenv("FH_PASSWORD")
    storage_path = Path("storage_state/fh_session.json")
    
    if not base_url or not username or not password:
        pytest.skip("FourHands credentials not configured in .env")
    
    print("\n" + "="*70)
    print("FOURHANDS AUTHENTICATION RECORDING")
    print("="*70)
    print(f"URL: {base_url}")
    print(f"Username: {username}")
    print(f"Storage Path: {storage_path}")
    print("="*70 + "\n")
    
    # Navigate to home
    home_page = FourHandsHomePage(page)
    home_page.navigate_to_home(base_url)
    
    # Click login
    home_page.click_login_button()
    
    # Perform login
    login_page = FourHandsLoginPage(page)
    login_page.login(username, password)
    
    # Wait for login to complete
    page.wait_for_load_state("networkidle", timeout=30000)
    
    # Verify logged in
    assert "fourhands" in page.url.lower(), \
        f"Login may have failed. Current URL: {page.url}"
    
    print(f"\n✓ Successfully authenticated. Current URL: {page.url}")
    
    # Save storage state
    print(f"\nSaving storage state to: {storage_path}")
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    page.context.storage_state(path=str(storage_path))
    
    print("✓ Storage state saved successfully!")
    print("\nYou can now run FourHands tests without re-authenticating.")
    print("="*70 + "\n")


@pytest.mark.record
@pytest.mark.fourhands
def test_verify_fh_storage_state():
    """Verify FourHands storage state file exists and is valid."""
    storage_path = Path("storage_state/fh_session.json")
    
    assert storage_path.exists(), \
        f"Storage state file not found at {storage_path}"
    
    assert storage_path.stat().st_size > 0, \
        "Storage state file exists but is empty"
    
    # Try to read and parse as JSON
    import json
    with open(storage_path, 'r') as f:
        state_data = json.load(f)
    
    assert "cookies" in state_data, "Storage state missing cookies"
    assert "origins" in state_data, "Storage state missing origins"
    
    print(f"\n✓ FourHands storage state is valid")
    print(f"  - Cookies: {len(state_data.get('cookies', []))}")
    print(f"  - Origins: {len(state_data.get('origins', []))}")
