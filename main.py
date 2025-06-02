#!/usr/bin/env python3
"""
YouTube View Bot - Main Entry Point
Educational and personal testing purposes only.
"""

import argparse
import logging
import sys
import time
from youtube_bot import YouTubeBot
from config_manager import ConfigManager

def setup_logging(log_level="INFO"):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('youtube_bot.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    parser = argparse.ArgumentParser(description='YouTube View Bot for Educational Testing')
    parser.add_argument('--url', required=True, help='YouTube video URL')
    parser.add_argument('--views', type=int, default=10, help='Number of views to generate (default: 10)')
    parser.add_argument('--config', default='config.ini', help='Configuration file path (default: config.ini)')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')
    parser.add_argument('--dry-run', action='store_true', help='Run in dry-run mode (no actual views)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config_manager = ConfigManager(args.config)
        
        # Initialize bot
        bot = YouTubeBot(config_manager)
        
        logger.info(f"Starting YouTube bot for URL: {args.url}")
        logger.info(f"Target views: {args.views}")
        logger.info(f"Dry run mode: {args.dry_run}")
        
        if args.dry_run:
            logger.info("DRY RUN MODE - No actual views will be generated")
            return
        
        # Run the bot
        success_count = bot.generate_views(args.url, args.views)
        
        logger.info(f"Bot completed. Successful views: {success_count}/{args.views}")
        
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot failed with error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
