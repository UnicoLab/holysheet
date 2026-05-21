// ─── HolySheet Type Definitions ───────────────────────────────────────────────

export type ThemeName = 'light' | 'dark' | 'executive';

export type KPIStatus = 'positive' | 'negative' | 'neutral';

// ─── Report Spec ──────────────────────────────────────────────────────────────

export interface ReportSpec {
  schema_version: string;
  title: string;
  subtitle?: string;
  theme: ThemeName;
  created_at: string;
  blocks: BlockSpec[];
}

// ─── Block Spec (generic envelope) ────────────────────────────────────────────

export interface BlockSpec {
  id: string;
  type: string;
  props: Record<string, any>;
}

// ─── KPI ──────────────────────────────────────────────────────────────────────

export interface KPIProps {
  label: string;
  value: string | number;
  unit?: string;
  delta?: string;
  status?: KPIStatus;
  description?: string;
}

// ─── Charts ───────────────────────────────────────────────────────────────────

export interface ChartProps {
  title: string;
  data: Record<string, any>[];
  x?: string;
  y?: string;
  name?: string;
  value?: string;
  series?: string;
  height?: number;
}

// ─── Table ────────────────────────────────────────────────────────────────────

export interface TableProps {
  title: string;
  data: Record<string, any>[];
  columns?: string[];
  searchable?: boolean;
  paginated?: boolean;
}

// ─── Markdown ─────────────────────────────────────────────────────────────────

export interface MarkdownProps {
  content: string;
}

// ─── Section ──────────────────────────────────────────────────────────────────

export interface SectionProps {
  title: string;
  description?: string;
  children: BlockSpec[];
}

// ─── Alert ────────────────────────────────────────────────────────────────────

export type AlertSeverity = 'info' | 'warning' | 'error' | 'success';

// ─── Scatter Chart ────────────────────────────────────────────────────────────

export interface ScatterChartProps {
  title: string;
  data: Record<string, any>[];
  x: string;
  y: string;
  size?: string;
  category?: string;
  height?: number;
}

// ─── Radar Chart ──────────────────────────────────────────────────────────────

export interface RadarChartProps {
  title: string;
  data: Record<string, any>[];
  indicators: string[];
  height?: number;
}

// ─── Gauge ────────────────────────────────────────────────────────────────────

export interface GaugeProps {
  title: string;
  value: number;
  min?: number;
  max?: number;
  unit?: string;
  thresholds?: { value: number; color: string }[];
  height?: number;
}

// ─── Funnel ───────────────────────────────────────────────────────────────────

export interface FunnelProps {
  title: string;
  data: Record<string, any>[];
  name: string;
  value: string;
  height?: number;
}

// ─── Treemap ──────────────────────────────────────────────────────────────────

export interface TreemapProps {
  title: string;
  data: Record<string, any>[];
  name: string;
  value: string;
  category?: string;
  height?: number;
}

// ─── Metric ───────────────────────────────────────────────────────────────────

export interface MetricProps {
  label: string;
  value: string | number;
  unit?: string;
  icon?: string;
}

// ─── Divider ──────────────────────────────────────────────────────────────────

export interface DividerProps {
  label?: string;
  variant?: 'solid' | 'dashed' | 'dotted';
}

// ─── Alert Props ──────────────────────────────────────────────────────────────

export interface AlertProps {
  severity: AlertSeverity;
  title?: string;
  message: string;
}

// ─── Progress ─────────────────────────────────────────────────────────────────

export interface ProgressProps {
  label: string;
  value: number;
  max?: number;
  color?: string;
  description?: string;
}

// ─── Columns ──────────────────────────────────────────────────────────────────

export interface ColumnsProps {
  children: BlockSpec[];
  widths?: number[];
}

// ─── Tabs ─────────────────────────────────────────────────────────────────────

export interface TabsProps {
  tabs: { label: string; children: BlockSpec[] }[];
}

// ─── Code Block ───────────────────────────────────────────────────────────────

export interface CodeBlockProps {
  code: string;
  language?: string;
  title?: string;
}

// ─── Image ────────────────────────────────────────────────────────────────────

export interface ImageProps {
  src: string;
  alt?: string;
  caption?: string;
  width?: string | number;
  height?: string | number;
}

// ─── Block component wrapper props ────────────────────────────────────────────

export interface BlockComponentProps {
  block: BlockSpec;
  index?: number;
}
