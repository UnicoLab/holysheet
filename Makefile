.PHONY: install frontend-install frontend-build test lint typecheck build clean dev wheel release-check

# Python setup (using uv if available, fallback to pip)
install:
	uv pip install -e ".[dev]" 2>/dev/null || pip install -e ".[dev]"

# Frontend setup
frontend-install:
	cd frontend && npm install

# Frontend build and copy assets to renderer
frontend-build:
	cd frontend && npm run build
	rm -rf src/holysheet/renderer/assets
	mkdir -p src/holysheet/renderer/assets
	cp frontend/dist/index.html src/holysheet/renderer/index.html
	cp frontend/dist/assets/*.js src/holysheet/renderer/assets/app.js
	cp frontend/dist/assets/*.css src/holysheet/renderer/assets/app.css 2>/dev/null || touch src/holysheet/renderer/assets/app.css

# Run tests
test:
	pytest tests/ -v --tb=short

# Run tests with coverage
test-cov:
	pytest tests/ -v --tb=short --cov=holysheet --cov-report=html --cov-report=term

# Lint
lint:
	ruff check src/ tests/ examples/
	ruff format --check src/ tests/ examples/

# Format
format:
	ruff check --fix src/ tests/ examples/
	ruff format src/ tests/ examples/

# Type check
typecheck:
	mypy src/holysheet/ --ignore-missing-imports

# Build wheel and sdist
build: frontend-build
	python -m build

# Build and verify wheel contents
wheel: build
	@echo "Verifying wheel contents..."
	pip install dist/*.whl --force-reinstall
	python -c "import holysheet; from pathlib import Path; p=Path(holysheet.__file__).parent; assert (p/'renderer'/'assets'/'app.js').exists(); print('✓ Wheel verified')"

# Semantic release dry-run
release-check:
	semantic-release version --no-commit --no-tag --no-push --no-vcs-release

# Clean
clean:
	rm -rf dist/ build/ *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +

# Development: build frontend and install package in editable mode
dev: frontend-install frontend-build install
