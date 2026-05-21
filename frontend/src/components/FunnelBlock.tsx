import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Funnel Block ─────────────────────────────────────────────────────────────

export const FunnelBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, data, name, value, height = 360 } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const accentColors = [
    '#6366f1', '#8b5cf6', '#a78bfa', '#c084fc',
    '#38bdf8', '#22d3ee', '#2dd4bf', '#34d399',
    '#fbbf24', '#f97316', '#fb7185', '#f43f5e',
  ];

  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';

    const funnelData = data.map((item: Record<string, any>, i: number) => ({
      name: String(item[name] ?? `Item ${i}`),
      value: Number(item[value] ?? 0),
      itemStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 1, y2: 0,
          colorStops: [
            { offset: 0, color: accentColors[i % accentColors.length] },
            { offset: 1, color: accentColors[(i + 1) % accentColors.length] },
          ],
        },
        borderColor: isDark ? '#12121a' : '#ffffff',
        borderWidth: 2,
      },
    }));

    return {
      tooltip: {
        trigger: 'item',
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: '{b}: {c}',
      },
      legend: {
        bottom: 0,
        textStyle: { color: textColor, fontSize: 12 },
        icon: 'circle',
        itemWidth: 8,
        itemHeight: 8,
      },
      series: [{
        type: 'funnel',
        left: '10%',
        top: 16,
        bottom: 40,
        width: '80%',
        sort: 'descending',
        gap: 4,
        label: {
          show: true,
          position: 'inside',
          color: '#fff',
          fontSize: 13,
          fontWeight: 600,
          formatter: '{b}\n{c}',
        },
        emphasis: {
          label: {
            fontSize: 15,
          },
          itemStyle: {
            shadowBlur: 20,
            shadowColor: 'rgba(99,102,241,0.4)',
          },
        },
        data: funnelData,
      }],
    };
  }, [data, name, value, isDark]);

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
