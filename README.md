<p align="center">
  <img src="assets/holysheet_logo.png" alt="HolySheet Mascot" width="280" />
</p>

<h1 align="center">📊 HolySheet</h1>

<p align="center">
  <strong>Python-first report compiler that turns raw data into beautiful,<br>portable, interactive React dashboards — in a single line of code.</strong>
</p>

<p align="center">
  <img src="assets/holysheet_hero.png" alt="HolySheet — Data to Dashboard" width="680" />
</p>

<p align="center">
  <a href="https://pypi.org/project/holysheet"><img alt="PyPI" src="https://img.shields.io/pypi/v/holysheet?color=3B82F6&style=flat-square"></a>
  <a href="https://pypi.org/project/holysheet"><img alt="Python" src="https://img.shields.io/pypi/pyversions/holysheet?color=8B5CF6&style=flat-square"></a>
  <a href="https://github.com/UnicoLab/HolySheet/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/UnicoLab/HolySheet?color=10B981&style=flat-square"></a>
  <a href="https://github.com/UnicoLab/HolySheet/actions"><img alt="CI" src="https://img.shields.io/github/actions/workflow/status/UnicoLab/HolySheet/ci.yml?style=flat-square&label=CI"></a>
</p>

<p align="center">
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-block-reference">Block Reference</a> •
  <a href="#-examples">Examples</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-development">Development</a>
</p>

---

## ✨ What is HolySheet?

**HolySheet** generates stunning, self-contained, interactive HTML dashboards powered by React + ECharts — without requiring the end user to install Node.js, npm, or any frontend tooling.

> *Write your dashboard in Python. Get a gorgeous interactive report as a single HTML file.*  
> *No server. No dependencies. Just open it in a browser. Holy Sheet, that's easy!*

```python
from holysheet import Report, KPI, LineChart, DataTable

report = Report(title="Executive Portfolio Report", theme="dark")

report.add(KPI(label="Revenue", value=1_250_000, unit="€", delta="+12%", status="positive"))
report.add(LineChart(title="Revenue Trend", data=revenue_df, x="date", y="revenue"))
report.add(DataTable(title="Projects", data=projects_df))

report.export_html("report.html")  # ← That's it. Open in any browser.
```

---

## 🙏 Why HolySheet?

| 😩 The Problem | 😇 The HolySheet Way |
|---|---|
| Dashboards require complex frontend setup | **Zero** frontend knowledge needed |
| Reports need a running server | Self-contained HTML files — open anywhere |
| Visualization libraries produce basic charts | Enterprise-grade React UI with interactive ECharts |
| Sharing reports is painful | Single HTML file — email it, Slack it, embed it |
| Python-to-dashboard tools look dated | Modern Material UI design with dark/light/executive themes |
| Data wrangling across libraries | Native **Pandas**, **Polars**, dict, and list support |

---

## 🚀 Quickstart

### 1. Install

```bash
pip install holysheet
```

### 2. Build a dashboard

```python
from holysheet import Report, KPI, LineChart, BarChart, PieChart, DataTable, Section

report = Report(
    title="Q4 Business Review",
    subtitle="Revenue & Operations Dashboard",
    theme="dark",
    author="Data Team",
)

# KPI cards — they auto-arrange in a responsive grid
report.add(KPI(label="Total Revenue", value=2_450_000, unit="€", delta="+18%", status="positive"))
report.add(KPI(label="Active Clients", value=142, delta="+12", status="positive"))
report.add(KPI(label="Churn Rate", value=3.2, unit="%", delta="-0.5%", status="positive"))
report.add(KPI(label="NPS Score", value=72, delta="+5", status="positive"))

# Charts — pass any DataFrame or list of dicts
report.add(LineChart(title="Monthly Revenue", data=revenue_data, x="month", y="revenue"))
report.add(BarChart(title="Revenue by Region", data=region_data, x="region", y="revenue"))
report.add(PieChart(title="Revenue Split", data=split_data, name="category", value="amount"))

# Searchable, paginated data table
report.add(DataTable(title="Top Clients", data=clients_data, columns=["name", "revenue", "status"]))

# Export → a single portable HTML file
report.export_html("q4_review.html")
```

