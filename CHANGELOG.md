# CHANGELOG


## v0.1.0 (2026-05-21)

### Features

- Initial release — HolySheet v0.2.0
  ([`9e0972e`](https://github.com/UnicoLab/holysheet/commit/9e0972e5e5accdb228160e1c2d7443a21cee49f1))

Production-ready Python package that generates beautiful interactive HTML dashboards from Python
  data/config, without requiring Node.js or React.

## Core Features - 26 block types: KPI, Metric, 9 chart types, DataTable, Markdown, CodeBlock,
  Image, Alert, ProgressBar, Divider, Section, Columns, Tabs, Slider, NumberInput, Toggle,
  Accordion, StatComparison - 3 themes: dark, light, executive - Self-contained HTML export (single
  file, no dependencies) - Multi-column layouts with CSS Grid (equal, bento, custom widths) -
  Collapsible sections and tabs - Print/PDF export button - Responsive auto-adaptive layout system -
  Auto-grouping of consecutive same-type blocks

## Architecture - Python backend: Pydantic v2 models → JSON schema - React frontend: Pre-built,
  bundled in package (no Node.js at runtime) - Jinja2 templating for standalone HTML generation

## Package - 116 tests passing - CI/CD with GitHub Actions (lint, test, semantic-release) -
  PyPI-ready with bundled frontend assets
