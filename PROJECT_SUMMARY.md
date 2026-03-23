# PROJECT SUMMARY - ai-context-core
Analysis Date: 2026-03-22 21:53:19
Analyzer Version: 3.1.1 (Ai-Context-Core)

## 📊 KEY METRICS
- **Quality Score**: 98.0/100
- **Source Lines (SLOC)**: 9,374
- **Total Physical Lines**: 14,297
- **Maintainability**: 57.0
- **Test Coverage**: 58 test files

## 📁 STRUCTURE
**Total Modules**: 240

```tree
./
    .ai_context_cache.json
    .coverage
    .dockerignore
    .gitignore
    .pre-commit-config.yaml
    AI_CONTEXT.md
    CHANGELOG.md
    ... (+23 more)
    src/
        __init__.py
        ai_context_core/
            __init__.py
            analyzer/
                __init__.py
                constants.py
                engine.py
                pattern_base.py
                registry.py
                visitors/
                    __init__.py
                    antipattern_base.py
                    antipattern_orchestrator.py
                    antipatterns.py
                    ast_entry_points.py
                    ast_metrics.py
                    ast_qgis.py
                    ... (+51 more)
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
                    ... (+9 more)
                summarizers/
                    __init__.py
                    base.py
                    git_patterns.py
                    issues.py
                    qgis.py
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
                graph/
                    __init__.py
                    builder.py
                qgis_checkers/
                    base.py
                    frameworks.py
                entry_point_detectors/
                    framework_rules.py
                security_checkers/
                    base.py
            context/
                manager.py
                components/
                    __init__.py
                    builders.py
                    extractor.py
                    store.py
            config/
                defaults.toml
                loader.py
                profiles/
                    qgis.toml
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
        ARCHITECTURE.md
        AiContextCore_Analysis_Report.md
        CHANGELOG.md
        COMMIT_GUIDELINES.md
        ... (+18 more)
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
                ... (+7 more)
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
            0006-elimination-of-root-facades-and-enforcement-of-strict-modularity.md
            0007-scoped-i18n-analysis-for-qgis-plugins.md
            ... (+1 more)
        secinterp/
            .ai_context_cache.json
            AI_CONTEXT.md
            PROJECT_SUMMARY.md
            ai_ctx_bug_report.md
            metadata.txt
            project_context.json
        maintenance/
            analysis_report.md
            bug_report_v320.md
            bug_report_v321_aggregation.md
            dev_feedback.md
            i18n_improvement_guide.md
            v250_fix_report.md
    tests/
        __init__.py
        test_absolute_final.py
        test_aggregator_extended.py
        test_antipatterns.py
        test_ast_extended.py
        test_ast_metrics_compatibility.py
        test_ast_security_extended.py
        ... (+48 more)
        fixtures/
            false_positives.py
    test_project/
        .ai-context-updates.yaml
        project_context.json
        test.py
    dist/
        .gitignore
        ai_context_core-3.2.1-py3-none-any.whl
        ai_context_core-3.2.1.tar.gz
```

## 🚨 CRITICAL ISSUES
### 🔒 Security Issues:
- **tests/test_final_100_percent.py**: 17 issues (Max: HIGH)
- **tests/test_issues.py**: 2 issues (Max: CRITICAL)
- **tests/test_secrets.py**: 2 issues (Max: CRITICAL)

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
### Strategy
- **Context** in `test_strategy.py` (100%)

## 🔄 GIT ANALYSIS
### Code Churn (last 30 days)
- **Files Changed**: 15
- **Additions**: +2060
- **Deletions**: -960
- **Total Churn**: 3020

### 🔥 Hotspots
- `src/ai_context_core/analyzer/engine.py`: 27 commits
- `src/ai_context_core/analyzer/issues.py`: 24 commits
- `src/ai_context_core/analyzer/fs_utils.py`: 24 commits
- `src/ai_context_core/analyzer/reporting.py`: 23 commits
- `src/ai_context_core/analyzer/ast_utils.py`: 21 commits

## 📈 COMPLEXITY DISTRIBUTION
- **Average Complexity**: 5.53
- **Max Complexity**: 45
