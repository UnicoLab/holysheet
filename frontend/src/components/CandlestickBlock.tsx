import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Candlestick Block ────────────────────────────────────────────────────────

export const CandlestickBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const {
    title,
    data,
    x = 'x',
    open = 'open',
    close = 'close',
    low = 'low',
    high = 'high',
    height = 400,
  } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const splitLineColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';

    const xData = data.map((d: Record<string, any>) => String(d[x] ?? ''));
    // ECharts candlestick expects [open, close, low, high]
    const candleData = data.map((d: Record<string, any>) => [
      Number(d[open] ?? 0),
      Number(d[close] ?? 0),
      Number(d[low] ?? 0),
      Number(d[high] ?? 0),
    ]);

    const upColor = '#22c55e';
    const downColor = '#ef4444';
    const upBorderColor = '#16a34a';
    const downBorderColor = '#dc2626';

    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'cross' },
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: (params: any) => {
          const p = params[0];
          if (!p) return '';
          const d = p.data;
          return [
            `<strong>${p.name}</strong>`,
            `Open: ${d[1]}`,
            `Close: ${d[2]}`,
            `Low: ${d[3]}`,
            `High: ${d[4]}`,
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
        data: xData,
        axisLabel: {
          color: textColor,
          fontSize: 11,
          rotate: xData.length > 20 ? 45 : 0,
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
        type: 'candlestick',
        data: candleData,
        itemStyle: {
          color: upColor,
          color0: downColor,
          borderColor: upBorderColor,
          borderColor0: downBorderColor,
          borderWidth: 1,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(99,102,241,0.3)',
          },
        },
      }],
      dataZoom: [
        {
          type: 'inside',
          xAxisIndex: 0,
          start: 0,
          end: 100,
        },
      ],
    };
  }, [data, x, open, close, low, high, isDark]);

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