### 3. Open & share

```bash
open q4_review.html   # macOS
xdg-open q4_review.html  # Linux
start q4_review.html  # Windows
```

The HTML file is fully standalone — no server, no internet, no Node.js. Send it via email, upload to S3, embed in Confluence — it just works.

---

## 📦 Installation

```bash
# Core (zero extras)
pip install holysheet

# With Pandas support
pip install holysheet[pandas]

# With Polars support
pip install holysheet[polars]

# Everything
pip install holysheet[all]
```

**Requirements:**
- 🐍 Python **3.11+**
- 🚫 No Node.js required
- 🚫 No frontend build step
- 🚫 No running server

**Core dependencies:** `pydantic v2` · `jinja2` · `orjson` · `loguru` · `click`

---

## 🧱 Block Reference

HolySheet ships with **20 block types** organized into four categories:

### 📊 Charts

| Block | Description | Key Props |
|---|---|---|
| `LineChart` | Multi-series line chart | `data`, `x`, `y`, `series` |
| `AreaChart` | Filled area chart | `data`, `x`, `y`, `series` |
| `BarChart` | Grouped/stacked bar chart | `data`, `x`, `y`, `series` |
| `PieChart` | Pie / donut chart | `data`, `name`, `value` |
| `ScatterChart` | Scatter / bubble plot | `data`, `x`, `y`, `size`, `category` |
| `RadarChart` | Radar / spider chart | `data`, `indicators` |
| `GaugeChart` | Speedometer gauge | `value`, `min`, `max`, `thresholds` |
| `FunnelChart` | Conversion funnel | `data`, `name`, `value` |
| `TreemapChart` | Hierarchical treemap | `data`, `name`, `value`, `category` |

### 📈 Metrics

| Block | Description | Key Props |
|---|---|---|
| `KPI` | Key metric card with delta | `label`, `value`, `unit`, `delta`, `status` |
| `Metric` | Compact inline metric | `label`, `value`, `unit`, `icon` |
| `ProgressBar` | Progress indicator | `label`, `value`, `max`, `color` |

### 📝 Content

| Block | Description | Key Props |
|---|---|---|
| `DataTable` | Searchable, paginated table | `data`, `columns`, `searchable`, `paginated` |
| `Markdown` | Rich text content | `content` |
| `CodeBlock` | Syntax-highlighted code | `code`, `language`, `title` |
| `Image` | Image display | `src`, `alt`, `caption` |
| `Alert` | Callout / notification | `severity`, `title`, `message` |

### 📐 Layout

| Block | Description | Key Props |
|---|---|---|
| `Section` | Group blocks with a heading | `title`, `description`, `children` |
| `Columns` | Multi-column responsive grid | `children`, `widths` |
| `Tabs` | Tabbed content panels | `tabs` (list of `{label, children}`) |
| `Divider` | Visual separator line | `label`, `variant` |

---

## 🎨 Themes

Three built-in themes ship out of the box:

```python
report = Report(title="Report", theme="dark")       # 🌙 Deep dark, vibrant accents
report = Report(title="Report", theme="light")      # ☀️ Clean, professional, airy
report = Report(title="Report", theme="executive")  # 👔 Premium serif with rich greens
```

Each theme defines a complete design system: colors, typography (Inter / Georgia), spacing, shadows, and an 8-color chart palette.

---

## 📚 Examples

### Minimal Status Page

```python
from holysheet import Report, KPI, Markdown, Alert

report = Report(title="System Status", theme="dark")

report.add(Alert(severity="success", title="All Systems Operational", message="Last checked: 2 minutes ago"))
report.add(KPI(label="Uptime", value=99.97, unit="%", status="positive"))
report.add(KPI(label="Response Time", value=142, unit="ms", status="neutral"))
report.add(KPI(label="Error Rate", value=0.03, unit="%", delta="-0.01%", status="positive"))
report.add(Markdown(content="Monitored endpoints: **API**, **Auth**, **CDN**, **Database**"))

report.export_html("status.html")
```

