"""Tests for v0.5.0 features — AI Insight, Google Sheet, anomaly detection,
PDF export, publish CLI, SQL block, narration, auto_narrate.
"""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from holysheet import (
    KPI,
    AIInsight,
    AreaChart,
    BarChart,
    GoogleSheet,
    LineChart,
    NarrationBlock,
    Report,
    SqlBlock,
)
from holysheet.cli import cli

# ---------------------------------------------------------------------------
# AIInsight block
# ---------------------------------------------------------------------------


class TestAIInsight:
    def test_basic_construction(self) -> None:
        block = AIInsight(
            title="Revenue Insight",
            data=[{"month": "Jan", "revenue": 100}],
            provider="openai",
        )
        assert block.type == "ai_insight"
        assert block.title == "Revenue Insight"
        assert block.provider == "openai"

    def test_serialize(self) -> None:
        block = AIInsight(title="Test", data=[{"x": 1}])
        result = block.serialize("block_001")
        assert result["id"] == "block_001"
        assert result["type"] == "ai_insight"
        assert "title" in result["props"]
        assert "text" in result["props"]

    def test_fallback_when_no_openai(self) -> None:
        """When openai is not installed, returns a helpful message."""
        block = AIInsight(title="Test", data=[{"x": 1}], provider="openai")
        props = block.to_props()
        # Since openai likely not installed in test env
        assert "text" in props
        assert isinstance(props["text"], str)

    def test_fallback_when_no_anthropic(self) -> None:
        block = AIInsight(title="Test", data=[{"x": 1}], provider="anthropic")
        props = block.to_props()
        assert "text" in props

    def test_fallback_when_no_google(self) -> None:
        block = AIInsight(title="Test", data=[{"x": 1}], provider="google")
        props = block.to_props()
        assert "text" in props

    def test_custom_prompt(self) -> None:
        block = AIInsight(
            title="Custom",
            data=[{"x": 1}],
            prompt="Summarise this data",
        )
        assert block.prompt == "Summarise this data"

    def test_in_report(self) -> None:
        r = Report(title="Test")
        r.add(AIInsight(title="Insight", data=[{"a": 1}]))
        schema = r.to_schema()
        assert len(schema.blocks) == 1
        assert schema.blocks[0]["type"] == "ai_insight"


# ---------------------------------------------------------------------------
# GoogleSheet block
# ---------------------------------------------------------------------------


class TestGoogleSheet:
    def test_basic_construction(self) -> None:
        block = GoogleSheet(
            spreadsheet_id="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
            title="Sales Data",
        )
        assert block.type == "google_sheet"
        assert block.spreadsheet_id == "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms"

    def test_serialize(self) -> None:
        block = GoogleSheet(spreadsheet_id="abc123", title="Sheet")
        result = block.serialize("block_001")
        assert result["type"] == "google_sheet"

    def test_fallback_when_no_gspread(self) -> None:
        """When gspread is not installed, returns error dict."""
        block = GoogleSheet(spreadsheet_id="abc123")
        props = block.to_props()
        assert "data" in props
        # Will contain error about missing gspread or network error
        assert isinstance(props["data"], list)

    def test_with_sheet_name(self) -> None:
        block = GoogleSheet(
            spreadsheet_id="abc123",
            sheet_name="Sheet2",
        )
        assert block.sheet_name == "Sheet2"

    def test_with_range(self) -> None:
        block = GoogleSheet(
            spreadsheet_id="abc123",
            range="A1:D100",
        )
        assert block.range == "A1:D100"

    def test_in_report(self) -> None:
        r = Report(title="Test")
        r.add(GoogleSheet(spreadsheet_id="abc", title="Data"))
        schema = r.to_schema()
        assert len(schema.blocks) == 1
        assert schema.blocks[0]["type"] == "google_sheet"


# ---------------------------------------------------------------------------
# Anomaly detection
# ---------------------------------------------------------------------------


class TestAnomalyDetection:
    def test_line_chart_anomaly_detection(self) -> None:
        data = [{"x": i, "y": 10} for i in range(20)]
        data.append({"x": 20, "y": 1000})  # outlier
        block = LineChart(title="Test", data=data, x="x", y="y", anomaly_detection=True)
        props = block.to_props()
        assert "annotations" in props
        annotations = props["annotations"]
        assert any(a.get("text") == "⚠ Anomaly" for a in annotations)

    def test_area_chart_anomaly_detection(self) -> None:
        data = [{"x": i, "y": 5} for i in range(20)]
        data.append({"x": 20, "y": -100})  # outlier
        block = AreaChart(title="Test", data=data, x="x", y="y", anomaly_detection=True)
        props = block.to_props()
        assert "annotations" in props

    def test_bar_chart_anomaly_detection(self) -> None:
        data = [{"cat": f"C{i}", "val": 50} for i in range(15)]
        data.append({"cat": "C99", "val": 500})
        block = BarChart(title="Test", data=data, x="cat", y="val", anomaly_detection=True)
        props = block.to_props()
        assert "annotations" in props

    def test_no_anomalies_in_uniform_data(self) -> None:
        data = [{"x": i, "y": 10} for i in range(20)]
        block = LineChart(title="Test", data=data, x="x", y="y", anomaly_detection=True)
        props = block.to_props()
        # All values identical = IQR is 0 = no anomalies
        assert props.get("annotations") is None or len(props.get("annotations", [])) == 0

    def test_anomaly_detection_disabled_by_default(self) -> None:
        data = [{"x": i, "y": 10} for i in range(20)]
        data.append({"x": 20, "y": 1000})
        block = LineChart(title="Test", data=data, x="x", y="y")
        props = block.to_props()
        # No anomaly annotations without the flag
        assert "annotations" not in props

    def test_anomaly_detection_with_few_points(self) -> None:
        data = [{"x": 1, "y": 1}, {"x": 2, "y": 100}]
        block = LineChart(title="Test", data=data, x="x", y="y", anomaly_detection=True)
        props = block.to_props()
        # Too few points (<4) for IQR, should not crash
        assert "annotations" not in props or len(props.get("annotations", [])) == 0


