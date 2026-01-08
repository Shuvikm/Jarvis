"""J.A.R.V.I.S. - Personal AI Assistant with Aizen Voice

Main entry point for the application.
"""

import sys
import logging
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from jarvis_core.assistant import JarvisAssistant


def setup_logging(verbose: bool = False):
    """Set up logging configuration.
    
    Args:
        verbose: Enable verbose debug logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'jarvis.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='J.A.R.V.I.S. - Personal AI Assistant with Aizen Voice'
    )
    
    parser.add_argument(
        '--mode',
        choices=['text', 'voice'],
        default='text',
        help='Interaction mode (default: text)'
    )
    
    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run in test mode with sample commands'
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting J.A.R.V.I.S. Assistant")
    
    try:
        # Create assistant
        assistant = JarvisAssistant(config_path=args.config)
        
        if args.test:
            # Test mode
            logger.info("Running in test mode")
            assistant.start()
            
            test_commands = [
                "Hello",
                "What time is it?",
                "What's today's date?",
                "Help",
                "Goodbye"
            ]
            
            for cmd in test_commands:
                print(f"\nYou: {cmd}")
                assistant.process_text_input(cmd)
            
        elif args.mode == 'voice':
            # Voice mode (not yet implemented)
            assistant.run_voice_mode()
        else:
            # Text mode
            assistant.run_text_mode()
            
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        print("\n\nShutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nError: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
