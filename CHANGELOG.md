# CHANGELOG


## v0.2.1 (2026-05-21)

### Bug Fixes

- Correct pyproject.toml version to 0.3.0 (was reverted during rebase)
  ([`7805f69`](https://github.com/UnicoLab/holysheet/commit/7805f690b52a1300dbb712aa43b8c4a25d1e902c))

### Documentation

- Update all documentation for v0.3.0 (47 block types)
  ([`79b51fd`](https://github.com/UnicoLab/holysheet/commit/79b51fde1c28a6f52efa323eaa290e2d2025dd54))

- Updated charts.md with 6 new chart types (HeatmapChart, CandlestickChart, SankeyChart,
  WaterfallChart, BoxPlotChart, MapChart) - Updated data-content.md with 11 new content blocks
  (Timeline, Callout, Embed, JsonViewer, UserCard, StatusList, InfoList, Stepper, TagList,
  Sparkline, Video) - Updated interactive.md with 4 new interactive blocks (Dropdown, TextInput,
  CheckboxGroup, RadioGroup) - Updated blocks/index.md with all 47 block types - Updated
  api-reference.md with 21 new constructor signatures - Updated changelog.md with v0.3.0 release
  notes - Updated index.md landing page (47 blocks, 15 charts) - Updated getting-started.md block
  count reference - Updated README.md with complete block reference


## v0.2.0 (2026-05-21)

### Features

- Add 21 new block types (47 total) + comprehensive docs
  ([`484e2c7`](https://github.com/UnicoLab/holysheet/commit/484e2c7159f893645b9783d34850e36b567979bc))

New chart blocks: - HeatmapChart: 2D heatmap with color gradient visualization - CandlestickChart:
  Financial OHLC candlestick charts - SankeyChart: Flow/energy diagrams - WaterfallChart: Revenue
  bridge / waterfall analysis - BoxPlotChart: Statistical distribution visualization - MapChart:
  Geographical scatter plots

New content blocks: - Timeline: Vertical event/milestone timeline - Callout: Styled quotes and
  highlights (3 variants) - Embed: iframe embedding with aspect ratio support - JsonViewer:
  Interactive JSON tree with collapsible levels - UserCard: Team member cards with avatar and stats
  - StatusList: Service health indicators with colored dots - InfoList: Key-value pair display -
  Stepper: Process/wizard step visualization

New interactive blocks: - Dropdown: Select from options with local state - TextInput: Text/textarea
  input with local state - CheckboxGroup: Multi-select checkboxes - RadioGroup: Single-select radio
  buttons

New display blocks: - TagList: Colored tag/badge chips - Sparkline: Compact inline mini-charts -
  Video: HTML5 video embed with controls

Also includes: - Version bump to 0.3.0 - 138 tests (21 new for new blocks) - Full MkDocs Material
  documentation (14 pages, 3560 lines) - Updated full_showcase.py with all new blocks - Updated
  frontend registry and size categories - Rebuilt frontend bundle with all components


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
