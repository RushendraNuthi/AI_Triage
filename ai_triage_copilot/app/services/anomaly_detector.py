import re

CRITICAL_PHRASES = [
    "data breach",
    "ransomware",
    "unauthorized access",
    "critical vulnerability",
    "system compromise"
]

def scan_for_anomalies(description):
    for phrase in CRITICAL_PHRASES:
        if re.search(phrase, description, re.IGNORECASE):
            return True
    return False
