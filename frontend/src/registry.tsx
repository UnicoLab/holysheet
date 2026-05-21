import React from 'react';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import { motion } from 'framer-motion';
import { KPIBlock } from './components/KPIBlock';
import { ChartBlock } from './components/ChartBlock';
import { TableBlock } from './components/TableBlock';
import { MarkdownBlock } from './components/MarkdownBlock';
import { SectionBlock } from './components/SectionBlock';
import { ErrorBoundary } from './components/ErrorBoundary';
import { RadarChartBlock } from './components/RadarChartBlock';
import { GaugeBlock } from './components/GaugeBlock';
import { FunnelBlock } from './components/FunnelBlock';
import { TreemapBlock } from './components/TreemapBlock';
import { MetricBlock } from './components/MetricBlock';
import { DividerBlock } from './components/DividerBlock';
import { AlertBlock } from './components/AlertBlock';
import { ProgressBlock } from './components/ProgressBlock';
import { ColumnsBlock } from './components/ColumnsBlock';
import { TabsBlock } from './components/TabsBlock';
import { CodeBlockComponent } from './components/CodeBlockComponent';
import { ImageBlock } from './components/ImageBlock';
import { HeatmapBlock } from './components/HeatmapBlock';
import { CandlestickBlock } from './components/CandlestickBlock';
import { SankeyBlock } from './components/SankeyBlock';
import { WaterfallBlock } from './components/WaterfallBlock';
import { BoxPlotBlock } from './components/BoxPlotBlock';
import { MapChartBlock } from './components/MapChartBlock';
import { TimelineBlock } from './components/TimelineBlock';
import { CalloutBlock } from './components/CalloutBlock';
import { EmbedBlock } from './components/EmbedBlock';
import { JsonViewerBlock } from './components/JsonViewerBlock';
import { UserCardBlock } from './components/UserCardBlock';
import { StatusListBlock } from './components/StatusListBlock';
import { InfoListBlock } from './components/InfoListBlock';
import { StepperBlock } from './components/StepperBlock';
import { DropdownBlock } from './components/DropdownBlock';
import { TextInputBlock } from './components/TextInputBlock';
import { CheckboxGroupBlock } from './components/CheckboxGroupBlock';
import { RadioGroupBlock } from './components/RadioGroupBlock';
import { TagListBlock } from './components/TagListBlock';
import { SparklineBlock } from './components/SparklineBlock';
import { VideoBlock } from './components/VideoBlock';
import { GanttChartBlock } from './components/GanttChartBlock';
import { DAGBlock } from './components/DAGBlock';
import { CorrelationMatrixBlock } from './components/CorrelationMatrixBlock';
import { ScorecardBlock } from './components/ScorecardBlock';
import { DataProfileBlock } from './components/DataProfileBlock';
import { CompareBlock } from './components/CompareBlock';
import { SqlBlock } from './components/SqlBlock';
import { NarrationBlock } from './components/NarrationBlock';
import { AIInsightBlock } from './components/AIInsightBlock';
import { GoogleSheetBlock } from './components/GoogleSheetBlock';
import type { BlockSpec } from './types';

// ─── Block Registry ───────────────────────────────────────────────────────────

export const blockRegistry: Record<string, React.ComponentType<any>> = {
  kpi: KPIBlock,
  line_chart: ChartBlock,
  bar_chart: ChartBlock,
  pie_chart: ChartBlock,
  area_chart: ChartBlock,
  scatter_chart: ChartBlock,
  data_table: TableBlock,
  markdown: MarkdownBlock,
  section: SectionBlock,
  radar_chart: RadarChartBlock,
  gauge: GaugeBlock,
  funnel_chart: FunnelBlock,
  treemap_chart: TreemapBlock,
  metric: MetricBlock,
  divider: DividerBlock,
  alert: AlertBlock,
  progress: ProgressBlock,
  columns: ColumnsBlock,
  tabs: TabsBlock,
  code_block: CodeBlockComponent,
  image: ImageBlock,
  // New chart blocks
  heatmap_chart: HeatmapBlock,
  candlestick_chart: CandlestickBlock,
  sankey_chart: SankeyBlock,
  waterfall_chart: WaterfallBlock,
  box_plot_chart: BoxPlotBlock,
  map_chart: MapChartBlock,
  // New content blocks
  timeline: TimelineBlock,
  callout: CalloutBlock,
  embed: EmbedBlock,
  json_viewer: JsonViewerBlock,
  user_card: UserCardBlock,
  status_list: StatusListBlock,
  info_list: InfoListBlock,
  stepper: StepperBlock,
  // New interactive blocks
  dropdown: DropdownBlock,
  text_input: TextInputBlock,
  checkbox_group: CheckboxGroupBlock,
  radio_group: RadioGroupBlock,
  // New display blocks
  tag_list: TagListBlock,
  sparkline: SparklineBlock,
  video: VideoBlock,
  // Advanced chart & analysis blocks
  gantt_chart: GanttChartBlock,
  dag_chart: DAGBlock,
  correlation_matrix: CorrelationMatrixBlock,
  scorecard: ScorecardBlock,
  data_profile: DataProfileBlock,
  compare: CompareBlock,
  sql_block: SqlBlock,
  narration: NarrationBlock,
  // Integration blocks
  ai_insight: AIInsightBlock,
  google_sheet: GoogleSheetBlock,
};

// ─── Size Categories ──────────────────────────────────────────────────────────

type SizeCategory = 'compact' | 'medium' | 'wide' | 'full';

