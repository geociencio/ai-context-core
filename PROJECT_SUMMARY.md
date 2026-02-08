# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-02-07 19:40:23
Analyzer Version: 3.1.1 (Ai-Context-Core)

## 📊 KEY METRICS
- **Quality Score**: 100.0/100
- **Source Lines (SLOC)**: 0
- **Maintainability**: 100.0
- **Test Coverage**: 0 test files

## 📁 STRUCTURE
**Total Modules**: 224

```tree
./
    .ai_context_cache.json
    .coverage
    .dockerignore
    .gitignore
    .pre-commit-config.yaml
    AI_CONTEXT.md
    ARCHITECTURE.mmd
    ... (+26 more)
    src/
        __init__.py
        ai_context_core/
            __init__.py
            analyzer/
                __init__.py
                aggregator.py
                ai_recommendations.py
                antipatterns.py
                ast_entry_points.py
                ast_metrics.py
                ast_qgis.py
                ... (+20 more)
                visitors/
                    __init__.py
                    antipattern_base.py
                    antipattern_orchestrator.py
                    antipatterns.py
                    ast_entry_points.py
                    ast_metrics.py
                    ast_qgis.py
                    ... (+50 more)
                builders/
                    __init__.py
                    aggregator.py
                    aggregator_qgis.py
                    ai_context_generator.py
                    ai_recommendations.py
                    algorithms.py
                    builder.py
                    ... (+20 more)
                providers/
                    __init__.py
                    analyzer.py
                    compiler.py
                    config_loader.py
                    fs_cache.py
                    fs_helpers.py
                    fs_scanner.py
                    ... (+8 more)
                metrics/
                    __init__.py
                    scorer.py
                issues_components/
                    __init__.py
                    registry.py
                patterns_components/
                    __init__.py
                    visitor.py
                security_checkers/
                    __init__.py
                    base.py
                    injection.py
                    insecure_calls.py
                summarizers/
                    __init__.py
                    base.py
                    git_patterns.py
                    issues.py
                    qgis.py
                ast_visitors_components/
                    __init__.py
                    classes.py
                    imports.py
                engine_components/
                    config_loader.py
                    worker.py
                context_builders/
                    dependencies.py
                    patterns.py
                    structure.py
                checkers/
                    __init__.py
                    optimization_checker.py
                    security_checker.py
                    tech_debt_checker.py
                patterns_detectors/
                    __init__.py
                    base.py
                    decorator.py
                    decorator_rules.py
                    factory.py
                    observer.py
                    observer_rules.py
                    ... (+3 more)
                ast_metrics_components/
                    __init__.py
                    sloc.py
                graph/
                    __init__.py
                    builder.py
                ignore_components/
                    __init__.py
                    loader.py
                dependency_analyser_components/
                    __init__.py
                    classifier.py
                    parser.py
                qgis_checkers/
                    __init__.py
                    base.py
                    frameworks.py
                entry_point_detectors/
                    __init__.py
                    framework_rules.py
            context/
                manager.py
                components/
                    __init__.py
                    builders.py
                    extractor.py
                    store.py
            config/
                defaults.toml
                defaults.yaml
                loader.py
                profiles/
                    qgis.yaml
            templates/
                initial_prompt.md
                workflows/
                    create-commit.md
                    end-session.md
                    start-session.md
                prompts/
            cli/
                .ai_context_cache.json
                AI_CONTEXT.md
                PROJECT_SUMMARY.md
                __init__.py
                __main__.py
                interactive.py
                project_context.json
                commands/
                    __init__.py
                    analysis.py
                    analyze.py
                    base.py
                    clean.py
                    compare.py
                    deps.py
                    ... (+15 more)
            commands/
                __init__.py
                clean.py
                report.py
            cli_groups/
                __init__.py
                specialized.py
                workflows.py
        ai_context_core.egg-info/
            PKG-INFO
            SOURCES.txt
            dependency_links.txt
            entry_points.txt
            requires.txt
            top_level.txt
    docs/
        AGENTIC_IMPLEMENTATION_GUIDE.md
        AGENTIC_STANDARDS_AND_SOURCES.md
        ARCHITECTURAL_ANALYSIS.md
        AiContextCore_Analysis_Report.md
        COMMIT_GUIDELINES.md
        CONFIGURATION.md
        DEVELOPMENT_LOG.md
        ... (+13 more)
        development/
            ARCHITECTURE.md
        releases/
            github/
            notes/
                v1.0.0.md
                v1.0.1.md
                v2.1.1.md
                v2.5.0.md
                v2.5.1.md
                v2.5.2.md
                v3.0.0.md
                ... (+4 more)
            walkthroughs/
                v3.1.0-walkthrough.md
        reports/
            initial_extraction.md
        research/
        user_guide/
            PROFILES_GUIDE.md
            QUICK_START.md
        sessions/
            session_2026-01-22_fix_config_release.md
            session_2026-01-25_analysis_planning.md
            session_2026-01-25_complete_workflows_summary.md
            session_2026-01-25_docker_integration.md
            session_2026-01-25_modularization_cycle.md
            session_2026-01-25_optimization_quality.md
            session_2026-01-25_phase1_completion.md
            ... (+9 more)
        adr/
            0001-use-adr-for-architecture-decisions.md
            0002-implement-13-improvements-roadmap.md
            0003-pattern-detection-scoring-strategy.md
            0004-multi-framework-entry-point-detection.md
            0005-optimization-refactoring-strategy.md
            README.md
            template.md
        secinterp/
            .ai_context_cache.json
            AI_CONTEXT.md
            PROJECT_SUMMARY.md
            ai_ctx_bug_report.md
            metadata.txt
            project_context.json
    tests/
        __init__.py
        test_absolute_final.py
        test_aggregator_extended.py
        test_antipatterns.py
        test_ast_extended.py
        test_ast_metrics_compatibility.py
        test_ast_security_extended.py
        ... (+46 more)
        fixtures/
            false_positives.py
    test_project/
        .ai-context-updates.yaml
        project_context.json
        test.py
    dist/
        .gitignore
        ai_context_core-3.1.1-py3-none-any.whl
        ai_context_core-3.1.1.tar.gz
```

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **.agent/scripts/skill_sync.py**: 2 issues (Max: HIGH)
- **src/ai_context_core/analyzer/builders/dependencies.py**: 2 issues (Max: HIGH)
- **src/ai_context_core/analyzer/builders/parser.py**: 1 issues (Max: HIGH)

