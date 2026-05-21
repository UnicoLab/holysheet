import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Correlation Matrix Block ─────────────────────────────────────────────────

export const CorrelationMatrixBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const {
    title,
    matrix = [],
    labels = [],
    height = 400,
  } = block.props as {
    title?: string;
    matrix: number[][];
    labels: string[];
    height?: number;
  };
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!matrix || matrix.length === 0 || !labels || labels.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const splitLineColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';

    // Build heatmap data as [xIdx, yIdx, value]
    const heatmapData: [number, number, number][] = [];
    for (let row = 0; row < matrix.length; row++) {
      for (let col = 0; col < (matrix[row]?.length ?? 0); col++) {
        const val = matrix[row][col];
        heatmapData.push([col, row, typeof val === 'number' ? Math.round(val * 100) / 100 : 0]);
      }
    }

    const totalCells = labels.length * labels.length;

    return {
      tooltip: {
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: (params: any) => {
          const d = params.data;
          const xLabel = labels[d[0]] ?? d[0];
          const yLabel = labels[d[1]] ?? d[1];
          return `${xLabel} × ${yLabel}<br/><strong>r = ${d[2].toFixed(2)}</strong>`;
        },
      },
      grid: {
        top: 16,
        right: 60,
        bottom: 60,
        left: 16,
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: labels,
        splitArea: { show: true },
        axisLabel: {
          color: textColor,
          fontSize: 11,
          rotate: labels.length > 8 ? 45 : 0,
          interval: 0,
        },
        axisLine: { lineStyle: { color: splitLineColor } },
        axisTick: { show: false },
        position: 'bottom',
      },
      yAxis: {
        type: 'category',
        data: labels,
        splitArea: { show: true },
        axisLabel: {
          color: textColor,
          fontSize: 11,
          interval: 0,
        },
        axisLine: { lineStyle: { color: splitLineColor } },
        axisTick: { show: false },
      },
      visualMap: {
        min: -1,
        max: 1,
        calculable: true,
        orient: 'vertical',
        right: 0,
        top: 'center',
        inRange: {
          color: isDark
            ? ['#ef4444', '#fca5a5', '#374151', '#93c5fd', '#3b82f6']
            : ['#dc2626', '#fca5a5', '#ffffff', '#93c5fd', '#2563eb'],
        },
        textStyle: { color: textColor, fontSize: 11 },
        borderColor: 'transparent',
      },
      series: [
        {
          type: 'heatmap',
          data: heatmapData,
          label: {
            show: totalCells <= 225, // Show labels when matrix is 15×15 or smaller
            formatter: (params: any) => params.data[2].toFixed(2),
            color: isDark ? '#fff' : '#1a1a2e',
            fontSize: totalCells <= 64 ? 11 : 9,
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
        },
      ],
    };
  }, [matrix, labels, isDark]);

  const hasData = matrix && matrix.length > 0 && labels && labels.length > 0;

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
            <Typography variant="body2">No correlation data available</Typography>
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
