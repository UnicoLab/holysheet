---
title: Report Templates
description: Pre-built report templates for common dashboard layouts
---

# :material-file-document-multiple: Report Templates

HolySheet ships with **3 pre-built report templates** that produce beautiful, ready-to-share dashboards with minimal code. Each template is a subclass of `Report` that automatically composes the right blocks based on your data.

---

## :material-chart-line: SalesDashboard

A complete sales dashboard with KPIs, revenue trend, regional breakdown, pipeline funnel, and top clients table.

### Quick Start

```python title="sales_minimal.py"
from holysheet.templates import SalesDashboard

report = SalesDashboard(data={
    "kpis": {
        "revenue": "$4.2M",
        "revenue_delta": "+22%",
        "revenue_status": "positive",
        "deals_won": 142,
        "deals_delta": "+18",
        "deals_status": "positive",
        "avg_deal": "$29.5K",
        "avg_deal_delta": "+$3.2K",
        "avg_deal_status": "positive",
        "win_rate": "68%",
        "win_rate_delta": "+4.2%",
        "win_rate_status": "positive",
    },
})

report.export_html("sales_dashboard.html")
```

### Full Data Format

```python title="sales_full.py"
from holysheet.templates import SalesDashboard

report = SalesDashboard(
    data={
        # KPI cards (4 metrics)
        "kpis": {
            "revenue": "$4.2M",
            "revenue_delta": "+22%",
            "revenue_status": "positive",
            "deals_won": 142,
            "deals_delta": "+18",
            "deals_status": "positive",
            "avg_deal": "$29.5K",
            "avg_deal_delta": "+$3.2K",
            "avg_deal_status": "positive",
            "win_rate": "68%",
            "win_rate_delta": "+4.2%",
            "win_rate_status": "positive",
        },

        # Revenue trend (AreaChart)
        "revenue": [
            {"month": "Jan", "revenue": 320_000},
            {"month": "Feb", "revenue": 345_000},
            {"month": "Mar", "revenue": 412_000},
            {"month": "Apr", "revenue": 398_000},
            {"month": "May", "revenue": 465_000},
            {"month": "Jun", "revenue": 512_000},
        ],
        "revenue_x": "month",      # X-axis column (default: "month")
        "revenue_y": "revenue",    # Y-axis column (default: "revenue")

        # Regional breakdown (PieChart)
        "by_region": [
            {"region": "North America", "revenue": 1_840_000},
            {"region": "Europe", "revenue": 1_250_000},
            {"region": "Asia Pacific", "revenue": 920_000},
        ],
        "region_name": "region",   # Name column (default: "region")
        "region_value": "revenue", # Value column (default: "revenue")

        # Pipeline funnel (FunnelChart)
        "pipeline": [
            {"stage": "Leads", "count": 2400},
            {"stage": "Qualified", "count": 1200},
            {"stage": "Proposal", "count": 680},
            {"stage": "Negotiation", "count": 340},
            {"stage": "Closed Won", "count": 142},
        ],
        "pipeline_name": "stage",  # Name column (default: "stage")
        "pipeline_value": "count", # Value column (default: "count")

        # Top clients (DataTable)
        "top_clients": [
            {"company": "Meridian Corp", "plan": "Enterprise", "mrr": "$12,400"},
            {"company": "Atlas Dynamics", "plan": "Enterprise", "mrr": "$9,800"},
            {"company": "Helix Systems", "plan": "Mid-Market", "mrr": "$5,600"},
        ],
    },
    theme="dark",
    title="Sales Dashboard — Q4 2026",
)

report.export_html("sales_dashboard.html")
```

### Layout Structure

The `SalesDashboard` generates the following layout:

```
┌────────────────────────────────────────────────────┐
│  Revenue KPI │ Deals Won KPI │ Avg Deal │ Win Rate │  ← Columns
├────────────────────────────────────────────────────┤
│  Monthly Revenue (AreaChart)                       │  ← Section
├────────────────────────────────────────────────────┤
│  ┌─ By Region ─┐ ┌─ Pipeline ─┐                   │  ← Tabs
│  │  PieChart    │ │ FunnelChart│                   │
│  └─────────────┘ └────────────┘                   │
├────────────────────────────────────────────────────┤
│  Top Clients (DataTable)                           │  ← Table
└────────────────────────────────────────────────────┘
```

---

## :material-crown: ExecutiveSummary

A polished executive summary with scorecards, key highlights, trend lines, and milestones timeline. Defaults to the `executive` theme.

