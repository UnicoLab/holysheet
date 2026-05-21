# Layout Blocks

Layout blocks control how other blocks are arranged in the dashboard. Use them to create multi-column grids, collapsible sections, tabbed views, and visual separators.

---

## Columns

Multi-column responsive grid layout. Renders children side-by-side.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `children` | `list[Block]` | `[]` | Ordered list of child blocks (one per column) |
| `widths` | `list[int] \| None` | `None` | Relative widths (must sum to 12 for MUI grid) |
| `layout` | `"equal" \| "bento" \| "custom"` | `"equal"` | Layout mode |

### Equal Widths (Default)

All children get equal width:

```python title="columns_equal.py"
from holysheet import Columns, KPI

Columns(children=[
    KPI(label="Revenue", value="$4.64M", delta="+23%", status="positive"),
    KPI(label="Deals", value=127, delta="+18", status="positive"),
    KPI(label="Win Rate", value=68, unit="%", status="positive"),
])
```

### Custom Widths

Use `widths` with values that sum to **12** (based on a 12-column MUI grid system):

```python title="columns_custom.py"
from holysheet import Columns, LineChart, DataTable

Columns(
    widths=[8, 4],  # 2/3 + 1/3
    layout="custom",
    children=[
        LineChart(title="Revenue Trend", data=data, x="month", y="revenue"),
        DataTable(title="Summary", data=summary),
    ],
)
```

### Common Width Patterns

| Pattern | Widths | Description |
|:--------|:-------|:------------|
| Two equal | `[6, 6]` | 50/50 split |
| Sidebar | `[8, 4]` | Main + sidebar |
| Sidebar left | `[4, 8]` | Sidebar + main |
| Three equal | `[4, 4, 4]` | Thirds |
| Four equal | `[3, 3, 3, 3]` | Quarters |
| Wide + narrow + narrow | `[6, 3, 3]` | Featured |

### Bento Layout

The `"bento"` layout mode provides automatic sizing based on block types:

```python title="columns_bento.py"
Columns(
    layout="bento",
    children=[
        KPI(label="Revenue", value="$1.2M"),
        KPI(label="Users", value="42K"),
        LineChart(title="Trend", data=data, x="month", y="value"),
    ],
)
```

!!! tip "Nesting"
    Columns can contain any block type, including other `Columns`, `Section`, `Tabs`, and `Accordion` blocks for complex nested layouts.

---

## Section

Grouping container that adds a heading and optional description around a collection of blocks.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `title` | `str` | *required* | Section heading |
| `description` | `str \| None` | `None` | Optional subtitle / description |
| `children` | `list[Block]` | `[]` | Ordered list of child blocks |

### Basic Example

```python title="section_basic.py"
from holysheet import Section, LineChart, BarChart

Section(
    title="Revenue Analytics",
    description="Monthly revenue breakdown with year-over-year trends.",
    children=[
        LineChart(
            title="Monthly Revenue vs Target",
            data=revenue_data,
            x="month",
            y=["revenue", "target"],
        ),
        BarChart(
            title="Revenue by Region",
            data=region_data,
            x="region",
            y="revenue",
        ),
    ],
)
```

### Nested Sections

Sections can be nested for hierarchical organization:

```python title="section_nested.py"
Section(
    title="Q4 Report",
    children=[
        Section(
            title="Financial Overview",
            children=[
                KPI(label="Revenue", value="$4.64M"),
                LineChart(title="Trend", data=data, x="month", y="revenue"),
            ],
        ),
        Section(
            title="Operations",
            children=[
                BarChart(title="Team Performance", data=team_data, x="team", y="delivered"),
            ],
        ),
    ],
)
```

---

## Tabs

Tabbed content container that organizes blocks into switchable panels.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `tabs` | `list[dict]` | `[]` | List of tab definitions |

Each tab dict has:

| Key | Type | Description |
|:----|:-----|:------------|
| `label` | `str` | Tab label text |
| `children` | `list[Block]` | Blocks to display in this tab |

### Example

```python title="tabs_example.py"
from holysheet import Tabs, LineChart, BarChart, PieChart

Tabs(tabs=[
    {
        "label": "📈 Revenue Trend",
        "children": [
            LineChart(
                title="Monthly Revenue, Costs & Profit",
                data=monthly_revenue,
                x="month",
                y=["revenue", "costs", "profit"],
                height=420,
            ),
        ],
    },
    {
        "label": "📊 By Product",
        "children": [
            BarChart(
                title="Revenue by Product — Q3 vs Q4",
                data=revenue_by_product,
                x="product",
                y=["q3", "q4"],
                height=400,
            ),
        ],
    },
    {
        "label": "🍩 By Segment",
        "children": [
            PieChart(
                title="Revenue Distribution",
                data=revenue_by_segment,
                name="segment",
                value="revenue",
            ),
        ],
    },
])
```

