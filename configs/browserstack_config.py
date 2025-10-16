"""
BrowserStack Automate configuration for D365 F&O automation.
Uses BrowserStack's capabilities-based approach (Non-SDK Integration).
"""
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# BrowserStack credentials
BS_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "")
BS_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "")

# BrowserStack project/build settings
BS_PROJECT = os.getenv("BROWSERSTACK_PROJECT_NAME", os.getenv("BS_PROJECT", "D365-Playwright-Python"))
BS_BUILD = os.getenv("BROWSERSTACK_BUILD_NAME", os.getenv("BS_BUILD", "D365-FO-Demo"))


def get_browserstack_capabilities():
    """
    Returns BrowserStack capabilities for Non-SDK Integration.
    This matches the format from BrowserStack's capability generator.
    """
    desired_cap = {
        'browser': 'chrome',
        'os': 'OS X',
        'os_version': 'Ventura',
        'browser_version': '115.0',
        'browserstack.username': BS_USERNAME,
        'browserstack.accessKey': BS_ACCESS_KEY,
        'browserstack.console': 'info',
        'browserstack.debug': 'true',
    }
    
    # Add build and project names if set
    if BS_BUILD:
        desired_cap['build'] = BS_BUILD
    if BS_PROJECT:
        desired_cap['project'] = BS_PROJECT
        
    return desired_cap


def get_cdp_url():
    """
    DEPRECATED: Use get_browserstack_capabilities() instead.
    
    BrowserStack CDP URL with authentication.
    Format from BrowserStack Playwright docs.
    """
    if not BS_USERNAME or not BS_ACCESS_KEY:
        raise ValueError(
            "BrowserStack credentials missing. "
            "Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables."
        )
    
    # BrowserStack CDP endpoint with basic auth
    # Format: wss://username:accessKey@cdp.browserstack.com/playwright
    cdp_url = f"wss://{BS_USERNAME}:{BS_ACCESS_KEY}@cdp.browserstack.com/playwright"
    
    return cdp_url


def get_browserstack_context_options():
    """
    Returns context options for BrowserStack execution.
    """
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": None,  # BrowserStack handles video recording
    }


def is_browserstack_enabled():
    """
    Check if BrowserStack execution is enabled.
    """
    use_bs = os.getenv("USE_BROWSERSTACK", "false").lower()
    build_name = os.getenv("BROWSERSTACK_BUILD_NAME", "")
    
    return use_bs == "true" or bool(build_name)
