"""
D365 Authentication Recording Test
Run this to save D365 authentication session.
"""
import pytest
from playwright.sync_api import Page
from pathlib import Path
import json


pytestmark = pytest.mark.record


@pytest.mark.record
def test_record_d365_authentication(page: Page):
    """
    Record D365 authentication session.
    
    IMPORTANT: Run this test manually with headed mode:
        pytest tests/d365/test_d365_auth.py -k record --headed -s
    
    Steps:
        1. Navigate to D365
        2. Login manually
        3. Wait for dashboard to load
        4. Session is saved automatically
    """
    storage_path = Path("storage_state/d365_session.json")
    
    print("\n" + "="*70)
    print("D365 AUTHENTICATION RECORDING")
    print("="*70)
    print(f"URL: https://fourhands-test.sandbox.operations.dynamics.com")
    print(f"Storage Path: {storage_path}")
    print("="*70)
    print("\n⏳ Please login manually in the browser...")
    print("   1. Enter your credentials")
    print("   2. Complete any 2FA if required")
    print("   3. Wait for dashboard to load")
    print("   4. Test will auto-save and continue\n")
    
    # Navigate to D365
    page.goto("https://fourhands-test.sandbox.operations.dynamics.com/?cmp=FH&mi=DefaultDashboard")
    
    # Wait for authentication - looking for D365 dashboard elements
    try:
        # Wait for navigation pane (indicates successful login)
        page.wait_for_selector("button[aria-label*='navigation']", timeout=120000)
        print("✅ Successfully authenticated. Dashboard loaded!")
        
    except Exception as e:
        pytest.fail(f"Authentication timeout. Please login within 2 minutes. Error: {e}")
    
    # Get current URL to verify we're authenticated
    current_url = page.url
    print(f"\n✓ Successfully authenticated. Current URL: {current_url}")
    
    # Save storage state
    print(f"\nSaving storage state to: {storage_path}")
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save with context
    page.context.storage_state(path=str(storage_path))
    
    print("✓ Storage state saved successfully!")
    print("\nYou can now run D365 tests without re-authenticating.")
    print("="*70)
    
    # Verify the saved file
    assert storage_path.exists(), "Storage state file was not created"
    
    # Verify it has cookies
    with open(storage_path, 'r') as f:
        state = json.load(f)
        cookie_count = len(state.get('cookies', []))
        print(f"\n✓ Saved {cookie_count} cookies")
        
        assert cookie_count > 0, "No cookies were saved"


@pytest.mark.smoke
def test_verify_d365_storage_state():
    """
    Verify D365 storage state exists and is valid.
    
    This test runs quickly to check if authentication is set up.
    """
    storage_path = Path("storage_state/d365_session.json")
    
    assert storage_path.exists(), \
        f"Storage state file not found at {storage_path}. Run: pytest tests/d365/test_d365_auth.py -k record --headed"
    
    # Verify file contents
    with open(storage_path, 'r') as f:
        state = json.load(f)
    
    cookies = state.get('cookies', [])
    origins = state.get('origins', [])
    
    assert len(cookies) > 0, "Storage state has no cookies"
    
    print(f"\n✓ D365 storage state is valid")
    print(f"  - Cookies: {len(cookies)}")
    print(f"  - Origins: {len(origins)}")