!!! tip "Emoji Labels"
    Use emoji in tab labels for visual clarity: `"📈 Trends"`, `"📊 Breakdown"`, `"🔄 Pipeline"`.

### Multiple Blocks per Tab

Each tab can contain multiple blocks:

```python title="tabs_multi.py"
Tabs(tabs=[
    {
        "label": "Overview",
        "children": [
            Markdown(content="## Summary\n\nKey findings..."),
            KPI(label="Revenue", value="$2.26M"),
            LineChart(title="Trend", data=data, x="month", y="revenue"),
        ],
    },
    {
        "label": "Details",
        "children": [
            DataTable(title="Raw Data", data=raw_data),
        ],
    },
])
```

---

## Divider

Visual separator line for creating visual breaks between report sections.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `label` | `str \| None` | `None` | Optional centered label text |
| `variant` | `"solid" \| "dashed" \| "dotted"` | `"solid"` | Line style |

### Examples

=== "Simple"

    ```python
    from holysheet import Divider

    Divider()  # Plain horizontal line
    ```

=== "With Label"

    ```python
    Divider(label="Key Performance Indicators")
    ```
    Renders a line with centered text.

=== "Dashed"

    ```python
    Divider(variant="dashed")
    ```

=== "Dotted with Label"

    ```python
    Divider(label="Section Break", variant="dotted")
    ```

!!! tip "Section Separators"
    Labeled dividers are a great lightweight alternative to `Section` when you want visual separation without the full section container styling.

---

## Accordion

Collapsible accordion panels for progressive disclosure of content.

### Props

| Prop | Type | Default | Description |
|:-----|:-----|:--------|:------------|
| `panels` | `list[dict]` | `[]` | List of panel definitions |

Each panel dict has:

| Key | Type | Description |
|:----|:-----|:------------|
| `title` | `str` | Panel heading |
| `subtitle` | `str` (optional) | Panel subtitle |
| `children` | `list[Block]` | Blocks inside the panel |
| `default_expanded` | `bool` (optional) | Start expanded? Default: `False` |

### Example

```python title="accordion_example.py"
from holysheet import Accordion, KPI, DataTable, LineChart

Accordion(panels=[
    {
        "title": "Financial Overview",
        "subtitle": "Revenue and cost metrics",
        "default_expanded": True,
        "children": [
            KPI(label="Revenue", value="$2.26M", delta="+34%", status="positive"),
            LineChart(title="Revenue Trend", data=revenue_data, x="month", y="revenue"),
        ],
    },
    {
        "title": "Customer Data",
        "subtitle": "Top accounts and health scores",
        "children": [
            DataTable(title="Top Accounts", data=customers_data),
        ],
    },
    {
        "title": "Technical Metrics",
        "children": [
            KPI(label="Uptime", value="99.97%", status="positive"),
            KPI(label="Response Time", value="142ms", status="neutral"),
        ],
    },
])
```

!!! tip "Progressive Disclosure"
    Use Accordion to keep dashboards clean by hiding detail sections that users can expand on demand. Set `default_expanded: True` on the most important panel.

---

## :jigsaw: Layout Patterns

### Full Dashboard Layout

```python title="full_layout.py"
from holysheet import (
    Report, KPI, Columns, Section, Tabs, Divider,
    LineChart, BarChart, PieChart, DataTable, Markdown,
)

report = Report(title="Dashboard", theme="dark")

# Hero section
report.add(Markdown(content="## Executive Summary\n\nKey findings..."))

# KPI row
report.add(Columns(children=[
    KPI(label="Revenue", value="$4.64M", delta="+23%", status="positive"),
    KPI(label="Deals", value=127, delta="+18", status="positive"),
    KPI(label="Win Rate", value="68%", delta="+4.2%", status="positive"),
]))

report.add(Divider(label="Detailed Analysis"))

# Charts in tabs within a section
report.add(Section(
    title="Revenue Analytics",
    children=[
        Tabs(tabs=[
            {"label": "📈 Trends", "children": [
                LineChart(title="Monthly Revenue", data=data, x="month", y="revenue"),
            ]},
            {"label": "📊 Breakdown", "children": [
                BarChart(title="By Region", data=region_data, x="region", y="sales"),
            ]},
        ]),
    ],
))

# Side-by-side charts
report.add(Columns(children=[
    PieChart(title="Revenue Split", data=segment_data, name="segment", value="revenue"),
    DataTable(title="Top Deals", data=deals_data),
]))

report.export_html("dashboard.html")
```
