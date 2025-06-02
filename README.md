# YouTube View Bot

A Python-based YouTube view automation tool with proxy rotation and natural behavior simulation for educational and personal testing purposes only.

## ⚠️ Important Disclaimer

This tool is designed for **educational and personal testing purposes only**. The use of this software to artificially inflate view counts on YouTube videos may violate YouTube's Terms of Service and could result in penalties to your account or content. Use at your own risk and responsibility.

## Features

- 🎯 YouTube video viewing automation
- 🔄 Proxy rotation system for IP distribution
- 🤖 Natural behavior simulation to avoid detection
- ⏱️ Configurable delays and watch durations
- 📊 Comprehensive logging and error handling
- 🎛️ Easy-to-use command-line interface
- 🔧 Modular and customizable design

## Requirements

- Python 3.7 or higher
- Chrome/Chromium browser
- ChromeDriver (automatically managed)

## Installation

1. Clone or download the project files
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your proxies in `proxies.txt` (optional but recommended)
4. Adjust settings in `config.ini` as needed

## Configuration

### Proxy Setup

Edit the `proxies.txt` file to add your proxy servers:

```txt
# HTTP proxies
proxy1.example.com:8080
192.168.1.100:3128

# SOCKS proxies
socks5://proxy2.example.com:1080

# Authenticated proxies
proxy.example.com:8080:username:password
