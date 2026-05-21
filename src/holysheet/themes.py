"""HolySheet theme definitions.

Each theme is a dictionary containing colours, fonts, and spacing tokens
consumed by the React renderer.
"""

from __future__ import annotations

from typing import Any

from holysheet.exceptions import HolySheetError

# ---------------------------------------------------------------------------
# Theme definitions
# ---------------------------------------------------------------------------

THEMES: dict[str, dict[str, Any]] = {
    "light": {
        "name": "light",
        "colors": {
            "background": "#FFFFFF",
            "surface": "#F8F9FA",
            "primary": "#2563EB",
            "primary_light": "#DBEAFE",
            "secondary": "#7C3AED",
            "text": "#1F2937",
            "text_secondary": "#6B7280",
            "border": "#E5E7EB",
            "success": "#059669",
            "warning": "#D97706",
            "danger": "#DC2626",
            "info": "#2563EB",
            "chart_palette": [
                "#2563EB",
                "#7C3AED",
                "#059669",
                "#D97706",
                "#DC2626",
                "#0891B2",
                "#4F46E5",
                "#BE185D",
            ],
        },
        "fonts": {
            "body": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "heading": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "mono": "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
            "size_base": "14px",
            "size_sm": "12px",
            "size_lg": "16px",
            "size_xl": "20px",
            "size_2xl": "24px",
            "size_3xl": "30px",
        },
        "spacing": {
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px",
            "2xl": "48px",
        },
        "border_radius": {
            "sm": "4px",
            "md": "8px",
            "lg": "12px",
            "xl": "16px",
        },
        "shadows": {
            "sm": "0 1px 2px rgba(0,0,0,0.05)",
            "md": "0 4px 6px -1px rgba(0,0,0,0.1)",
            "lg": "0 10px 15px -3px rgba(0,0,0,0.1)",
        },
    },
    "dark": {
        "name": "dark",
        "colors": {
            "background": "#111827",
            "surface": "#1F2937",
            "primary": "#3B82F6",
            "primary_light": "#1E3A5F",
            "secondary": "#8B5CF6",
            "text": "#F9FAFB",
            "text_secondary": "#9CA3AF",
            "border": "#374151",
            "success": "#10B981",
            "warning": "#F59E0B",
            "danger": "#EF4444",
            "info": "#3B82F6",
            "chart_palette": [
                "#3B82F6",
                "#8B5CF6",
                "#10B981",
                "#F59E0B",
                "#EF4444",
                "#06B6D4",
                "#6366F1",
                "#EC4899",
            ],
        },
        "fonts": {
            "body": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "heading": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            "mono": "'JetBrains Mono', 'Fira Code', 'Consolas', monospace",
            "size_base": "14px",
            "size_sm": "12px",
            "size_lg": "16px",
            "size_xl": "20px",
            "size_2xl": "24px",
            "size_3xl": "30px",
        },
        "spacing": {
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px",
            "2xl": "48px",
        },
        "border_radius": {
            "sm": "4px",
            "md": "8px",
            "lg": "12px",
            "xl": "16px",
        },
        "shadows": {
            "sm": "0 1px 2px rgba(0,0,0,0.3)",
            "md": "0 4px 6px -1px rgba(0,0,0,0.4)",
            "lg": "0 10px 15px -3px rgba(0,0,0,0.5)",
        },
    },
    "executive": {
        "name": "executive",
        "colors": {
            "background": "#FAF9F7",
            "surface": "#FFFFFF",
            "primary": "#1B4332",
            "primary_light": "#D8F3DC",
            "secondary": "#40916C",
            "text": "#2D3436",
            "text_secondary": "#636E72",
            "border": "#DFE6E9",
            "success": "#00B894",
            "warning": "#FDCB6E",
            "danger": "#E17055",
            "info": "#0984E3",
            "chart_palette": [
                "#1B4332",
                "#40916C",
                "#2D6A4F",
                "#52B788",
                "#74C69D",
                "#95D5B2",
                "#0984E3",
                "#6C5CE7",
            ],
        },
        "fonts": {
            "body": "'Georgia', 'Times New Roman', serif",
            "heading": "'Georgia', 'Times New Roman', serif",
            "mono": "'Courier New', 'Courier', monospace",
            "size_base": "15px",
            "size_sm": "13px",
            "size_lg": "17px",
            "size_xl": "21px",
            "size_2xl": "26px",
            "size_3xl": "32px",
        },
        "spacing": {
            "xs": "4px",
            "sm": "8px",
            "md": "16px",
            "lg": "24px",
            "xl": "32px",
            "2xl": "48px",
        },
        "border_radius": {
            "sm": "2px",
            "md": "4px",
            "lg": "8px",
            "xl": "12px",
        },
        "shadows": {
            "sm": "0 1px 3px rgba(0,0,0,0.04)",
            "md": "0 2px 8px rgba(0,0,0,0.06)",
            "lg": "0 6px 16px rgba(0,0,0,0.08)",
        },
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def validate_theme(name: str) -> dict[str, Any]:
    """Return the theme dict for *name*, raising on unknown themes.

    Args:
        name: One of ``'light'``, ``'dark'``, or ``'executive'``.

    Returns:
        The full theme dictionary.

    Raises:
        HolySheetError: If *name* is not a known theme.
    """
    if name not in THEMES:
        available = ", ".join(sorted(THEMES.keys()))
        raise HolySheetError(f"Unknown theme '{name}'. Available themes: {available}")
    return THEMES[name]


def list_themes() -> list[str]:
    """Return sorted list of available theme names.

    Returns:
        Sorted list of theme name strings.
    """
    return sorted(THEMES.keys())


# ---------------------------------------------------------------------------
# Custom Theme API
# ---------------------------------------------------------------------------


class Theme:
    """Custom theme builder for branded dashboards.

    Create a fully custom theme by overriding base theme tokens::

        from holysheet.themes import Theme

        brand = Theme(
            name="brand",
            primary="#FF6B00",
            background="#0A0A0F",
            font="Satoshi",
            chart_palette=["#FF6B00", "#00D4AA", "#6366F1"],
        )
        report = Report(title="Branded", theme=brand)

    Args:
        name: Theme name identifier.
        base: Base theme to extend (``'dark'``, ``'light'``, ``'executive'``).
        primary: Primary brand color.
        secondary: Secondary color.
        background: Background color.
        surface: Card/surface color.
        text: Main text color.
        text_secondary: Secondary text color.
        border: Border color.
        success: Success status color.
        warning: Warning status color.
        danger: Danger/error color.
        info: Info color.
        font: Body + heading font family.
        mono_font: Monospace font family.
        chart_palette: List of chart colors.
    """

    def __init__(
        self,
        name: str = "custom",
        base: str = "dark",
        primary: str | None = None,
        secondary: str | None = None,
        background: str | None = None,
        surface: str | None = None,
        text: str | None = None,
        text_secondary: str | None = None,
        border: str | None = None,
        success: str | None = None,
        warning: str | None = None,
        danger: str | None = None,
        info: str | None = None,
        font: str | None = None,
        mono_font: str | None = None,
        chart_palette: list[str] | None = None,
    ) -> None:
        if base not in THEMES:
            available = ", ".join(sorted(THEMES.keys()))
            raise HolySheetError(f"Unknown base theme '{base}'. Available: {available}")

        import copy

        self.name = name
        self._theme = copy.deepcopy(THEMES[base])
        self._theme["name"] = name

        # Override colors
        color_overrides = {
            "primary": primary,
            "secondary": secondary,
            "background": background,
            "surface": surface,
            "text": text,
            "text_secondary": text_secondary,
            "border": border,
            "success": success,
            "warning": warning,
            "danger": danger,
            "info": info,
        }
        for key, value in color_overrides.items():
            if value is not None:
                self._theme["colors"][key] = value

        if chart_palette is not None:
            self._theme["colors"]["chart_palette"] = chart_palette

        # Override fonts
        if font is not None:
            font_stack = f"'{font}', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
            self._theme["fonts"]["body"] = font_stack
            self._theme["fonts"]["heading"] = font_stack

        if mono_font is not None:
            mono_stack = f"'{mono_font}', 'Fira Code', 'Consolas', monospace"
            self._theme["fonts"]["mono"] = mono_stack

    def to_dict(self) -> dict[str, Any]:
        """Return the full theme dictionary.

        Returns:
            Complete theme dict compatible with the renderer.
        """
        return self._theme

    def __repr__(self) -> str:
        return f"Theme(name={self.name!r})"
