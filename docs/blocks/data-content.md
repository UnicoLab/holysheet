# Data & Content Blocks

These blocks handle tabular data display, rich text, code, images, alerts, and progress indicators.

---

## DataTable

Interactive, searchable, paginated data table. Ideal for detailed drill-down data.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Table title |
| `data` | `Any` | `None` | Tabular data (list of dicts, DataFrame, etc.) |
| `columns` | `list[str] \| None` | `None` | Explicit column list; auto-detected from data if omitted |
| `searchable` | `bool` | `True` | Enable text search across all columns |
| `paginated` | `bool` | `True` | Enable pagination |

### Basic Example

```python title="table_basic.py"
from holysheet import DataTable

DataTable(
    title="Top Customers",
    data=[
        {"company": "Meridian Corp", "plan": "Enterprise", "mrr": "$12,400"},
        {"company": "Atlas Dynamics", "plan": "Enterprise", "mrr": "$9,800"},
        {"company": "Helix Systems", "plan": "Mid-Market", "mrr": "$5,600"},
    ],
)
```

### With Explicit Columns

Control which columns appear and their order:

```python title="table_columns.py"
DataTable(
    title="Project Portfolio",
    data=projects_data,
    columns=["project", "owner", "risk", "status", "completion", "budget_used"],
)
```

### With Pandas DataFrame

```python title="table_pandas.py"
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Carol"],
    "Score": [95, 87, 92],
    "Grade": ["A", "B+", "A-"],
})

DataTable(title="Student Grades", data=df)
```

### Disabling Features

```python title="table_minimal.py"
DataTable(
    title="Static Data",
    data=my_data,
    searchable=False,  # No search bar
    paginated=False,   # Show all rows
)
```

!!! tip "Auto-Detection"
    When `columns` is `None`, HolySheet automatically detects column names from the first record in the data. Specify `columns` explicitly to control column order or exclude certain fields.

---

## Markdown

Free-form rich text content using Markdown syntax. Perfect for narrative sections, executive summaries, and documentation.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `content` | `str` | *required* | Markdown-formatted string |

### Example

```python title="markdown_example.py"
from holysheet import Markdown

Markdown(content="""## Executive Summary

Portfolio health remains **strong** with 42 active projects delivering on schedule.
Risk-adjusted returns are trending positively, with a **12% improvement** in delivery
confidence over the past quarter.

### Key Highlights

- Revenue exceeded targets for 10 consecutive months
- Overall portfolio risk score decreased from 72 to 38
- Frontend team delivered 110% of planned capacity

---

> _This report was generated with HolySheet v0.2.0_
""")
```

!!! info "Supported Markdown"
    The React renderer supports standard Markdown including headings, bold, italic, lists, links, blockquotes, code spans, and horizontal rules.

---

## CodeBlock

Syntax-highlighted code display with optional title. Great for API examples, configuration snippets, and developer resources.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `code` | `str` | *required* | The source code string |
| `language` | `str \| None` | `None` | Programming language for syntax highlighting |
| `title` | `str \| None` | `None` | Optional title above the code block |

### Example

```python title="codeblock_example.py"
from holysheet import CodeBlock

CodeBlock(
    code=(
        "from holysheet import Report, KPI, LineChart\n\n"
        "report = Report(title='Q4 Metrics', theme='dark')\n"
        "report.add(KPI(label='Revenue', value='$258K', delta='+12%', status='positive'))\n"
        "report.add(LineChart(title='Trend', data=monthly_data, x='month', y='revenue'))\n\n"
        "report.export_html('q4_report.html')\n"
    ),
    language="python",
    title="Quick Start — Generate a Report",
)
```

### Multiple Languages

=== "Python"

    ```python
    CodeBlock(code="print('Hello')", language="python")
    ```

=== "JavaScript"

    ```python
    CodeBlock(code="console.log('Hello');", language="javascript")
    ```

