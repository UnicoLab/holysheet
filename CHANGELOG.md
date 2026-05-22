# CHANGELOG


## v0.3.0 (2026-05-22)

### Continuous Integration

- Complete CI/CD pipeline with semantic-release, PyPI, and mike docs
  ([`187731f`](https://github.com/UnicoLab/holysheet/commit/187731fd009352d498b094109804f15969861062))

- ci.yml: add workflow_call trigger + TypeScript check step - release.yml: gate on CI, frontend
  build before semantic-release, PyPI trusted publishing, manual trigger with dry-run/force options,
  GitHub Release upload, job summary - docs.yml: rewrite with mike for versioned docs — auto-deploy
  'dev' on push to main, deploy major.minor on release tag, manual trigger with version input -
  mkdocs.yml: add mike plugin + version provider for header selector - pyproject.toml: add mike>=2.1
  to docs deps

- **release**: Add full CI/CD pipeline aligned with FlowyML
  ([`06c2192`](https://github.com/UnicoLab/holysheet/commit/06c21924795d97d50b2e88a04b434f73e676ab67))

- Bump version to 0.5.0 (sync pyproject.toml + __init__.py with CHANGELOG) - Add
  .pre-commit-config.yaml (ruff, standard hooks, conventional commits) - Add PRECOMMITS.yml workflow
  (PR title validation + pre-commit) - Add PR_PREVIEW.yml workflow (docs preview on PRs) - Add
  MANUAL_PYPI_PUBLISH.yml workflow (recovery: manual PyPI publish) - Add MANUAL_DOCS_PUBLISH.yml
  workflow (recovery: manual docs deploy) - Enhance ci.yml (dev branch, concurrency, coverage with
  Codecov, path filters) - Enhance release.yml (retry logic, skip_ci option, release outputs) -
  Enhance docs.yml (add dev branch to triggers) - Fix test_cli_commands.py to use dynamic
  __version__ instead of hardcoded

### Documentation

- Update features documentation for v0.5.0 + fix mkdocs nav
  ([`0804ba1`](https://github.com/UnicoLab/holysheet/commit/0804ba170c55da10042da44689e5b7462fcbb723))

- Added documentation for: PDF Export, Anomaly Detection, AI Insight, Google Sheets, SQL Block,
  Narration, Cloud Publish - Fixed broken nav reference: templates/ → report-templates/ - mkdocs
  build --strict now passes clean

### Features

- Complete all 49 features — AI Insight, Google Sheets, anomaly fix, tests
  ([`db3fc80`](https://github.com/UnicoLab/holysheet/commit/db3fc800686c3cf27961443f44f4716e114f00af))

NEW BLOCKS: - AIInsight: LLM-powered data narrative generation (OpenAI/Anthropic/Google) with
  graceful fallback when provider SDK is not installed - GoogleSheet: data source block that fetches
  from Google Sheets via gspread with graceful fallback when credentials are not configured

IMPROVEMENTS: - Anomaly detection: fixed IQR=0 edge case with MAD (Median Absolute Deviation)
  fallback — now correctly flags outliers even in nearly-uniform data distributions

TESTS (311 total, +33 new): - test_v050_features.py: comprehensive tests for AIInsight, GoogleSheet,
  anomaly detection (6 cases), SqlBlock, NarrationBlock, auto_narrate, PDF export, publish CLI

BLOCK COUNT: 57 (was 55) FEATURE STATUS: 49/49 killer features implemented

- Complete v0.4.0 — tests, docs, annotations, multi-page React
  ([`8ab24a9`](https://github.com/UnicoLab/holysheet/commit/8ab24a9ed832aa065781897a7aad502c392f18b7))

ENHANCEMENTS: - Chart annotations: LineChart/AreaChart/BarChart/ScatterChart now support
  annotations=[{x, text, color}] for vertical event markers and point labels - KPI tooltip_detail:
  KPI blocks support rich tooltip breakdowns on hover - DataTable formatting: conditional color_map,
  data_bar, icon_map per column - downloadable flag: tables and charts can individually enable CSV
  export - Multi-page React rendering: tabbed page navigation in the viewer - Custom theme types:
  ThemeName accepts arbitrary strings for custom themes

COMPREHENSIVE TEST SUITE (278 tests): - test_new_blocks.py: 54 tests for GanttChart, DAGChart,
  CorrelationMatrix, Scorecard, DataProfile, Compare - test_features.py: 66 tests for Theme, feature
  flags, multi-page, filters, expiry, compression, password, widget, Jupyter, templates -
  test_cli_commands.py: 20 tests for dev/lint/diff/validate CLI commands

DOCUMENTATION (v0.4.0): - docs/features/index.md: comprehensive feature guide -
  docs/templates/index.md: template documentation - docs/cli/index.md: CLI command reference with
  all 6 commands - docs/changelog.md: v0.4.0 changelog entry - docs/blocks/index.md: updated with 6
  new block types - mkdocs.yml: updated navigation with new sections

README: - Updated block count to 53 - Added Advanced Features section with code examples - Updated
  CLI section with 3 new commands - Updated roadmap (12 items checked off)

- Killer features v0.4.0 — 53 block types + advanced capabilities
  ([`e26b93a`](https://github.com/UnicoLab/holysheet/commit/e26b93aa2fd8f21d0e46612bfba74d230801d990))

NEW BLOCK TYPES (6 new → 53 total): - GanttChart: project timeline visualization (ECharts custom
  series) - DAGChart: directed acyclic graph (ECharts graph layout) - CorrelationMatrix: statistical
  correlation heatmap - Scorecard: conditional color metric grid - DataProfile: auto-EDA summary
  cards - Compare: side-by-side comparison layout

REPORT-LEVEL FEATURES: - Custom Theme API: Theme(name, primary, background, font, chart_palette) -
  Multi-page reports: report.add_page('Overview', children=[...]) - Global filter bar:
  report.add_filter('region', options=[...]) - Feature flags: theme_switch, presentation_mode,
  download_buttons - Jupyter integration: _repr_html_() + report.show() - Password-protected
  reports: Report(password='secret') - Expiring reports: Report(expires='2025-12-31') - Gzip
  compression: Report(compress=True) - Widget export: report.export_widget('widget.html',
  block_ids=[...])

REACT APP FEATURES: - Dark/Light theme toggle in header - Presentation mode (sections as slides,
  keyboard nav) - CSV download buttons on tables and charts - Conditional table formatting
  (color_map, data_bar, icon_map) - Skeleton loading states for heavy components - KPI tooltip rich
  cards with breakdown

CLI COMMANDS (3 new): - holysheet dev: hot reload dev server with file watching - holysheet lint:
  report linting with 7 rules - holysheet diff: compare two report JSON specs

TEMPLATES: - SalesDashboard: pre-built sales dashboard - ExecutiveSummary: pre-built executive
  report - OpsMonitor: pre-built operations dashboard

- Production polish — docs, frontend, examples, optional deps
  ([`56a5ae3`](https://github.com/UnicoLab/holysheet/commit/56a5ae3a69cdb71074b11491d8b7addb02ae4324))

DOCUMENTATION: - README: updated to 57 blocks, added v0.5.0 features (AI, PDF, SQL, narration,
  anomaly detection, cloud publish), updated install extras, updated roadmap - Blocks docs: added
  SqlBlock, NarrationBlock, AIInsight, GoogleSheet reference - CLI docs: added 'publish' command
  with S3/GCS examples - CHANGELOG: added comprehensive v0.5.0 release notes (13 features)

FRONTEND: - AIInsightBlock.tsx: provider-aware card with gradient bg and accent colors -
  GoogleSheetBlock.tsx: table with sticky header, error state, Google branding - registry.tsx:
  registered ai_insight and google_sheet block types - Rebuilt frontend bundle (1,785 kB)

PROJECT CONFIG: - pyproject.toml: added [pdf], [ai], [cloud], [gsheets] optional dep groups - Added
  jupyter, pdf, ai, cloud keywords

EXAMPLES: - v050_showcase.py: demonstrates anomaly detection, SQL, narration, filters

- V0.5.0 — remaining killer features + CI fixes
  ([`bcfcebe`](https://github.com/UnicoLab/holysheet/commit/bcfcebe4232a14510ccd8e480da3467af9f27dcc))

NEW FEATURES: - PDF Export: report.export_pdf() via Playwright or headless Chrome - Anomaly
  Detection: anomaly_detection=True on LineChart/AreaChart/BarChart uses IQR method to auto-annotate
  outliers - SQL Block: inline SQL queries against report data (client-side engine) - Narration
  Block: text-to-speech readback with Web Speech API - Auto Narrate: report.auto_narrate() generates
  plain text from KPIs - Cloud Publish CLI: holysheet publish to S3/GCS - Cross-Block Reactivity:
  FilterBar + FilterContext for client-side dropdown/text/date_range/checkbox filtering across all
  charts & tables - Virtual Scrolling: tables >200 rows use virtualized rendering - Report
  Navigator: floating minimap with block anchors + scroll tracking - PWA Mode: installable dashboard
  with service worker - Responsive Columns: breakpoint-aware layouts (desktop/tablet/mobile)

CI/CD FIXES: - Release workflow: manual-only (removed push trigger) - Fixed 10 mypy errors: dict
  type args, list invariance, unused ignores, json.loads Any returns, features dict typing - All
  quality gates green: mypy, ruff, pytest 278, TS, Vite build

BLOCK COUNT: 55 (was 53) CLI COMMANDS: 8 (validate, serve, version, dev, lint, diff, publish)


## v0.2.1 (2026-05-21)

### Bug Fixes

- Correct pyproject.toml version to 0.3.0 (was reverted during rebase)
  ([`7805f69`](https://github.com/UnicoLab/holysheet/commit/7805f690b52a1300dbb712aa43b8c4a25d1e902c))

### Documentation

- Update all documentation for v0.3.0 (47 block types)
  ([`79b51fd`](https://github.com/UnicoLab/holysheet/commit/79b51fde1c28a6f52efa323eaa290e2d2025dd54))

- Updated charts.md with 6 new chart types (HeatmapChart, CandlestickChart, SankeyChart,
  WaterfallChart, BoxPlotChart, MapChart) - Updated data-content.md with 11 new content blocks
  (Timeline, Callout, Embed, JsonViewer, UserCard, StatusList, InfoList, Stepper, TagList,
  Sparkline, Video) - Updated interactive.md with 4 new interactive blocks (Dropdown, TextInput,
  CheckboxGroup, RadioGroup) - Updated blocks/index.md with all 47 block types - Updated
  api-reference.md with 21 new constructor signatures - Updated changelog.md with v0.3.0 release
  notes - Updated index.md landing page (47 blocks, 15 charts) - Updated getting-started.md block
  count reference - Updated README.md with complete block reference


## v0.2.0 (2026-05-21)

### Features

- Add 21 new block types (47 total) + comprehensive docs
  ([`484e2c7`](https://github.com/UnicoLab/holysheet/commit/484e2c7159f893645b9783d34850e36b567979bc))

New chart blocks: - HeatmapChart: 2D heatmap with color gradient visualization - CandlestickChart:
  Financial OHLC candlestick charts - SankeyChart: Flow/energy diagrams - WaterfallChart: Revenue
  bridge / waterfall analysis - BoxPlotChart: Statistical distribution visualization - MapChart:
  Geographical scatter plots

New content blocks: - Timeline: Vertical event/milestone timeline - Callout: Styled quotes and
  highlights (3 variants) - Embed: iframe embedding with aspect ratio support - JsonViewer:
  Interactive JSON tree with collapsible levels - UserCard: Team member cards with avatar and stats
  - StatusList: Service health indicators with colored dots - InfoList: Key-value pair display -
  Stepper: Process/wizard step visualization

New interactive blocks: - Dropdown: Select from options with local state - TextInput: Text/textarea
  input with local state - CheckboxGroup: Multi-select checkboxes - RadioGroup: Single-select radio
  buttons

New display blocks: - TagList: Colored tag/badge chips - Sparkline: Compact inline mini-charts -
  Video: HTML5 video embed with controls

Also includes: - Version bump to 0.3.0 - 138 tests (21 new for new blocks) - Full MkDocs Material
  documentation (14 pages, 3560 lines) - Updated full_showcase.py with all new blocks - Updated
  frontend registry and size categories - Rebuilt frontend bundle with all components


## v0.1.0 (2026-05-21)

### Features

- Initial release — HolySheet v0.2.0
  ([`9e0972e`](https://github.com/UnicoLab/holysheet/commit/9e0972e5e5accdb228160e1c2d7443a21cee49f1))

Production-ready Python package that generates beautiful interactive HTML dashboards from Python
  data/config, without requiring Node.js or React.

## Core Features - 26 block types: KPI, Metric, 9 chart types, DataTable, Markdown, CodeBlock,
  Image, Alert, ProgressBar, Divider, Section, Columns, Tabs, Slider, NumberInput, Toggle,
  Accordion, StatComparison - 3 themes: dark, light, executive - Self-contained HTML export (single
  file, no dependencies) - Multi-column layouts with CSS Grid (equal, bento, custom widths) -
  Collapsible sections and tabs - Print/PDF export button - Responsive auto-adaptive layout system -
  Auto-grouping of consecutive same-type blocks

## Architecture - Python backend: Pydantic v2 models → JSON schema - React frontend: Pre-built,
  bundled in package (no Node.js at runtime) - Jinja2 templating for standalone HTML generation

## Package - 116 tests passing - CI/CD with GitHub Actions (lint, test, semantic-release) -
  PyPI-ready with bundled frontend assets
