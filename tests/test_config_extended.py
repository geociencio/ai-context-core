import pathlib
from unittest.mock import patch

from ai_context_core.analyzer.providers.config_loader import load_config
from ai_context_core.config.loader import list_profiles


def test_list_profiles_directory_missing():
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = False
        profiles = list_profiles()
        assert profiles == ["generic"]


def test_list_profiles_includes_generic():
    assert "generic" in list_profiles()


def test_load_config_profile_not_found_falls_back_to_defaults():
    cfg = load_config(pathlib.Path("/tmp"), profile_name="ghost")
    assert cfg is not None
    assert "scoring" in cfg
