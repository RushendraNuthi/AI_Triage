# StegoMailLogger - Educational Steganographic Keylogger Project

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-Educational-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey.svg)

## 🔒 **IMPORTANT EDUCATIONAL DISCLAIMER** 🔒

**⚠️ THIS SOFTWARE IS FOR EDUCATIONAL CYBERSECURITY PURPOSES ONLY ⚠️**

- ✅ **ONLY** use in controlled educational environments
- ✅ **ONLY** for learning about steganography and cybersecurity concepts
- ✅ **ONLY** with explicit permission in authorized lab environments
- ❌ **NEVER** use for malicious purposes or unauthorized monitoring
- ❌ **NEVER** deploy in production environments
- ❌ **NEVER** use without proper authorization and consent

By using this software, you agree to use it responsibly and ethically for educational purposes only.

## 📖 Project Overview

StegoMailLogger is a comprehensive educational project that demonstrates advanced steganographic techniques combined with simulated cybersecurity payloads. This project is designed to teach cybersecurity professionals and students about:

- **Steganography**: Hiding payloads within innocent-looking images
- **Payload Deployment**: Simulating how malware can be concealed and triggered
- **Email Exfiltration**: Educational demonstration of data transmission methods
- **Security Analysis**: Understanding how such attacks work to better defend against them

## 🏗️ Project Architecture

```
stegomail_logger/
├── steg/                   # Steganography modules
│   ├── encoder.py         # Payload embedding functionality
│   └── decoder.py         # Payload extraction functionality
├── logger/                 # Keylogger simulation modules
│   ├── keylogger.py       # Educational keylogger implementation
│   └── mailer.py          # Email transmission functionality
├── trigger/                # Execution trigger modules
│   └── opener.py          # Image opening simulation
├── utils/                  # Utility modules
│   └── encryptor.py       # Encryption/decryption utilities
├── main.py                # Main CLI interface
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables example
├── README.md              # This documentation
└── Dockerfile             # Container setup for isolation
```

## ✨ Key Features

### 🖼️ **Steganographic Embedding**
- **LSB (Least Significant Bit)** technique for hiding payloads in images
- Support for PNG, JPEG, and other image formats
- **Encrypted payload protection** using XOR and AES encryption
- Configurable embedding parameters (channels, bit depth)

### 🎯 **Educational Keylogger**
- **Safe, controlled keylogger** for educational demonstration
- Configurable logging duration and stealth modes
- **System information collection** for learning purposes
- VM detection for additional safety measures

### 📧 **Email Transmission**
- **Multiple SMTP provider support**: Gmail, SMTP2GO, Mailgun, Mailjet
- Secure credential management via environment variables
- **Formatted log reports** with system information
- Connection encryption and authentication

### 🚀 **Payload Execution Simulation**
- **Image opening trigger** simulation
- Automatic payload extraction and execution
- **Environment safety checks** to prevent misuse
- Background execution capabilities for demonstration

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Virtual environment (recommended)
- Access to educational/lab environment

### 1. Clone and Setup
```bash
# Navigate to the project directory
cd stegomail_logger

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration Setup

#### Option A: Using config.json
```bash
# Edit the configuration file
nano config.json
```

Configure your email settings:
```json
{
    "email": {
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "username": "your_email@gmail.com",
        "password": "your_app_password",
        "target_email": "target@example.com",
        "subject": "Educational Log Report"
    },
    "encryption": {
        "method": "xor",
        "key": "your_encryption_key_here",
        "aes_enabled": false
    }
}
```

#### Option B: Using Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit environment variables
nano .env
```

