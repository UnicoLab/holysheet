import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── DAG Block ────────────────────────────────────────────────────────────────

interface DAGNode {
  id: string;
  label?: string;
  color?: string;
  icon?: string;
}

interface DAGEdge {
  from: string;
  to: string;
  label?: string;
}

const accentColors = [
  '#6366f1', '#8b5cf6', '#38bdf8', '#2dd4bf',
  '#34d399', '#fbbf24', '#f97316', '#fb7185',
  '#a78bfa', '#c084fc', '#22d3ee', '#f43f5e',
];

export const DAGBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const {
    title,
    nodes = [],
    edges = [],
    height = 400,
    layout = 'force',
  } = block.props as {
    title?: string;
    nodes: DAGNode[];
    edges: DAGEdge[];
    height?: number;
    layout?: 'force' | 'circular';
  };
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!nodes || nodes.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';

    const graphNodes = nodes.map((node, i) => ({
      id: String(node.id),
      name: node.label || node.id,
      symbolSize: 40,
      itemStyle: {
        color: node.color || accentColors[i % accentColors.length],
        borderColor: isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.1)',
        borderWidth: 2,
        shadowBlur: 8,
        shadowColor: 'rgba(99,102,241,0.2)',
      },
      label: {
        show: true,
        formatter: node.icon ? `${node.icon}\n{name|${node.label || node.id}}` : node.label || node.id,
        color: textColor,
        fontSize: 11,
        fontWeight: 500,
        rich: {
          name: {
            fontSize: 10,
            color: textColor,
            padding: [4, 0, 0, 0],
          },
        },
      },
    }));

    const graphLinks = (edges || []).map((edge) => ({
      source: String(edge.from),
      target: String(edge.to),
      label: edge.label
        ? {
            show: true,
            formatter: edge.label,
            color: textColor,
            fontSize: 10,
          }
        : { show: false },
      lineStyle: {
        color: isDark ? 'rgba(255,255,255,0.25)' : 'rgba(0,0,0,0.2)',
        curveness: 0.2,
        width: 2,
      },
    }));

    const layoutConfig =
      layout === 'circular'
        ? { layout: 'circular', circular: { rotateLabel: true } }
        : {
            layout: 'force',
            force: {
              repulsion: 300,
              gravity: 0.1,
              edgeLength: [80, 200],
              layoutAnimation: true,
            },
          };

    return {
      tooltip: {
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: (params: any) => {
          if (params.dataType === 'edge') {
            let html = `${params.data.source} → ${params.data.target}`;
            if (params.data.label?.formatter) html += `<br/>${params.data.label.formatter}`;
            return html;
          }
          return `<strong>${params.data.name || params.data.id}</strong>`;
        },
      },
      series: [
        {
          type: 'graph',
          ...layoutConfig,
          roam: true,
          draggable: true,
          data: graphNodes,
          links: graphLinks,
          edgeSymbol: ['none', 'arrow'],
          edgeSymbolSize: [0, 10],
          emphasis: {
            focus: 'adjacency',
            lineStyle: {
              width: 4,
              opacity: 0.8,
            },
            itemStyle: {
              shadowBlur: 16,
              shadowColor: 'rgba(99,102,241,0.4)',
            },
          },
          animationDuration: 800,
          animationEasingUpdate: 'quinticInOut',
        },
      ],
    };
  }, [nodes, edges, layout, isDark]);

  const hasData = nodes && nodes.length > 0;

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        height: '100%',
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: isDark ? '0 8px 32px rgba(99,102,241,0.12)' : '0 8px 32px rgba(0,0,0,0.06)',
          borderColor: isDark ? 'rgba(99,102,241,0.2)' : 'rgba(99,102,241,0.15)',
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        {title && (
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, fontSize: '1rem' }}>
            {title}
          </Typography>
        )}
        {!hasData ? (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height,
              color: 'text.secondary',
            }}
          >
            <Typography variant="body2">No graph data available</Typography>
          </Box>
        ) : (
          <ReactECharts
            option={option}
            style={{ height, width: '100%' }}
            opts={{ renderer: 'svg' }}
            notMerge
          />
        )}
      </CardContent>
    </Card>
  );
};
