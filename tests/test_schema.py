"""Tests for holysheet.schema — ReportSchema model."""

from __future__ import annotations

import json
from typing import Any

from holysheet.schema import ReportSchema


class TestReportSchemaDefaults:
    """Test ReportSchema default values."""

    def test_defaults(self) -> None:
        """Schema has sensible defaults."""
        schema = ReportSchema()
        assert schema.schema_version == "1.0.0"
        assert schema.title == "Untitled Report"
        assert schema.subtitle is None
        assert schema.theme == "light"
        assert schema.logo_url is None
        assert schema.blocks == []
        assert schema.created_at  # non-empty string

    def test_custom_values(self) -> None:
        """Schema accepts custom values."""
        schema = ReportSchema(
            title="My Report",
            subtitle="Q4 2024",
            theme="dark",
            logo_url="https://example.com/logo.png",
        )
        assert schema.title == "My Report"
        assert schema.subtitle == "Q4 2024"
        assert schema.theme == "dark"
        assert schema.logo_url == "https://example.com/logo.png"


class TestReportSchemaSerialisation:
    """Test serialisation methods."""

    def test_to_dict(self) -> None:
        """to_dict returns a plain dict."""
        schema = ReportSchema(title="Test")
        d = schema.to_dict()
        assert isinstance(d, dict)
        assert d["title"] == "Test"
        assert d["schema_version"] == "1.0.0"
        assert "blocks" in d

    def test_to_json(self) -> None:
        """to_json returns a valid JSON string."""
        schema = ReportSchema(title="JSON Test")
        json_str = schema.to_json()
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed["title"] == "JSON Test"

    def test_to_json_pretty(self) -> None:
        """Pretty JSON has indentation."""
        schema = ReportSchema(title="Pretty")
        json_str = schema.to_json(pretty=True)
        assert "\n" in json_str
        assert "  " in json_str

    def test_to_json_bytes(self) -> None:
        """to_json_bytes returns bytes."""
        schema = ReportSchema(title="Bytes")
        result = schema.to_json_bytes()
        assert isinstance(result, bytes)
        parsed = json.loads(result)
        assert parsed["title"] == "Bytes"

    def test_with_blocks(self) -> None:
        """Blocks are included in serialisation."""
        blocks = [
            {"id": "block_001", "type": "kpi", "props": {"label": "Test", "value": 42}},
        ]
        schema = ReportSchema(title="With Blocks", blocks=blocks)
        d = schema.to_dict()
        assert len(d["blocks"]) == 1
        assert d["blocks"][0]["type"] == "kpi"

    def test_roundtrip(self) -> None:
        """Schema survives JSON roundtrip."""
        original = ReportSchema(
            title="Roundtrip",
            subtitle="Test",
            theme="executive",
            blocks=[{"id": "block_001", "type": "markdown", "props": {"content": "Hello"}}],
        )
        json_str = original.to_json()
        restored = ReportSchema.model_validate_json(json_str)
        assert restored.title == original.title
        assert restored.subtitle == original.subtitle
        assert restored.theme == original.theme
        assert len(restored.blocks) == len(original.blocks)


class TestReportSchemaValidation:
    """Test Pydantic validation on ReportSchema."""

    def test_model_validate_dict(self) -> None:
        """model_validate works with a raw dict."""
        data: dict[str, Any] = {
            "title": "From Dict",
            "schema_version": "1.0.0",
            "theme": "light",
            "blocks": [],
        }
        schema = ReportSchema.model_validate(data)
        assert schema.title == "From Dict"

    def test_extra_fields_allowed(self) -> None:
        """Extra fields don't raise (Pydantic default: ignore)."""
        data: dict[str, Any] = {
            "title": "Extra",
            "unknown_field": "should be ignored",
        }
        schema = ReportSchema.model_validate(data)
        assert schema.title == "Extra"
