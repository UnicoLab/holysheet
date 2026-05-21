import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Heatmap Block ────────────────────────────────────────────────────────────

export const HeatmapBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const {
    title,
    data,
    x = 'x',
    y = 'y',
    value = 'value',
    height = 360,
  } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const splitLineColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';

    // Extract unique x and y categories
    const xCategories = Array.from(new Set(data.map((d: Record<string, any>) => String(d[x] ?? ''))));
    const yCategories = Array.from(new Set(data.map((d: Record<string, any>) => String(d[y] ?? ''))));

    // Build heatmap data as [xIndex, yIndex, value]
    const heatmapData = data.map((d: Record<string, any>) => {
      const xIdx = xCategories.indexOf(String(d[x] ?? ''));
      const yIdx = yCategories.indexOf(String(d[y] ?? ''));
      return [xIdx, yIdx, Number(d[value] ?? 0)];
    });

    const values = heatmapData.map((d: number[]) => d[2]);
    const minVal = Math.min(...values);
    const maxVal = Math.max(...values);

    return {
      tooltip: {
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: (params: any) => {
          const d = params.data;
          return `${xCategories[d[0]]} × ${yCategories[d[1]]}<br/><strong>${d[2]}</strong>`;
        },
      },
      grid: {
        top: 16,
        right: 60,
        bottom: 40,
        left: 60,
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: xCategories,
        splitArea: { show: true },
        axisLabel: {
          color: textColor,
          fontSize: 11,
          rotate: xCategories.length > 10 ? 45 : 0,
        },
        axisLine: { lineStyle: { color: splitLineColor } },
        axisTick: { show: false },
      },
      yAxis: {
        type: 'category',
        data: yCategories,
        splitArea: { show: true },
        axisLabel: { color: textColor, fontSize: 11 },
        axisLine: { lineStyle: { color: splitLineColor } },
        axisTick: { show: false },
      },
      visualMap: {
        min: minVal,
        max: maxVal,
        calculable: true,
        orient: 'vertical',
        right: 0,
        top: 'center',
        inRange: {
          color: isDark
            ? ['#1e1b4b', '#3730a3', '#6366f1', '#a78bfa', '#c4b5fd']
            : ['#eef2ff', '#c7d2fe', '#818cf8', '#6366f1', '#4338ca'],
        },
        textStyle: { color: textColor, fontSize: 11 },
        borderColor: 'transparent',
      },
      series: [{
        type: 'heatmap',
        data: heatmapData,
        label: {
          show: heatmapData.length <= 100,
          color: isDark ? '#fff' : '#1a1a2e',
          fontSize: 10,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 12,
            shadowColor: 'rgba(99,102,241,0.4)',
          },
        },
        itemStyle: {
          borderColor: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)',
          borderWidth: 1,
          borderRadius: 2,
        },
      }],
    };
  }, [data, x, y, value, isDark]);

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
