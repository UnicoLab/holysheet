# Changelog

All notable changes to HolySheet are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] — 2026-05-21

### :sparkles: First Public Release

The initial release of HolySheet — a Python-first report compiler that generates beautiful, portable, interactive React dashboards.

### Added

#### Core

- **`Report` class** — Main entry point for composing dashboards with method chaining
- **26 block types** organized into 5 categories (KPI/Metrics, Charts, Data/Content, Layout, Interactive)
- **3 built-in themes** — `dark`, `light`, `executive` — each with a complete design system
- **3 export modes** — Standalone HTML, folder, and JSON
- **CLI** — `holysheet validate`, `holysheet serve`, `holysheet version`

#### Block Types

**KPI & Metrics:**

- `KPI` — Key performance indicator cards with delta and status colors
- `Metric` — Compact inline metrics for dense grids
- `StatComparison` — Side-by-side current vs previous comparison

**Charts (powered by Apache ECharts):**

- `LineChart` — Multi-series line charts
- `AreaChart` — Filled area charts
- `BarChart` — Grouped/stacked bar charts
- `PieChart` — Pie/donut charts
- `ScatterChart` — Scatter/bubble plots
- `RadarChart` — Radar/spider charts
- `GaugeChart` — Speedometer gauges with thresholds
- `FunnelChart` — Conversion funnel charts
- `TreemapChart` — Hierarchical treemaps

**Data & Content:**

- `DataTable` — Interactive, searchable, paginated data tables
- `Markdown` — Rich text content with full Markdown support
- `CodeBlock` — Syntax-highlighted code display
- `Image` — Image display with captions
- `Alert` — Callout blocks (info, success, warning, error)
- `ProgressBar` — Progress indicators with custom colors

**Layout:**

- `Section` — Grouping container with heading and description
- `Columns` — Multi-column responsive grid (equal, bento, custom widths)
- `Tabs` — Tabbed content panels
- `Divider` — Visual separators with optional labels
- `Accordion` — Collapsible panels for progressive disclosure

**Interactive:**

- `Slider` — Single value and range sliders
- `NumberInput` — Numeric input with increment/decrement
- `Toggle` — On/off switches

#### Data Support

- **Pandas DataFrames** — Auto-conversion via `.to_dict(orient='records')`
- **Polars DataFrames** — Auto-conversion via `.to_dicts()`
- **`list[dict]`** — Pass-through with value sanitization
- **`dict[str, list]`** — Column-oriented to row-oriented conversion
- **Value sanitization** — Automatic handling of NaN, Inf, Decimal, datetime, numpy scalars

#### Architecture

- **Pydantic v2** models for all blocks with full type safety and validation
- **JSON schema spec** (v1.0.0) consumed by the React renderer
- **Pre-built React bundle** — No Node.js required at runtime
- **Jinja2 templates** for HTML generation
- **orjson** for fast JSON serialization

#### Developer Experience

- Full type hints throughout the codebase
- Comprehensive docstrings
- Custom exception hierarchy (`HolySheetError`, `DataConversionError`, `ExportError`, etc.)
- `loguru` debug logging

### Dependencies

| Package | Version |
|:--------|:--------|
| `pydantic` | ≥ 2.0, < 3.0 |
| `jinja2` | ≥ 3.1, < 4.0 |
| `orjson` | ≥ 3.9, < 4.0 |
| `loguru` | ≥ 0.7, < 1.0 |
| `click` | ≥ 8.1, < 9.0 |

**Optional:**

| Extra | Package | Version |
|:------|:--------|:--------|
| `pandas` | `pandas` | ≥ 2.0 |
| `polars` | `polars` | ≥ 0.20 |

---

## Roadmap

Planned for future releases:

- :material-chart-sankey: Additional chart types (Sankey, Gantt, DAG, Heatmap)
- :material-robot: AI narrative blocks (auto-generated insights)
- :material-filter: Interactive filters and cross-chart drill-down
- :material-file-pdf-box: PDF export
- :material-presentation: PowerPoint export
- :material-puzzle: Custom React component injection
- :material-palette-swatch: Enterprise theme gallery + custom theme API
- :material-lock: Signed / offline report bundles
- :material-chat: Local chatbot over report data

---

<div style="text-align: center; margin-top: 2rem; color: var(--md-default-fg-color--lighter);">
<em>Holy Sheet, that's a beautiful changelog!</em> :raised_hands:
</div>
