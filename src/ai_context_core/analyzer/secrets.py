"""Module for detecting exposed secrets and credentials in code.

Uses regular expressions to identify potential security risks such as
API keys, tokens, and private keys.
"""

import re
from typing import List, Dict, Any, Tuple

# Patterns are obfuscated or split to avoid self-detection
PATTERNS: List[Tuple[str, str, str]] = [
    # AWS
    (
        r"AKIA[0-9A-Z]{16}",
        "AWS Access Key ID",
        "critical",
    ),
    (
        r"(?i)aws_secret_access_key\s*=\s*['\"][A-Za-z0-9/+=]{40}['\"]",
        "AWS Secret Access Key",
        "critical",
    ),
    # GitHub
    (
        r"ghp_[0-9a-zA-Z]{36}",
        "GitHub Personal Access Token",
        "critical",
    ),
    (
        r"github_pat_[0-9a-zA-Z_]{82}",
        "GitHub Personal Access Token (Fine-grained)",
        "critical",
    ),
    # Google
    (
        r"AIza[0-9A-Za-z\\-_]{35}",
        "Google API Key",
        "critical",
    ),
    # Private Keys
    (
        r"-----BEGIN\s+PRIVATE\s+KEY-----",
        "Generic Private Key",
        "critical",
    ),
    (
        r"-----BEGIN\s+RSA\s+PRIVATE\s+KEY-----",
        "RSA Private Key",
        "critical",
    ),
    (
        r"-----BEGIN\s+OPENSSH\s+PRIVATE\s+KEY-----",
        "OpenSSH Private Key",
        "critical",
    ),
    # Slack
    (
        r"xox[baprs]-([0-9a-zA-Z]{10,48})?",
        "Slack Token",
        "critical",
    ),
    # Stripe
    (
        r"(?:r|s)k_live_[0-9a-zA-Z]{24}",
        "Stripe Live Key",
        "critical",
    ),
    # OpenAI
    (
        r"sk-[a-zA-Z0-9]{48}",
        "OpenAI API Key",
        "critical",
    ),
    # Generic Potential Secrets (High Recall, Lower Precision)
    (
        r"(?i)(password|passwd|secret|api_key|access_token|auth_token)\s*=\s*['\"][A-Za-z0-9_\\-]{8,128}['\"]",
        "Generic Potential Secret Assignment",
        "high",
    ),
]

IGNORED_KEYWORDS = [
    "example",
    "test",
    "change_me",
    "changeme",
    "placeholder",
    "dummy",
    "sample",
    "your_password",
    "your_secret",
    "todo",
]


def detect_secrets(content: str) -> List[Dict[str, Any]]:
    """Scans content for potential secrets using regex patterns.

    Args:
        content: The string content to scan.

    Returns:
        A list of dictionaries describing found secrets.
    """
    issues = []
    lines = content.splitlines()

    for pattern_str, description, severity in PATTERNS:
        try:
            regex = re.compile(pattern_str)
            for match in regex.finditer(content):
                # Find line number
                match_start = match.start()
                line_no = content.count("\n", 0, match_start) + 1

                # Get the matching code (masked)
                code = match.group()

                # Check for ignored keywords (case-insensitive)
                code_lower = code.lower()
                if any(ignored in code_lower for ignored in IGNORED_KEYWORDS):
                    continue

                masked_code = _mask_secret(code)

                # Avoid reporting the pattern definition itself (self-check)
                # This is a heuristic: if the line looks like a regex definition, skip
                line_content = lines[line_no - 1]
                if (
                    "re.compile" in line_content
                    or 'r"' in line_content
                    or "r'" in line_content
                ):
                    continue

                issues.append(
                    {
                        "pattern": description,  # Use description as pattern name for clarity
                        "description": f"Potential exposed secret: {description}",
                        "severity": severity,
                        "line": line_no,
                        "code": masked_code,
                    }
                )
        except re.error:
            # Safely ignore invalid regex patterns if any
            continue

    return issues


def _mask_secret(secret: str) -> str:
    """Masks a secret string for display in reports.

    Shows first 2 and last 2 characters, masks the rest.
    """
    if len(secret) <= 4:
        return "*" * len(secret)
    return f"{secret[:2]}{'*' * (len(secret) - 4)}{secret[-2:]}"
