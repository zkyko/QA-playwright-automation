"""
BrowserStack Automate configuration for D365 F&O automation.
Non-SDK Integration approach with proper capabilities.
"""
import os
import json
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# BrowserStack credentials
BS_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "")
BS_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "")

# BrowserStack project/build settings
BS_PROJECT = os.getenv("BROWSERSTACK_PROJECT_NAME", os.getenv("BS_PROJECT", "FourHands & D365 Automation"))
BS_BUILD = os.getenv("BROWSERSTACK_BUILD_NAME", os.getenv("BS_BUILD", "D365-FO-Demo"))


def get_browserstack_capabilities():
    """
    Returns BrowserStack capabilities for Non-SDK Integration.
    This matches the format from your BrowserStack config.
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


def get_browserstack_cdp_url():
    """
    Get BrowserStack CDP URL with capabilities as query parameters.
    This is the correct format for Playwright Non-SDK integration.
    """
    if not BS_USERNAME or not BS_ACCESS_KEY:
        raise ValueError(
            "BrowserStack credentials missing. "
            "Set BROWSERSTACK_USERNAME and BROWSERSTACK_ACCESS_KEY environment variables."
        )
    
    # Build capabilities as query parameters
    caps = {
        'browser': 'chrome',
        'browser_version': 'latest',
        'os': 'Windows',
        'os_version': '11',
        'name': 'GitHub Actions Test',
    }
    
    if BS_BUILD:
        caps['build'] = BS_BUILD
    if BS_PROJECT:
        caps['project'] = BS_PROJECT
    
    # Build query string
    cap_params = '&'.join([f'caps.{k}={urllib.parse.quote(str(v))}' for k, v in caps.items()])
    
    # BrowserStack CDP URL with authentication and capabilities
    cdp_url = f"wss://{BS_USERNAME}:{BS_ACCESS_KEY}@cdp.browserstack.com/playwright?{cap_params}"
    
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
