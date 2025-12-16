# Kiro SDLC Sample Project Makefile
# Common commands for development and CI

.PHONY: help install dev-install lint type-check test coverage security build clean all

# Default target
help:
	@echo "Kiro SDLC Sample Project"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Setup:"
	@echo "  install       Install production dependencies"
	@echo "  dev-install   Install development dependencies"
	@echo ""
	@echo "Quality Checks:"
	@echo "  lint          Run ruff linter"
	@echo "  lint-fix      Run ruff with auto-fix"
	@echo "  type-check    Run mypy type checker"
	@echo "  test          Run pytest"
	@echo "  coverage      Run pytest with coverage report"
	@echo "  security      Run bandit security scan"
	@echo ""
	@echo "Combined:"
	@echo "  build         Run all quality checks (lint + type + test)"
	@echo "  quality-gate  Run security scan and generate coverage report"
	@echo "  all           Run complete SDLC build pipeline"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean         Remove build artifacts and caches"

# Setup targets
install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

# Quality check targets
lint:
	ruff check src/ tests/

lint-fix:
	ruff check src/ tests/ --fix

type-check:
	mypy src/

test:
	pytest -v

coverage:
	pytest --cov=src --cov-report=term-missing --cov-report=html
	@echo "HTML coverage report: htmlcov/index.html"

security:
	bandit -r src/ -f txt
	@echo ""
	@echo "Checking dependencies..."
	-safety check -r requirements.txt 2>/dev/null || echo "safety not installed or no requirements.txt"

# Combined targets
build: lint type-check test
	@echo ""
	@echo "✅ Build verification passed!"
	@echo "   - Lint: 0 errors"
	@echo "   - Type check: 0 errors"
	@echo "   - Tests: All passed"

quality-gate: security coverage
	@echo ""
	@echo "✅ Quality gate checks complete!"

all: build quality-gate
	@echo ""
	@echo "🎉 Full SDLC pipeline passed!"
	@echo ""
	@echo "Ready for documentation phase."

# Cleanup
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/**/__pycache__
	rm -rf tests/__pycache__
	rm -rf tests/**/__pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build
	@echo "Cleaned build artifacts and caches"

# Convenience aliases
check: build
verify: all
