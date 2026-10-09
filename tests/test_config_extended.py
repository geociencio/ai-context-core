import pathlib
from unittest.mock import patch

import pytest

from ai_context_core.analyzer.providers.config_loader import load_config
from ai_context_core.config.loader import ConfigLoader, list_profiles


def test_config_loader_facade_emits_deprecation_warning():
    loader = ConfigLoader()
    with pytest.warns(DeprecationWarning):
        cfg = loader.load_config()
    assert cfg is not None
    assert "quality_weights" in cfg


def test_list_profiles_directory_missing():
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = False
        profiles = list_profiles()
        assert profiles == ["generic"]


def test_load_config_profile_not_found_falls_back_to_defaults():
    cfg = load_config(pathlib.Path("/tmp"), profile_name="ghost")
    assert cfg is not None
    assert "quality_weights" in cfg
