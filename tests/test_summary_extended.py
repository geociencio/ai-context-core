from ai_context_core.analyzer.builders.summary_generator import ProjectSummaryGenerator


def test_generate_markdown_with_optimizations(tmp_path):
    analyses = {
        "metrics": {
            "quality_score": 90,
            "total_lines_code": 100,
            "total_physical_lines": 120,
        },
        "complexity": {"total_modules": 5},
        "optimizations": [
            {
                "module": "utils.py",
                "suggestions": [{"message": "Use list comprehension"}],
            }
        ],
        "dependencies": {"import_graph": {"main.py": ["utils.py"], "utils.py": []}},
    }
    output_file = tmp_path / "report.md"
    generator = ProjectSummaryGenerator(analyses, "TestProject")
    generator.generate_markdown(output_file)

    assert output_file.exists()
    content = output_file.read_text()
    assert "KEY METRICS" in content
    assert "utils.py" in content


def test_build_manual_notes():
    analyses = {"manual_notes": "Custom architecture notes"}
    generator = ProjectSummaryGenerator(analyses, "Test")
    assert generator._build_manual_notes() == "Custom architecture notes"