=== "SQL"

    ```python
    CodeBlock(code="SELECT * FROM users WHERE active = true;", language="sql")
    ```

=== "YAML"

    ```python
    CodeBlock(code="theme: dark\ntitle: My Report", language="yaml")
    ```

---

## Image

Display an image from a URL or data URI.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `src` | `str` | *required* | Image URL or data URI |
| `alt` | `str \| None` | `None` | Accessibility alt text |
| `caption` | `str \| None` | `None` | Caption text below the image |
| `width` | `str \| int \| None` | `None` | Width (CSS value or pixels) |
| `height` | `str \| int \| None` | `None` | Height (CSS value or pixels) |

### Example

```python title="image_example.py"
from holysheet import Image

Image(
    src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800",
    alt="Data Visualization Dashboard",
    caption="NovaPulse Platform — Live Dashboard View",
    width="100%",
)
```

### With Fixed Dimensions

```python title="image_sized.py"
Image(
    src="https://example.com/chart.png",
    alt="Q4 Revenue Chart",
    width=600,
    height=400,
)
```

!!! warning "External URLs"
    Images referenced by URL require internet access when viewing the report. For fully offline reports, consider using data URIs (base64-encoded images).

---

## Alert

Alert / callout block for important messages, warnings, and notifications.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `severity` | `"info" \| "warning" \| "error" \| "success"` | `"info"` | Alert level |
| `title` | `str \| None` | `None` | Optional alert title |
| `message` | `str` | `""` | Alert message body |

### Severity Levels

=== ":material-information: Info"

    ```python
    Alert(
        severity="info",
        title="Upcoming Renewal Cycle",
        message="12 Enterprise accounts are up for renewal in Q1.",
    )
    ```
    Blue accent — use for informational notices.

=== ":material-check-circle: Success"

    ```python
    Alert(
        severity="success",
        title="Milestone Reached!",
        message="Crossed 42,000 monthly active users, exceeding the annual target by 20%.",
    )
    ```
    Green accent — use for positive announcements.

=== ":material-alert: Warning"

    ```python
    Alert(
        severity="warning",
        title="Cost Alert",
        message="Compute costs increased 18% month-over-month. Review autoscaling policies.",
    )
    ```
    Yellow/amber accent — use for caution notices.

=== ":material-close-circle: Error"

    ```python
    Alert(
        severity="error",
        title="Action Required",
        message="Quantum Forge usage dropped 34% in the last 30 days. Escalate to CS team.",
    )
    ```
    Red accent — use for critical issues.

---

## ProgressBar

Visual progress indicator for completion tracking, utilization metrics, and goal progress.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str` | *required* | Progress label |
| `value` | `int \| float` | `0` | Current value |
| `max` | `int \| float` | `100` | Maximum value |
| `color` | `str \| None` | `None` | Optional CSS color for the bar |
| `description` | `str \| None` | `None` | Optional helper text |

### Example

```python title="progress_example.py"
from holysheet import ProgressBar, Columns

Columns(children=[
    ProgressBar(
        label="CPU Utilisation",
        value=73,
        description="18 / 24 vCPUs allocated",
    ),
    ProgressBar(
        label="Memory Usage",
        value=61,
        description="49 GB / 80 GB",
    ),
    ProgressBar(
        label="Disk I/O",
        value=42,
        description="Healthy throughput",
    ),
    ProgressBar(
        label="Network Bandwidth",
        value=88,
        description="Approaching limit — consider upgrade",
        color="#EF4444",  # Red to indicate warning
    ),
])
```

### Custom Ranges

```python title="progress_custom.py"
ProgressBar(
    label="Sprint Progress",
    value=34,
    max=50,       # 34 out of 50 story points
    description="34 / 50 story points completed",
)
```

!!! tip "Using with Columns"
    Wrap multiple `ProgressBar` blocks in a `Columns` layout to create a utilization dashboard row.