Set your credentials:
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
TARGET_EMAIL=target@example.com
ENCRYPTION_KEY=your_secret_key
```

### 3. Email Provider Setup

#### Gmail Setup
1. Enable 2-Factor Authentication
2. Generate an App Password: [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Use the app password in your configuration

#### SMTP2GO Setup
1. Create account: [SMTP2GO](https://www.smtp2go.com/)
2. Get SMTP credentials from dashboard
3. Configure: `mail.smtp2go.com:587`

#### Mailgun Setup
1. Create account: [Mailgun](https://www.mailgun.com/)
2. Set up sandbox domain for testing
3. Configure: `smtp.mailgun.org:587`

#### Mailjet Setup
1. Create account: [Mailjet](https://www.mailjet.com/)
2. Get API credentials
3. Configure: `in-v3.mailjet.com:587`

## 🚀 Usage Examples

### 1. Create Sample Files
```bash
# Generate sample payload and cover image
python main.py samples
```

This creates:
- `sample_keylogger.py` - Basic educational payload
- `enhanced_keylogger.py` - Advanced educational payload  
- `sample_cover.png` - Cover image for steganography

### 2. Encode Payload into Image
```bash
# Embed keylogger into image
python main.py encode --payload sample_keylogger.py --image sample_cover.png --output stego_image.png
```

### 3. Analyze Steganographic Image
```bash
# Extract and analyze payload
python main.py decode --image stego_image.png --output extracted_payload.py
```

### 4. Simulate Image Opening
```bash
# Simulate opening the steganographic image
python main.py open --image stego_image.png

# Open without displaying image
python main.py open --image stego_image.png --no-display

# Extract only, don't execute
python main.py open --image stego_image.png --no-execute
```

### 5. Test Individual Components

#### Test Keylogger
```bash
# Run educational keylogger for 30 seconds
python main.py keylogger --duration 30
```

#### Test Email Functionality
```bash
# Test email configuration
python main.py email-test
```

## 🔧 Advanced Configuration

### Encryption Methods
The project supports multiple encryption methods:

**XOR Encryption (Default)**
```json
{
    "encryption": {
        "method": "xor",
        "key": "simple_key_123"
    }
}
```

**AES Encryption**
```json
{
    "encryption": {
        "method": "aes",
        "key": "strong_password_here",
        "aes_enabled": true
    }
}
```

### Steganography Settings
```json
{
    "steganography": {
        "embed_method": "lsb",
        "channels": ["red", "green", "blue"],
        "bit_depth": 1
    }
}
```

### Keylogger Settings
```json
{
    "keylogger": {
        "log_file": "keylog.txt",
        "send_interval": 300,
        "stealth_mode": true,
        "max_log_size": 1024
    }
}
```

## 🐳 Docker Deployment (Recommended)

### Build Container
```dockerfile
# Create Dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# Run in isolated environment
CMD ["python", "main.py", "samples"]
```

### Run in Container
```bash
# Build image
docker build -t stegomail-logger .

# Run safely isolated
docker run --rm -it stegomail-logger

# Interactive mode
docker run --rm -it stegomail-logger bash
```

## 🛡️ Security & Safety Features

### Environment Detection
- **VM Detection**: Automatically detects virtual environments
- **Hostname Checks**: Looks for educational/lab indicators
- **User Context**: Validates safe execution context

### Safety Mechanisms
- **Educational Markers**: All payloads clearly marked as educational
- **Time Limits**: Automatic termination of demonstration activities
- **Consent Required**: Multiple confirmation prompts
- **Logging**: Comprehensive activity logging for transparency

### Responsible Disclosure
- All techniques are well-documented educational methods
- No zero-day exploits or novel attack vectors
- Focus on defensive learning and awareness

## 📊 Technical Details

### Steganography Implementation
- **LSB Modification**: Modifies least significant bits in image pixels
- **Channel Support**: Red, Green, Blue channels configurable
- **Capacity Calculation**: Automatic payload size validation
- **Format Support**: PNG, JPEG, BMP, TIFF

### Encryption Implementation
- **XOR Cipher**: Simple educational encryption method
- **AES-256**: Production-grade encryption via Fernet
- **Key Derivation**: PBKDF2 for password-based keys
- **Base64 Encoding**: Safe text representation

### Email Implementation
- **SMTP Protocol**: Standard email transmission
- **TLS Encryption**: Secure connection support
- **Authentication**: Username/password and OAuth2 support
- **Error Handling**: Comprehensive error reporting

## 🎓 Educational Use Cases

### Cybersecurity Training
1. **Steganography Analysis**: Learn to detect hidden payloads
2. **Incident Response**: Practice payload extraction and analysis  
3. **Network Monitoring**: Understand email-based exfiltration
4. **Malware Analysis**: Safe environment for studying techniques

### Academic Research
1. **Steganography Effectiveness**: Measure detection rates
2. **Encryption Strength**: Compare different encryption methods
3. **Behavioral Analysis**: Study payload execution patterns
4. **Defense Development**: Create detection mechanisms

### Professional Development
1. **Security Awareness**: Understand attack vectors
2. **Tool Development**: Build defensive capabilities
3. **Penetration Testing**: Authorized security assessments
4. **Forensics Training**: Digital evidence collection

## 🚨 Legal & Ethical Guidelines

### ✅ **AUTHORIZED USE**
- Educational institutions with proper permissions
- Authorized penetration testing engagements
- Personal learning in controlled environments
- Security research with proper approvals
- Corporate security training programs

### ❌ **PROHIBITED USE**
- Unauthorized monitoring of individuals
- Corporate espionage or data theft
- Malicious payload deployment
- Privacy violations
- Any illegal surveillance activities

### 📋 **COMPLIANCE REQUIREMENTS**
- Obtain written permission before use
- Document all educational activities
- Follow institutional security policies
- Respect privacy and data protection laws
- Report any security vulnerabilities responsibly

## 🔍 Troubleshooting

### Common Issues

**Email Authentication Fails**
```bash
# Check credentials
python main.py email-test

