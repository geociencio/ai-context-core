import pathlib
from unittest.mock import patch
from ai_context_core.config.loader import ConfigLoader, list_profiles


def test_config_loader_yaml_error():
    loader = ConfigLoader()
    with patch("pathlib.Path.read_text") as mock_read:
        mock_read.side_effect = Exception("Permission denied")
        # Should return {} on error and log it
        assert loader._load_yaml(pathlib.Path("fake.yaml")) == {}


def test_list_profiles_directory_missing():
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = False
        # Should return ['generic'] if profiles dir doesn't exist
        profiles = list_profiles()
        assert profiles == ["generic"]


def test_config_loader_profile_not_found():
    loader = ConfigLoader()
    # Mock profiles_path to a non-existent dir
    loader.profiles_path = pathlib.Path("/tmp/missing_profiles_dir")
    cfg = loader.load_config(profile_name="ghost")
    assert cfg is not None
    # Should fallback to defaults