### Executive Dashboard with Sections & Columns

```python
from holysheet import Report, KPI, LineChart, BarChart, DataTable, Section, Columns, Markdown

report = Report(
    title="AIFlow Executive Report",
    subtitle="Portfolio risk and delivery intelligence",
    theme="executive",
    author="Strategy Team",
)

# Executive summary
report.add(Markdown(content="""
## Executive Summary

Portfolio health remains strong with 42 active projects delivering on schedule.
Risk-adjusted returns are trending positively, with a 12% improvement in delivery confidence.
"""))

# KPI grid inside a section
report.add(Section(
    title="Key Metrics",
    children=[
        KPI(label="Active Projects", value=42, delta="+3", status="positive"),
        KPI(label="On-Track", value=87, unit="%", status="positive"),
        KPI(label="At-Risk", value=5, status="negative"),
        KPI(label="Budget Utilization", value=76, unit="%", status="neutral"),
    ],
))

# Side-by-side charts
report.add(Columns(children=[
    LineChart(title="Risk Score Trend", data=risk_df, x="date", y="score"),
    BarChart(title="Delivery by Team", data=team_df, x="team", y="delivered"),
]))

# Detailed data
report.add(DataTable(
    title="Project Details",
    data=projects_df,
    columns=["project", "owner", "risk", "status", "completion"],
))

report.export_html("executive_report.html")
```

### Multi-Chart Analytics with Tabs

```python
from holysheet import Report, Tabs, LineChart, BarChart, PieChart, FunnelChart

report = Report(title="Sales Analytics", theme="dark")

report.add(Tabs(tabs=[
    {
        "label": "📈 Trends",
        "children": [
            LineChart(title="Monthly Sales", data=sales_df, x="month", y="total"),
            LineChart(title="Customer Growth", data=growth_df, x="month", y="customers"),
        ],
    },
    {
        "label": "📊 Breakdown",
        "children": [
            BarChart(title="Sales by Region", data=region_df, x="region", y="sales"),
            PieChart(title="Product Mix", data=product_df, name="product", value="revenue"),
        ],
    },
    {
        "label": "🔄 Pipeline",
        "children": [
            FunnelChart(title="Sales Funnel", data=funnel_df, name="stage", value="count"),
        ],
    },
]))

report.export_html("sales_analytics.html")
```

> 💡 **More examples** in the [`examples/`](examples/) directory — including a full showcase with every block type.

---

## 📤 Export Modes

### Standalone HTML *(default)*

```python
report.export_html("report.html")
```

Generates a **single, self-contained HTML file** (~1.5 MB) with embedded React, CSS, and data. Zero external dependencies. Open directly in any browser.

### Folder Export

```python
report.export_folder("dist/")
```

Generates a deployable folder structure:

```
dist/
  index.html       ← Entry point
  assets/
    app.js         ← React bundle
    app.css        ← Styles
  report.json      ← Dashboard spec
```

Ideal for hosting on a web server, S3, or CDN.

### JSON Export

```python
report.export_json("report.json")
```

Exports just the dashboard specification as JSON. Useful for debugging, version control, or feeding into external rendering pipelines.

---

## 🗄️ Data Formats

HolySheet auto-detects and converts data from multiple formats:

```python
# ✅ List of dicts
data = [{"name": "Alice", "score": 95}, {"name": "Bob", "score": 87}]

# ✅ Dict of lists
data = {"name": ["Alice", "Bob"], "score": [95, 87]}

# ✅ Pandas DataFrame
import pandas as pd
data = pd.DataFrame({"name": ["Alice", "Bob"], "score": [95, 87]})

# ✅ Polars DataFrame
import polars as pl
data = pl.DataFrame({"name": ["Alice", "Bob"], "score": [95, 87]})
```

All formats are normalized to records internally via `holysheet.data.to_records()`.

---

