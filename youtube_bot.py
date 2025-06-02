"""
YouTube Bot - Main automation logic
"""

import logging
import random
import time
from typing import Optional
from browser_manager import BrowserManager
from proxy_manager import ProxyManager
from config_manager import ConfigManager

class YouTubeBot:
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.logger = logging.getLogger(__name__)
        self.proxy_manager = ProxyManager(config_manager.get_proxy_file())
        self.browser_manager = BrowserManager(config_manager)
        self.success_count = 0
        self.failed_count = 0
        
    def generate_views(self, video_url: str, target_views: int) -> int:
        """Generate views for a YouTube video"""
        self.logger.info(f"Starting view generation for {target_views} views")
        
        for i in range(target_views):
            try:
                self.logger.info(f"Generating view {i + 1}/{target_views}")
                
                # Get a proxy (if available)
                proxy = self.proxy_manager.get_random_proxy()
                if proxy:
                    self.logger.debug(f"Using proxy: {proxy['host']}:{proxy['port']}")
                
                # Create browser instance
                browser = self.browser_manager.create_browser(proxy)
                
                if browser:
                    success = self._simulate_view(browser, video_url)
                    if success:
                        self.success_count += 1
                        self.logger.info(f"View {i + 1} completed successfully")
                    else:
                        self.failed_count += 1
                        self.logger.warning(f"View {i + 1} failed")
                        
                    # Close browser
                    self.browser_manager.close_browser(browser)
                else:
                    self.failed_count += 1
                    self.logger.error(f"Failed to create browser for view {i + 1}")
                
                # Wait between views
                if i < target_views - 1:  # Don't wait after the last view
                    delay = self._get_random_delay()
                    self.logger.debug(f"Waiting {delay} seconds before next view...")
                    time.sleep(delay)
                    
            except Exception as e:
                self.failed_count += 1
                self.logger.error(f"Error during view {i + 1}: {str(e)}")
                
        self.logger.info(f"View generation completed. Success: {self.success_count}, Failed: {self.failed_count}")
        return self.success_count
    
    def _simulate_view(self, browser, video_url: str) -> bool:
        """Simulate a single view"""
        try:
            # Navigate to video
            self.logger.debug("Navigating to video URL")
            browser.get(video_url)
            
            # Wait for page load
            time.sleep(random.uniform(2, 5))
            
            # Check if video is loaded
            try:
                video_element = browser.find_element("css selector", "video")
                if not video_element:
                    self.logger.warning("Video element not found")
                    return False
            except Exception as e:
                self.logger.warning(f"Could not find video element: {str(e)}")
                return False
            
            # Simulate human-like interaction
            self._simulate_human_behavior(browser)
            
            # Watch video for random duration
            watch_duration = self._get_random_watch_duration()
            self.logger.debug(f"Watching video for {watch_duration} seconds")
            time.sleep(watch_duration)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error during view simulation: {str(e)}")
            return False
    
    def _simulate_human_behavior(self, browser):
        """Simulate natural human behavior"""
        try:
            # Random scroll
            if random.random() < 0.3:  # 30% chance to scroll
                scroll_amount = random.randint(100, 500)
                browser.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(1, 3))
            
            # Random mouse movement simulation
            if random.random() < 0.2:  # 20% chance to move cursor
                # Simulate cursor movement by clicking on a safe area
                try:
                    body = browser.find_element("tag name", "body")
                    browser.execute_script("arguments[0].style.cursor = 'pointer';", body)
                    time.sleep(0.5)
                except:
                    pass
            
            # Random pause
            if random.random() < 0.4:  # 40% chance for random pause
                time.sleep(random.uniform(1, 4))
                
        except Exception as e:
            self.logger.debug(f"Error during behavior simulation: {str(e)}")
    
    def _get_random_delay(self) -> float:
        """Get random delay between views"""
        min_delay = self.config.get_min_delay()
        max_delay = self.config.get_max_delay()
        return random.uniform(min_delay, max_delay)
    
    def _get_random_watch_duration(self) -> float:
        """Get random watch duration"""
        min_duration = self.config.get_min_watch_duration()
        max_duration = self.config.get_max_watch_duration()
        return random.uniform(min_duration, max_duration)
