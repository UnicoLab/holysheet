"""Tests for new CLI commands — dev, lint, diff."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from click.testing import CliRunner

from holysheet.cli import cli

# ---------------------------------------------------------------------------
# version command (sanity check)
# ---------------------------------------------------------------------------


class TestVersionCommand:
    """Test the version CLI command."""

    def test_version_output(self) -> None:
        """version command prints the current version."""
        from holysheet import __version__

        runner = CliRunner()
        result = runner.invoke(cli, ["version"])
        assert result.exit_code == 0
        assert "holysheet" in result.output.lower()
        assert __version__ in result.output


# ---------------------------------------------------------------------------
# dev — Hot Reload Dev Server
# ---------------------------------------------------------------------------


class TestDevCommand:
    """Test the dev CLI command."""

    def test_help(self) -> None:
        """dev --help shows usage information."""
        runner = CliRunner()
        result = runner.invoke(cli, ["dev", "--help"])
        assert result.exit_code == 0
        output = result.output.lower()
        assert "hot" in output or "reload" in output or "dev" in output or "script" in output

    def test_dev_missing_script(self) -> None:
        """dev with nonexistent script fails gracefully."""
        runner = CliRunner()
        result = runner.invoke(cli, ["dev", "nonexistent_script.py"])
        assert result.exit_code != 0


# ---------------------------------------------------------------------------
# lint — Report Linting
# ---------------------------------------------------------------------------


class TestLintCommand:
    """Test the lint CLI command."""

    def test_help(self) -> None:
        """lint --help shows usage information."""
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", "--help"])
        assert result.exit_code == 0
        output = result.output.lower()
        assert "lint" in output or "source" in output

    def test_lint_valid_json(self, tmp_path: Path) -> None:
        """lint on a minimal valid spec JSON succeeds."""
        spec: dict[str, Any] = {
            "title": "Test Report",
            "theme": "dark",
            "blocks": [
                {
                    "id": "b1",
                    "type": "kpi",
                    "props": {
                        "label": "Revenue",
                        "value": 42,
                        "delta": "+10%",
                        "status": "positive",
                    },
                },
            ],
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(spec))
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", str(f)])
        assert result.exit_code == 0

    def test_lint_kpi_without_delta(self, tmp_path: Path) -> None:
        """lint flags KPI blocks without delta."""
        spec: dict[str, Any] = {
            "title": "Test",
            "theme": "dark",
            "blocks": [
                {
                    "id": "b1",
                    "type": "kpi",
                    "props": {"label": "Test", "value": 42},
                },
            ],
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(spec))
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", str(f)])
        assert result.exit_code == 0
        assert "delta" in result.output.lower() or "suggestion" in result.output.lower()

    def test_lint_chart_without_title(self, tmp_path: Path) -> None:
        """lint flags charts without titles."""
        spec: dict[str, Any] = {
            "title": "Test",
            "theme": "dark",
            "blocks": [
                {
                    "id": "b1",
                    "type": "line_chart",
                    "props": {"title": "", "data": [{"x": 1, "y": 2}], "x": "x", "y": "y"},
                },
            ],
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(spec))
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", str(f)])
        assert result.exit_code == 0
        assert "title" in result.output.lower() or "warning" in result.output.lower()

    def test_lint_empty_chart_data(self, tmp_path: Path) -> None:
        """lint flags charts with empty data."""
        spec: dict[str, Any] = {
            "title": "Test",
            "theme": "dark",
            "blocks": [
                {
                    "id": "b1",
                    "type": "bar_chart",
                    "props": {"title": "Empty Bar", "data": [], "x": "x", "y": "y"},
                },
            ],
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(spec))
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", str(f)])
        # Empty data should be flagged as error
        assert "empty" in result.output.lower() or "error" in result.output.lower()

    def test_lint_no_theme(self, tmp_path: Path) -> None:
        """lint flags missing theme."""
        spec: dict[str, Any] = {
            "title": "Test",
            "blocks": [],
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(spec))
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", str(f)])
        assert result.exit_code == 0
        assert "theme" in result.output.lower()

    def test_lint_strict_mode(self, tmp_path: Path) -> None:
        """lint --strict treats warnings as errors."""
        spec: dict[str, Any] = {
            "title": "Test",
            "theme": "dark",
            "blocks": [
                {
                    "id": "b1",
                    "type": "line_chart",
                    "props": {"title": "", "data": [{"x": 1, "y": 2}], "x": "x", "y": "y"},
                },
            ],
        }
        f = tmp_path / "test.json"
        f.write_text(json.dumps(spec))
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", "--strict", str(f)])
        assert result.exit_code == 1

    def test_lint_invalid_json(self, tmp_path: Path) -> None:
        """lint with invalid JSON fails gracefully."""
        f = tmp_path / "bad.json"
        f.write_text("not json {{{")
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", str(f)])
        assert result.exit_code != 0

    def test_lint_missing_file(self) -> None:
        """lint with nonexistent file fails."""
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", "nonexistent.json"])
        assert result.exit_code != 0

    def test_lint_perfect_report(self, tmp_path: Path) -> None:
        """lint on a well-formed report reports no issues."""
        spec: dict[str, Any] = {
            "title": "Perfect Report",
            "theme": "dark",
            "blocks": [
                {
                    "id": "b1",
                    "type": "kpi",
                    "props": {
                        "label": "Revenue",
                        "value": "$1.2M",
                        "delta": "+12%",
                        "status": "positive",
                    },
                },
                {
                    "id": "b2",
                    "type": "line_chart",
                    "props": {
                        "title": "Revenue Trend",
                        "data": [{"x": 1, "y": 10}],
                        "x": "x",
                        "y": "y",
                    },
                },
            ],
        }
        f = tmp_path / "perfect.json"
        f.write_text(json.dumps(spec))
        runner = CliRunner()
        result = runner.invoke(cli, ["lint", str(f)])
        assert result.exit_code == 0
        assert "no issues" in result.output.lower() or "great" in result.output.lower()


# ---------------------------------------------------------------------------
# diff — Report Comparison
# ---------------------------------------------------------------------------


class TestDiffCommand:
    """Test the diff CLI command."""

    def test_help(self) -> None:
        """diff --help shows usage information."""
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", "--help"])
        assert result.exit_code == 0
        output = result.output.lower()
        assert "file_a" in output or "compare" in output or "diff" in output

    def test_diff_identical(self, tmp_path: Path) -> None:
        """diff with identical files shows no differences."""
        spec: dict[str, Any] = {
            "title": "Test",
            "blocks": [],
        }
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text(json.dumps(spec))
        f2.write_text(json.dumps(spec))
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", str(f1), str(f2)])
        assert result.exit_code == 0
        assert "no differences" in result.output.lower() or "no diff" in result.output.lower()

    def test_diff_title_changed(self, tmp_path: Path) -> None:
        """diff detects title metadata change."""
        spec_a: dict[str, Any] = {"title": "Report A", "blocks": []}
        spec_b: dict[str, Any] = {"title": "Report B", "blocks": []}
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text(json.dumps(spec_a))
        f2.write_text(json.dumps(spec_b))
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", str(f1), str(f2)])
        assert result.exit_code == 0
        output = result.output.lower()
        assert "title" in output or "metadata" in output or "report a" in output

    def test_diff_block_changed(self, tmp_path: Path) -> None:
        """diff detects block prop changes."""
        spec_a: dict[str, Any] = {
            "title": "Test",
            "blocks": [
                {"id": "b1", "type": "kpi", "props": {"label": "X", "value": 1}},
            ],
        }
        spec_b: dict[str, Any] = {
            "title": "Test",
            "blocks": [
                {"id": "b1", "type": "kpi", "props": {"label": "X", "value": 2}},
            ],
        }
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text(json.dumps(spec_a))
        f2.write_text(json.dumps(spec_b))
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", str(f1), str(f2)])
        assert result.exit_code == 0
        output = result.output.lower()
        assert "changed" in output or "value" in output

    def test_diff_block_added(self, tmp_path: Path) -> None:
        """diff detects added blocks."""
        spec_a: dict[str, Any] = {
            "title": "Test",
            "blocks": [
                {"id": "b1", "type": "kpi", "props": {"label": "A", "value": 1}},
            ],
        }
        spec_b: dict[str, Any] = {
            "title": "Test",
            "blocks": [
                {"id": "b1", "type": "kpi", "props": {"label": "A", "value": 1}},
                {"id": "b2", "type": "kpi", "props": {"label": "B", "value": 2}},
            ],
        }
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text(json.dumps(spec_a))
        f2.write_text(json.dumps(spec_b))
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", str(f1), str(f2)])
        assert result.exit_code == 0
        output = result.output.lower()
        assert "added" in output

    def test_diff_block_removed(self, tmp_path: Path) -> None:
        """diff detects removed blocks."""
        spec_a: dict[str, Any] = {
            "title": "Test",
            "blocks": [
                {"id": "b1", "type": "kpi", "props": {"label": "A", "value": 1}},
                {"id": "b2", "type": "kpi", "props": {"label": "B", "value": 2}},
            ],
        }
        spec_b: dict[str, Any] = {
            "title": "Test",
            "blocks": [
                {"id": "b1", "type": "kpi", "props": {"label": "A", "value": 1}},
            ],
        }
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text(json.dumps(spec_a))
        f2.write_text(json.dumps(spec_b))
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", str(f1), str(f2)])
        assert result.exit_code == 0
        output = result.output.lower()
        assert "removed" in output

    def test_diff_theme_changed(self, tmp_path: Path) -> None:
        """diff detects theme metadata change."""
        spec_a: dict[str, Any] = {"title": "Test", "theme": "light", "blocks": []}
        spec_b: dict[str, Any] = {"title": "Test", "theme": "dark", "blocks": []}
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text(json.dumps(spec_a))
        f2.write_text(json.dumps(spec_b))
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", str(f1), str(f2)])
        assert result.exit_code == 0
        output = result.output.lower()
        assert "theme" in output

    def test_diff_invalid_json(self, tmp_path: Path) -> None:
        """diff with invalid JSON fails gracefully."""
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text("not json")
        f2.write_text("{}")
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", str(f1), str(f2)])
        assert result.exit_code != 0

    def test_diff_missing_file(self) -> None:
        """diff with nonexistent file fails."""
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", "nonexistent_a.json", "nonexistent_b.json"])
        assert result.exit_code != 0

    def test_diff_block_type_changed(self, tmp_path: Path) -> None:
        """diff detects block type changes."""
        spec_a: dict[str, Any] = {
            "title": "Test",
            "blocks": [
                {"id": "b1", "type": "kpi", "props": {"label": "A", "value": 1}},
            ],
        }
        spec_b: dict[str, Any] = {
            "title": "Test",
            "blocks": [
                {"id": "b1", "type": "markdown", "props": {"content": "Hello"}},
            ],
        }
        f1 = tmp_path / "a.json"
        f2 = tmp_path / "b.json"
        f1.write_text(json.dumps(spec_a))
        f2.write_text(json.dumps(spec_b))
        runner = CliRunner()
        result = runner.invoke(cli, ["diff", str(f1), str(f2)])
        assert result.exit_code == 0
        output = result.output.lower()
        assert "changed" in output or "type" in output


# ---------------------------------------------------------------------------
# validate command
# ---------------------------------------------------------------------------


class TestValidateCommand:
    """Test the validate CLI command."""

    def test_help(self) -> None:
        """validate --help shows usage information."""
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", "--help"])
        assert result.exit_code == 0

    def test_validate_valid_json(self, tmp_path: Path) -> None:
        """validate with valid spec JSON succeeds."""
        spec: dict[str, Any] = {
            "title": "Test",
            "theme": "dark",
            "blocks": [],
        }
        f = tmp_path / "valid.json"
        f.write_text(json.dumps(spec))
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", str(f)])
        assert result.exit_code == 0
        assert "valid" in result.output.lower()

    def test_validate_invalid_json(self, tmp_path: Path) -> None:
        """validate with invalid JSON fails."""
        f = tmp_path / "bad.json"
        f.write_text("not json {{{")
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", str(f)])
        assert result.exit_code != 0
