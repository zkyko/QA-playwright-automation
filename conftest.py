"""
Enhanced conftest.py with Allure screenshots, videos, and attachments.
This makes Allure reports more like BrowserStack with visual debugging.
"""
import pytest
import allure
from playwright.sync_api import Browser, BrowserContext, Page, Playwright
from pathlib import Path
from typing import Generator
import os
from datetime import datetime

from configs.playwright_config import (
    get_browser_launch_options,
    get_context_options,
    get_storage_state_path,
    D365_BASE_URL,
    HEADED,
    TIMEOUT
)
from configs.browserstack_config import (
    is_browserstack_enabled,
    get_cdp_url,
    get_browserstack_context_options
)
from utils.env import get_env


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test (quick validation)"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as end-to-end test (comprehensive)"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "record: mark test for recording auth storage state"
    )
    config.addinivalue_line(
        "markers", "quarantine: mark test as quarantined (known flake)"
    )
    config.addinivalue_line(
        "markers", "finance: mark test as finance module test"
    )
    config.addinivalue_line(
        "markers", "warehouse: mark test as warehouse module test"
    )
    config.addinivalue_line(
        "markers", "fourhands: mark test as FourHands webapp test"
    )


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Provide browser launch arguments."""
    return get_browser_launch_options()


@pytest.fixture(scope="session")
def browser_context_args():
    """Provide browser context arguments with video recording."""
    if is_browserstack_enabled():
        return get_browserstack_context_options()
    
    # Enhanced context options with video recording for Allure
    context_options = get_context_options()
    
    # Add video recording
    context_options['record_video_dir'] = 'test-results/videos'
    context_options['record_video_size'] = {"width": 1920, "height": 1080}
    
    return context_options


@pytest.fixture(scope="session")
def playwright_browser(playwright: Playwright) -> Generator[Browser, None, None]:
    """Provide browser instance (local or BrowserStack)."""
    if is_browserstack_enabled():
        cdp_url = get_cdp_url()
        browser = playwright.chromium.connect_over_cdp(cdp_url)
        yield browser
        browser.close()
    else:
        launch_options = get_browser_launch_options()
        browser = playwright.chromium.launch(**launch_options)
        yield browser
        browser.close()


@pytest.fixture
def context(playwright_browser: Browser, browser_context_args) -> Generator[BrowserContext, None, None]:
    """Provide browser context with storage state if available."""
    context = playwright_browser.new_context(**browser_context_args)
    context.set_default_timeout(TIMEOUT)
    
    # Enable tracing for debugging
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield context
    
    # Save trace
    trace_path = f"test-results/traces/trace-{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    Path("test-results/traces").mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=trace_path)
    
    context.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Provide page instance."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture
def d365_base_url() -> str:
    """Provide D365 base URL from environment."""
    env = get_env()
    if not env.d365_base_url:
        pytest.skip("D365_BASE_URL not configured")
    return env.d365_base_url


@pytest.fixture
def storage_state_path() -> Path:
    """Provide storage state path."""
    return get_storage_state_path()


@pytest.fixture
def authenticated_context(
    playwright_browser: Browser,
    storage_state_path: Path
) -> Generator[BrowserContext, None, None]:
    """Provide authenticated context using storage state."""
    if not storage_state_path.exists():
        pytest.skip(f"Storage state not found at {storage_state_path}. Run auth setup first.")
    
    context_options = get_context_options()
    
    # Add video recording
    context_options['record_video_dir'] = 'test-results/videos'
    context_options['record_video_size'] = {"width": 1920, "height": 1080}
    
    context = playwright_browser.new_context(**context_options)
    context.set_default_timeout(TIMEOUT)
    
    # Enable tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    
    yield context
    
    # Save trace
    trace_path = f"test-results/traces/trace-{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    Path("test-results/traces").mkdir(parents=True, exist_ok=True)
    context.tracing.stop(path=trace_path)
    
    context.close()


@pytest.fixture
def authenticated_page(authenticated_context: BrowserContext) -> Generator[Page, None, None]:
    """Provide page with authenticated context."""
    page = authenticated_context.new_page()
    yield page
    page.close()


# Enhanced Allure reporting hooks
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshots, videos, and traces on failure AND success."""
    outcome = yield
    rep = outcome.get_result()
    
    # Add attachments for both passed and failed tests
    if call.when == "call":
        # Get any page fixture (check multiple possible names)
        page = None
        page_fixture_names = [
            'page', 
            'authenticated_page', 
            'fh_authenticated_page',
            'd365_authenticated_page',  # Add D365 fixture
        ]
        
        for fixture_name in page_fixture_names:
            if fixture_name in item.funcargs:
                page = item.funcargs[fixture_name]
                break
        
        if page:
            try:
                # Always attach screenshot (for both pass and fail)
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"Screenshot - {rep.nodeid.split('::')[-1]}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Attach page HTML
                html_content = page.content()
                allure.attach(
                    html_content,
                    name="Page HTML",
                    attachment_type=allure.attachment_type.HTML
                )
                
                # Attach current URL
                allure.attach(
                    page.url,
                    name="Page URL",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # Attach video if available
                try:
                    video_path = page.video.path() if page.video else None
                    if video_path:
                        # Close page to finalize video
                        page.context.close()
                        
                        # Wait a moment for video to be written
                        import time
                        time.sleep(1)
                        
                        if os.path.exists(video_path):
                            with open(video_path, 'rb') as video_file:
                                allure.attach(
                                    video_file.read(),
                                    name="Test Video",
                                    attachment_type=allure.attachment_type.WEBM
                                )
                except Exception as video_error:
                    print(f"Could not attach video: {video_error}")
                
            except Exception as e:
                print(f"Could not attach media to Allure: {e}")


# Pytest command line options
def pytest_addoption(parser):
    """Add custom command line options."""
    # Note: --headed is provided by pytest-playwright
    parser.addoption(
        "--use-browserstack",
        action="store_true",
        default=False,
        help="Run tests on BrowserStack Automate"
    )


@pytest.fixture(autouse=True)
def configure_browserstack(request):
    """Configure BrowserStack from command line."""
    if request.config.getoption("--use-browserstack"):
        os.environ["USE_BROWSERSTACK"] = "true"
