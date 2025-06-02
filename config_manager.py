"""
Configuration Manager - Handle application configuration
"""

import configparser
import logging
import os
from typing import Any

class ConfigManager:
    def __init__(self, config_file: str = 'config.ini'):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self.config = configparser.ConfigParser()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                self.config.read(self.config_file)
                self.logger.info(f"Configuration loaded from {self.config_file}")
            else:
                self._create_default_config()
                self.logger.info(f"Created default configuration at {self.config_file}")
        except Exception as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            self._create_default_config()
    
    def _create_default_config(self):
        """Create default configuration"""
        self.config['GENERAL'] = {
            'proxy_file': 'proxies.txt',
            'headless_mode': 'False',
            'disable_images': 'True',
            'log_level': 'INFO'
        }
        
        self.config['TIMING'] = {
            'min_delay_between_views': '30',
            'max_delay_between_views': '120',
            'min_watch_duration': '30',
            'max_watch_duration': '180',
            'page_load_timeout': '30'
        }
        
        self.config['BEHAVIOR'] = {
            'scroll_probability': '0.3',
            'pause_probability': '0.4',
            'mouse_move_probability': '0.2',
            'random_behavior_enabled': 'True'
        }
        
        self.config['BROWSER'] = {
            'user_agent_rotation': 'True',
            'window_size_randomization': 'True',
            'disable_webrtc': 'True',
            'disable_plugins': 'True'
        }
        
        self._save_config()
    
    def _save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                self.config.write(f)
        except Exception as e:
            self.logger.error(f"Error saving configuration: {str(e)}")
    
    def get(self, section: str, key: str, fallback: Any = None) -> str:
        """Get configuration value"""
        try:
            return self.config.get(section, key, fallback=fallback)
        except Exception:
            return fallback
    
    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get boolean configuration value"""
        try:
            return self.config.getboolean(section, key, fallback=fallback)
        except Exception:
            return fallback
    
    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """Get integer configuration value"""
        try:
            return self.config.getint(section, key, fallback=fallback)
        except Exception:
            return fallback
    
    def get_float(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get float configuration value"""
        try:
            return self.config.getfloat(section, key, fallback=fallback)
        except Exception:
            return fallback
    
    # Convenience methods for commonly used settings
    def get_proxy_file(self) -> str:
        return self.get('GENERAL', 'proxy_file', 'proxies.txt')
    
    def get_headless_mode(self) -> bool:
        return self.get_bool('GENERAL', 'headless_mode', False)
    
    def get_disable_images(self) -> bool:
        return self.get_bool('GENERAL', 'disable_images', True)
    
    def get_min_delay(self) -> float:
        return self.get_float('TIMING', 'min_delay_between_views', 30.0)
    
    def get_max_delay(self) -> float:
        return self.get_float('TIMING', 'max_delay_between_views', 120.0)
    
    def get_min_watch_duration(self) -> float:
        return self.get_float('TIMING', 'min_watch_duration', 30.0)
    
    def get_max_watch_duration(self) -> float:
        return self.get_float('TIMING', 'max_watch_duration', 180.0)
    
    def get_page_load_timeout(self) -> int:
        return self.get_int('TIMING', 'page_load_timeout', 30)
    
    def get_scroll_probability(self) -> float:
        return self.get_float('BEHAVIOR', 'scroll_probability', 0.3)
    
    def get_pause_probability(self) -> float:
        return self.get_float('BEHAVIOR', 'pause_probability', 0.4)
    
    def get_mouse_move_probability(self) -> float:
        return self.get_float('BEHAVIOR', 'mouse_move_probability', 0.2)
    
    def is_random_behavior_enabled(self) -> bool:
        return self.get_bool('BEHAVIOR', 'random_behavior_enabled', True)
