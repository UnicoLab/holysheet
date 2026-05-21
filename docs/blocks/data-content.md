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

---

## Timeline

Vertical event/milestone timeline for roadmaps, changelogs, and process histories.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str \| None` | `None` | Section title |
| `events` | `list[dict]` | *required* | List of event dicts |

**Event dict keys:** `date` (str, required), `title` (str, required), `description` (str, optional), `icon` (str, optional), `color` (str, optional hex color)

!!! example "Product Roadmap"

    ```python title="timeline_example.py"
    from holysheet import Timeline

    Timeline(
        title="Product Roadmap 2024",
        events=[
            {"date": "Jan 2024", "title": "v1.0 Launch", "description": "Initial public release", "color": "#22c55e"},
            {"date": "Mar 2024", "title": "v1.5 Charts", "description": "Added 9 chart types", "color": "#6366f1"},
            {"date": "Jun 2024", "title": "v2.0 Interactive", "description": "Sliders, toggles, dropdowns", "color": "#f59e0b"},
            {"date": "Sep 2024", "title": "v3.0 Pro", "description": "21 new block types", "color": "#ef4444"},
        ],
    )
    ```

---

## Callout

Styled quote, highlight, or note block — perfect for pull quotes, key takeaways, and editorial content.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `content` | `str` | *required* | The callout text |
| `author` | `str \| None` | `None` | Attribution text |
| `icon` | `str \| None` | `None` | Icon emoji/string |
| `variant` | `"quote" \| "highlight" \| "note"` | `"quote"` | Visual style variant |

!!! example "Callout Variants"

    === "Quote"

        ```python
        Callout(
            content="The best dashboards tell a story.",
            author="Product Team",
            variant="quote",
            icon="💡",
        )
        ```

    === "Highlight"

        ```python
        Callout(
            content="47 block types. 3 themes. Zero Node.js required.",
            variant="highlight",
        )
        ```

    === "Note"

        ```python
        Callout(
            content="Data is refreshed every 15 minutes.",
            variant="note",
        )
        ```

---

## Embed

Embed external content via an iframe — dashboards, maps, videos, or any web page.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `url` | `str` | *required* | URL to embed |
| `title` | `str \| None` | `None` | Accessible title |
| `height` | `int` | `400` | Iframe height in pixels |
| `aspect_ratio` | `str \| None` | `None` | Optional CSS aspect ratio (e.g. `"16/9"`) |

```python title="embed_example.py"
from holysheet import Embed

Embed(
    url="https://www.google.com/maps/embed?pb=...",
    title="Office Locations",
    height=450,
)
```

!!! warning "Security"
    The embedded page must allow iframe embedding via its `X-Frame-Options` or `Content-Security-Policy` headers.

---

## JsonViewer

Interactive JSON tree with syntax highlighting, collapsible levels, and color-coded types.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `data` | `Any` | *required* | Any JSON-serializable Python object |
| `title` | `str \| None` | `None` | Title above the viewer |
| `collapsed_depth` | `int` | `2` | Auto-collapse levels deeper than this |

!!! example "Configuration Viewer"

    ```python title="json_viewer_example.py"
    from holysheet import JsonViewer

    JsonViewer(
        data={
            "app": {"name": "NovaPulse", "version": "3.0.0"},
            "features": ["charts", "interactive", "timeline"],
            "metrics": {"users": 45000, "uptime": 99.97},
        },
        title="Application Config",
        collapsed_depth=1,
    )
    ```

---

## UserCard

Team member / person card with avatar, role, email, and optional stats.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `name` | `str` | *required* | Person's name |
| `role` | `str \| None` | `None` | Job title / role |
| `avatar_url` | `str \| None` | `None` | URL for avatar image |
| `email` | `str \| None` | `None` | Email address |
| `stats` | `list[dict] \| None` | `None` | List of `{label, value}` dicts |

!!! example "Team Cards"

    ```python title="user_card_example.py"
    from holysheet import UserCard, Columns

    Columns(children=[
        UserCard(
            name="Alice Chen",
            role="Chief Data Officer",
            email="alice@company.io",
            stats=[{"label": "Reports", "value": "142"}, {"label": "Dashboards", "value": "38"}],
        ),
        UserCard(
            name="Marcus Johnson",
            role="VP Engineering",
            stats=[{"label": "Deployments", "value": "1.2K"}, {"label": "Uptime", "value": "99.97%"}],
        ),
    ])
    ```

---

## StatusList

List with colored status indicators — ideal for service health, deployment status, and task tracking.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str \| None` | `None` | Section title |
| `items` | `list[dict]` | *required* | List of status item dicts |

