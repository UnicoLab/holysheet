# Block Types Overview

HolySheet ships with **26 block types** organized into five categories. Each block is a Pydantic v2 model with full type safety and validation.

---

## :bar_chart: Quick Reference

### :chart_with_upwards_trend: Charts (9 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`LineChart`](charts.md#linechart) | `line_chart` | Multi-series line chart | `data`, `x`, `y`, `series`, `height` |
| [`AreaChart`](charts.md#areachart) | `area_chart` | Filled area chart | `data`, `x`, `y`, `series`, `height` |
| [`BarChart`](charts.md#barchart) | `bar_chart` | Grouped/stacked bar chart | `data`, `x`, `y`, `series`, `height` |
| [`PieChart`](charts.md#piechart) | `pie_chart` | Pie / donut chart | `data`, `name`, `value`, `height` |
| [`ScatterChart`](charts.md#scatterchart) | `scatter_chart` | Scatter / bubble plot | `data`, `x`, `y`, `size`, `category` |
| [`RadarChart`](charts.md#radarchart) | `radar_chart` | Radar / spider chart | `data`, `indicators`, `height` |
| [`GaugeChart`](charts.md#gaugechart) | `gauge` | Speedometer gauge | `value`, `min`, `max`, `thresholds` |
| [`FunnelChart`](charts.md#funnelchart) | `funnel_chart` | Conversion funnel | `data`, `name`, `value`, `height` |
| [`TreemapChart`](charts.md#treemapchart) | `treemap_chart` | Hierarchical treemap | `data`, `name`, `value`, `category` |

### :chart_with_upwards_trend: KPI & Metrics (3 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`KPI`](kpi-metrics.md#kpi) | `kpi` | Key metric card with delta | `label`, `value`, `unit`, `delta`, `status` |
| [`Metric`](kpi-metrics.md#metric) | `metric` | Compact inline metric | `label`, `value`, `unit`, `icon` |
| [`StatComparison`](kpi-metrics.md#statcomparison) | `stat_comparison` | Side-by-side stat comparison | `title`, `items` |

### :page_facing_up: Data & Content (6 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`DataTable`](data-content.md#datatable) | `data_table` | Searchable, paginated table | `data`, `columns`, `searchable`, `paginated` |
| [`Markdown`](data-content.md#markdown) | `markdown` | Rich text content | `content` |
| [`CodeBlock`](data-content.md#codeblock) | `code_block` | Syntax-highlighted code | `code`, `language`, `title` |
| [`Image`](data-content.md#image) | `image` | Image display | `src`, `alt`, `caption`, `width` |
| [`Alert`](data-content.md#alert) | `alert` | Callout / notification | `severity`, `title`, `message` |
| [`ProgressBar`](data-content.md#progressbar) | `progress` | Progress indicator | `label`, `value`, `max`, `color` |

### :bricks: Layout (5 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`Section`](layout.md#section) | `section` | Group blocks with heading | `title`, `description`, `children` |
| [`Columns`](layout.md#columns) | `columns` | Multi-column grid | `children`, `widths`, `layout` |
| [`Tabs`](layout.md#tabs) | `tabs` | Tabbed content panels | `tabs` (list of `{label, children}`) |
| [`Divider`](layout.md#divider) | `divider` | Visual separator line | `label`, `variant` |
| [`Accordion`](layout.md#accordion) | `accordion` | Collapsible panels | `panels` |

### :video_game: Interactive (3 types)

| Block | Type Key | Description | Key Props |
|:------|:---------|:------------|:----------|
| [`Slider`](interactive.md#slider) | `slider` | Interactive slider | `label`, `min`, `max`, `step`, `default_value` |
| [`NumberInput`](interactive.md#numberinput) | `number_input` | Number input with buttons | `label`, `min`, `max`, `step` |
| [`Toggle`](interactive.md#toggle) | `toggle` | On/off switch | `label`, `description`, `default_value` |

---

## :jigsaw: How Blocks Work

Every block inherits from `Block` — a Pydantic v2 `BaseModel` with a `type` discriminator:

```python title="Basic block usage"
from holysheet import Report, KPI, LineChart

report = Report(title="Dashboard", theme="dark")

# Just instantiate and add
report.add(KPI(label="Revenue", value="$1.2M", delta="+12%", status="positive"))
report.add(LineChart(title="Trend", data=my_data, x="date", y="revenue"))

report.export_html("dashboard.html")
```

!!! tip "Method Chaining"
    `report.add()` returns `self`, so you can chain calls:

    ```python
    report.add(KPI(label="A", value=1)).add(KPI(label="B", value=2))
    ```

---

## :frame_with_picture: Block Categories at a Glance

```
┌─────────────────────────────────────────────────────┐
│                     Report                          │
│                                                     │
│  ┌─── KPI & Metrics ──┐  ┌──── Charts ──────────┐  │
│  │ KPI                 │  │ LineChart  BarChart   │  │
│  │ Metric              │  │ AreaChart  PieChart   │  │
│  │ StatComparison      │  │ ScatterChart Radar    │  │
│  └─────────────────────┘  │ Gauge Funnel Treemap  │  │
│                           └──────────────────────┘  │
│  ┌── Data & Content ──┐  ┌──── Layout ──────────┐  │
│  │ DataTable           │  │ Section  Columns     │  │
│  │ Markdown  CodeBlock │  │ Tabs     Divider     │  │
│  │ Image  Alert        │  │ Accordion            │  │
│  │ ProgressBar         │  └──────────────────────┘  │
│  └─────────────────────┘                            │
│  ┌── Interactive ─────┐                             │
│  │ Slider NumberInput  │                            │
│  │ Toggle              │                            │
│  └─────────────────────┘                            │
└─────────────────────────────────────────────────────┘
```

---

## :arrow_right: Detailed References

- **[KPI & Metrics](kpi-metrics.md)** — KPI cards, compact metrics, stat comparisons
- **[Charts](charts.md)** — All 9 chart types with data format examples
- **[Data & Content](data-content.md)** — Tables, markdown, code, images, alerts
- **[Layout](layout.md)** — Columns, sections, tabs, dividers, accordions
- **[Interactive](interactive.md)** — Sliders, number inputs, toggles
