"""Security checker implementation."""

from typing import List, Dict, Any
from . import BaseChecker
from ..ast_security import ASTSecurityDetector
from ..secrets import detect_secrets


class SecurityChecker(BaseChecker):
    """Checks for security vulnerabilities and secrets."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)

    def get_category(self) -> str:
        return "security"

    def check(self, module_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        issues = []
        issues = []
        # path = module_info.get("path", "") - unused

        # AST-based security checks
        if "ast_tree" in module_info:
            # Pass full config to detector (it extracts security_patterns)
            detector = ASTSecurityDetector(self.config)
            issues.extend(detector.detect(module_info["ast_tree"]))

        # Secret detection (on content)
        # Note: In a real integration, content might need to be read or passed in
        # Assuming module_info might have content or we read it here.
        # Ideally, the engine passes content. If not, we might skip or read carefully.
        # For this refactor, let's assume content is available or we read it if path exists
        # But to be safe and avoid IO in checker if possible, we check if content is provided.

        content = module_info.get("content")
        if content:
            secret_issues = detect_secrets(content)
            issues.extend(secret_issues)

        return issues
