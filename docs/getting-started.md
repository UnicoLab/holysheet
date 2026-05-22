# Getting Started

Welcome to HolySheet! This guide will take you from zero to a fully interactive dashboard in under 5 minutes.

---

## :package: Installation

### Basic Install

```bash
pip install holysheet
```

### With DataFrame Support

=== "Pandas"

    ```bash
    pip install holysheet[pandas]
    ```

=== "Polars"

    ```bash
    pip install holysheet[polars]
    ```

=== "Everything"

    ```bash
    pip install holysheet[all]
    ```

!!! info "Requirements"
    - :fontawesome-brands-python: Python **3.11+**
    - :octicons-x-12: No Node.js required
    - :octicons-x-12: No frontend build step
    - :octicons-x-12: No running server

**Core dependencies** (installed automatically): `pydantic v2` · `jinja2` · `orjson` · `loguru` · `click`

---

## :memo: Your First Report

### Step 1: Import

```python title="my_report.py"
from holysheet import Report, KPI, LineChart, Markdown
```

### Step 2: Create a Report

```python title="my_report.py"
report = Report(
    title="My First Dashboard",
    subtitle="Built with HolySheet",
    theme="dark",
)
```

### Step 3: Add Blocks

```python title="my_report.py"
# Add a welcome message
report.add(Markdown(content="## Welcome\n\nThis is my first HolySheet dashboard!"))

# Add KPI cards
report.add(KPI(label="Total Users", value="2,890", delta="+13.8%", status="positive"))
report.add(KPI(label="Active Rate", value=78, unit="%", delta="+2.1%", status="positive"))
report.add(KPI(label="Revenue", value="$124K", delta="+18%", status="positive"))

# Add a chart
monthly_data = [
    {"month": "Jan", "users": 1_200},
    {"month": "Feb", "users": 1_450},
    {"month": "Mar", "users": 1_830},
    {"month": "Apr", "users": 2_100},
    {"month": "May", "users": 2_540},
    {"month": "Jun", "users": 2_890},
]

report.add(LineChart(
    title="User Growth",
    data=monthly_data,
    x="month",
    y="users",
    height=400,
))
```

### Step 4: Export

```python title="my_report.py"
report.export_html("my_report.html")
print("Done! Open my_report.html in your browser.")
```

### Step 5: Open & Share

=== "macOS"

    ```bash
    open my_report.html
    ```

=== "Linux"

    ```bash
    xdg-open my_report.html
    ```

=== "Windows"

    ```bash
    start my_report.html
    ```

!!! success "Congratulations!"
    You just built an interactive dashboard with zero frontend knowledge. The HTML file is fully self-contained — share it however you like.

---

## :building_construction: Understanding the Architecture

HolySheet operates in two distinct phases:

```
Python API  →  Pydantic v2 Schema  →  JSON Spec  →  React Renderer  →  HTML Dashboard
```

### :wrench: Build Time (Python — your machine)

1. **Define blocks** using the Python API (`KPI`, `LineChart`, etc.)
2. **Validate** everything with Pydantic v2 models — catch errors early
3. **Generate** a versioned JSON dashboard specification
4. **Inject** the spec into a prebuilt React application
5. **Export** a self-contained HTML file via Jinja2 templates

### :globe_with_meridians: Runtime (Browser — any machine)

1. Browser opens the HTML file (no server needed)
2. React reads the embedded dashboard spec from `<script id="report-data">`
3. Renders each block through a **component registry** (`type` → React component)
4. Charts become interactive via **Apache ECharts**
5. Tables support real-time search and pagination

!!! tip "Key Insight"
    The React app is **prebuilt and bundled inside the Python package**. End users never need Node.js, npm, or any frontend tooling. The magic happens at `pip install` time.

### How Blocks Work

Every block in HolySheet is a **Pydantic v2 model** with a `type` discriminator field:

```python
from holysheet.blocks import KPI

kpi = KPI(label="Revenue", value="$1.2M", delta="+12%", status="positive")

# Each block serializes to a dict for the React renderer:
print(kpi.to_props())
# {'label': 'Revenue', 'value': '$1.2M', 'delta': '+12%', ...}
```

The `Report` class manages a list of blocks and assigns sequential IDs (`block_001`, `block_002`, …) for deterministic output.

---

## :outbox_tray: Export Formats

HolySheet supports three export modes:

### Standalone HTML (Recommended)

```python
report.export_html("report.html")
```

Generates a **single self-contained HTML file** (~1.5 MB) with embedded React, CSS, and data. Zero external dependencies.

!!! example "Best for"
    Email attachments, Slack sharing, embedding in Confluence or Notion, offline viewing.

### Folder Export

```python
report.export_folder("dist/")
```

Generates a deployable folder structure:

```
dist/
├── index.html          ← Entry point
├── report.json         ← Dashboard spec
├── spec-loader.js      ← Auto-generated loader
└── assets/
    ├── app.js          ← React bundle
    └── app.css         ← Styles
```

!!! example "Best for"
    Hosting on a web server, S3, CDN, or GitHub Pages.

### JSON Export

```python
report.export_json("report.json")
```

Exports just the dashboard specification as JSON.

!!! example "Best for"
    Debugging, version control, feeding into external rendering pipelines, programmatic manipulation.

---

## :arrow_right: Next Steps

Now that you have the basics down, explore:

- **[Block Types](blocks/index.md)** — Learn about all 57 available blocks
- **[Themes](themes.md)** — Choose and customize your theme
- **[Data Sources](data-sources.md)** — Work with pandas, polars, and more
- **[Examples Gallery](examples.md)** — Copy-paste real-world dashboards
