import pathlib
from unittest.mock import patch, MagicMock
from ai_context_core.analyzer.providers.config_loader import (
    load_config,
    _get_hardcoded_defaults,
)
from ai_context_core.analyzer.providers.worker import AnalysisWorker


def test_load_config_failed_defaults():
    # Coverage for config_loader.py line 30
    # Simulate tomllib error during defaults loading
    with patch("ai_context_core.analyzer.providers.config_loader.tomllib") as mock_toml:
        # Mocking that defaults file exists but load fails
        with patch("pathlib.Path.exists", return_value=True):
            mock_toml.load.side_effect = Exception("Load fail")
            # Should fallback to hardcoded
            res = load_config(pathlib.Path("/tmp"))
            assert res == _get_hardcoded_defaults()


def test_load_config_failed_project_override():
    # Coverage for config_loader.py line 43
    # Defaults load fine, but project override fails
    with patch("ai_context_core.analyzer.providers.config_loader.tomllib") as mock_toml:
        # We need to simulate that the FIRST load (defaults) works
        # and the SECOND load (project) fails
        mock_toml.load.side_effect = [{"defaults": {}}, Exception("Project fail")]
        # Mock paths
        with patch("pathlib.Path.exists", side_effect=[True, True]):
            # This is a bit complex due to how side_effect interacts with open()
            # Let's try simpler: mock logger directly
            with patch(
                "ai_context_core.analyzer.providers.config_loader.logger"
            ) as mock_log:
                # Cause the open/load to fail for project config
                with patch(
                    "builtins.open", side_effect=[MagicMock(), Exception("Open fail")]
                ):
                    load_config(pathlib.Path("/tmp"))
                    mock_log.warning.assert_called()


def test_load_config_non_dict_override():
    # Coverage for config_loader.py line 50
    # override_config with non-dict values for a section
    with patch("ai_context_core.analyzer.providers.config_loader.tomllib") as mock_toml:
        mock_toml.load.side_effect = [
            {"section": {"k": "v"}},  # defaults
            {"section": "not-a-dict"},  # override
        ]
        with patch("pathlib.Path.exists", return_value=True):
            with patch("builtins.open"):
                res = load_config(pathlib.Path("/tmp"))
                assert res["section"] == "not-a-dict"


def test_worker_read_empty_file():
    # Coverage for worker.py line 94
    worker = AnalysisWorker(pathlib.Path("/tmp"), {}, 1, {})
    with patch(
        "ai_context_core.analyzer.providers.fs_utils.read_file_fast", return_value=""
    ):
        assert worker.analyze_single(pathlib.Path("/tmp/empty.py")) == {}


def test_worker_analyze_single_exception():
    # Coverage for worker.py line 126-132
    worker = AnalysisWorker(pathlib.Path("/tmp"), {}, 1, {})
    # Trigger syntax error or other exception in ast.parse
    with patch(
        "ai_context_core.analyzer.providers.fs_utils.read_file_fast",
        return_value="invalid syntax",
    ):
        res = worker.analyze_single(pathlib.Path("/tmp/fail.py"))
        assert res["syntax_error"] is True
        assert "error" in res


def test_worker_run_parallel_exception():
    # Coverage for worker.py line 71
    worker = AnalysisWorker(pathlib.Path("/tmp"), {}, 2, {})
    # Mock concurrent.futures to yield a future that raises an exception
    with patch("concurrent.futures.ProcessPoolExecutor") as mock_exc:
        mock_executor = mock_exc.return_value.__enter__.return_value
        mock_future = MagicMock()
        mock_future.result.side_effect = Exception("Future fail")
        # PARALLEL_MIN_FILES is usually 5. Use 10 files.
        files = [pathlib.Path(f"/tmp/file{i}.py") for i in range(10)]

        # mock_executor.submit should return our future
        mock_executor.submit.return_value = mock_future

        # as_completed should yield our failing future
        with patch("concurrent.futures.as_completed", return_value=[mock_future]):
            with patch(
                "ai_context_core.analyzer.providers.fs_utils.calculate_file_hash",
                return_value="hash",
            ):
                # to_analyze needs to be filled
                worker.run_parallel(files)
                # Should have logged error
                assert "Future fail" in str(worker.error_log)
