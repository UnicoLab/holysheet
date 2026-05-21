import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Treemap Block ────────────────────────────────────────────────────────────

export const TreemapBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, data, name, value, category, height = 360 } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const accentColors = [
    '#6366f1', '#8b5cf6', '#a78bfa', '#c084fc',
    '#38bdf8', '#22d3ee', '#2dd4bf', '#34d399',
    '#fbbf24', '#f97316', '#fb7185', '#f43f5e',
  ];

  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    let treemapData: any[];

    if (category) {
      // Group by category
      const groups = new Map<string, any[]>();
      data.forEach((item: Record<string, any>) => {
        const cat = String(item[category] ?? 'Other');
        if (!groups.has(cat)) groups.set(cat, []);
        groups.get(cat)!.push({
          name: String(item[name] ?? ''),
          value: Number(item[value] ?? 0),
        });
      });
      treemapData = Array.from(groups.entries()).map(([catName, children], i) => ({
        name: catName,
        itemStyle: { color: accentColors[i % accentColors.length] },
        children,
      }));
    } else {
      treemapData = data.map((item: Record<string, any>, i: number) => ({
        name: String(item[name] ?? `Item ${i}`),
        value: Number(item[value] ?? 0),
        itemStyle: { color: accentColors[i % accentColors.length] },
      }));
    }

    return {
      tooltip: {
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: (params: any) => `${params.name}: ${params.value}`,
      },
      series: [{
        type: 'treemap',
        data: treemapData,
        roam: false,
        nodeClick: false,
        breadcrumb: { show: false },
        width: '100%',
        height: '100%',
        squareRatio: 0.5 * (1 + Math.sqrt(5)),
        label: {
          show: true,
          formatter: '{b}',
          color: '#fff',
          fontSize: 12,
          fontWeight: 600,
          textShadowBlur: 4,
          textShadowColor: 'rgba(0,0,0,0.4)',
        },
        upperLabel: {
          show: category ? true : false,
          height: 24,
          color: '#fff',
          fontSize: 12,
          fontWeight: 600,
          textShadowBlur: 4,
          textShadowColor: 'rgba(0,0,0,0.4)',
        },
        itemStyle: {
          borderColor: isDark ? '#12121a' : '#ffffff',
          borderWidth: 2,
          borderRadius: 4,
          gapWidth: 2,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 20,
            shadowColor: 'rgba(99,102,241,0.3)',
          },
        },
        levels: [
          {
            itemStyle: {
              borderColor: isDark ? '#1a1a2e' : '#e2e8f0',
              borderWidth: 3,
              gapWidth: 3,
            },
          },
          {
            itemStyle: {
              borderColor: isDark ? '#12121a' : '#ffffff',
              borderWidth: 1,
              gapWidth: 1,
            },
          },
        ],
      }],
    };
  }, [data, name, value, category, isDark]);

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        height: '100%',
      }}
    >
      <CardContent sx={{ p: 3 }}>
        {title && (
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, fontSize: '1rem' }}>
            {title}
          </Typography>
        )}
        {(!data || data.length === 0) ? (
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