## 💻 CLI

```bash
# Validate a report spec
holysheet validate report.json

# Serve a report locally (opens browser)
holysheet serve report.json

# Show version
holysheet version
```

---

## 🏗️ Architecture

```
Python API  →  Pydantic v2 Schema  →  JSON Spec  →  React Renderer  →  HTML Dashboard
```

HolySheet operates in two distinct phases:

### 🔧 Build Time *(Python — your machine)*

1. You define blocks using the Python API
2. HolySheet validates everything with **Pydantic v2** models
3. Generates a versioned JSON dashboard specification
4. Injects the spec into a **prebuilt React application**
5. Exports a self-contained HTML file via **Jinja2** templates

### 🌐 Runtime *(Browser — any machine)*

1. Browser opens the HTML file (no server needed)
2. React reads the embedded dashboard spec from `<script id="report-data">`
3. Renders each block through a **component registry** (`type` → React component)
4. Charts become interactive via **Apache ECharts**
5. Tables support real-time search and pagination

> **The key insight:** The React app is **prebuilt and bundled inside the Python package**. End users never need Node.js, npm, or any frontend tooling.

### Project Structure

```
HolySheet/
  src/holysheet/           # Python package
    __init__.py            #   Public API (20 block types + Report)
    blocks.py              #   Pydantic v2 block models
    schema.py              #   Report schema model
    report.py              #   Main Report class + export methods
    data.py                #   Data normalization (pandas/polars/dict/list)
    exporters.py           #   HTML / folder / JSON exporters
    themes.py              #   Theme system (light / dark / executive)
    exceptions.py          #   Custom exception hierarchy
    cli.py                 #   Click-based CLI (validate, serve, version)
    renderer/              #   Prebuilt React assets (JS + CSS)
    templates/             #   Jinja2 HTML templates

  frontend/                # React source (development only)
    src/
      components/          #   React block components
      theme.ts             #   MUI theme definitions
      registry.tsx         #   Block type → component mapping
      types.ts             #   TypeScript interfaces

  tests/                   # Python test suite
  examples/                # Example scripts
```

---

## 🛠️ Development

### Prerequisites

- Python **3.11+**
- Node.js **18+** *(frontend development only)*
- Make

### Setup

```bash
git clone https://github.com/UnicoLab/HolySheet.git
cd HolySheet

# Full development setup (frontend + Python)
make dev

# Or step by step:
make frontend-install   # Install frontend npm dependencies
make frontend-build     # Build React app → src/holysheet/renderer/
make install            # Install Python package in editable mode
```

### Common Commands

```bash
make test              # Run Python test suite
make lint              # Lint with ruff
make typecheck         # Type-check with mypy (strict mode)
make format            # Auto-format with ruff
make build             # Build distributable wheel + sdist
make clean             # Clean all build artifacts
```

### Releases

HolySheet uses [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release) with conventional commits:

| Prefix | Effect |
|---|---|
| `feat:` | Minor version bump |
| `fix:` / `perf:` | Patch version bump |
| `BREAKING CHANGE:` | Major version bump |

---

## 🗺️ Roadmap

- [ ] 📊 Additional chart types (Sankey, Gantt, DAG, Heatmap)
- [ ] 🤖 AI narrative blocks (auto-generated insights)
- [ ] 🔍 Interactive filters and cross-chart drill-down
- [ ] 📑 Tabbed navigation across report pages
- [ ] 📄 PDF export
- [ ] 📊 PowerPoint export
- [ ] 🧩 Custom React component injection
- [ ] 🎨 Enterprise theme gallery + custom theme API
- [ ] 🔐 Signed / offline report bundles
- [ ] 💬 Local chatbot over report data

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/amazing-feature`)
3. Make your changes with tests
4. Run the checks: `make lint && make typecheck && make test`
5. Commit with [conventional commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, etc.)
6. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/UnicoLab">UnicoLab</a>
</p>

<p align="center">
  <sub>Holy Sheet, that's a beautiful dashboard! 🙌</sub>
</p>
