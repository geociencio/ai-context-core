# Design Patterns Detection Guide

This document describes how `ai-context-core` detects architectural design patterns in Python code using Abstract Syntax Tree (AST) analysis.

## Overview

The detection system looks for linguistic and structural "evidence" within classes and functions to estimate the likelihood of a specific pattern being implemented. Each pattern has a **confidence score** based on the accumulation of this evidence.

## Supported Patterns

### 1. Singleton
Ensures a class has only one instance and provides a global point of access to it.

*   **Evidence:**
    *   Overriding `__new__` (Score: 60)
    *   Methods like `get_instance`, `instance` (Score: 30)
    *   Static instance variables like `_instance` (Score: 20)
*   **Threshold:** >50% confidence.

### 2. Factory
Provides an interface for creating objects in a superclass but allows subclasses to alter the type of objects that will be created.

*   **Evidence:**
    *   Class name includes "Factory" (Score: 30)
    *   Method names like `create_*`, `build_*`, `make_*` (Score: 40)
    *   Method contains a `return` statement that calls a constructor (Score: 30)
*   **Threshold:** >60% confidence.

### 3. Observer
Defines a subscription mechanism to notify multiple objects about any events that happen to the object they’re observing.

*   **Evidence:**
    *   Initializing collections like `self.subscribers` or `self.observers` (Score: 20)
    *   Management methods like `subscribe`, `attach`, `register` (Score: 15 per method)
    *   A loop inside a `notify` or `emit` method that iterates over the collection (Score: 30)
*   **Threshold:** >50% confidence.

### 4. Strategy
Defines a family of algorithms, puts each of them into a separate class, and makes their objects interchangeable.

*   **Evidence:**
    *   Dependency injection of an object via `__init__` or `set_*` methods (Score: 30)
    *   Delegating work to the injected object in other methods (Score: 40)
*   **Threshold:** >50% confidence.

### 5. Decorator (Wrapper)
Lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.

*   **Evidence (Function-based):**
    *   Function contains an inner function and returns it (Score: 50)
    *   Use of `@functools.wraps` (Score: 40)
*   **Evidence (Class-based):**
    *   Class implements both `__init__` (accepting a callable) and `__call__` (Score: 60)
*   **Threshold:** >50% confidence.

## Limitations

Since detection is based on **static analysis** (source code only, no execution), it may produce false positives if naming conventions are used without implementing the actual logic, or false negatives for highly dynamic or unconventional implementations.
