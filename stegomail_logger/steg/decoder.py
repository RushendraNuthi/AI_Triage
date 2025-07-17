"""
Steganography decoder for extracting encrypted payloads from images.
Uses LSB (Least Significant Bit) extraction technique with Pillow library.

Author: Educational Cybersecurity Project
Warning: For educational use only in controlled environments.
"""

import os
import sys
from PIL import Image
import json
import logging
import hashlib
import tempfile

# Import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.encryptor import PayloadEncryptor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StegoDecoder:
    """
    Handles extraction and decryption of payloads from steganographic images.
    """
    
    def __init__(self, config_path="config.json"):
        """
        Initialize the decoder with configuration.
        
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
    
    def binary_to_string(self, binary_data):
        """
        Convert binary data to string.
        
        Args:
            binary_data (str): Binary string
            
        Returns:
            str: Converted string
        """
        try:
            # Ensure binary data length is multiple of 8
            if len(binary_data) % 8 != 0:
                binary_data = binary_data[:-(len(binary_data) % 8)]
            
            # Convert 8-bit chunks to characters
            text = ""
            for i in range(0, len(binary_data), 8):
                byte = binary_data[i:i+8]
                if len(byte) == 8:
                    char_code = int(byte, 2)
                    if 0 <= char_code <= 127:  # Valid ASCII range
                        text += chr(char_code)
                    else:
                        break  # Stop at invalid characters
            
            return text
            
        except Exception as e:
            logger.error(f"Failed to convert binary to string: {e}")
            return ""
    
    def extract_lsb(self, image_path, max_extraction_size=1048576):
        """
        Extract data using LSB (Least Significant Bit) technique.
        
        Args:
            image_path (str): Path to stego image
            max_extraction_size (int): Maximum data size to extract (in bits)
            
        Returns:
            str: Extracted binary data
        """
        try:
            # Open image
            with Image.open(image_path) as img:
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Get image data
                pixels = list(img.getdata())
                width, height = img.size
                
                logger.info(f"Extracting from {len(pixels)} pixels")
                
                # Channel mapping
                channel_map = {"red": 0, "green": 1, "blue": 2}
                
                # Extract binary data from pixels
                binary_data = ""
                extraction_limit = min(max_extraction_size, len(pixels) * len(self.channels))
                
                for pixel in pixels:
                    if len(binary_data) >= extraction_limit:
                        break
                    
                    # Extract data from specified channels
                    for channel_name in self.channels:
                        if len(binary_data) >= extraction_limit:
                            break
                        
                        channel_index = channel_map.get(channel_name, 0)
                        
                        # Extract LSB from the channel
                        lsb = pixel[channel_index] & 1
                        binary_data += str(lsb)
                
                logger.info(f"Extracted {len(binary_data)} bits")
                return binary_data
                
        except Exception as e:
            logger.error(f"LSB extraction failed: {e}")
            return ""
    
    def find_payload_boundaries(self, text_data):
        """
        Find payload start and end markers in extracted text.
        
        Args:
            text_data (str): Extracted text data
            
        Returns:
            tuple: (header, payload, footer) or (None, None, None) if not found
        """
        try:
            start_marker = "|||PAYLOAD_START|||"
            end_marker = "|||PAYLOAD_END|||"
            
            start_pos = text_data.find(start_marker)
            end_pos = text_data.find(end_marker)
            
            if start_pos == -1 or end_pos == -1:
                logger.warning("Payload markers not found")
                return None, None, None
            
            if start_pos >= end_pos:
                logger.warning("Invalid payload marker positions")
                return None, None, None
            
            # Extract components
            header = text_data[:start_pos]
            payload_start = start_pos + len(start_marker)
            payload = text_data[payload_start:end_pos]
            footer = text_data[end_pos + len(end_marker):]
            
            logger.info(f"Found payload: {len(payload)} characters")
            return header, payload, footer
            
        except Exception as e:
            logger.error(f"Failed to find payload boundaries: {e}")
            return None, None, None
    
    def parse_metadata(self, header):
        """
        Parse metadata from header.
        
        Args:
            header (str): Header text containing metadata
            
        Returns:
            dict: Parsed metadata or None if parsing fails
        """
        try:
            # Find JSON metadata at the end of header
            lines = header.strip().split('\n')
            for line in reversed(lines):
                line = line.strip()
                if line.startswith('{') and line.endswith('}'):
                    try:
                        metadata = json.loads(line)
                        logger.info("Metadata parsed successfully")
                        return metadata
                    except json.JSONDecodeError:
                        continue
            
            # Try to parse the entire header as JSON
            try:
                metadata = json.loads(header.strip())
                logger.info("Header parsed as JSON metadata")
                return metadata
            except json.JSONDecodeError:
                logger.warning("No valid JSON metadata found in header")
                return None
                
        except Exception as e:
            logger.error(f"Failed to parse metadata: {e}")
            return None
    
    def verify_payload(self, decrypted_payload, metadata):
        """
        Verify payload integrity using checksum.
        
        Args:
            decrypted_payload (str): Decrypted payload data
            metadata (dict): Payload metadata
            
        Returns:
            bool: True if verification successful
        """
        try:
            if not metadata or "checksum" not in metadata:
                logger.warning("No checksum available for verification")
                return False
            
            expected_checksum = metadata["checksum"]
            actual_checksum = hashlib.md5(decrypted_payload.encode()).hexdigest()
            
            if expected_checksum == actual_checksum:
                logger.info("Payload verification successful")
                return True
            else:
                logger.error(f"Payload verification failed: {expected_checksum} != {actual_checksum}")
                return False
                
        except Exception as e:
            logger.error(f"Payload verification error: {e}")
            return False
    
    def extract_payload(self, image_path, output_path=None):
        """
        Main method to extract payload from image.
        
        Args:
            image_path (str): Path to stego image
            output_path (str): Optional output path for extracted payload
            
        Returns:
            tuple: (success, payload_content, metadata)
        """
        try:
            logger.info("Starting payload extraction process...")
            
            # Validate input file
            if not os.path.exists(image_path):
                logger.error(f"Stego image not found: {image_path}")
                return False, None, None
            
            # Extract binary data using specified method
            if self.embed_method == "lsb":
                binary_data = self.extract_lsb(image_path)
            else:
                logger.error(f"Unsupported extraction method: {self.embed_method}")
                return False, None, None
            
            if not binary_data:
                logger.error("No data extracted from image")
                return False, None, None
            
            # Convert binary to text
            text_data = self.binary_to_string(binary_data)
            if not text_data:
                logger.error("Failed to convert extracted data to text")
                return False, None, None
            
            # Find payload boundaries
            header, encrypted_payload, footer = self.find_payload_boundaries(text_data)
            if not encrypted_payload:
                logger.error("No valid payload found in extracted data")
                return False, None, None
            
            # Parse metadata
            metadata = self.parse_metadata(header)
            
            # Decrypt payload
            try:
                decrypted_payload = self.encryptor.decrypt(encrypted_payload)
                logger.info("Payload decryption successful")
            except Exception as e:
                logger.error(f"Payload decryption failed: {e}")
                return False, None, metadata
            
            # Verify payload integrity
            if metadata:
                verification_result = self.verify_payload(decrypted_payload, metadata)
                if not verification_result:
                    logger.warning("Payload verification failed, but proceeding anyway")
            
            # Save to output file if specified
            if output_path:
                try:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(decrypted_payload)
                    logger.info(f"Extracted payload saved to: {output_path}")
                except Exception as e:
                    logger.error(f"Failed to save payload: {e}")
            
            logger.info("Payload extraction completed successfully")
            return True, decrypted_payload, metadata
            
        except Exception as e:
            logger.error(f"Extraction process failed: {e}")
            return False, None, None
    
    def execute_payload(self, payload_content, metadata=None):
        """
        Execute extracted payload in a controlled manner.
        
        Args:
            payload_content (str): Extracted payload code
            metadata (dict): Optional payload metadata
            
        Returns:
            bool: True if execution successful
        """
        try:
            logger.info("=== PAYLOAD EXECUTION WARNING ===")
            logger.info("About to execute extracted payload")
            logger.info("This is for educational purposes only!")
            
            if metadata:
                logger.info(f"Payload type: {metadata.get('type', 'unknown')}")
                logger.info(f"Payload version: {metadata.get('version', 'unknown')}")
            
            # Create temporary file for payload
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(payload_content)
                temp_path = temp_file.name
            
            try:
                # Execute the payload
                logger.info(f"Executing payload from: {temp_path}")
                exec(compile(payload_content, temp_path, 'exec'))
                logger.info("Payload execution completed")
                return True
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Payload execution failed: {e}")
            return False
    
    def analyze_image(self, image_path):
        """
        Analyze image for steganographic content without extraction.
        
        Args:
            image_path (str): Path to image to analyze
            
        Returns:
            dict: Analysis results
        """
        try:
            analysis = {
                "file_exists": os.path.exists(image_path),
                "file_size": 0,
                "image_format": None,
                "image_size": None,
                "estimated_capacity": 0,
                "has_stegomail_markers": False
            }
            
            if not analysis["file_exists"]:
                return analysis
            
            analysis["file_size"] = os.path.getsize(image_path)
            
            # Analyze image properties
            with Image.open(image_path) as img:
                analysis["image_format"] = img.format
                analysis["image_size"] = img.size
                
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                width, height = img.size
                total_pixels = width * height
                available_channels = len(self.channels)
                available_bits = total_pixels * available_channels * self.bit_depth
                analysis["estimated_capacity"] = available_bits // 8
            
            # Quick check for stegomail markers
            try:
                binary_data = self.extract_lsb(image_path, max_extraction_size=8192)  # Check first 1KB
                text_data = self.binary_to_string(binary_data)
                
                if "stegomail_payload" in text_data or "|||PAYLOAD_START|||" in text_data:
                    analysis["has_stegomail_markers"] = True
                    
            except Exception as e:
                logger.warning(f"Marker detection failed: {e}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Image analysis failed: {e}")
            return {"error": str(e)}


def demo_decoder():
    """
    Demonstration of the decoder functionality.
    """
    print("=== StegoDecoder Demo ===")
    print("Educational steganography decoding demonstration")
    
    decoder = StegoDecoder()
    
    # Check for sample files
    test_images = ["sample_cover.png", "stego_image.png", "encoded.png"]
    
    print("\nLooking for test images...")
    for image_path in test_images:
        if os.path.exists(image_path):
            print(f"\nAnalyzing: {image_path}")
            analysis = decoder.analyze_image(image_path)
            
            print(f"  File size: {analysis.get('file_size', 0)} bytes")
            print(f"  Image format: {analysis.get('image_format', 'Unknown')}")
            print(f"  Image size: {analysis.get('image_size', 'Unknown')}")
            print(f"  Estimated capacity: {analysis.get('estimated_capacity', 0)} bytes")
            print(f"  Has StegoMail markers: {analysis.get('has_stegomail_markers', False)}")
            
            if analysis.get('has_stegomail_markers', False):
                print(f"  -> This image appears to contain a StegoMail payload!")
        else:
            print(f"  {image_path}: Not found")
    
    print("\nDemo completed!")
    print("Use main.py to perform actual payload extraction and execution.")


if __name__ == "__main__":
    demo_decoder()