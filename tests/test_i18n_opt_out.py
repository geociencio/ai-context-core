import ast

from ai_context_core.analyzer.visitors.i18n_components import (
    find_no_i18n_lines,
    is_translatable_string,
)
from ai_context_core.analyzer.visitors.logic import check_qgis_compliance


def test_find_no_i18n_lines_detects_inline_and_standalone():
    code = (
        'a = "counted one"\n'
        'b = "skipped inline"  # no-i18n\n'
        "# no-i18n standalone\n"
        'c = "counted two"\n'
        'd = "not annotated"\n'
    )
    lines = find_no_i18n_lines(code)
    assert lines == frozenset({2, 3})


def test_no_i18n_opt_out_skips_annotated_strings():
    code = (
        'a = "This is translatable"\n'
        'b = "This is not translatable"  # no-i18n\n'
        'c = "Another translatable string"\n'
    )
    tree = ast.parse(code)
    tree.no_i18n_lines = find_no_i18n_lines(code)

    res = check_qgis_compliance(tree)
    assert res["i18n_usage"]["total_strings"] == 2


def test_no_annotation_counts_everything():
    code = 'a = "This is translatable"\nb = "Another translatable string"\n'
    tree = ast.parse(code)
    tree.no_i18n_lines = find_no_i18n_lines(code)

    res = check_qgis_compliance(tree)
    assert res["i18n_usage"]["total_strings"] == 2


def test_punctuation_dominated_strings_rejected():
    assert is_translatable_string("... ...") is False
    assert is_translatable_string("<< >>") is False
    assert is_translatable_string("Hello, world!") is True