function getSizeCategory(type: string): SizeCategory {
  switch (type) {
    case 'kpi':
    case 'metric':
    case 'sparkline':
      return 'compact';
    case 'gauge':
    case 'progress':
    case 'user_card':
    case 'tag_list':
      return 'medium';
    case 'pie_chart':
    case 'line_chart':
    case 'bar_chart':
    case 'area_chart':
    case 'scatter_chart':
    case 'radar_chart':
    case 'funnel_chart':
    case 'treemap_chart':
    case 'heatmap_chart':
    case 'candlestick_chart':
    case 'sankey_chart':
    case 'waterfall_chart':
    case 'box_plot_chart':
    case 'map_chart':
    case 'gantt_chart':
    case 'dag_chart':
    case 'correlation_matrix':
    case 'sql_block':
    case 'google_sheet':
      return 'wide';
    case 'ai_insight':
      return 'full';
    default:
      return 'full';
  }
}

// Grid sizing ONLY for top-level blocks (NOT inside ColumnsBlock)
function getTopLevelGridSize(
  category: SizeCategory,
  groupSize: number,
): { xs: number; sm: number; md: number; lg: number } {
  switch (category) {
    case 'compact':
      if (groupSize <= 2) return { xs: 12, sm: 6, md: 6, lg: 6 };
      if (groupSize === 3) return { xs: 12, sm: 6, md: 4, lg: 4 };
      return { xs: 12, sm: 6, md: 3, lg: 3 };

    case 'medium':
      if (groupSize <= 2) return { xs: 12, sm: 6, md: 6, lg: 6 };
      if (groupSize === 3) return { xs: 12, sm: 6, md: 4, lg: 4 };
      return { xs: 12, sm: 6, md: 3, lg: 3 };

    case 'wide':
      if (groupSize === 1) return { xs: 12, sm: 12, md: 12, lg: 12 };
      return { xs: 12, sm: 12, md: 6, lg: 6 };

    case 'full':
    default:
      return { xs: 12, sm: 12, md: 12, lg: 12 };
  }
}

// ─── Smart Block Grouping ─────────────────────────────────────────────────────

interface BlockGroup {
  category: SizeCategory;
  blocks: { block: BlockSpec; originalIndex: number }[];
}

function groupBlocks(blocks: BlockSpec[]): BlockGroup[] {
  const groups: BlockGroup[] = [];
  let currentGroup: BlockGroup | null = null;

  for (let i = 0; i < blocks.length; i++) {
    const block = blocks[i];
    const category = getSizeCategory(block.type);

    // Full-width blocks always get their own group
    if (category === 'full') {
      currentGroup = null;
      groups.push({ category, blocks: [{ block, originalIndex: i }] });
      continue;
    }

    if (currentGroup && currentGroup.category === category) {
      currentGroup.blocks.push({ block, originalIndex: i });
    } else {
      currentGroup = { category, blocks: [{ block, originalIndex: i }] };
      groups.push(currentGroup);
    }
  }

  return groups;
}

// ─── Motion variants ─────────────────────────────────────────────────────────

const itemVariants = {
  hidden: { opacity: 0, y: 16 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: {
      delay: Math.min(i * 0.04, 0.6),
      duration: 0.4,
      ease: [0.25, 0.46, 0.45, 0.94],
    },
  }),
};

// ─── Block Renderer ───────────────────────────────────────────────────────────
//
// KEY DESIGN: When a single block is passed (e.g. from ColumnsBlock), it renders
// at full width (xs:12) because the PARENT already handles column sizing.
// Grid sizing is only applied when multiple blocks are rendered together.

interface BlockRendererProps {
  blocks: BlockSpec[];
}

export const BlockRenderer: React.FC<BlockRendererProps> = ({ blocks }) => {
  if (!blocks || blocks.length === 0) {
    return null;
  }

  // ── Single block: render at full width, no extra grid nesting ──
  if (blocks.length === 1) {
    const block = blocks[0];
    const Component = blockRegistry[block.type];
    if (!Component) {
      console.warn(`[HolySheet] Unknown block type: "${block.type}"`);
      return null;
    }
    return (
      <motion.div
        id={block.id ? `block-${block.id}` : undefined}
        custom={0}
        initial="hidden"
        animate="visible"
        variants={itemVariants}
        style={{ width: '100%' }}
      >
        <ErrorBoundary blockId={block.id}>
          <Component block={block} index={0} />
        </ErrorBoundary>
      </motion.div>
    );
  }

  // ── Multiple blocks: group and apply smart grid sizing ──
  const groups = groupBlocks(blocks);

  return (
    <Grid container spacing={2.5} sx={{ alignItems: 'stretch' }}>
      {groups.map((group) =>
        group.blocks.map(({ block, originalIndex }) => {
          const Component = blockRegistry[block.type];
          if (!Component) {
            console.warn(`[HolySheet] Unknown block type: "${block.type}"`);
            return null;
          }

          const gridSize = getTopLevelGridSize(group.category, group.blocks.length);

          return (
            <Grid
              item
              key={block.id || `block-${originalIndex}`}
              {...gridSize}
              sx={{
                display: 'flex',
                flexDirection: 'column',
                '& > *': { flex: 1, minWidth: 0 },
              }}
            >
              <motion.div
                id={block.id ? `block-${block.id}` : undefined}
                custom={originalIndex}
                initial="hidden"
                animate="visible"
                variants={itemVariants}
                style={{ width: '100%', flex: 1, display: 'flex', flexDirection: 'column' }}
              >
                <ErrorBoundary blockId={block.id}>
                  <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column', '& > *': { flex: 1 } }}>
                    <Component block={block} index={originalIndex} />
                  </Box>
                </ErrorBoundary>
              </motion.div>
            </Grid>
          );
        })
      )}
    </Grid>
  );
};
