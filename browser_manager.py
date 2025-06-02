"""
Browser Manager - Handle browser creation and configuration
"""

import logging
import random
import time
from typing import Optional, Dict
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

class BrowserManager:
    def __init__(self, config_manager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.ua = UserAgent()
        
    def create_browser(self, proxy: Optional[Dict] = None):
        """Create a new browser instance with random configuration"""
        try:
            options = self._get_chrome_options(proxy)
            
            # Create service object
            service = Service()
            
            # Create driver
            driver = webdriver.Chrome(service=service, options=options)
            
            # Set timeouts
            driver.set_page_load_timeout(30)
            driver.implicitly_wait(10)
            
            # Set random window size
            self._set_random_window_size(driver)
            
            self.logger.debug("Browser created successfully")
            return driver
            
        except Exception as e:
            self.logger.error(f"Failed to create browser: {str(e)}")
            return None
    
    def _get_chrome_options(self, proxy: Optional[Dict] = None) -> Options:
        """Configure Chrome options for stealth browsing"""
        options = Options()
        
        # Basic stealth options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Random user agent
        user_agent = self._get_random_user_agent()
        options.add_argument(f"--user-agent={user_agent}")
        
        # Disable images and CSS for faster loading (optional)
        if self.config.get_disable_images():
            prefs = {
                "profile.managed_default_content_settings.images": 2,
                "profile.default_content_setting_values.notifications": 2
            }
            options.add_experimental_option("prefs", prefs)
        
        # Language settings
        options.add_argument("--lang=en-US")
        
        # Disable logging
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        
        # Memory optimization
        options.add_argument("--memory-pressure-off")
        options.add_argument("--max_old_space_size=4096")
        
        # Additional stealth options
        options.add_argument("--disable-plugins-discovery")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-default-apps")
        options.add_argument("--disable-sync")
        
        # Proxy configuration
        if proxy:
            proxy_option = f"--proxy-server={proxy['protocol']}://{proxy['host']}:{proxy['port']}"
            options.add_argument(proxy_option)
            
            # If proxy has authentication, we need to handle it differently
            if 'username' in proxy and 'password' in proxy:
                self.logger.warning("Proxy authentication requires additional setup")
        
        # Headless mode (optional)
        if self.config.get_headless_mode():
            options.add_argument("--headless")
        
        return options
    
    def _get_random_user_agent(self) -> str:
        """Get a random realistic user agent"""
        try:
            # Get random Chrome user agent
            user_agent = self.ua.chrome
            self.logger.debug(f"Using user agent: {user_agent}")
            return user_agent
        except Exception:
            # Fallback user agent
            fallback_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            ]
            return random.choice(fallback_agents)
    
    def _set_random_window_size(self, driver):
        """Set a random window size to mimic different devices"""
        sizes = [
            (1920, 1080),  # Full HD
            (1366, 768),   # HD
            (1536, 864),   # HD+
            (1440, 900),   # WXGA+
            (1280, 720),   # HD
            (1024, 768),   # XGA
        ]
        
        width, height = random.choice(sizes)
        driver.set_window_size(width, height)
        self.logger.debug(f"Set window size to {width}x{height}")
    
    def close_browser(self, driver):
        """Safely close browser instance"""
        try:
            if driver:
                driver.quit()
                self.logger.debug("Browser closed successfully")
        except Exception as e:
            self.logger.warning(f"Error closing browser: {str(e)}")
    
    def execute_stealth_script(self, driver):
        """Execute JavaScript to make the browser more stealth"""
        stealth_script = """
        // Remove webdriver property
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Mock languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['en-US', 'en'],
        });
        
        // Mock plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Override the `chrome` object
        window.chrome = {
            runtime: {},
        };
        
        // Override permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        """
        
        try:
            driver.execute_script(stealth_script)
            self.logger.debug("Executed stealth script")
        except Exception as e:
            self.logger.warning(f"Failed to execute stealth script: {str(e)}")