### Quick Start

```python title="exec_minimal.py"
from holysheet.templates import ExecutiveSummary

report = ExecutiveSummary(data={
    "metrics": [
        {"label": "Revenue", "value": "$12.8M", "delta": "+34%", "status": "positive"},
        {"label": "EBITDA", "value": "$3.2M", "delta": "+18%", "status": "positive"},
        {"label": "Headcount", "value": 284, "delta": "+12", "status": "neutral"},
    ],
})

report.export_html("executive_summary.html")
```

### Full Data Format

```python title="exec_full.py"
from holysheet.templates import ExecutiveSummary

report = ExecutiveSummary(
    data={
        # Scorecard metrics (up to 6, displayed as KPI cards)
        "metrics": [
            {"label": "Revenue", "value": "$12.8M", "unit": "USD",
             "delta": "+34%", "status": "positive"},
            {"label": "EBITDA", "value": "$3.2M",
             "delta": "+18%", "status": "positive"},
            {"label": "NRR", "value": "127%",
             "delta": "+8%", "status": "positive"},
            {"label": "Headcount", "value": 284,
             "delta": "+12", "status": "neutral"},
        ],

        # Key highlights (rendered as Alert blocks)
        "highlights": [
            {"severity": "success", "title": "Record Quarter",
             "message": "Q4 revenue exceeded target by 22%."},
            {"severity": "info", "title": "New Market Entry",
             "message": "APAC operations launched on schedule."},
            {"severity": "warning", "title": "Churn Alert",
             "message": "Enterprise churn increased 0.3pp."},
        ],

        # Trend chart (LineChart)
        "trends": [
            {"period": "Q1", "revenue": 8_200_000, "ebitda": 1_800_000},
            {"period": "Q2", "revenue": 9_600_000, "ebitda": 2_100_000},
            {"period": "Q3", "revenue": 11_200_000, "ebitda": 2_700_000},
            {"period": "Q4", "revenue": 12_800_000, "ebitda": 3_200_000},
        ],
        "trends_x": "period",                    # X column (default: "period")
        "trends_y": ["revenue", "ebitda"],        # Y column(s)

        # Milestones (Timeline block)
        "milestones": [
            {"date": "Jan 2026", "title": "Series B Close",
             "description": "$42M raised at $320M valuation"},
            {"date": "Mar 2026", "title": "SOC 2 Certification",
             "description": "Type II audit completed"},
            {"date": "Sep 2026", "title": "100th Enterprise Client",
             "description": "Meridian Corp signed as 100th enterprise"},
        ],
    },
    theme="executive",
    title="Executive Summary — FY2026",
)

report.export_html("exec_summary.html")
```

### Layout Structure

```
┌────────────────────────────────────────────────────┐
│  Revenue │ EBITDA │ NRR │ Headcount                │  ← KPI Columns
├────────────────────────────────────────────────────┤
│  Key Highlights                                    │  ← Section
│  ┌ ✅ Record Quarter ──────────────────────────┐   │
│  ┌ ℹ️  New Market Entry ───────────────────────┐   │  ← Alert blocks
│  ┌ ⚠️  Churn Alert ────────────────────────────┐   │
├────────────────────────────────────────────────────┤
│  Key Trends (LineChart)                            │
├────────────────────────────────────────────────────┤
│  Key Milestones (Timeline)                         │
└────────────────────────────────────────────────────┘
```

---

## :material-monitor-dashboard: OpsMonitor

A real-time-style operations monitoring dashboard with service health, gauge meters, error rates, latency charts, and SLO progress bars.

### Quick Start

```python title="ops_minimal.py"
from holysheet.templates import OpsMonitor

report = OpsMonitor(data={
    "services": [
        {"label": "API Gateway", "status": "success", "value": "12ms"},
        {"label": "Database", "status": "success", "value": "45ms"},
        {"label": "ML Pipeline", "status": "error", "value": "DOWN"},
    ],
})

report.export_html("ops_monitor.html")
```

### Full Data Format

