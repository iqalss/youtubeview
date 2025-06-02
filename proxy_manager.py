"""
Proxy Manager - Handle proxy rotation and validation
"""

import logging
import random
import requests
from typing import List, Dict, Optional

class ProxyManager:
    def __init__(self, proxy_file: str):
        self.proxy_file = proxy_file
        self.logger = logging.getLogger(__name__)
        self.proxies = []
        self.working_proxies = []
        self.failed_proxies = set()
        self.load_proxies()
    
    def load_proxies(self):
        """Load proxies from file"""
        try:
            with open(self.proxy_file, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    proxy = self._parse_proxy_line(line)
                    if proxy:
                        self.proxies.append(proxy)
            
            self.logger.info(f"Loaded {len(self.proxies)} proxies from {self.proxy_file}")
            
        except FileNotFoundError:
            self.logger.warning(f"Proxy file {self.proxy_file} not found. Running without proxies.")
        except Exception as e:
            self.logger.error(f"Error loading proxies: {str(e)}")
    
    def _parse_proxy_line(self, line: str) -> Optional[Dict]:
        """Parse a proxy line from the file"""
        try:
            # Support formats: host:port, host:port:username:password, protocol://host:port
            parts = line.split(':')
            
            if len(parts) >= 2:
                # Check if it starts with protocol
                if '//' in parts[0]:
                    protocol = parts[0].split('//')[0]
                    host = parts[0].split('//')[1]
                    port = int(parts[1])
                else:
                    protocol = 'http'  # Default to HTTP
                    host = parts[0]
                    port = int(parts[1])
                
                proxy = {
                    'host': host,
                    'port': port,
                    'protocol': protocol
                }
                
                # Add authentication if provided
                if len(parts) >= 4:
                    proxy['username'] = parts[2]
                    proxy['password'] = parts[3]
                
                return proxy
            
        except Exception as e:
            self.logger.warning(f"Failed to parse proxy line '{line}': {str(e)}")
        
        return None
    
    def get_random_proxy(self) -> Optional[Dict]:
        """Get a random working proxy"""
        if not self.proxies:
            return None
        
        # First, try to use working proxies
        available_proxies = [p for p in self.proxies if self._proxy_key(p) not in self.failed_proxies]
        
        if not available_proxies:
            self.logger.warning("No working proxies available")
            return None
        
        proxy = random.choice(available_proxies)
        
        # Test proxy if not already tested
        if not self._is_proxy_tested(proxy):
            if self._test_proxy(proxy):
                self.working_proxies.append(proxy)
            else:
                self.failed_proxies.add(self._proxy_key(proxy))
                return self.get_random_proxy()  # Try another proxy
        
        return proxy
    
    def _proxy_key(self, proxy: Dict) -> str:
        """Generate a unique key for a proxy"""
        return f"{proxy['host']}:{proxy['port']}"
    
    def _is_proxy_tested(self, proxy: Dict) -> bool:
        """Check if proxy has been tested"""
        key = self._proxy_key(proxy)
        return key in self.failed_proxies or proxy in self.working_proxies
    
    def _test_proxy(self, proxy: Dict) -> bool:
        """Test if a proxy is working"""
        try:
            proxy_url = self._format_proxy_url(proxy)
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                timeout=10
            )
            
            if response.status_code == 200:
                self.logger.debug(f"Proxy {self._proxy_key(proxy)} is working")
                return True
            else:
                self.logger.debug(f"Proxy {self._proxy_key(proxy)} returned status {response.status_code}")
                return False
                
        except Exception as e:
            self.logger.debug(f"Proxy {self._proxy_key(proxy)} failed test: {str(e)}")
            return False
    
    def _format_proxy_url(self, proxy: Dict) -> str:
        """Format proxy as URL for requests"""
        protocol = proxy.get('protocol', 'http')
        host = proxy['host']
        port = proxy['port']
        
        if 'username' in proxy and 'password' in proxy:
            return f"{protocol}://{proxy['username']}:{proxy['password']}@{host}:{port}"
        else:
            return f"{protocol}://{host}:{port}"
    
    def mark_proxy_failed(self, proxy: Dict):
        """Mark a proxy as failed"""
        key = self._proxy_key(proxy)
        self.failed_proxies.add(key)
        if proxy in self.working_proxies:
            self.working_proxies.remove(proxy)
        self.logger.debug(f"Marked proxy {key} as failed")
    
    def get_proxy_stats(self) -> Dict:
        """Get proxy statistics"""
        return {
            'total': len(self.proxies),
            'working': len(self.working_proxies),
            'failed': len(self.failed_proxies),
            'untested': len(self.proxies) - len(self.working_proxies) - len(self.failed_proxies)
        }
