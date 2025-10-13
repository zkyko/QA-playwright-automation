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
BS_PROJECT = os.getenv("BS_PROJECT", "D365-Playwright-Python")
BS_BUILD = os.getenv("BS_BUILD", "D365-FO-Demo")

# Browser capabilities
BS_BROWSER = os.getenv("BS_BROWSER", "chrome")
BS_BROWSER_VERSION = os.getenv("BS_BROWSER_VERSION", "latest")
BS_OS = os.getenv("BS_OS", "Windows")
BS_OS_VERSION = os.getenv("BS_OS_VERSION", "11")

# Execution settings
BS_RESOLUTION = os.getenv("BS_RESOLUTION", "1920x1080")
BS_LOCAL = os.getenv("BS_LOCAL", "false")
BS_DEBUG = os.getenv("BS_DEBUG", "false")
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
    
    capabilities = get_browserstack_capabilities()
    
    # Encode capabilities as URL parameters
    caps_param = urllib.parse.quote(str(capabilities))
    
    # Construct CDP endpoint URL
    cdp_url = (
        f"wss://cdp.browserstack.com/playwright?"
        f"caps={caps_param}"
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
        "storage_state": str(PROJECT_ROOT / STORAGE_STATE_PATH) if os.path.exists(
            PROJECT_ROOT / STORAGE_STATE_PATH
        ) else None
    }


def is_browserstack_enabled():
    """
    Check if BrowserStack execution is enabled.
    Can be triggered via environment variable or pytest config.
    """
    return os.getenv("USE_BROWSERSTACK", "false").lower() == "true"


# Example usage in conftest.py or test files:
# 
# if is_browserstack_enabled():
#     from playwright.sync_api import sync_playwright
#     with sync_playwright() as p:
#         browser = p.chromium.connect_over_cdp(get_cdp_url())
#         context = browser.new_context(**get_browserstack_context_options())
#         page = context.new_page()