```python title="ops_full.py"
from holysheet.templates import OpsMonitor

report = OpsMonitor(
    data={
        # Service health (StatusList)
        "services": [
            {"label": "API Gateway", "status": "success", "value": "12ms"},
            {"label": "Redis Cache", "status": "warning", "value": "85%",
             "description": "Memory elevated"},
            {"label": "ML Pipeline", "status": "error", "value": "DOWN"},
            {"label": "Email Service", "status": "pending", "value": "Queue: 142"},
        ],

        # Key metrics (GaugeChart — up to 4)
        "metrics": [
            {"label": "CPU", "value": 73, "min": 0, "max": 100, "unit": "%"},
            {"label": "Memory", "value": 61, "min": 0, "max": 100, "unit": "%"},
            {"label": "Disk I/O", "value": 42, "min": 0, "max": 100, "unit": "%"},
            {"label": "Bandwidth", "value": 88, "min": 0, "max": 100, "unit": "%"},
        ],

        # Error rate (BarChart)
        "errors": [
            {"time": "00:00", "count": 12},
            {"time": "04:00", "count": 8},
            {"time": "08:00", "count": 23},
            {"time": "12:00", "count": 45},
            {"time": "16:00", "count": 31},
            {"time": "20:00", "count": 18},
        ],
        "errors_x": "time",       # X column (default: "time")
        "errors_y": "count",      # Y column (default: "count")

        # Latency percentiles (LineChart)
        "latency": [
            {"time": "00:00", "p50": 45, "p95": 120, "p99": 250},
            {"time": "04:00", "p50": 42, "p95": 110, "p99": 230},
            {"time": "08:00", "p50": 55, "p95": 150, "p99": 320},
            {"time": "12:00", "p50": 68, "p95": 180, "p99": 410},
            {"time": "16:00", "p50": 62, "p95": 160, "p99": 350},
            {"time": "20:00", "p50": 48, "p95": 125, "p99": 260},
        ],
        "latency_x": "time",                       # X column (default: "time")
        "latency_y": ["p50", "p95", "p99"],         # Y columns

        # SLO compliance (ProgressBar)
        "slos": [
            {"label": "Uptime (99.9%)", "value": 99.97, "max": 100, "color": "#10B981"},
            {"label": "Latency p99 < 500ms", "value": 94, "max": 100},
            {"label": "Error Rate < 1%", "value": 88, "max": 100, "color": "#F59E0B"},
        ],
    },
    theme="dark",
    title="Operations Monitor — Production",
)

report.export_html("ops_monitor.html")
```

### Layout Structure

```
┌────────────────────────────────────────────────────┐
│  Service Health (StatusList)                       │
├────────────────────────────────────────────────────┤
│  CPU Gauge │ Memory Gauge │ Disk Gauge │ BW Gauge  │  ← Columns
├────────────────────────────────────────────────────┤
│  Error Rate (BarChart)                             │
├────────────────────────────────────────────────────┤
│  Latency p50/p95/p99 (LineChart)                   │
├────────────────────────────────────────────────────┤
│  SLO Compliance                                    │  ← Section
│  ┌ Uptime ████████████████████████████░ 99.97% ┐   │
│  ┌ Latency ██████████████████████████░░ 94%    ┐   │  ← ProgressBars
│  ┌ Error Rate █████████████████████░░░░ 88%    ┐   │
└────────────────────────────────────────────────────┘
```

---

## :bulb: Template Tips

### Customization

Templates accept all `Report` constructor arguments via `**kwargs`:

```python title="template_customization.py"
from holysheet.templates import SalesDashboard

report = SalesDashboard(
    data=my_data,
    theme="executive",                    # Override theme
    title="Custom Sales Report",          # Override title
    author="Data Team",                   # Pass Report kwargs
    theme_switch=True,                    # Enable feature flags
    password="s3cret",                    # Password protect
)
```

### Adding More Blocks

Since templates are `Report` subclasses, you can add more blocks after construction:

```python title="template_extend.py"
from holysheet.templates import SalesDashboard
from holysheet import Markdown, Alert

report = SalesDashboard(data=my_data)

# Add extra blocks after the template builds
report.add(Markdown(content="## Additional Notes\n\nQ4 exceeded expectations."))
report.add(Alert(severity="info", message="Next review: Jan 15, 2027"))

report.export_html("extended_dashboard.html")
```

### Partial Data

All data keys are optional — the template gracefully skips sections when data is missing:

```python title="template_partial.py"
# Only KPIs and revenue trend — no pipeline, no clients table
report = SalesDashboard(data={
    "kpis": {"revenue": "$4.2M", "deals_won": 142},
    "revenue": monthly_revenue_data,
})
```

!!! tip "Use Templates as Starting Points"
    Templates are great for getting a polished dashboard up quickly. For full control, compose blocks manually using the [Block Types](../blocks/index.md) API.
