import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Sankey Block ─────────────────────────────────────────────────────────────

export const SankeyBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, nodes, links, height = 400 } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const accentColors = [
    '#6366f1', '#8b5cf6', '#a78bfa', '#c084fc',
    '#38bdf8', '#22d3ee', '#2dd4bf', '#34d399',
    '#fbbf24', '#f97316', '#fb7185', '#f43f5e',
  ];

  const option = useMemo(() => {
    if (!nodes || nodes.length === 0 || !links || links.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';

    const sankeyNodes = nodes.map((node: any, i: number) => ({
      name: String(node.name ?? node ?? `Node ${i}`),
      itemStyle: {
        color: accentColors[i % accentColors.length],
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        borderWidth: 1,
      },
    }));

    const sankeyLinks = links.map((link: any) => ({
      source: String(link.source ?? ''),
      target: String(link.target ?? ''),
      value: Number(link.value ?? 0),
    }));

    return {
      tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove',
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
      },
      series: [{
        type: 'sankey',
        data: sankeyNodes,
        links: sankeyLinks,
        orient: 'horizontal',
        layoutIterations: 32,
        nodeGap: 12,
        nodeWidth: 20,
        left: 16,
        right: 16,
        top: 16,
        bottom: 16,
        label: {
          color: textColor,
          fontSize: 12,
          fontWeight: 500,
        },
        lineStyle: {
          color: 'gradient',
          curveness: 0.5,
          opacity: isDark ? 0.35 : 0.25,
        },
        emphasis: {
          focus: 'adjacency',
          lineStyle: {
            opacity: 0.6,
          },
          itemStyle: {
            shadowBlur: 12,
            shadowColor: 'rgba(99,102,241,0.3)',
          },
        },
      }],
    };
  }, [nodes, links, isDark]);

  const hasData = nodes && nodes.length > 0 && links && links.length > 0;

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
            <Typography variant="body2">No data available</Typography>
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
