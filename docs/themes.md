---
title: Theming
description: Customize the look and feel of your HolySheet dashboards
---

# :material-palette: Theming

HolySheet ships with **three carefully designed themes** that give your dashboards a polished, professional appearance out of the box.

<div style="display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; margin: 2rem 0;">
<div style="text-align: center; flex: 1; min-width: 250px;">
<img src="../assets/screenshots/screenshot_dark_theme.png" alt="Dark Theme" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.3);" />
<p style="font-weight: 600; margin-top: 0.5rem;">🌙 Dark Theme</p>
</div>
<div style="text-align: center; flex: 1; min-width: 250px;">
<img src="../assets/screenshots/screenshot_light_theme.png" alt="Light Theme" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.15);" />
<p style="font-weight: 600; margin-top: 0.5rem;">☀️ Light Theme</p>
</div>
<div style="text-align: center; flex: 1; min-width: 250px;">
<img src="../assets/screenshots/screenshot_executive_theme.png" alt="Executive Theme" style="width: 100%; border-radius: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.3);" />
<p style="font-weight: 600; margin-top: 0.5rem;">👔 Executive Theme</p>
</div>
</div>

!!! info "KPI Cards Across All Themes"
    <img src="../assets/screenshots/screenshot_kpi_cards.png" alt="KPI Cards Comparison" style="width: 100%; border-radius: 8px; margin-top: 0.5rem;" />
    <p style="text-align: center; font-size: 0.85rem; margin-top: 0.5rem;"><em>The same KPI cards automatically adapt to your chosen theme's design system.</em></p>

## Available Themes

=== ":material-weather-night: Dark"

    The default theme — a sleek dark interface with vibrant accent colors, perfect for data-heavy dashboards viewed on screens.

    ```python
    report = Report(title="My Dashboard", theme="dark")
    ```

    | Property | Value |
    |---|---|
    | Background | `#0a0a0f` |
    | Cards | Frosted glass (`rgba(20, 20, 35, 0.85)`) |
    | Primary | `#6C63FF` (Indigo) |
    | Secondary | `#00D9FF` (Cyan) |
    | Positive | `#34D399` (Emerald) |
    | Negative | `#F87171` (Rose) |

=== ":material-white-balance-sunny: Light"

    A clean, bright theme ideal for printing or embedding in professional reports.

    ```python
    report = Report(title="My Dashboard", theme="light")
    ```

    | Property | Value |
    |---|---|
    | Background | `#F5F7FA` |
    | Cards | `#FFFFFF` |
    | Primary | `#4F46E5` (Indigo) |
    | Secondary | `#0EA5E9` (Sky) |
    | Positive | `#10B981` (Emerald) |
    | Negative | `#EF4444` (Red) |

=== ":material-crown: Executive"

    A premium gold-accented dark theme designed for C-suite presentations and board reports.

    ```python
    report = Report(title="Board Report Q4", theme="executive")
    ```

    | Property | Value |
    |---|---|
    | Background | `#09090C` |
    | Cards | `rgba(18, 18, 24, 0.9)` with gold borders |
    | Primary | `#D4AF37` (Gold) |
    | Secondary | `#C0A062` (Antique Gold) |
    | Positive | `#34D399` (Emerald) |
    | Negative | `#F87171` (Rose) |

## Design Features

All themes share these premium design qualities:

<div class="hs-features" markdown>
<div class="hs-feature-card" markdown>
### :material-blur: Glassmorphism
Cards use frosted glass effects with `backdrop-filter: blur()` for depth and elegance.
</div>

<div class="hs-feature-card" markdown>
### :material-gesture-tap: Hover Effects
Every card lifts on hover with smooth shadow transitions, making the dashboard feel alive.
</div>

<div class="hs-feature-card" markdown>
### :material-format-font: Inter Typography
Modern Inter font with optimized sizing, weight hierarchy, and letter spacing.
</div>

<div class="hs-feature-card" markdown>
### :material-responsive: Responsive
Layouts auto-adapt from desktop to tablet to mobile with fluid grid breakpoints.
</div>
</div>

## Chart Colors

Each theme includes a curated 8-color palette for charts:

```python
# Dark theme chart colors
['#6C63FF', '#00D9FF', '#34D399', '#FBBF24',
 '#F87171', '#A78BFA', '#FB923C', '#38BDF8']

# Light theme chart colors
['#4F46E5', '#0EA5E9', '#10B981', '#F59E0B',
 '#EF4444', '#8B5CF6', '#F97316', '#06B6D4']

# Executive theme chart colors
['#D4AF37', '#C0A062', '#34D399', '#F5F0E8',
 '#F87171', '#A78BFA', '#E8C547', '#8B7536']
```

Multi-series charts automatically cycle through these colors.

## Choosing the Right Theme

| Use Case | Recommended Theme |
|---|---|
| Internal dashboards | `dark` |
| Client-facing reports | `light` |
| Board presentations | `executive` |
| Printed reports | `light` |
| Data exploration | `dark` |
| Financial reports | `executive` |

!!! tip "Theme Consistency"
    Choose one theme per report. All blocks within a report automatically inherit the theme's colors, fonts, and styling — no per-block configuration needed.