## 💡 MAIN RECOMMENDATIONS
### src/ai_context_core/analyzer/builders/algorithms.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/builders/dependencies.py
- Consider breaking down large logic
### src/ai_context_core/analyzer/engine.py
- Consider breaking down large logic

## 🏗️ DESIGN PATTERNS
### Factory
- **DependencyAnalyzer** in `src/ai_context_core/analyzer/builders/dependencies.py` (70%)
- **GitPatternsSummarizer** in `src/ai_context_core/analyzer/builders/git_patterns.py` (70%)
- **GitPatternsSummarizer** in `src/ai_context_core/analyzer/builders/git_patterns.py` (70%)
- **IssuesSummarizer** in `src/ai_context_core/analyzer/builders/issues.py` (70%)
- **IssuesSummarizer** in `src/ai_context_core/analyzer/builders/issues.py` (70%)
### Decorator
- **register_detector** in `src/ai_context_core/analyzer/registry.py` (50%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 1225
- **Additions**: +114491
- **Deletions**: -59570
- **Total Churn**: 174061

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 26 commits
- `src/ai_context_core/analyzer/fs_utils.py`: 24 commits
- `src/ai_context_core/analyzer/issues.py`: 22 commits
- `src/ai_context_core/cli.py`: 21 commits
- `src/ai_context_core/analyzer/reporting.py`: 21 commits

## 📈 COMPLEXITY DISTRIBUTION
- **Average Complexity**: 5.21
- **Max Complexity**: 33
