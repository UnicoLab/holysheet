# Changelog

All notable changes to HolySheet are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.4.0] — 2026-05-21

### :sparkles: Features, Templates & CLI (53 Block Types)

A feature-packed release that adds custom themes, multi-page reports, global filters, report templates, new CLI commands, Jupyter integration, and 6 new block types.

### Added

#### New Block Types (6 new → 53 total)

**Charts (3 new → 18 total):**

- `GanttChart` — Project timeline / Gantt chart with task progress bars
- `DAGChart` — Directed acyclic graph for workflows and dependency trees
- `CorrelationMatrix` — Statistical correlation heatmap (2D matrix)

**Data & Content (2 new → 14 total):**

- `Scorecard` — Conditional color metric grid with configurable thresholds
- `DataProfile` — Auto-EDA summary with per-column statistics

**Layout (1 new → 8 total):**

- `Compare` — Side-by-side comparison container with labeled panels

#### Custom Theme API

- `Theme` class for building fully branded dashboards
- Extends any built-in theme (`dark`, `light`, `executive`) with custom overrides
- Supports: colors (14 tokens), fonts (body, heading, mono), chart palette
- Pass `Theme` instances directly to `Report(theme=...)`

#### Multi-Page Reports

- `Report.add_page(label, children)` for tabbed / sidebar navigation
- Sidebar navigation auto-generated from page labels
- Full support for nested blocks within pages

#### Global Filters

- `Report.add_filter(key, type, label, options, default)`
- Filter types: `dropdown`, `date_range`, `text`
- Filters rendered in the report header, affecting all blocks

#### Feature Flags

- `theme_switch=True` — Dark/light mode toggle for viewers
- `presentation_mode=True` — Fullscreen slideshow mode
- `download_buttons=True` — Per-block CSV/PNG export

#### Report Security & Distribution

- `password="..."` — Client-side AES encryption with PBKDF2 key derivation
- `expires="2026-12-31"` — Expiration date overlay
- `compress=True` — Gzip-compress embedded JSON data

#### Widget Export

- `Report.export_widget(path, block_ids)` — Lightweight embeddable widgets
- Filter to specific block IDs for minimal, targeted embeds

#### Jupyter Integration

- `_repr_html_()` — Auto-display in Jupyter notebooks
- `Report.show(height)` — Explicit rendering with custom iframe height
- Base64-encoded iframe for full CSS isolation

#### CLI Commands (3 new → 6 total)

- `holysheet dev SCRIPT` — Hot-reload dev server with live rebuild
- `holysheet lint SOURCE [--strict]` — Report linter with 7 rules
- `holysheet diff FILE_A FILE_B` — Compare two JSON spec files

#### Report Templates

- `SalesDashboard` — KPIs, revenue trend, pipeline funnel, top clients
- `ExecutiveSummary` — Scorecards, highlights, trends, milestones
- `OpsMonitor` — Service health, gauges, error rate, latency, SLOs

### Changed

- Updated block overview from 47 to 53 block types
- Updated chart reference from 15 to 18 chart types
- Updated data & content reference from 12 to 14 types
- Updated layout reference from 7 to 8 types
- Added Features, Templates, and CLI documentation pages
- Updated `mkdocs.yml` navigation with new pages

---

## [0.3.0] — 2026-05-21

### :sparkles: 21 New Block Types (47 Total)

A massive expansion that nearly doubles the available block types, adding advanced charts, content blocks, and interactive controls.

### Added

#### Charts (6 new → 15 total)

- `HeatmapChart` — 2D heatmap with color gradient visualization
- `CandlestickChart` — Financial OHLC candlestick charts (green/red)
- `SankeyChart` — Flow / energy diagrams with node-link architecture
- `WaterfallChart` — Revenue bridge / waterfall analysis charts
- `BoxPlotChart` — Statistical box-and-whisker distribution plots
- `MapChart` — Geographical scatter with bubble sizing

#### Content & Display (8 new → 14 total)

- `Timeline` — Vertical event/milestone timeline with colored markers
- `Callout` — Styled quotes, highlights, and notes (3 variants)
- `Embed` — iframe embedding with aspect ratio support
- `JsonViewer` — Interactive JSON tree with syntax highlighting
- `UserCard` — Team member cards with avatar and stats
- `StatusList` — Service health indicators with colored dots
- `InfoList` — Key-value pair display with icons
- `Stepper` — Process/wizard step visualization

#### Interactive (4 new → 7 total)

- `Dropdown` — Select from options with local state
- `TextInput` — Text/textarea input with placeholder
- `CheckboxGroup` — Multiple checkbox selection
- `RadioGroup` — Single-select radio buttons

#### Display (3 new)

- `TagList` — Colored tag/badge chips
- `Sparkline` — Compact inline mini-charts (ECharts)
- `Video` — HTML5 video embed with poster and controls

### Changed

- Updated `full_showcase.py` example to demonstrate all 47 block types
- Updated frontend registry and size category mappings
- Rebuilt React frontend bundle with all new components
- 138 tests (21 new for new blocks)
- Complete MkDocs Material documentation (14 pages)

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

- :material-robot: AI narrative blocks (auto-generated insights)
- :material-file-pdf-box: PDF export
- :material-presentation: PowerPoint export
- :material-puzzle: Custom React component injection
- :material-lock: Signed / offline report bundles
- :material-chat: Local chatbot over report data
- :material-earth: i18n / localization support
- :material-api: Webhook-triggered report rebuilds

**Shipped in v0.4.0:** ~~Interactive filters~~, ~~Custom theme API~~, ~~Gantt chart and DAG visualization~~

---

<div style="text-align: center; margin-top: 2rem; color: var(--md-default-fg-color--lighter);">
<em>Holy Sheet, that's a beautiful changelog!</em> :raised_hands:
</div>