**Item dict keys:** `label` (str, required), `status` (`"success"` \| `"warning"` \| `"error"` \| `"info"` \| `"pending"`, required), `description` (str, optional), `value` (str, optional)

!!! example "Service Health"

    ```python title="status_list_example.py"
    from holysheet import StatusList

    StatusList(
        title="Service Health",
        items=[
            {"label": "API Gateway", "status": "success", "value": "12ms"},
            {"label": "Redis Cache", "status": "warning", "value": "85%", "description": "Memory elevated"},
            {"label": "ML Pipeline", "status": "error", "value": "DOWN"},
            {"label": "Email Service", "status": "pending", "value": "Queue: 142"},
        ],
    )
    ```

---

## InfoList

Key-value pair display with optional icons — for configuration panels, metadata, and summary lists.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str \| None` | `None` | Section title |
| `items` | `list[dict]` | *required* | List of `{key, value, icon?}` dicts |

```python title="info_list_example.py"
from holysheet import InfoList

InfoList(
    title="System Configuration",
    items=[
        {"key": "Environment", "value": "Production", "icon": "🌐"},
        {"key": "Region", "value": "us-east-1", "icon": "📍"},
        {"key": "Python", "value": "3.12.4", "icon": "🐍"},
        {"key": "Database", "value": "PostgreSQL 16.2", "icon": "🗄️"},
    ],
)
```

---

## Stepper

Process / wizard step visualization showing sequential stages with status indicators.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str \| None` | `None` | Section title |
| `steps` | `list[dict]` | *required* | List of step dicts |
| `current_step` | `int \| None` | `None` | Zero-based index of current active step |

**Step dict keys:** `label` (str, required), `description` (str, optional), `status` (`"complete"` \| `"active"` \| `"pending"`, optional)

!!! example "Deployment Pipeline"

    ```python title="stepper_example.py"
    from holysheet import Stepper

    Stepper(
        title="Deployment Pipeline",
        steps=[
            {"label": "Build", "description": "Compile & bundle", "status": "complete"},
            {"label": "Test", "description": "Unit + integration", "status": "complete"},
            {"label": "Staging", "description": "Canary deploy", "status": "active"},
            {"label": "Production", "description": "Blue-green deploy", "status": "pending"},
        ],
        current_step=2,
    )
    ```

---

## TagList

Display a collection of colored tags/badges — for technology stacks, categories, and labels.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str \| None` | `None` | Section title |
| `tags` | `list[dict]` | *required* | List of `{label, color?, variant?}` dicts |

```python title="tag_list_example.py"
from holysheet import TagList

TagList(
    title="Tech Stack",
    tags=[
        {"label": "Python", "color": "#3776AB"},
        {"label": "React", "color": "#61DAFB"},
        {"label": "TypeScript", "color": "#3178C6"},
        {"label": "PostgreSQL", "color": "#4169E1"},
    ],
)
```

---

## Sparkline

Tiny inline chart — a compact line/area visualization with no axes, perfect for showing trends at a glance.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `data` | `list[int \| float]` | *required* | Numeric values for the line |
| `color` | `str \| None` | `None` | Line color (CSS color) |
| `height` | `int` | `60` | Chart height in pixels |
| `show_area` | `bool` | `True` | Fill area below the line |

```python title="sparkline_example.py"
from holysheet import Sparkline, Columns

Columns(children=[
    Sparkline(data=[10, 25, 18, 35, 28, 42, 55, 48, 62, 75], color="#6C63FF"),
    Sparkline(data=[50, 45, 52, 48, 55, 42, 58, 62, 68, 80], color="#34d399"),
])
```

!!! tip "Use with KPIs"
    Place a `Sparkline` next to a `KPI` in a `Columns` layout to add trend context to your metrics.

---

## Video

HTML5 video embed with poster image, controls, and responsive sizing.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `src` | `str` | *required* | Video URL |
| `title` | `str \| None` | `None` | Title above the player |
| `poster` | `str \| None` | `None` | Poster/thumbnail image URL |
| `autoplay` | `bool` | `False` | Auto-play on load |
| `controls` | `bool` | `True` | Show playback controls |

```python title="video_example.py"
from holysheet import Video

Video(
    src="https://example.com/demo.mp4",
    title="Product Demo",
    poster="https://example.com/poster.jpg",
    controls=True,
)
```