# ---------------------------------------------------------------------------
# SQL Block
# ---------------------------------------------------------------------------


class TestSqlBlock:
    def test_basic(self) -> None:
        block = SqlBlock(
            query="SELECT * FROM data",
            data=[{"a": 1, "b": 2}],
            title="Query",
        )
        assert block.type == "sql_block"
        props = block.to_props()
        assert props["query"] == "SELECT * FROM data"
        assert props["data"] == [{"a": 1, "b": 2}]

    def test_serialize(self) -> None:
        block = SqlBlock(query="SELECT 1", title="Test")
        result = block.serialize("block_001")
        assert result["type"] == "sql_block"

    def test_output_chart(self) -> None:
        block = SqlBlock(query="SELECT x, y FROM t", output="chart")
        assert block.output == "chart"

    def test_in_report(self) -> None:
        r = Report(title="Test")
        r.add(SqlBlock(query="SELECT * FROM t", data=[{"x": 1}]))
        schema = r.to_schema()
        assert schema.blocks[0]["type"] == "sql_block"


# ---------------------------------------------------------------------------
# Narration Block
# ---------------------------------------------------------------------------


class TestNarrationBlock:
    def test_basic(self) -> None:
        block = NarrationBlock(text="Revenue grew by 15% this quarter.")
        assert block.type == "narration"
        props = block.to_props()
        assert props["text"] == "Revenue grew by 15% this quarter."
        assert props["autoplay"] is False

    def test_autoplay(self) -> None:
        block = NarrationBlock(text="Hello", autoplay=True)
        assert block.autoplay is True

    def test_serialize(self) -> None:
        block = NarrationBlock(text="Test")
        result = block.serialize("block_001")
        assert result["type"] == "narration"


# ---------------------------------------------------------------------------
# Auto-narrate
# ---------------------------------------------------------------------------


class TestAutoNarrate:
    def test_basic_narration(self) -> None:
        r = Report(title="Q4 Summary")
        r.add(KPI(label="Revenue", value="$1.2M", delta="+12%"))
        r.add(KPI(label="Users", value="42K", unit="users"))
        text = r.auto_narrate()
        assert "Revenue is $1.2M" in text
        assert "+12%" in text
        assert "Users is 42K" in text
        assert "users" in text

    def test_empty_report(self) -> None:
        r = Report(title="Empty")
        text = r.auto_narrate()
        assert "Empty" in text

    def test_with_chart_titles(self) -> None:
        r = Report(title="Test")
        r.add(LineChart(title="Revenue Trend", data=[], x="x", y="y"))
        text = r.auto_narrate()
        assert "Revenue Trend" in text


# ---------------------------------------------------------------------------
# PDF export
# ---------------------------------------------------------------------------


class TestPDFExport:
    def test_export_pdf_produces_file(self, tmp_path: Path) -> None:
        """PDF export should produce a file (if Chrome/Playwright available) or raise."""
        r = Report(title="Test")
        r.add(KPI(label="X", value=1))
        out = tmp_path / "out.pdf"
        try:
            result = r.export_pdf(out)
            # If it succeeds, a PDF file should exist
            assert result.exists()
            assert result.stat().st_size > 0
        except RuntimeError as exc:
            # No browser available — expected in CI
            assert "headless browser" in str(exc)


# ---------------------------------------------------------------------------
# Publish CLI
# ---------------------------------------------------------------------------


class TestPublishCLI:
    def test_help(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["publish", "--help"])
        assert result.exit_code == 0
        assert "s3" in result.output.lower() or "S3" in result.output

    def test_unsupported_scheme(self, tmp_path: Path) -> None:
        f = tmp_path / "report.html"
        f.write_text("<html></html>")
        runner = CliRunner()
        result = runner.invoke(cli, ["publish", str(f), "-t", "ftp://example.com/x"])
        assert result.exit_code != 0
        assert "Unsupported" in result.output

    def test_missing_boto3(self, tmp_path: Path) -> None:
        f = tmp_path / "report.html"
        f.write_text("<html></html>")
        runner = CliRunner()
        result = runner.invoke(cli, ["publish", str(f), "-t", "s3://bucket/key"])
        # Should fail gracefully with install message
        assert result.exit_code != 0
