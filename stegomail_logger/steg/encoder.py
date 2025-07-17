"""
Steganography encoder for embedding encrypted payloads into images.
Uses LSB (Least Significant Bit) technique with Pillow library.

Author: Educational Cybersecurity Project
Warning: For educational use only in controlled environments.
"""

import os
import sys
from PIL import Image
import json
import logging
import hashlib

# Import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.encryptor import PayloadEncryptor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StegoEncoder:
    """
    Handles embedding of encrypted payloads into images using steganography.
    """
    
    def __init__(self, config_path="config.json"):
        """
        Initialize the encoder with configuration.
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.embed_method = self.config.get("steganography", {}).get("embed_method", "lsb")
        self.channels = self.config.get("steganography", {}).get("channels", ["red", "green", "blue"])
        self.bit_depth = self.config.get("steganography", {}).get("bit_depth", 1)
        
        # Initialize encryptor
        encryption_config = self.config.get("encryption", {})
        self.encryptor = PayloadEncryptor(
            method=encryption_config.get("method", "xor"),
            key=encryption_config.get("key", "default_key")
        )
    
    def _load_config(self, config_path):
        """
        Load configuration from file.
        
        Args:
            config_path (str): Path to config file
            
        Returns:
            dict: Configuration dictionary
        """
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"Config file not found: {config_path}")
                return {}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def prepare_payload(self, payload_path):
        """
        Read and prepare payload for embedding.
        
        Args:
            payload_path (str): Path to payload file
            
        Returns:
            str: Prepared payload string
        """
        try:
            # Read payload file
            with open(payload_path, 'r', encoding='utf-8') as f:
                payload_content = f.read()
            
            logger.info(f"Payload loaded: {len(payload_content)} characters")
            
            # Encrypt payload
            encrypted_payload = self.encryptor.encrypt(payload_content)
            logger.info(f"Payload encrypted: {len(encrypted_payload)} characters")
            
            # Add metadata header
            metadata = {
                "type": "stegomail_payload",
                "version": "1.0",
                "encryption": self.encryptor.method,
                "checksum": hashlib.md5(payload_content.encode()).hexdigest()
            }
            
            # Combine metadata and payload
            header = json.dumps(metadata) + "|||PAYLOAD_START|||"
            full_payload = header + encrypted_payload + "|||PAYLOAD_END|||"
            
            logger.info(f"Final payload size: {len(full_payload)} characters")
            return full_payload
            
        except Exception as e:
            logger.error(f"Failed to prepare payload: {e}")
            raise
    
    def check_capacity(self, image_path, payload_size):
        """
        Check if image has sufficient capacity for payload.
        
        Args:
            image_path (str): Path to cover image
            payload_size (int): Size of payload in bytes
            
        Returns:
            bool: True if image can hold payload
        """
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                width, height = img.size
                total_pixels = width * height
                
                # Calculate available bits (using specified channels and bit depth)
                available_channels = len(self.channels)
                available_bits = total_pixels * available_channels * self.bit_depth
                available_bytes = available_bits // 8
                
                logger.info(f"Image capacity: {available_bytes} bytes")
                logger.info(f"Payload size: {payload_size} bytes")
                
                return payload_size <= available_bytes
                
        except Exception as e:
            logger.error(f"Failed to check image capacity: {e}")
            return False
    
    def string_to_binary(self, text):
        """
        Convert string to binary representation.
        
        Args:
            text (str): Text to convert
            
        Returns:
            str: Binary string
        """
        try:
            binary = ''.join(format(ord(char), '08b') for char in text)
            return binary
        except Exception as e:
            logger.error(f"Failed to convert string to binary: {e}")
            raise
    
    def embed_lsb(self, image_path, payload, output_path):
        """
        Embed payload using LSB (Least Significant Bit) technique.
        
        Args:
            image_path (str): Path to cover image
            payload (str): Payload to embed
            output_path (str): Path for output image
            
        Returns:
            bool: True if embedding successful
        """
        try:
            # Open and prepare image
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Get image data
                pixels = list(img.getdata())
                width, height = img.size
                
                # Convert payload to binary
                binary_payload = self.string_to_binary(payload)
                payload_length = len(binary_payload)
                
                logger.info(f"Embedding {payload_length} bits into {len(pixels)} pixels")
                
                # Check capacity
                if not self.check_capacity(image_path, len(payload.encode('utf-8'))):
                    logger.error("Image capacity insufficient for payload")
                    return False
                
                # Channel mapping
                channel_map = {"red": 0, "green": 1, "blue": 2}
                
                # Embed binary data into pixels
                binary_index = 0
                modified_pixels = []
                
                for pixel in pixels:
                    if binary_index >= payload_length:
                        # No more data to embed
                        modified_pixels.append(pixel)
                        continue
                    
                    # Convert pixel to list for modification
                    pixel_list = list(pixel)
                    
                    # Embed data in specified channels
                    for channel_name in self.channels:
                        if binary_index >= payload_length:
                            break
                        
                        channel_index = channel_map.get(channel_name, 0)
                        
                        # Modify LSB of the channel
                        if binary_index < payload_length:
                            # Clear LSB and set new bit
                            pixel_list[channel_index] = (pixel_list[channel_index] & 0xFE) | int(binary_payload[binary_index])
                            binary_index += 1
                    
                    modified_pixels.append(tuple(pixel_list))
                
                # Create new image with modified pixels
                stego_image = Image.new('RGB', (width, height))
                stego_image.putdata(modified_pixels)
                
                # Save the stego image
                stego_image.save(output_path)
                logger.info(f"Stego image saved: {output_path}")
                
                return True
                
        except Exception as e:
            logger.error(f"LSB embedding failed: {e}")
            return False
    
    def embed_payload(self, payload_path, image_path, output_path):
        """
        Main method to embed payload into image.
        
        Args:
            payload_path (str): Path to payload file
            image_path (str): Path to cover image
            output_path (str): Path for output stego image
            
        Returns:
            bool: True if embedding successful
        """
        try:
            logger.info("Starting payload embedding process...")
            
            # Validate input files
            if not os.path.exists(payload_path):
                logger.error(f"Payload file not found: {payload_path}")
                return False
            
            if not os.path.exists(image_path):
                logger.error(f"Cover image not found: {image_path}")
                return False
            
            # Prepare payload
            prepared_payload = self.prepare_payload(payload_path)
            
            # Embed using specified method
            if self.embed_method == "lsb":
                success = self.embed_lsb(image_path, prepared_payload, output_path)
            else:
                logger.error(f"Unsupported embedding method: {self.embed_method}")
                return False
            
            if success:
                logger.info("Payload embedding completed successfully")
                
                # Verify output file
                if os.path.exists(output_path):
                    file_size = os.path.getsize(output_path)
                    logger.info(f"Output file size: {file_size} bytes")
                    return True
                else:
                    logger.error("Output file was not created")
                    return False
            else:
                logger.error("Payload embedding failed")
                return False
                
        except Exception as e:
            logger.error(f"Embedding process failed: {e}")
            return False
    
    def create_sample_payload(self, output_path="sample_keylogger.py"):
        """
        Create a sample keylogger payload for testing.
        
        Args:
            output_path (str): Path for sample payload
        """
        sample_payload = '''#!/usr/bin/env python3
"""
Sample keylogger payload for educational steganography demonstration.
This payload is embedded within an image and executed when triggered.
"""

import os
import sys
import time
import logging
from datetime import datetime

# Configure logging for the payload
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def educational_keylogger_payload():
    """
    Educational keylogger payload - demonstrates concept only.
    """
    logger.info("=== EDUCATIONAL PAYLOAD EXECUTED ===")
    logger.info("This is a demonstration of steganographic payload execution")
    logger.info(f"Execution time: {datetime.now()}")
    logger.info(f"Current directory: {os.getcwd()}")
    logger.info(f"Python version: {sys.version}")
    
    # Simulate keylogger initialization
    logger.info("Initializing educational keylogger...")
    
    # In a real scenario, this would start actual keylogging
    # For educational purposes, we just log some information
    system_info = {
        "OS": os.name,
        "Platform": sys.platform,
        "User": os.environ.get("USER", "Unknown"),
        "Home": os.environ.get("HOME", "Unknown")
    }
    
    logger.info("System Information:")
    for key, value in system_info.items():
        logger.info(f"  {key}: {value}")
    
    # Simulate running for a short time
    logger.info("Payload running for 5 seconds (educational demo)...")
    time.sleep(5)
    
    logger.info("Educational payload execution completed")
    logger.info("=== END OF PAYLOAD ===")

# Execute the payload
if __name__ == "__main__":
    try:
        educational_keylogger_payload()
    except Exception as e:
        logger.error(f"Payload execution error: {e}")
'''
        
        try:
            with open(output_path, 'w') as f:
                f.write(sample_payload)
            logger.info(f"Sample payload created: {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to create sample payload: {e}")
            return False
    
    def create_sample_image(self, output_path="sample_cover.png", width=800, height=600):
        """
        Create a sample cover image for testing.
        
        Args:
            output_path (str): Path for sample image
            width (int): Image width
            height (int): Image height
        """
        try:
            # Create a simple gradient image
            img = Image.new('RGB', (width, height))
            pixels = []
            
            for y in range(height):
                for x in range(width):
                    # Create a gradient pattern
                    r = int((x / width) * 255)
                    g = int((y / height) * 255)
                    b = int(((x + y) / (width + height)) * 255)
                    pixels.append((r, g, b))
            
            img.putdata(pixels)
            img.save(output_path)
            logger.info(f"Sample cover image created: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create sample image: {e}")
            return False


def demo_encoder():
    """
    Demonstration of the encoder functionality.
    """
    print("=== StegoEncoder Demo ===")
    print("Educational steganography encoding demonstration")
    
    encoder = StegoEncoder()
    
    # Create sample files
    print("\n1. Creating sample payload...")
    encoder.create_sample_payload()
    
    print("2. Creating sample cover image...")
    encoder.create_sample_image()
    
    print("3. Testing payload preparation...")
    if os.path.exists("sample_keylogger.py"):
        payload = encoder.prepare_payload("sample_keylogger.py")
        print(f"   Prepared payload size: {len(payload)} characters")
    
    print("4. Testing image capacity check...")
    if os.path.exists("sample_cover.png"):
        capacity = encoder.check_capacity("sample_cover.png", 1024)
        print(f"   Image can hold 1KB payload: {capacity}")
    
    print("\nDemo completed! Files created:")
    print("  - sample_keylogger.py (sample payload)")
    print("  - sample_cover.png (sample cover image)")
    print("\nUse main.py to perform actual embedding.")


if __name__ == "__main__":
    demo_encoder()