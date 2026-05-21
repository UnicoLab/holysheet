"""Tests for holysheet.report — Report class."""

from __future__ import annotations

import json
from typing import Any

import pytest

from holysheet import KPI, BarChart, DataTable, LineChart, Markdown, PieChart, Report, Section
from holysheet.exceptions import HolySheetError
from holysheet.schema import ReportSchema

# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestReportConstruction:
    """Test Report instantiation."""

    def test_defaults(self) -> None:
        """Report has sensible defaults."""
        r = Report()
        assert r.title == "Untitled Report"
        assert r.subtitle is None
        assert r.theme == "light"
        assert r.logo_url is None
        assert len(r) == 0

    def test_custom_values(self) -> None:
        """Report accepts custom constructor args."""
        r = Report(
            title="Q4 Review",
            subtitle="Financial Summary",
            theme="dark",
            logo_url="https://example.com/logo.png",
        )
        assert r.title == "Q4 Review"
        assert r.subtitle == "Financial Summary"
        assert r.theme == "dark"
        assert r.logo_url == "https://example.com/logo.png"

    def test_invalid_theme_raises(self) -> None:
        """Unknown theme raises HolySheetError."""
        with pytest.raises(HolySheetError, match="Unknown theme"):
            Report(theme="neon")

    def test_repr(self) -> None:
        """repr is human-readable."""
        r = Report(title="Test", theme="light")
        assert "Test" in repr(r)
        assert "light" in repr(r)


# ---------------------------------------------------------------------------
# Block management
# ---------------------------------------------------------------------------


class TestBlockManagement:
    """Test adding blocks."""

    def test_add_single(self, kpi_block: KPI) -> None:
        """Adding a block increases length."""
        r = Report()
        r.add(kpi_block)
        assert len(r) == 1

    def test_add_chaining(self, kpi_block: KPI, markdown_block: Markdown) -> None:
        """add() returns self for chaining."""
        r = Report()
        result = r.add(kpi_block).add(markdown_block)
        assert result is r
        assert len(r) == 2

    def test_blocks_property(self, kpi_block: KPI) -> None:
        """blocks property returns a copy."""
        r = Report()
        r.add(kpi_block)
        blocks = r.blocks
        assert len(blocks) == 1
        blocks.clear()  # Modifying copy shouldn't affect report
        assert len(r) == 1


# ---------------------------------------------------------------------------
# Schema generation
# ---------------------------------------------------------------------------


class TestSchemaGeneration:
    """Test converting Report to ReportSchema."""

    def test_empty_report_schema(self, empty_report: Report) -> None:
        """Empty report produces valid schema."""
        schema = empty_report.to_schema()
        assert isinstance(schema, ReportSchema)
        assert schema.title == "Test Report"
        assert schema.theme == "light"
        assert schema.blocks == []
        assert schema.schema_version == "1.0.0"

    def test_schema_block_ids(self, kpi_block: KPI, markdown_block: Markdown) -> None:
        """Block IDs are sequential."""
        r = Report()
        r.add(kpi_block)
        r.add(markdown_block)
        schema = r.to_schema()
        assert schema.blocks[0]["id"] == "block_001"
        assert schema.blocks[1]["id"] == "block_002"

    def test_schema_block_types(self, populated_report: Report) -> None:
        """Each block has the correct type in schema."""
        schema = populated_report.to_schema()
        types = [b["type"] for b in schema.blocks]
        assert "kpi" in types
        assert "line_chart" in types
        assert "bar_chart" in types
        assert "pie_chart" in types
        assert "data_table" in types
        assert "markdown" in types

    def test_kpi_props(self, kpi_block: KPI) -> None:
        """KPI block props are correct."""
        r = Report()
        r.add(kpi_block)
        schema = r.to_schema()
        props = schema.blocks[0]["props"]
        assert props["label"] == "Total Revenue"
        assert props["value"] == "$1.2M"
        assert props["delta"] == "+12.3%"
        assert props["status"] == "positive"

    def test_chart_data_conversion(self, sample_records: list[dict[str, Any]]) -> None:
        """Chart data is converted to records in props."""
        r = Report()
        r.add(LineChart(title="Test", data=sample_records, x="month", y="revenue"))
        schema = r.to_schema()
        props = schema.blocks[0]["props"]
        assert isinstance(props["data"], list)
        assert len(props["data"]) == 4

    def test_section_serialisation(self, section_block: Section) -> None:
        """Section serialises with children."""
        r = Report()
        r.add(section_block)
        schema = r.to_schema()
        block = schema.blocks[0]
        assert block["type"] == "section"
        assert "children" in block["props"]
        assert len(block["props"]["children"]) == 2

    def test_stable_ids_across_calls(self) -> None:
        """IDs are deterministic across multiple to_schema calls."""
        r = Report()
        r.add(KPI(label="A", value=1))
        r.add(KPI(label="B", value=2))
        schema1 = r.to_schema()
        schema2 = r.to_schema()
        assert schema1.blocks[0]["id"] == schema2.blocks[0]["id"]
        assert schema1.blocks[1]["id"] == schema2.blocks[1]["id"]


# ---------------------------------------------------------------------------
# JSON serialisation
# ---------------------------------------------------------------------------


class TestJsonSerialisation:
    """Test Report.to_json()."""

    def test_to_json_valid(self, populated_report: Report) -> None:
        """to_json() produces valid JSON."""
        json_str = populated_report.to_json()
        parsed = json.loads(json_str)
        assert parsed["title"] == "Full Test Report"
        assert len(parsed["blocks"]) == 6

    def test_to_json_pretty(self, empty_report: Report) -> None:
        """Pretty JSON has newlines."""
        json_str = empty_report.to_json(pretty=True)
        assert "\n" in json_str


# ---------------------------------------------------------------------------
# All block types in one report
# ---------------------------------------------------------------------------


class TestAllBlockTypes:
    """Integration test: all block types in a single report."""

    def test_comprehensive_report(self) -> None:
        """Create a report with every block type and verify schema."""
        data = [
            {"x": 1, "y": 10},
            {"x": 2, "y": 20},
            {"x": 3, "y": 30},
        ]

        r = Report(title="Comprehensive", theme="executive")
        r.add(KPI(label="Metric", value=100, delta="-5.0", status="negative"))
        r.add(LineChart(title="Line", data=data, x="x", y="y"))
        r.add(BarChart(title="Bar", data=data, x="x", y="y"))
        r.add(PieChart(title="Pie", data=data, name="x", value="y"))
        r.add(DataTable(title="Table", data=data))
        r.add(Markdown(content="# Hello\nWorld"))
        r.add(
            Section(
                title="Group",
                children=[KPI(label="Nested", value=42)],
            )
        )

        schema = r.to_schema()
        assert len(schema.blocks) == 7
        assert schema.theme == "executive"

        # Verify JSON roundtrip
        json_str = r.to_json()
        parsed = json.loads(json_str)
        assert parsed["schema_version"] == "1.0.0"
        assert len(parsed["blocks"]) == 7
