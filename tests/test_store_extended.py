import pytest
from ai_context_core.context.components.store_components.loaders import (
    load_single_context_file,
)
from ai_context_core.context.components.store_components.updaters import (
    update_context_file,
    _load_current_updates,
)
from ai_context_core.context.components.builders import PromptBuilder


def test_prompt_builder_abstract():
    # Test builders.py line 18
    builder = PromptBuilder()
    with pytest.raises(NotImplementedError):
        builder.build("task", "ctx", "proj")


def test_loader_exception_handling(tmp_path):
    # Test loaders.py line 29-30
    p = tmp_path / "test.json"
    p.mkdir()  # Make it a directory to cause read_text error
    assert load_single_context_file(p) == ""


def test_updater_load_exception_handling(tmp_path):
    # Test updaters.py line 30-31
    p = tmp_path / ".ai-context-updates.yaml"
    p.mkdir()  # Make it a directory to cause read_text error
    assert _load_current_updates(p) == {}


def test_updater_merge_lists(tmp_path):
    # Coverage for updaters.py line 16-17 (list extension)
    p = tmp_path / ".ai-context-updates.yaml"
    p.write_text("list_key: [1, 2]")
    update_context_file(tmp_path, {"list_key": [3]})

    import yaml

    with open(p) as f:
        data = yaml.safe_load(f)
    assert data["list_key"] == [1, 2, 3]


def test_updater_merge_dicts(tmp_path):
    # Coverage for updaters.py line 14-15 (dict update)
    p = tmp_path / ".ai-context-updates.yaml"
    p.write_text("dict_key: {a: 1}")
    update_context_file(tmp_path, {"dict_key": {"b": 2}})

    import yaml

    with open(p) as f:
        data = yaml.safe_load(f)
    assert data["dict_key"] == {"a": 1, "b": 2}
