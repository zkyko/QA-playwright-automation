"""
Local Playwright configuration for D365 F&O automation.
Reads from .env and provides default settings for local execution.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root
PROJECT_ROOT = Path(__file__).parent.parent

# D365 Configuration
D365_BASE_URL = os.getenv("D365_BASE_URL", "")
STORAGE_STATE_PATH = os.getenv("STORAGE_STATE", "storage_state/aad.json")

# Playwright Settings
HEADED = os.getenv("HEADED", "false").lower() == "true"
SLOW_MO = int(os.getenv("SLOW_MO", "0"))
TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))

# Browser Settings
BROWSER = os.getenv("BROWSER", "chromium")
VIEWPORT = {
    "width": int(os.getenv("VIEWPORT_WIDTH", "1920")),
    "height": int(os.getenv("VIEWPORT_HEIGHT", "1080"))
}

# Screenshot & Video Settings
SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
VIDEO_ON = os.getenv("VIDEO_ON", "retain-on-failure")
TRACE_ON = os.getenv("TRACE_ON", "retain-on-failure")

# Playwright launch options for local execution
LOCAL_BROWSER_OPTIONS = {
    "headless": not HEADED,
    "slow_mo": SLOW_MO,
    "args": [
        "--disable-blink-features=AutomationControlled",
        "--disable-dev-shm-usage"
    ]
}

# Context options
CONTEXT_OPTIONS = {
    "viewport": VIEWPORT,
    "ignore_https_errors": True,
    "java_script_enabled": True,
    "storage_state": str(PROJECT_ROOT / STORAGE_STATE_PATH) if os.path.exists(
        PROJECT_ROOT / STORAGE_STATE_PATH
    ) else None
}

# Test settings
RETRY_FAILURES = int(os.getenv("RETRY_FAILURES", "1"))
PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "1"))


def get_browser_launch_options():
    """Returns browser launch options for local execution."""
    return LOCAL_BROWSER_OPTIONS


def get_context_options():
    """Returns browser context options."""
    return CONTEXT_OPTIONS


def get_storage_state_path():
    """Returns the full path to storage state file."""
    return PROJECT_ROOT / STORAGE_STATE_PATH
