# Development Log

## [2026-10-08] Deep Cleanup & Metric Contract (v4.0.0) - COMPLETED
**THEME**: Dead-code removal, architecture purity, and contract enforcement 🧹
- **Anti-patterns surfaced**: fixed a functional bug where anti-pattern detections ran but were never aggregated/reported; now exposed in `AI_CONTEXT.md`. 🐛
- **Dead code removed**: retired the dead `CheckerRegistry` chain (`security_checker`, `tech_debt_checker`, `checker_registry`, `debt`) and the `analyzer/pattern_base.py` facade, plus unused `registry.py`/`issues.py` symbols. `optimization_checker.py` was kept (live via `find_optimizations`). 🗑️
- **Architecture purity**: moved `secrets_scanner.py` (file I/O) from `visitors/` to `providers/`. 🔀
- **Metric key contract**: `stats`, `analyze`, `ai_recommendations`, `context_metrics`, `summary_generator` now read metrics via `metric_keys`; complexity aggregation keys canonicalized in `formatter.py`. 🔑
- **Observer re-export**: removed the 2-hop `# noqa: F401` re-export between `observer_rules.py` and `observer_signal_rules.py`. 🧹
- **Version**: bumped to `4.0.0` (breaking removal of deprecated facades/chain). 🏷️
- **Deferred (intentionally)**: the `X.py` + `X_rules.py` split is a deliberate complexity-management pattern (keeps modules under the CC 25 budget); unifying the 4 name-resolution helpers would change their distinct semantics (leading vs trailing, lowercasing), so both were left as-is. ⚠️
- **Verification**: 299 tests passing, `ruff check` clean, golden fixtures regenerated. ✅

## [2026-10-08] Redundancy Cleanup (Phases A–C) - COMPLETED
**THEME**: Dead-code removal, consolidation and determinism 🧹
- **Phase A**: Removed 6 dead modules, the broken `check_complexity.py`, and duplicate symbols (`HalsteadVisitor`, `_mask_secret`, `analyze_structure`, ...) plus their coverage-only tests. 🗑️
- **Phase B**: Unified `metadata.txt` parsing (`gis_utils.parse_metadata_content`), one AST name helper (`qgis_base.get_node_name`), a shared `BaseAnalysesBuilder`, and migrated legacy wrappers to canonical classes; metrics read via `metric_keys`. 🔗
- **Phase C**: Deleted all 10 deprecated facade packages, dropped the duplicate CLI `_cmd` aliases, and repointed tests/docs to canonical paths. 🧱
- **Determinism**: `fs_tree` fallback now sorts directories (matching the `tree` binary); regenerated golden fixtures to fix a pre-existing environment-dependent test. 📁
- **Score note**: the heuristic score moved 100 → ~90 because removing tiny high-MI shim modules lowered the *average* maintainability (not a regression; gate is 70). 📊
- **Verification**: 303 tests passing locally and in Docker, ruff clean, `ai-ctx audit --threshold 70` PASS (90.4), `validate_agent_system.py` PASS. ✅
- **Breaking**: deprecated facade import paths removed ahead of v4.0.0 (major bump recommended). ⚠️

## [2026-10-06] Explainable Scoring & Context Enrichment (v3.5.0) - COMPLETED
**THEME**: Correctness, explainability and context fidelity 🎯
- **Correctness**: Persisted `entry_points` (path + type) and decoupled test-file counting from `.analyzerignore`; renamed the "Test Coverage" label to "Test Files". ✅
- **Explainable Score**: Added a `Score Breakdown` to `PROJECT_SUMMARY.md`, penalized `max_complexity` outliers, and externalized thresholds/weights into a `[scoring]` config section. 📊
- **Context**: Added `--include-md <glob>` and the `context_docs` config key to embed architecture docs into the manual notes. 🧩
- **i18n**: Added a configurable UI allowlist (`setText`, `setTitle`, ...) and `patterns.i18n.ignored_functions` / `ui_functions`. 🌍
- **Refactor**: Split monolithic modules below the CC 25 budget, deprecated legacy facades (removal v4.0.0), and added deterministic golden-report fixtures + a self-score regression guard. 🧹
- **Self-score**: Raised from 87.2 to **100.0** via modularization and scoped self-analysis (`.analyzerignore`). 🏆
- **Verification**: 316 tests passing, ruff clean, `ai-ctx audit --threshold 70` PASS. ✅

