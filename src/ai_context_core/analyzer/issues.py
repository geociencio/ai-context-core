from typing import Any
from .visitors import issues as _v_issues
from .builders import issues as _b_issues

# Detection functions (direct access if possible, else via getattr)
detect = _v_issues.detect
detect_ast_security_issues = _v_issues.detect_ast_security_issues
find_secrets = _v_issues.find_secrets
find_security_issues = _v_issues.find_security_issues
run_analysis = _v_issues.run_analysis
find_technical_debt = _v_issues.find_technical_debt
find_optimizations = _v_issues.find_optimizations

# Legacy class aliases
GenericIssueDetector = _v_issues.GenericIssueDetector
IssuesSummarizer = _b_issues.IssuesSummarizer


def __getattr__(name: str) -> Any:
    if name == "ASTSecurityDetector":
        from .visitors.ast_security import ASTSecurityDetector

        return ASTSecurityDetector
    if name == "IssueDetector":
        from .visitors.ast_security import IssueDetector

        return IssueDetector
    raise AttributeError(f"module {__name__} has no attribute {name}")