# Verify SMTP settings
# Enable "Less secure app access" for Gmail (not recommended for production)
# Use App Passwords for 2FA accounts
```

**Payload Extraction Fails**
```bash
# Verify image integrity
python main.py decode --image stego_image.png

# Check encryption settings match encoding configuration
```

**Permission Errors**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Check file permissions
chmod +x main.py
```

**Dependencies Issues**
```bash
# Update pip
pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Debug Mode
```bash
# Enable verbose logging
export PYTHONPATH=$(pwd)
python -v main.py samples
```

## 🤝 Contributing

### Educational Contributions Welcome
- Improved detection algorithms
- Additional encryption methods
- Enhanced safety mechanisms
- Documentation improvements
- Educational use case examples

### Contribution Guidelines
1. Fork the repository
2. Create feature branch (`git checkout -b feature/educational-enhancement`)
3. Commit changes (`git commit -am 'Add educational feature'`)
4. Push to branch (`git push origin feature/educational-enhancement`)
5. Create Pull Request with detailed description

### Code of Conduct
- All contributions must maintain educational focus
- No malicious code or actual attack tools
- Respect ethical guidelines and legal boundaries
- Include appropriate disclaimers and safety measures

## 📄 License

This project is released under an **Educational Use License**:

- ✅ Educational and research use permitted
- ✅ Modification and distribution for learning purposes
- ❌ Commercial use prohibited
- ❌ Malicious use strictly forbidden
- ❌ Production deployment not authorized

See `LICENSE` file for complete terms.

## 📚 Further Reading

### Steganography Resources
- [Steganography Techniques](https://en.wikipedia.org/wiki/Steganography)
- [LSB Steganography Explained](https://ieeexplore.ieee.org/document/8272525)
- [Digital Forensics and Steganography](https://link.springer.com/book/10.1007/978-1-4471-4543-1)

### Cybersecurity Education
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [SANS Security Training](https://www.sans.org/)
- [Cybersecurity and Infrastructure Security Agency](https://www.cisa.gov/)

### Ethical Hacking
- [Ethical Hacking Methodology](https://www.eccouncil.org/ethical-hacking/)
- [Penetration Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Responsible Disclosure](https://www.bugcrowd.com/resource/what-is-responsible-disclosure/)

## 🆘 Support & Contact

### Educational Support
For educational use questions and support:
- Create GitHub issue with "Educational Support" label
- Include environment details and use case description
- Specify educational institution and approval status

### Security Concerns
To report security issues or concerns:
- Use responsible disclosure practices
- Contact maintainers privately for security issues
- Provide detailed reproduction steps

### Feature Requests
For educational feature enhancements:
- Create detailed GitHub issue
- Explain educational value and use case
- Provide implementation suggestions if possible

---

**Remember: This tool is designed to educate and defend, not to attack. Use responsibly! 🛡️**

---

*StegoMailLogger v1.0 - Educational Cybersecurity Project*  
*Created for learning, built for safety, designed for defense.*