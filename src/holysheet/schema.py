"""Report schema model for HolySheet.

:class:`ReportSchema` is the top-level Pydantic model that describes a
complete report specification.  It is serialised to JSON and consumed by
the React renderer via ``window.__HOLYSHEET_SPEC__``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import orjson
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Schema model
# ---------------------------------------------------------------------------


class ReportSchema(BaseModel):
    """Full HolySheet report schema.

    Attributes:
        schema_version: Spec version string (``"1.0.0"``).
        title: Report title.
        subtitle: Optional report subtitle.
        theme: Theme name (``"light"``, ``"dark"``, ``"executive"``).
        logo_url: Optional URL to a logo image.
        created_at: ISO-8601 creation timestamp.
        blocks: Serialised block dicts.
        features: Feature flags for the React renderer.
        custom_theme: Custom theme dict when using Theme API.
        expires: ISO-8601 date after which the report shows expired.
    """

    schema_version: str = "1.0.0"
    title: str = "Untitled Report"
    subtitle: str | None = None
    theme: str = "light"
    logo_url: str | None = None
    author: str | None = None
    report_version: str | None = None
    footer: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    blocks: list[dict[str, Any]] = Field(default_factory=list)

    # v0.4.0 additions
    features: dict[str, Any] | None = None
    custom_theme: dict[str, Any] | None = None
    expires: str | None = None
    filters: list[dict[str, Any]] = Field(default_factory=list)

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        """Convert schema to a plain dict.

        Returns:
            Dictionary representation suitable for JSON encoding.
        """
        d = self.model_dump(mode="python")
        # Remove None values for cleaner JSON
        return {k: v for k, v in d.items() if v is not None}

    def to_json(self, *, pretty: bool = False) -> str:
        """Serialise schema to a JSON string using orjson.

        Args:
            pretty: If ``True``, format the JSON with indentation.

        Returns:
            UTF-8 JSON string.
        """
        opts = orjson.OPT_NON_STR_KEYS
        if pretty:
            opts |= orjson.OPT_INDENT_2
        return orjson.dumps(self.to_dict(), option=opts).decode("utf-8")

    def to_json_bytes(self) -> bytes:
        """Serialise schema to JSON bytes using orjson.

        Returns:
            UTF-8 encoded JSON bytes.
        """
        return orjson.dumps(self.to_dict(), option=orjson.OPT_NON_STR_KEYS)
