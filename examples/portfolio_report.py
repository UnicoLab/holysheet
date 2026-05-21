#!/usr/bin/env python3
"""Comprehensive portfolio report showcasing ALL HolySheet block types.

Run:
    python examples/portfolio_report.py
"""

from holysheet import (
    KPI,
    BarChart,
    DataTable,
    LineChart,
    Markdown,
    PieChart,
    Report,
    Section,
)

# ── Fake data ──────────────────────────────────────────────────────────────────

# Monthly revenue data
revenue_data = [
    {"month": "Jan", "revenue": 820_000, "target": 800_000},
    {"month": "Feb", "revenue": 910_000, "target": 850_000},
    {"month": "Mar", "revenue": 1_050_000, "target": 900_000},
    {"month": "Apr", "revenue": 980_000, "target": 950_000},
    {"month": "May", "revenue": 1_120_000, "target": 1_000_000},
    {"month": "Jun", "revenue": 1_250_000, "target": 1_050_000},
    {"month": "Jul", "revenue": 1_180_000, "target": 1_100_000},
    {"month": "Aug", "revenue": 1_340_000, "target": 1_150_000},
    {"month": "Sep", "revenue": 1_420_000, "target": 1_200_000},
    {"month": "Oct", "revenue": 1_510_000, "target": 1_250_000},
    {"month": "Nov", "revenue": 1_600_000, "target": 1_300_000},
    {"month": "Dec", "revenue": 1_780_000, "target": 1_350_000},
]

# Risk score trend
risk_data = [
    {"week": "W1", "risk_score": 72},
    {"week": "W2", "risk_score": 68},
    {"week": "W3", "risk_score": 65},
    {"week": "W4", "risk_score": 71},
    {"week": "W5", "risk_score": 63},
    {"week": "W6", "risk_score": 58},
    {"week": "W7", "risk_score": 55},
    {"week": "W8", "risk_score": 52},
    {"week": "W9", "risk_score": 48},
    {"week": "W10", "risk_score": 45},
    {"week": "W11", "risk_score": 42},
    {"week": "W12", "risk_score": 38},
]

# Team delivery data
team_data = [
    {"team": "Platform", "delivered": 47, "planned": 52},
    {"team": "ML Ops", "delivered": 38, "planned": 40},
    {"team": "Frontend", "delivered": 55, "planned": 50},
    {"team": "Data Eng", "delivered": 32, "planned": 35},
    {"team": "DevOps", "delivered": 28, "planned": 30},
    {"team": "QA", "delivered": 41, "planned": 42},
]

# Budget allocation
budget_data = [
    {"category": "Engineering", "amount": 2_400_000},
    {"category": "Infrastructure", "amount": 800_000},
    {"category": "Marketing", "amount": 600_000},
    {"category": "Operations", "amount": 450_000},
    {"category": "Research", "amount": 350_000},
    {"category": "Other", "amount": 200_000},
]

# Project details
projects_data = [
    {
        "project": "AIFlow Core v3",
        "owner": "Sarah Chen",
        "risk": "Low",
        "status": "On Track",
        "completion": "87%",
        "budget_used": "€1.2M",
    },
    {
        "project": "ML Pipeline Redesign",
        "owner": "Marcus Johnson",
        "risk": "Medium",
        "status": "At Risk",
        "completion": "62%",
        "budget_used": "€890K",
    },
    {
        "project": "Client Portal 2.0",
        "owner": "Ana Rodriguez",
        "risk": "Low",
        "status": "On Track",
        "completion": "91%",
        "budget_used": "€540K",
    },
    {
        "project": "Data Warehouse Migration",
        "owner": "James Park",
        "risk": "High",
        "status": "Delayed",
        "completion": "45%",
        "budget_used": "€1.8M",
    },
    {
        "project": "Real-time Analytics",
        "owner": "Priya Sharma",
        "risk": "Medium",
        "status": "On Track",
        "completion": "73%",
        "budget_used": "€650K",
    },
    {
        "project": "Security Audit Platform",
        "owner": "David Kim",
        "risk": "Low",
        "status": "Completed",
        "completion": "100%",
        "budget_used": "€320K",
    },
    {
        "project": "API Gateway v2",
        "owner": "Lisa Wang",
        "risk": "Low",
        "status": "On Track",
        "completion": "82%",
        "budget_used": "€410K",
    },
    {
        "project": "Mobile SDK",
        "owner": "Tom Harris",
        "risk": "Medium",
        "status": "On Track",
        "completion": "56%",
        "budget_used": "€290K",
    },
]

# ── Build Report ───────────────────────────────────────────────────────────────

report = Report(
    title="AIFlow Executive Portfolio Report",
    subtitle="Q4 2026 · Portfolio risk and delivery intelligence",
    theme="dark",
)

# Executive summary
report.add(
    Markdown(
        content="""## Executive Summary

Portfolio health remains **strong** with 42 active projects delivering on schedule.
Risk-adjusted returns are trending positively, with a **12% improvement** in delivery
confidence over the past quarter.

### Key Highlights

- Revenue exceeded targets for 10 consecutive months
- Overall portfolio risk score decreased from 72 to 38
- Frontend team delivered 110% of planned capacity
- One project (Data Warehouse Migration) requires executive attention

---
"""
    )
)

# Top-level KPIs
report.add(KPI(label="Total Revenue", value="€14.96M", delta="+18.2%", status="positive"))
report.add(KPI(label="Active Projects", value=42, delta="+3", status="positive"))
report.add(
    KPI(
        label="On-Track Rate",
        value=87,
        unit="%",
        delta="+5.2%",
        status="positive",
        description="Projects meeting timeline targets",
    )
)
report.add(
    KPI(
        label="Risk Score",
        value=38,
        delta="-34",
        status="positive",
        description="Lower is better",
    )
)

# Revenue section
report.add(
    Section(
        title="Revenue & Financial",
        description="Monthly revenue performance and budget allocation",
        children=[
            LineChart(
                title="Monthly Revenue vs Target",
                data=revenue_data,
                x="month",
                y="revenue",
            ),
            PieChart(
                title="Budget Allocation",
                data=budget_data,
                name="category",
                value="amount",
            ),
        ],
    )
)

# Delivery section
report.add(
    Section(
        title="Delivery & Operations",
        description="Team delivery metrics and risk trends",
        children=[
            BarChart(
                title="Team Delivery Performance",
                data=team_data,
                x="team",
                y="delivered",
            ),
            LineChart(
                title="Portfolio Risk Score Trend",
                data=risk_data,
                x="week",
                y="risk_score",
            ),
        ],
    )
)

# Project details table
report.add(
    DataTable(
        title="Project Portfolio Details",
        data=projects_data,
        columns=["project", "owner", "risk", "status", "completion", "budget_used"],
    )
)

# ── Export ──────────────────────────────────────────────────────────────────────

output_path = report.export_html("portfolio_report.html")
print(f"✅ Portfolio report exported to: {output_path}")
print(f"   Open in browser: file://{output_path}")
