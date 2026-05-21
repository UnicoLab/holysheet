import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Map Chart Block (Geo Scatter) ───────────────────────────────────────────

export const MapChartBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const {
    title,
    data,
    lat = 'lat',
    lng = 'lng',
    value = 'value',
    name: nameField = 'name',
    height = 400,
  } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const splitLineColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';

    const scatterData = data.map((d: Record<string, any>) => ({
      value: [Number(d[lng] ?? 0), Number(d[lat] ?? 0), Number(d[value] ?? 1)],
      name: String(d[nameField] ?? ''),
    }));

    const values = scatterData.map((d: any) => d.value[2]);
    const minVal = Math.min(...values);
    const maxVal = Math.max(...values);
    const hasValues = maxVal > minVal;

    return {
      tooltip: {
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: (params: any) => {
          const d = params.data;
          const label = d.name ? `<strong>${d.name}</strong><br/>` : '';
          return `${label}Lng: ${d.value[0].toFixed(2)}, Lat: ${d.value[1].toFixed(2)}<br/>Value: ${d.value[2]}`;
        },
      },
      grid: {
        top: 24,
        right: hasValues ? 60 : 16,
        bottom: 40,
        left: 16,
        containLabel: true,
      },
      xAxis: {
        type: 'value',
        name: 'Longitude',
        nameLocation: 'center',
        nameGap: 28,
        nameTextStyle: { color: textColor, fontSize: 12 },
        min: -180,
        max: 180,
        axisLabel: { color: textColor, fontSize: 11 },
        axisLine: { lineStyle: { color: splitLineColor } },
        splitLine: {
          lineStyle: {
            color: splitLineColor,
            type: 'dashed',
          },
        },
      },
      yAxis: {
        type: 'value',
        name: 'Latitude',
        nameLocation: 'center',
        nameGap: 40,
        nameTextStyle: { color: textColor, fontSize: 12 },
        min: -90,
        max: 90,
        axisLabel: { color: textColor, fontSize: 11 },
        axisLine: { lineStyle: { color: splitLineColor } },
        splitLine: {
          lineStyle: {
            color: splitLineColor,
            type: 'dashed',
          },
        },
      },
      ...(hasValues
        ? {
            visualMap: {
              min: minVal,
              max: maxVal,
              dimension: 2,
              calculable: true,
              orient: 'vertical',
              right: 0,
              top: 'center',
              inRange: {
                color: ['#6366f1', '#22d3ee', '#34d399', '#fbbf24', '#f43f5e'],
                symbolSize: [8, 30],
              },
              textStyle: { color: textColor, fontSize: 11 },
              borderColor: 'transparent',
            },
          }
        : {}),
      series: [{
        type: 'scatter',
        data: scatterData,
        symbolSize: hasValues
          ? (val: number[]) => {
              const size = ((val[2] - minVal) / (maxVal - minVal || 1)) * 22 + 8;
              return size;
            }
          : 12,
        itemStyle: {
          color: '#6366f1',
          shadowBlur: 6,
          shadowColor: 'rgba(99,102,241,0.4)',
          opacity: 0.85,
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 16,
            shadowColor: 'rgba(99,102,241,0.6)',
            borderColor: '#fff',
            borderWidth: 2,
          },
          label: {
            show: true,
            formatter: (params: any) => params.data.name || '',
            color: textColor,
            fontSize: 12,
            fontWeight: 600,
          },
        },
      }],
    };
  }, [data, lat, lng, value, nameField, isDark]);

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
        {!title && (
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, fontSize: '1rem', color: 'text.secondary' }}>
            Geo Scatter
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
