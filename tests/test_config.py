import pytest

from ai_context_core.analyzer.providers.config_loader import load_config


class TestConfigLoading:
    def test_load_config_defaults_sanity(self, tmp_path):
        """Verify that load_config returns at least the hardcoded or file defaults."""
        config = load_config(tmp_path)
        assert "scoring" in config
        assert "quality_thresholds" in config

    def test_project_override(self, tmp_path):
        """Verify that project specific config.toml overrides defaults."""
        ai_context_dir = tmp_path / ".ai-context"
        ai_context_dir.mkdir()
        (ai_context_dir / "config.toml").write_text("""
[quality_thresholds.complexity]
error = 99
""")

        config = load_config(tmp_path)

        assert "scoring" in config
        assert config["quality_thresholds"]["complexity"]["error"] == 99

    def test_merge_logic(self, tmp_path):
        """Verify a nested override preserves sibling keys (deep merge)."""
        ai_context_dir = tmp_path / ".ai-context"
        ai_context_dir.mkdir()
        (ai_context_dir / "config.toml").write_text("""
[quality_thresholds.complexity]
error = 0.99
""")

        config = load_config(tmp_path)

        assert config["quality_thresholds"]["complexity"]["error"] == 0.99
        # The sibling "warning" key from defaults must be preserved.
        assert len(config["quality_thresholds"]["complexity"]) > 1

    def test_malformed_project_config(self, tmp_path, caplog):
        """Test graceful failure on bad TOML."""
        ai_context_dir = tmp_path / ".ai-context"
        ai_context_dir.mkdir()
        (ai_context_dir / "config.toml").write_text("INVALID TOML [ [")

        config = load_config(tmp_path)
        assert "scoring" in config

    def test_project_config_yaml_legacy_fallback(self, tmp_path):
        """Verify legacy .ai-context/config.yaml is read with a deprecation warning."""
        ai_context_dir = tmp_path / ".ai-context"
        ai_context_dir.mkdir()
        (ai_context_dir / "config.yaml").write_text("scoring:\n  base_score: 50.0\n")

        with pytest.warns(DeprecationWarning):
            config = load_config(tmp_path)

        assert config["scoring"]["base_score"] == 50.0

    def test_project_config_toml_preferred_over_yaml(self, tmp_path):
        """Verify config.toml wins and config.yaml is ignored when both exist."""
        ai_context_dir = tmp_path / ".ai-context"
        ai_context_dir.mkdir()
        (ai_context_dir / "config.toml").write_text("[scoring]\nbase_score = 42.0\n")
        (ai_context_dir / "config.yaml").write_text("scoring:\n  base_score: 99.0\n")

        config = load_config(tmp_path)
        assert config["scoring"]["base_score"] == 42.0

    def test_project_config_profile_name_honored(self, tmp_path):
        """Verify a profile_name key in project config selects a profile."""
        ai_context_dir = tmp_path / ".ai-context"
        ai_context_dir.mkdir()
        (ai_context_dir / "config.toml").write_text(
            'profile_name = "generic"\n[quality_thresholds]\nscore = 90\n'
        )

        config = load_config(tmp_path)
        assert "profile_name" not in config
        assert config["quality_thresholds"]["score"] == 90
