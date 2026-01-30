# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python learning repository containing code examples and exercises from the book "Pythonic Programming". The codebase demonstrates idiomatic Python patterns and best practices across various domains.

Always use Context7 MCP when I need library/API documentation, code generation, setup or configuration steps without me having to explicitly ask.

## Development Commands

### Package Management
- Install dependencies: `uv sync`
- Install dev dependencies: `uv sync --group dev`

### Testing
- Run all tests: `pytest`
- Run tests with coverage: `pytest --cov=pythonic --cov-report=term-missing`
- Coverage must be ≥80% (configured in pyproject.toml)

### Code Quality
- Lint and format: `ruff check --fix && ruff format`
- Type checking: `mypy pythonic/`
- Pre-commit hooks: `pre-commit run --all-files`

### Building
- Build package: `uv build`

## Code Architecture

### Module Organization

The `pythonic/` package is organized by topic, with each module demonstrating specific Python concepts:

- **common.py**: Shared utilities (e.g., `assert_throw` for exception testing)
- **data.py**: Data structures and types (tuples, strings, collections, Counter, complex numbers, fractions, infinity/NaN handling)
- **documentation.py**: Documentation practices (docstrings, constants, enums)
- **function.py**: Function design patterns (return types, parameters, generators, lambdas)
- **general.py**: General Python idioms (iteration, comprehensions, conditional expressions, pickle serialization, string operations)
- **performance.py**: Performance optimization (timeit, caching with pickle/hashlib, checkpointing, sorting, garbage collection)
- **safety.py**: Safe coding practices (global variables, truthiness, file handling with context managers, private fields, properties)

### Key Patterns

**Import Structure**: Modules import from `common.py` for shared utilities. Note that some imports use relative imports (e.g., `from common import assert_throw`) which may need adjustment depending on execution context.

**Executable Modules**: Many modules contain executable code at the module level (not just in `if __name__ == "__main__"` blocks), demonstrating concepts through direct execution.

**Type Annotations**: The codebase uses modern Python 3.13 features including PEP 695 type parameter syntax (e.g., `def assert_throw[T: Exception]`).

## Configuration Notes

- **Python Version**: Requires Python ≥3.13
- **Build System**: Uses `uv_build` as the build backend
- **Linting**: Ruff is configured with per-file ignores (tests can use assertions, documentation.py allows unused imports)
- **Type Checking**: mypy strict mode is enabled
- **Coverage**: Source is `pythonic/`, `__init__.py` files are omitted, branch coverage is enabled

## Testing Approach

Tests should be placed in the `tests/` directory (currently empty). When writing tests:
- Use pytest fixtures and parametrization
- Test utilities like `assert_throw` from `common.py` can verify exception behavior
- Maintain ≥80% coverage threshold
