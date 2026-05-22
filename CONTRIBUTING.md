# Contributing to HolySheet

Thank you for your interest in contributing to HolySheet! 🎉

## Development Setup

### Prerequisites

- **Python 3.11+** — for the core library
- **Node.js 18+** — for frontend development only
- **Make** — for running development commands

### Quick Setup

```bash
git clone https://github.com/UnicoLab/holysheet.git
cd holysheet

# Full setup (frontend + Python)
make dev

# Or step by step:
make frontend-install   # Install npm dependencies
make frontend-build     # Build React app → src/holysheet/renderer/
make install            # Install Python package in editable mode
```

### Running Tests

```bash
make test              # Run test suite
make lint              # Lint with ruff
make typecheck         # Type-check with mypy (strict)
make format            # Auto-format with ruff
```

---

## How to Contribute

### 1. Find or Create an Issue

- Browse [open issues](https://github.com/UnicoLab/holysheet/issues)
- For new features, open an issue first to discuss the approach
- Issues labeled `good first issue` are great starting points

### 2. Fork & Branch

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR-USERNAME/holysheet.git
cd holysheet
git checkout -b feat/your-feature-name
```

### 3. Make Your Changes

- **Python code** lives in `src/holysheet/`
- **React components** live in `frontend/src/components/`
- **Tests** go in `tests/`
- **Documentation** goes in `docs/`

### 4. Write Tests

All new features and bug fixes should include tests:

```bash
make test                     # Run full suite
pytest tests/test_blocks.py   # Run specific test file
```

### 5. Check Quality

```bash
make lint       # ruff check
make format     # ruff format
make typecheck  # mypy --strict
```

### 6. Commit with Conventional Commits

We use [Conventional Commits](https://www.conventionalcommits.org/) for automatic versioning:

| Prefix | Effect | Example |
|--------|--------|---------|
| `feat:` | Minor version bump | `feat: add RadarChart block` |
| `fix:` | Patch version bump | `fix: handle NaN in data tables` |
| `perf:` | Patch version bump | `perf: optimize JSON serialization` |
| `docs:` | No version bump | `docs: update theme examples` |
| `test:` | No version bump | `test: add BarChart edge cases` |
| `ci:` | No version bump | `ci: fix PyPI publish workflow` |
| `BREAKING CHANGE:` | Major version bump | `feat!: rename export_html to render` |

### 7. Open a Pull Request

- Push your branch and open a PR against `main`
- Fill in the PR template
- Ensure all CI checks pass
- Request a review

---

## Architecture Overview

```
Python API  →  Pydantic v2 Schema  →  JSON Spec  →  React Renderer  →  HTML Dashboard
```

### Key Directories

| Path | Description |
|------|-------------|
| `src/holysheet/` | Core Python package |
| `src/holysheet/blocks.py` | All 57 block type models (Pydantic v2) |
| `src/holysheet/report.py` | Main `Report` class |
| `src/holysheet/renderer/` | Prebuilt React assets (bundled at build time) |
| `frontend/src/` | React source code |
| `frontend/src/components/` | Block components (one per block type) |
| `tests/` | Python test suite |
| `docs/` | MkDocs documentation |
| `examples/` | Example Python scripts |

### Adding a New Block Type

1. Define the Pydantic model in `src/holysheet/blocks.py`
2. Register it in `src/holysheet/__init__.py`
3. Create the React component in `frontend/src/components/`
4. Register it in `frontend/src/registry.tsx`
5. Add tests in `tests/`
6. Document in `docs/blocks/`

---

## Code Style

- **Python**: Ruff (replaces flake8, isort, black), line length 100
- **TypeScript**: Prettier + ESLint
- **Commits**: Conventional Commits format
- **Docstrings**: Google style

## Questions?

- Open a [Discussion](https://github.com/UnicoLab/holysheet/discussions)
- Check the [Documentation](https://unicolab.github.io/holysheet/)

---

Thank you for helping make HolySheet better! 🙌
