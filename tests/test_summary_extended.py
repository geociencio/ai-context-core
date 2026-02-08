from ai_context_core.analyzer.builders.summary_generator import SummaryGenerator


def test_generate_html_with_findings(tmp_path):
    analyses = {
        "metrics": {
            "quality_score": 90,
            "total_lines_code": 100,
            "total_physical_lines": 120,
        },
        "complexity": {"total_modules": 5},
        "security": [{"module": "main.py", "total_issues": 2, "max_severity": "high"}],
        "optimizations": [
            {
                "module": "utils.py",
                "suggestions": [{"message": "Use list comprehension"}],
            }
        ],
        "dependencies": {"import_graph": {"main.py": ["utils.py"], "utils.py": []}},
    }
    output_file = tmp_path / "report.html"
    generator = SummaryGenerator(analyses, "TestProject")
    generator.generate_html(output_file)

    assert output_file.exists()
    content = output_file.read_text()
    assert "SECURITY ISSUES" in content
    assert "main.py" in content
    assert "RECOMMENDATIONS" in content
    assert "utils.py" in content
    assert "DEPENDENCY GRAPH" in content
    assert "mermaid" in content


def test_build_manual_notes():
    analyses = {"manual_notes": "Custom architecture notes"}
    generator = SummaryGenerator(analyses, "Test")
    assert generator._build_manual_notes() == "Custom architecture notes"
