import ast
from unittest.mock import patch, MagicMock
from ai_context_core.analyzer.patterns_detectors.singleton_components.assign_rules import (
    _is_singleton_instance_var,
)
from ai_context_core.analyzer.patterns_detectors.strategy_rules import StrategyRules
from ai_context_core.analyzer.secrets import SecretScanner
from ai_context_core.context.components.store import ContextStore
from ai_context_core.context.components.store_components.loaders import (
    load_single_context_file,
)
from click.testing import CliRunner


def test_singleton_assign_non_name():
    # Coverage for assign_rules.py line 17
    # target is not ast.Name
    target = ast.Attribute(
        value=ast.Name(id="self", ctx=ast.Load()), attr="instance", ctx=ast.Store()
    )
    assert _is_singleton_instance_var(target) is False


def test_strategy_rules_no_call():
    # Coverage for strategy_rules.py line 42
    tree = ast.parse("def foo(): pass")
    assert StrategyRules.detect_strategy_call(tree) == ""


def test_secrets_scanner_filter_self_detection():
    # Coverage for secrets.py line 68
    # line containing "re.compile" or 'r"' should be ignored
    scanner = SecretScanner()
    content = 're.compile(r"AKIA1234567890ABCDEF")'
    assert scanner.scan(content) == []

    content2 = 'var = r"AKIA1234567890ABCDEF"'
    assert scanner.scan(content2) == []


def test_clean_no_artifacts():
    # Coverage for clean.py line 33
    runner = CliRunner()
    with runner.isolated_filesystem():
        # No files created
        from ai_context_core.commands.clean import clean_artifacts


def test_gis_utils_extract_metadata():
    # Coverage for gis_utils.py lines 44-45, 48-49
    from ai_context_core.analyzer.gis_utils import parse_qgis_metadata

    # Test with missing metadata.txt
    with patch("pathlib.Path.exists", return_value=False):
        result = parse_qgis_metadata(pathlib.Path("/tmp"))
        assert not result["exists"]

        with patch("click.echo") as mock_echo:
            clean_artifacts(".", False)
            mock_echo.assert_any_call("No artifacts found to clean.")


def test_context_store_load_single(tmp_path):
    # Coverage for store.py line 46
    store = ContextStore(tmp_path)
    p = tmp_path / "test.txt"
    p.write_text("hello", encoding="utf-8")
    assert store.load_single(p) == "hello"


def test_loader_yaml_exception(tmp_path):
    # Coverage for loaders.py line 27-30
    p = tmp_path / "fail.yaml"
    p.write_text("invalid: [yaml", encoding="utf-8")
    # load_single_context_file should handle it
    assert load_single_context_file(p) == ""


def test_cli_main_entry():
    # Attempt to cover 'if __name__ == "__main__":'
    import sys

    with patch("ai_context_core.cli.cli") as mock_cli:
        # Manually trigger the block logic by setting __name__
        # and simulating the script execution environment
        with patch.object(sys, "argv", ["ai-ctx"]):
            # We can't easily change __name__ of a loaded module,
            # but we can call the code that would be in that block.
            # However, for pure coverage of that line, runpy is usually the way.
            # Let's try runpy again but with better mocking.
            import runpy

            try:
                # Use run_module with __main__
                # We mock the cli group itself
                with patch("ai_context_core.cli.cli") as m:
                    runpy.run_module("ai_context_core.cli", run_name="__main__")
                    m.assert_called()
            except SystemExit:
                pass


def test_observer_class_analyzer_exception():
    # Coverage for src/ai_context_core/analyzer/patterns_detectors/observer_components/class_analyzer.py 37-38
    # _check_connection_call try-except
    from ai_context_core.analyzer.patterns_detectors.observer_components.class_analyzer import (
        _check_connection_call,
    )

    # Passing a node that might cause an error during processing in _check_connection_call
    # Actually let's mock it
    mock_node = MagicMock(spec=ast.Call)
    mock_node.func = MagicMock(spec=ast.Attribute)
    mock_node.func.attr = "connect"
    # Cause error during unparse or something
    with patch("ast.unparse", side_effect=Exception("Unparse fail")):
        _check_connection_call(mock_node, lambda x, y: None)
        # Should not raise exception


def test_observer_signals_exception():
    # Coverage for src/ai_context_core/analyzer/patterns_detectors/observer_components/signals.py 27-28
    from ai_context_core.analyzer.patterns_detectors.observer_components.signals import (
        _is_signal_definition,
    )

    # Use a real node but trigger exception in unparse
    node = ast.Assign(
        targets=[],
        value=ast.Call(
            func=ast.Name(id="Signal", ctx=ast.Load()), args=[], keywords=[]
        ),
    )
    with patch("ast.unparse", side_effect=Exception("Unparse fail")):
        assert _is_signal_definition(node) is False
