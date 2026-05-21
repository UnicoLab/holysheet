import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Radar Chart Block ────────────────────────────────────────────────────────

export const RadarChartBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, data, indicators, height = 360 } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const accentColors = [
    '#6366f1', '#8b5cf6', '#a78bfa', '#c084fc',
    '#38bdf8', '#22d3ee', '#2dd4bf', '#34d399',
    '#fbbf24', '#f97316', '#fb7185', '#f43f5e',
  ];

  const option = useMemo(() => {
    if (!data || data.length === 0 || !indicators || indicators.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const splitLineColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';

    // Compute max values for each indicator
    const indicatorConfig = indicators.map((ind: string) => {
      const maxVal = Math.max(...data.map((d: Record<string, any>) => Number(d[ind] || 0)));
      return { name: ind, max: Math.ceil(maxVal * 1.2) || 100 };
    });

    const seriesData = data.map((record: Record<string, any>, i: number) => ({
      value: indicators.map((ind: string) => Number(record[ind] || 0)),
      name: record.name || record.label || `Series ${i + 1}`,
      areaStyle: {
        color: accentColors[i % accentColors.length] + '20',
      },
      lineStyle: {
        color: accentColors[i % accentColors.length],
        width: 2,
      },
      itemStyle: {
        color: accentColors[i % accentColors.length],
      },
      symbol: 'circle',
      symbolSize: 6,
    }));

    return {
      tooltip: {
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
      },
      legend: {
        bottom: 0,
        textStyle: { color: textColor, fontSize: 12 },
        icon: 'circle',
        itemWidth: 8,
        itemHeight: 8,
      },
      radar: {
        indicator: indicatorConfig,
        shape: 'polygon',
        splitNumber: 5,
        axisName: {
          color: textColor,
          fontSize: 12,
        },
        splitLine: {
          lineStyle: { color: splitLineColor },
        },
        splitArea: {
          show: true,
          areaStyle: {
            color: isDark
              ? ['rgba(99,102,241,0.04)', 'rgba(99,102,241,0.02)']
              : ['rgba(99,102,241,0.03)', 'rgba(99,102,241,0.01)'],
          },
        },
        axisLine: {
          lineStyle: { color: splitLineColor },
        },
      },
      series: [{
        type: 'radar',
        data: seriesData,
        emphasis: {
          lineStyle: { width: 3 },
        },
      }],
    };
  }, [data, indicators, isDark]);

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
