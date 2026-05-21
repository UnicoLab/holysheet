import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Sparkline Block ──────────────────────────────────────────────────────────

export const SparklineBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { data = [], color = '#6366f1', height = 60, show_area = false } = block.props as {
    data: number[];
    color?: string;
    height?: number;
    show_area?: boolean;
  };
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    return {
      grid: { top: 4, right: 4, bottom: 4, left: 4 },
      xAxis: {
        type: 'category' as const,
        show: false,
        boundaryGap: false,
        data: data.map((_: number, i: number) => i),
      },
      yAxis: {
        type: 'value' as const,
        show: false,
      },
      tooltip: {
        trigger: 'axis' as const,
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 12 },
        borderRadius: 8,
        padding: [6, 10],
        formatter: (params: any) => {
          const val = Array.isArray(params) ? params[0]?.data : params?.data;
          return `${val}`;
        },
      },
      series: [
        {
          type: 'line',
          data: data,
          smooth: true,
          symbol: 'none',
          lineStyle: { width: 2, color },
          areaStyle: show_area
            ? {
                color: {
                  type: 'linear',
                  x: 0,
                  y: 0,
                  x2: 0,
                  y2: 1,
                  colorStops: [
                    { offset: 0, color: color + '30' },
                    { offset: 1, color: color + '05' },
                  ],
                },
              }
            : undefined,
        },
      ],
    };
  }, [data, color, show_area, isDark]);

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
      <CardContent sx={{ p: 1.5, pb: '12px !important' }}>
        {(!data || data.length === 0) ? (
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height,
              color: 'text.secondary',
              fontSize: '0.8rem',
            }}
          >
            No data
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
