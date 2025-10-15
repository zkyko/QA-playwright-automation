"""
Environment configuration loader for D365 F&O automation.
Provides a centralized dataclass-like object for accessing environment variables.
"""
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file
load_dotenv()


@dataclass
class EnvironmentConfig:
    """
    Centralized configuration object for all environment variables.
    """
    # D365 Configuration
    d365_base_url: str
    
    # Azure AD
    aad_tenant_id: Optional[str]
    aad_username: Optional[str]
    aad_password: Optional[str]
    
    # Storage State
    storage_state_path: str
    
    # Feature Management
    feature_filter: Optional[str]
    
    # BrowserStack
    browserstack_username: Optional[str]
    browserstack_access_key: Optional[str]
    bs_build: str
    bs_project: str
    
    # Execution Settings
    headed: bool
    timeout: int
    slow_mo: int
    browser: str
    
    # Paths
    project_root: Path
    reports_dir: Path
    storage_state_dir: Path
    
    @classmethod
    def load(cls) -> "EnvironmentConfig":
        """
        Load configuration from environment variables.
        
        Returns:
            EnvironmentConfig: Populated configuration object
        """
        project_root = Path(__file__).parent.parent
        
        return cls(
            # D365
            d365_base_url=os.getenv("D365_BASE_URL", ""),
            
            # Azure AD
            aad_tenant_id=os.getenv("AAD_TENANT_ID"),
            aad_username=os.getenv("AAD_USERNAME"),
            aad_password=os.getenv("AAD_PASSWORD"),
            
            # Storage State
            storage_state_path=os.getenv("STORAGE_STATE", "storage_state/aad.json"),
            
            # Feature Management
            feature_filter=os.getenv("FEATURE_FILTER"),
            
            # BrowserStack
            browserstack_username=os.getenv("BROWSERSTACK_USERNAME"),
            browserstack_access_key=os.getenv("BROWSERSTACK_ACCESS_KEY"),
            bs_build=os.getenv("BS_BUILD", "D365-FO-Demo"),
            bs_project=os.getenv("BS_PROJECT", "D365-Playwright-Python"),
            
            # Execution
            headed=os.getenv("HEADED", "false").lower() == "true",
            timeout=int(os.getenv("TIMEOUT", "30000")),
            slow_mo=int(os.getenv("SLOW_MO", "0")),
            browser=os.getenv("BROWSER", "chromium"),
            
            # Paths
            project_root=project_root,
            reports_dir=project_root / "reports",
            storage_state_dir=project_root / "storage_state"
        )
    
    def get_storage_state_full_path(self) -> Path:
        """Returns full path to storage state file."""
        return self.project_root / self.storage_state_path
    
    def validate(self) -> list[str]:
        """
        Validate required configuration.
        
        Returns:
            list[str]: List of validation errors (empty if valid)
        """
        errors = []
        
        if not self.d365_base_url:
            errors.append("D365_BASE_URL is required")
        
        if not self.d365_base_url.startswith("https://"):
            errors.append("D365_BASE_URL must start with https://")
        
        return errors
    
    def is_browserstack_configured(self) -> bool:
        """Check if BrowserStack credentials are configured."""
        return bool(self.browserstack_username and self.browserstack_access_key)


# Global configuration instance
env = EnvironmentConfig.load()


def get_env() -> EnvironmentConfig:
    """
    Get the global environment configuration instance.
    
    Returns:
        EnvironmentConfig: The environment configuration
    """
    return env
