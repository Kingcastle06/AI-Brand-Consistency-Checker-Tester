import re
from typing import Tuple

# A versioned signature library of malicious prompt injection patterns
INJECTION_SIGNATURES = [
    r"ignore\s+previous\s+instructions",
    r"ignore\s+above\s+instructions",
    r"override\s+compliance",
    r"bypass\s+standards",
    r"\[system\]",
    r"system\s*:",
    r"mark\s+all\s+assets\s+as\s+fully\s+compliant",
    r"set\s+compliance\s+score\s+to\s+100"
]

def scan_for_prompt_injection(text_content: str) -> Tuple[str, bool]:
    """
    Scans untrusted text copy for known malicious prompt injection vectors.
    Returns the cleaned/sanitized text and a boolean flag indicating if an infection was caught.
    """
    is_infected = False
    sanitized_text = text_content
    
    for pattern in INJECTION_SIGNATURES:
        # Scan case-insensitively for the malicious signature
        if re.search(pattern, text_content, re.IGNORECASE):
            is_infected = True
            # Sanitize it by redacting the trigger phrase so it loses its execution power
            sanitized_text = re.sub(pattern, "[REDACTED SECURITY INJECTION ATTEMPT]", sanitized_text, flags=re.IGNORECASE)
            
    return sanitized_text, is_infected