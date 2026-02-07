import pytest
from ai_context_core.analyzer.issues_components.registry import CheckerRegistry
from ai_context_core.analyzer.checkers import BaseChecker


class MockChecker(BaseChecker):
    def get_category(self):
        return "mock"

    def check(self, info):
        return [{"message": "mock issue"}]


def test_checker_registry_register_and_run():
    # Test registry.py lines 22, 29-38
    # 1. Register mock checker
    CheckerRegistry.register(MockChecker)

    # 2. Run all
    results = CheckerRegistry.run_all({"path": "test.py"})

    assert "mock" in results
    assert results["mock"][0]["message"] == "mock issue"

    # Clean up to avoid affecting other tests
    if MockChecker in CheckerRegistry._checkers:
        CheckerRegistry._checkers.remove(MockChecker)


def test_base_checker_abstract():
    # BaseChecker is in src/ai_context_core/analyzer/checkers/__init__.py or similar
    from ai_context_core.analyzer.checkers import BaseChecker

    checker = BaseChecker({})
    with pytest.raises(NotImplementedError):
        checker.check({})
    with pytest.raises(NotImplementedError):
        checker.get_category()
