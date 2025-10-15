"""
FourHands test fixtures and configuration.
"""
import pytest
from playwright.sync_api import Page, BrowserContext
from pathlib import Path
from configs.playwright_config import get_context_options


@pytest.fixture
def fh_test_product() -> str:
    """
    Provide a test product ID for FourHands tests.
    
    Returns:
        str: Product SKU/ID
    """
    return "108422-001"  # Default test product


@pytest.fixture
def fh_test_products() -> list:
    """
    Provide multiple test product IDs.
    
    Returns:
        list: List of product SKUs
    """
    return ["108422-001", "108422-002", "000022-"]


@pytest.fixture(scope="session")
def fh_storage_state_path() -> Path:
    """
    Provide FourHands storage state path.
    
    Returns:
        Path: Path to FH auth storage
    """
    return Path("storage_state/fh_auth.json")


@pytest.fixture
def fh_authenticated_context(playwright_browser, fh_storage_state_path) -> BrowserContext:
    """
    Provide authenticated FourHands context.
    
    Args:
        playwright_browser: Browser instance from conftest
        fh_storage_state_path: Path to auth storage
        
    Yields:
        BrowserContext: Authenticated context
    """
    if not fh_storage_state_path.exists():
        pytest.skip(f"FH auth not found at {fh_storage_state_path}. Run scripts/save_fh_auth.py")
    
    context_options = get_context_options()
    context_options['storage_state'] = str(fh_storage_state_path)
    
    # Add video recording
    context_options['record_video_dir'] = 'test-results/videos'
    context_options['record_video_size'] = {"width": 1920, "height": 1080}
    
    context = playwright_browser.new_context(**context_options)
    
    # Enable tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield context
    
    # Save trace
    from datetime import datetime
    trace_path = f"test-results/traces/fh-trace-{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    Path("test-results/traces").mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=trace_path)
    
    context.close()


@pytest.fixture
def fh_authenticated_page(fh_authenticated_context: BrowserContext) -> Page:
    """
    Provide authenticated FourHands page.
    
    Args:
        fh_authenticated_context: Authenticated context
        
    Yields:
        Page: Authenticated page
    """
    page = fh_authenticated_context.new_page()
    
    # Navigate to FourHands
    page.goto("https://fh-test-fourhandscom.azurewebsites.net/")
    
    yield page
    
    page.close()
