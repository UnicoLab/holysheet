"""Tests for holysheet.exporters — HTML, folder, and JSON export."""

from __future__ import annotations

import json
from pathlib import Path

from holysheet import KPI, Markdown, Report
from holysheet.exporters import export_folder, export_json, export_standalone_html
from holysheet.schema import ReportSchema

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_schema() -> ReportSchema:
    """Build a minimal ReportSchema for testing."""
    r = Report(title="Export Test")
    r.add(KPI(label="Users", value=42_000, status="positive"))
    r.add(Markdown(content="Hello world"))
    return r.to_schema()


# ---------------------------------------------------------------------------
# Standalone HTML export
# ---------------------------------------------------------------------------


class TestStandaloneHtmlExport:
    """Test export_standalone_html()."""

    def test_creates_file(self, tmp_path: Path) -> None:
        """HTML file is created."""
        schema = _make_schema()
        out = tmp_path / "report.html"
        result = export_standalone_html(schema, out)
        assert result.exists()
        assert result.suffix == ".html"

    def test_contains_spec(self, tmp_path: Path) -> None:
        """HTML contains the JSON spec."""
        schema = _make_schema()
        out = tmp_path / "report.html"
        export_standalone_html(schema, out)
        html = out.read_text(encoding="utf-8")
        assert "window.__HOLYSHEET_SPEC__" in html
        assert "Export Test" in html

    def test_contains_css_and_js(self, tmp_path: Path) -> None:
        """HTML embeds CSS and JS."""
        schema = _make_schema()
        out = tmp_path / "report.html"
        export_standalone_html(schema, out)
        html = out.read_text(encoding="utf-8")
        assert "<style>" in html
        assert "<script>" in html

    def test_valid_html_structure(self, tmp_path: Path) -> None:
        """HTML has proper structure."""
        schema = _make_schema()
        out = tmp_path / "report.html"
        export_standalone_html(schema, out)
        html = out.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in html
        assert '<div id="root">' in html
        assert "<title>" in html

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        """Parent directories are created."""
        schema = _make_schema()
        out = tmp_path / "subdir" / "nested" / "report.html"
        result = export_standalone_html(schema, out)
        assert result.exists()

    def test_report_shortcut(self, tmp_path: Path) -> None:
        """Report.export_html() works as a shortcut."""
        r = Report(title="Shortcut Test")
        r.add(KPI(label="A", value=1))
        result = r.export_html(tmp_path / "report.html")
        assert result.exists()


# ---------------------------------------------------------------------------
# Folder export
# ---------------------------------------------------------------------------


class TestFolderExport:
    """Test export_folder()."""

    def test_creates_structure(self, tmp_path: Path) -> None:
        """Folder export creates expected structure."""
        schema = _make_schema()
        out_dir = tmp_path / "output"
        result = export_folder(schema, out_dir)
        assert result.is_dir()
        assert (result / "index.html").exists()
        assert (result / "report.json").exists()
        assert (result / "assets").is_dir()

    def test_report_json_valid(self, tmp_path: Path) -> None:
        """report.json is valid JSON with correct content."""
        schema = _make_schema()
        out_dir = tmp_path / "output"
        export_folder(schema, out_dir)
        json_path = out_dir / "report.json"
        data = json.loads(json_path.read_text(encoding="utf-8"))
        assert data["title"] == "Export Test"
        assert len(data["blocks"]) == 2

    def test_assets_copied(self, tmp_path: Path) -> None:
        """Asset files are copied."""
        schema = _make_schema()
        out_dir = tmp_path / "output"
        export_folder(schema, out_dir)
        assets = list((out_dir / "assets").iterdir())
        assert len(assets) >= 1  # At least the placeholder files

    def test_spec_loader_created(self, tmp_path: Path) -> None:
        """spec-loader.js is created."""
        schema = _make_schema()
        out_dir = tmp_path / "output"
        export_folder(schema, out_dir)
        loader = out_dir / "spec-loader.js"
        assert loader.exists()
        content = loader.read_text(encoding="utf-8")
        assert "__HOLYSHEET_SPEC__" in content

    def test_report_shortcut(self, tmp_path: Path) -> None:
        """Report.export_folder() works as a shortcut."""
        r = Report(title="Folder Shortcut")
        r.add(KPI(label="B", value=2))
        result = r.export_folder(tmp_path / "folder_out")
        assert result.is_dir()


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------


class TestJsonExport:
    """Test export_json()."""

    def test_creates_file(self, tmp_path: Path) -> None:
        """JSON file is created."""
        schema = _make_schema()
        out = tmp_path / "report.json"
        result = export_json(schema, out)
        assert result.exists()

    def test_valid_json(self, tmp_path: Path) -> None:
        """Output is valid JSON."""
        schema = _make_schema()
        out = tmp_path / "report.json"
        export_json(schema, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["title"] == "Export Test"
        assert data["schema_version"] == "1.0.0"

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        """Parent directories are created."""
        schema = _make_schema()
        out = tmp_path / "deep" / "path" / "report.json"
        result = export_json(schema, out)
        assert result.exists()

    def test_report_shortcut(self, tmp_path: Path) -> None:
        """Report.export_json() works as a shortcut."""
        r = Report(title="JSON Shortcut")
        r.add(KPI(label="C", value=3))
        result = r.export_json(tmp_path / "out.json")
        assert result.exists()
        data = json.loads(result.read_text(encoding="utf-8"))
        assert data["title"] == "JSON Shortcut"
