import ast
import pytest
from ai_context_core.analyzer.ast_security import (
    IssueDetector,
    ASTSecurityDetector,
    detect_ast_security_issues,
)


def test_issue_detector_abstract():
    # Test ast_security.py line 19
    det = IssueDetector()
    with pytest.raises(NotImplementedError):
        det.detect()


def test_detect_ast_security_issues_facade():
    # Coverage for detect_ast_security_issues line 73
    tree = ast.parse("eval('1+1')")
    issues = detect_ast_security_issues(tree)
    assert any("eval" in str(i).lower() for i in issues)


def test_ast_security_detector_init_with_config():
    # Coverage for ASTSecurityDetector line 35
    config = {"security_patterns": {"dangerous_functions": ["magic"]}}
    det = ASTSecurityDetector(config)
    # Check if config was passed to checkers (indirectly)
    checker = det.checkers[1]  # InsecureCallsChecker
    assert "magic" in checker.dangerous_functions
