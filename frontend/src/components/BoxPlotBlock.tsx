import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── BoxPlot Block ────────────────────────────────────────────────────────────

export const BoxPlotBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const {
    title,
    data,
    categories,
    height = 360,
  } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const splitLineColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';

    // data should be array of [min, Q1, median, Q3, max]
    const boxData = data.map((d: any) => {
      if (Array.isArray(d)) return d.map(Number);
      // If objects, try to extract fields
      return [
        Number(d.min ?? 0),
        Number(d.q1 ?? d.Q1 ?? 0),
        Number(d.median ?? 0),
        Number(d.q3 ?? d.Q3 ?? 0),
        Number(d.max ?? 0),
      ];
    });

    const xAxisData = categories && categories.length > 0
      ? categories.map(String)
      : boxData.map((_: any, i: number) => `Group ${i + 1}`);

    return {
      tooltip: {
        trigger: 'item',
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: (params: any) => {
          const d = params.data;
          if (!d || !Array.isArray(d)) return '';
          return [
            `<strong>${params.name || xAxisData[params.dataIndex] || ''}</strong>`,
            `Max: ${d[5] ?? d[4]}`,
            `Q3: ${d[4] ?? d[3]}`,
            `Median: ${d[3] ?? d[2]}`,
            `Q1: ${d[2] ?? d[1]}`,
            `Min: ${d[1] ?? d[0]}`,
          ].join('<br/>');
        },
      },
      grid: {
        top: 24,
        right: 16,
        bottom: 40,
        left: 16,
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: xAxisData,
        boundaryGap: true,
        axisLabel: {
          color: textColor,
          fontSize: 11,
          rotate: xAxisData.length > 10 ? 30 : 0,
        },
        axisLine: { lineStyle: { color: splitLineColor } },
        axisTick: { show: false },
      },
      yAxis: {
        type: 'value',
        scale: true,
        axisLabel: { color: textColor, fontSize: 11 },
        axisLine: { show: false },
        splitLine: { lineStyle: { color: splitLineColor } },
      },
      series: [{
        type: 'boxplot',
        data: boxData,
        itemStyle: {
          color: isDark ? 'rgba(99,102,241,0.15)' : 'rgba(99,102,241,0.1)',
          borderColor: '#6366f1',
          borderWidth: 2,
        },
        emphasis: {
          itemStyle: {
            borderColor: '#818cf8',
            borderWidth: 3,
            shadowBlur: 12,
            shadowColor: 'rgba(99,102,241,0.3)',
          },
        },
      }],
    };
  }, [data, categories, isDark]);

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