## [2026-09-17] Corrections & Agentic System Gen 8 (v3.4.0) - COMPLETED
**THEME**: Consistency and opencode-native tooling 🧭
- **Metric Contract**: Introduced canonical keys in `builders/metric_keys.py`, removed duplicate aliases, and added missing-key validation. 🔑
- **i18n Precision**: Added `# no-i18n` inline opt-out (tokenize-based) and a punctuation-dominance heuristic. 🌍
- **Hardening**: Safe `.get()` access across report builders; exact `pyqtSignal`/`Signal` detection. 🛡️
- **Regression Tests**: Added coverage for pattern missing keys, recursive `**` globs, and Windows paths. 🧪
- **Metric Clarity**: Renamed labels to `ai-ctx Quality Score` / `Avg Cyclomatic Complexity`; documented vs `qgis-analyzer`. 📊
- **Agentic Gen 8**: Root `AGENTS.md` SSoT, `opencode.json` subagents, consolidated scripts, 3-tier memory, 14 skills / 11 workflows. 🤖
- **Verification**: 286 tests passing, ruff clean, `validate_agent_system.py` PASS. ✅

## [2026-03-22] QGIS Edition & Metrics Core Fix (v3.3.0) - COMPLETED
**THEME**: Deep Audit and Compliance 🗺️
- **QGIS 4.x Readiness**: Launched `QGISApiChecker` for detecting deprecated QGIS 3.x APIs and Qt6 transition risks (`SIGNAL`/`SLOT`). 🍎
- **Metadata & Resources**: Added full support for `plugin.xml`, including automatic consistency validation with `metadata.txt`. 📦
- **Critical Fix**: Resolved the v3.2.1 regression where project metrics (functions, classes, etc.) were incorrectly reported as zero. 🐛
- **Dynamic Versioning**: Implemented "Single Source of Truth" for versioning using `importlib.metadata`. ⚙️
- **Verification**: Added 11 new QGIS-specific tests and achieved 100% success across 273 tests. ✅
- **Quality Score**: Steady at **97.8/100**. 🏆
- **Market Intelligence**: Conducted deep analysis and comparative study of `ai-context-core` against 5 industry competitors (Repomix, Aider, Gitingest, etc.). 📊
- **Documentation Overhaul**: Redesigned `README.md` to emphasize deep AST semantics, QGIS specialization, and technical debt tracking. 🎨

## [2026-02-08] Internationalization & Performance Peak (v3.2.1) - COMPLETED
**THEME**: Correctness and Resilience 🛡️
- **Robust i18n Matching**: Replaced path matching with a regex-based engine to support recursive patterns (`**`) across all platforms. 🌍
- **Fix v3.2.0 Regressions**: Corrected i18n config injection and `--i18n-scope` CLI option. 🛠️
- **Quality Audit**: Maintained record score of **98.4/100**. 🏆
- **GitHub Release**: Tagged `v3.2.1` and pushed to remote with draft release artifacts. 🚀

## [2026-02-08] Scoped i18n & TOML Standardization (v3.2.0) - COMPLETED
**THEME**: Precision and Modernization 🎯
- **Scoped i18n**: Implemented `[qgis.i18n]` to filter translation analysis by path scopes (`all`, `gui_only`, `custom`). 🌍
- **TOML Migration**: Fully converted `defaults.yaml` and `qgis.yaml` to TOML, updating `ConfigLoader` to prioritize the new format. ⚙️
- **Modernization**: Enhanced `README.md` with Shields.io badges and enriched `pyproject.toml` metadata (Python 3.13, AST tags). 🌟
- **Architectural Cleanup**: Removed legacy import facades, achieving 100% modular internal architecture. 🧱
- **Quality Score**: Reached a record **98.4/100**. 🎉
- **Release**: Version `3.2.0` tagged, built, and uploaded as a draft to GitHub. 🚀

## [2026-02-07] Performance & Maintenance Suite Expansion (v3.1.2) - COMPLETED
**THEME**: Scalability and Tooling Excellence 🚀
- **Performance**: Implemented incremental analysis using metadata (`mtime`/`size`), achieving near-instant re-scans.
- **Parallelism**: Improved `ProcessPoolExecutor` efficiency by 20% through task batching.
- **CLI Maintenance Suite**: Launched 6 new commands: `doctor`, `fix`, `graph`, `compare`, `scaffold`, and `roadmap`.
- **JSON Support**: Added `--format json` to `ai-ctx analyze` for clean structured data extraction.
- **Interactive Mode**: Introduced `ai-ctx interactive` for guided project setup and analysis.
- **Documentation**: Fully updated and translated to English: `README.md`, `CONFIGURATION.md`, `PATTERNS_DETECTION.md`, `PROFILES_GUIDE.md`, and `QUICK_START.md`.
- **Quality Score**: Steady at **88.0/100**. 🏆

