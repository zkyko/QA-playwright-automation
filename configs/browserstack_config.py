"""
BrowserStack Automate configuration for D365 F&O automation.
Provides CDP WebSocket URL with encoded capabilities for remote execution.
"""
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# BrowserStack credentials
BS_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "")
BS_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "")

# BrowserStack project/build settings
BS_PROJECT = os.getenv("BROWSERSTACK_PROJECT_NAME", os.getenv("BS_PROJECT", "D365-Playwright-Python"))
BS_BUILD = os.getenv("BROWSERSTACK_BUILD_NAME", os.getenv("BS_BUILD", "D365-FO-Demo"))

# Browser capabilities
BS_BROWSER = os.getenv("BS_BROWSER", "chrome")
BS_BROWSER_VERSION = os.getenv("BS_BROWSER_VERSION", "latest")
BS_OS = os.getenv("BS_OS", "Windows")
BS_OS_VERSION = os.getenv("BS_OS_VERSION", "11")

# Execution settings
BS_RESOLUTION = os.getenv("BS_RESOLUTION", "1920x1080")
BS_LOCAL = os.getenv("BS_LOCAL", "false")
BS_DEBUG = os.getenv("BS_DEBUG", "true")
BS_NETWORK_LOGS = os.getenv("BS_NETWORK_LOGS", "true")
BS_CONSOLE_LOGS = os.getenv("BS_CONSOLE_LOGS", "errors")


def get_browserstack_capabilities():
    """
    Returns BrowserStack capabilities as a dictionary.
    """
    capabilities = {
        "browser": BS_BROWSER,
        "browser_version": BS_BROWSER_VERSION,
        "os": BS_OS,
        "os_version": BS_OS_VERSION,
        "resolution": BS_RESOLUTION,
        "project": BS_PROJECT,
        "build": BS_BUILD,
        "name": os.getenv("PYTEST_CURRENT_TEST", "D365 Test"),
        "browserstack.local": BS_LOCAL,
        "browserstack.debug": BS_DEBUG,
        "browserstack.networkLogs": BS_NETWORK_LOGS,
        "browserstack.console": BS_CONSOLE_LOGS,
        "browserstack.seleniumVersion": "4.0.0"
    }
    return capabilities


def get_cdp_url():
    """
    Generates BrowserStack CDP WebSocket URL with encoded capabilities.
    
    Returns:
        str: CDP WebSocket URL for connecting to BrowserStack Automate
        
    Raises:
        ValueError: If credentials are missing
    """
    if not BS_USERNAME or not BS_ACCESS_KEY:
        raise ValueError(
            "BrowserStack credentials missing. "
            "Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables."
        )
    
    # BrowserStack CDP URL format for Playwright with authentication
    # Format: wss://USERNAME:ACCESS_KEY@cdp.browserstack.com/playwright?caps...
    cdp_url = (
        f"wss://{urllib.parse.quote(BS_USERNAME)}:{urllib.parse.quote(BS_ACCESS_KEY)}@"
        f"cdp.browserstack.com/playwright?"
        f"caps.browserName=chrome&"
        f"caps.browserVersion=latest&"
        f"caps.os=Windows&"
        f"caps.osVersion=11&"
        f"caps.projectName={urllib.parse.quote(BS_PROJECT)}&"
        f"caps.buildName={urllib.parse.quote(BS_BUILD)}&"
        f"caps.sessionName={urllib.parse.quote(os.getenv('PYTEST_CURRENT_TEST', 'D365 Test'))}&"
        f"caps.debug=true&"
        f"caps.networkLogs=true&"
        f"caps.video=true&"
        f"caps.consoleLogs=verbose"
    )
    
    return cdp_url


def get_browserstack_context_options():
    """
    Returns context options for BrowserStack execution.
    """
    from configs.playwright_config import STORAGE_STATE_PATH, PROJECT_ROOT
    import os
    
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": None,  # BrowserStack handles video recording
        # Don't use storage_state on BrowserStack - auth programmatically instead
        # "storage_state": str(PROJECT_ROOT / STORAGE_STATE_PATH) if os.path.exists(
        #     PROJECT_ROOT / STORAGE_STATE_PATH
        # ) else None
    }


def is_browserstack_enabled():
    """
    Check if BrowserStack execution is enabled.
    Can be triggered via environment variable or pytest config.
    """
    use_bs = os.getenv("USE_BROWSERSTACK", "false").lower()
    build_name = os.getenv("BROWSERSTACK_BUILD_NAME", "")
    
    # Return True if USE_BROWSERSTACK is explicitly set to true
    # OR if BROWSERSTACK_BUILD_NAME is set (indicates BrowserStack context)
    return use_bs == "true" or bool(build_name)


# Example usage in conftest.py or test files:
# 
# if is_browserstack_enabled():
#     from playwright.sync_api import sync_playwright
#     with sync_playwright() as p:
#         browser = p.chromium.connect_over_cdp(get_cdp_url())
#         context = browser.new_context(**get_browserstack_context_options())
#         page = context.new_page()
