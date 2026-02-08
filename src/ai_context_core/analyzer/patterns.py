from .visitors import patterns as _v_patterns

detect_patterns = _v_patterns.detect_patterns
detect_singleton = _v_patterns.detect_singleton
detect_factory = _v_patterns.detect_factory
detect_observer = _v_patterns.detect_observer
detect_strategy = _v_patterns.detect_strategy
detect_decorator = _v_patterns.detect_decorator

PatternsUnifiedVisitor = _v_patterns.PatternsUnifiedVisitor
