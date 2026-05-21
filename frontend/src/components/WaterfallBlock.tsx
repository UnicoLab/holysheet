import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Waterfall Block ──────────────────────────────────────────────────────────

export const WaterfallBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const {
    title,
    data,
    category = 'category',
    value = 'value',
    height = 360,
  } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const splitLineColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';

    const positiveColor = '#22c55e';
    const negativeColor = '#ef4444';
    const totalColor = '#6366f1';

    const categories: string[] = [];
    const baseValues: number[] = [];
    const barValues: number[] = [];
    const barColors: string[] = [];

    let cumulative = 0;

    data.forEach((item: Record<string, any>) => {
      const cat = String(item[category] ?? '');
      const val = Number(item[value] ?? 0);
      const isTotal = item.total === true || item.isTotal === true;

      categories.push(cat);

      if (isTotal) {
        // Total bar starts from zero
        baseValues.push(0);
        barValues.push(cumulative);
        barColors.push(totalColor);
      } else {
        if (val >= 0) {
          baseValues.push(cumulative);
          barValues.push(val);
          barColors.push(positiveColor);
        } else {
          baseValues.push(cumulative + val);
          barValues.push(Math.abs(val));
          barColors.push(negativeColor);
        }
        cumulative += val;
      }
    });

    return {
      tooltip: {
        trigger: 'axis',
        axisPointer: { type: 'shadow' },
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: (params: any) => {
          // params[0] is invisible base, params[1] is visible bar
          const bar = params[1];
          if (!bar) return '';
          const idx = bar.dataIndex;
          const isTotal = data[idx]?.total === true || data[idx]?.isTotal === true;
          const rawVal = isTotal ? barValues[idx] : Number(data[idx][value] ?? 0);
          const sign = rawVal >= 0 ? '+' : '';
          return `<strong>${categories[idx]}</strong><br/>${isTotal ? 'Total: ' : sign}${rawVal}`;
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
        data: categories,
        axisLabel: {
          color: textColor,
          fontSize: 11,
          rotate: categories.length > 8 ? 30 : 0,
        },
        axisLine: { lineStyle: { color: splitLineColor } },
        axisTick: { show: false },
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: textColor, fontSize: 11 },
        axisLine: { show: false },
        splitLine: { lineStyle: { color: splitLineColor } },
      },
      series: [
        {
          // Invisible base
          name: '_base',
          type: 'bar',
          stack: 'waterfall',
          data: baseValues,
          itemStyle: {
            borderColor: 'transparent',
            color: 'transparent',
          },
          emphasis: {
            itemStyle: {
              borderColor: 'transparent',
              color: 'transparent',
            },
          },
          tooltip: { show: false },
        },
        {
          // Visible bar
          name: 'Value',
          type: 'bar',
          stack: 'waterfall',
          data: barValues.map((v, i) => ({
            value: v,
            itemStyle: {
              color: barColors[i],
              borderRadius: [4, 4, 0, 0],
            },
          })),
          label: {
            show: data.length <= 20,
            position: 'top',
            color: textColor,
            fontSize: 11,
            formatter: (params: any) => {
              const idx = params.dataIndex;
              const isTotal = data[idx]?.total === true || data[idx]?.isTotal === true;
              const rawVal = isTotal ? barValues[idx] : Number(data[idx][value] ?? 0);
              return String(rawVal);
            },
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 12,
              shadowColor: 'rgba(99,102,241,0.3)',
            },
          },
        },
      ],
    };
  }, [data, category, value, isDark]);

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