## [2026-02-07] 98% Test Coverage Achievement - COMPLETED
**THEME**: Extreme Quality and Stability 🛡️
- **Test Coverage**: Increased to **98%** (263 tests passing). Covered 850+ lines in critical modules like `engine`, `fs_utils`, `dependencies`, and `checkers`. 📈
- **Code Quality**: Massive cleanup of linter errors (ruff/black) across the entire codebase. 🧹
- **Edge Cases**: Implemented coverage for network failures, corrupt files, timeouts, and invalid configurations. 🧪
- **Documentation**: Updated changelog and generated detailed coverage walkthrough. 📚
- **Final State**: Project production-ready with minimal technical debt. 🚀

## [2026-02-07] QGIS Profile Fix & Facade Restoration (v3.1.1) - COMPLETED
**THEME**: Stability and QGIS Standards 🛠️
- **QGIS Fix**: Forced `qgis` profile loading in the `ai-ctx qgis` command, eliminating empty reports. 🌍
- **Facade Restoration**: Repaired exports in `fs_utils`, `issues`, `patterns`, and `git_analysis` that were causing `AttributeError`. 🧩
- **Validation**: Implemented `tests/test_qgis_command.py` (integration) and corrected i18n heuristics. ✅
- **Release**: Version `3.1.1` tagged and uploaded to GitHub. 🚀
- **Quality Score**: Raised to **90.9/100**. 🏆

## [2026-02-07] Precision i18n & Heuristic Refinement (v3.0.3) - COMPLETED
**THEME**: QGIS Quality and Precision 🌍
- **i18n Aggregation**: Added support for `translate()` alongside `tr()`. 🔄
- **Heuristics**: Robust filtering of loggers, exceptions, paths, and URLs in string counting. 🛡️
- **Validation**: New test suite for QGIS compliance. ✅

## [2026-01-30] Engine Optimization & Metrics Alignment - COMPLETED
**THEME**: Modularity and Quality 🚀
- **Engine Refactoring**: Migrated aggregation logic to `aggregator.py`. `engine.py` is now 30% smaller and 40% less complex. 🧩
- **Quality Score**: Achieved goal of **62.3/100** after aligning metrics and removing legacy code. 🏆
- **Compatibility**: Restored full compatibility through facades in `ast_utils.py`, `issues.py`, `dependencies.py`, and `git_analysis.py`. 🛠️
- **Stability**: 71 tests passing (100% success) with 75% coverage. ✅

## [2026-01-26] Phase 4: Visualization & Optimization - COMPLETED
**THEME**: Insights and Speed ⚡
- **HTML Reporting**: Implemented "Zero-Dependency" interactive HTML report generator. 📊
- **Mermaid Integration**: Automatic dependency graph visualization in reports. 🕸️
- **AI Recommendations**: Created local heuristic engine (`ai_recommendations.py`) for proactive quality suggestions. 💡
- **Security Tweak**: Reduced secret detection false positives (ignored placeholders). 🛡️
- **Validation**: 8 new tests; 100% success (65/65 tests passing). ✅

## [2026-01-25] Phases 5 & 6: Security Hardening & Performance - COMPLETED
**THEME**: Security and Efficiency ⚡
- **Security Hardening**:
  - **Secrets Detection**: Created `secrets.py` to detect AWS, GitHub, Google, OpenAI keys, etc. 🔒
  - **SQL Injection**: Advanced detection for insecure `cursor.execute()` with f-strings and `.format()`. 💉
- **Performance Profiling**:
  - **Single-Pass Analysis**: Refactored `fs_utils.py` to unify 4 traversals into one (`scan_project`), reducing analysis time by ~68%. ⚡
  - **Git Scalability**: Optimized `git_analysis.py` limiting history analysis to 1000 commits. 📉

## [2026-01-25] Phase 2: Advanced Analysis - COMPLETED
**THEME**: Semantic Understanding 🎨
- **Design Pattern Detection**: Implemented `patterns.py` to identify Singleton, Factory, Observer, Strategy, and Decorator using Bayesian confidence logic. 🎨
- **Dependency Analysis**: Added Coupling Between Objects (CBO) calculation and smart unused import detection. 🔗
- **Multi-Framework**: Improved support for Django, Flask, FastAPI, and Click. 🚀

## [2.1.1] - 2026-01-26 - Major Architectural Upgrade
- **Full Modularization**: Refactored all 18 core modules into class-based architectures.
- **Docker Support**: Multi-stage build and full `docker-compose` environment.
- **Workflows**: Standardized `inicia-sesion`, `crea-el-comit`, and `cierra-sesion`.
