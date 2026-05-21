import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockSpec } from '../types';

interface ChartBlockProps {
  block: BlockSpec;
  index: number;
}

const accentColors = [
  '#6366f1', '#8b5cf6', '#a78bfa', '#c084fc',
  '#38bdf8', '#22d3ee', '#2dd4bf', '#34d399',
  '#fbbf24', '#f97316', '#fb7185', '#f43f5e',
];

export const ChartBlock: React.FC<ChartBlockProps> = ({ block }) => {
  const theme = useTheme();
  const { title, data, x, y, name, value, series, height = 360 } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!data || data.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const axisLineColor = isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)';
    const splitLineColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)';

    const tooltipStyle = {
      backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
      borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
      textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
      borderRadius: 12,
      padding: [12, 16],
    };

    // ── Pie chart ─────────────────────────────────────────────
    if (block.type === 'pie_chart') {
      const pieData = data.map((item: Record<string, any>, i: number) => ({
        name: String(item[name] ?? `Item ${i}`),
        value: Number(item[value] ?? 0),
      }));

      return {
        tooltip: { ...tooltipStyle, trigger: 'item', formatter: '{b}: {c} ({d}%)' },
        legend: {
          bottom: 0,
          textStyle: { color: textColor, fontSize: 12 },
          icon: 'circle',
          itemWidth: 8,
          itemHeight: 8,
        },
        series: [{
          type: 'pie',
          radius: ['45%', '72%'],
          center: ['50%', '45%'],
          avoidLabelOverlap: true,
          itemStyle: {
            borderRadius: 6,
            borderColor: isDark ? '#12121a' : '#ffffff',
            borderWidth: 3,
          },
          label: {
            show: true,
            color: textColor,
            fontSize: 12,
            formatter: '{b}\n{d}%',
          },
          emphasis: {
            itemStyle: { shadowBlur: 20, shadowColor: 'rgba(99,102,241,0.4)' },
            label: { show: true, fontSize: 14, fontWeight: 'bold' },
          },
          data: pieData,
          color: accentColors,
        }],
      };
    }

    // ── Scatter chart ─────────────────────────────────────────
    if (block.type === 'scatter_chart') {
      const { size: sizeField, category: categoryField } = block.props;

      let scatterSeries: any[];

      if (categoryField) {
        const groups = new Map<string, Record<string, any>[]>();
        data.forEach((item: Record<string, any>) => {
          const key = String(item[categoryField] ?? 'Other');
          if (!groups.has(key)) groups.set(key, []);
          groups.get(key)!.push(item);
        });

        scatterSeries = Array.from(groups.entries()).map(([groupName, items], i) => ({
          name: groupName,
          type: 'scatter',
          data: items.map((item: Record<string, any>) => {
            const point: any[] = [Number(item[x] ?? 0), Number(item[y] ?? 0)];
            if (sizeField) point.push(Number(item[sizeField] ?? 10));
            return point;
          }),
          symbolSize: sizeField
            ? (val: any[]) => Math.max(8, Math.min(50, Math.sqrt(val[2] || 10) * 3))
            : 14,
          itemStyle: { color: accentColors[i % accentColors.length] },
          emphasis: {
            itemStyle: { shadowBlur: 12, shadowColor: 'rgba(99,102,241,0.4)' },
          },
        }));
      } else {
        scatterSeries = [{
          type: 'scatter',
          data: data.map((item: Record<string, any>) => {
            const point: any[] = [Number(item[x] ?? 0), Number(item[y] ?? 0)];
            if (sizeField) point.push(Number(item[sizeField] ?? 10));
            return point;
          }),
          symbolSize: sizeField
            ? (val: any[]) => Math.max(8, Math.min(50, Math.sqrt(val[2] || 10) * 3))
            : 14,
          itemStyle: { color: accentColors[0] },
          emphasis: {
            itemStyle: { shadowBlur: 12, shadowColor: 'rgba(99,102,241,0.4)' },
          },
        }];
      }

      return {
        tooltip: {
          ...tooltipStyle,
          trigger: 'item',
          formatter: (params: any) => {
            const d = params.data;
            return `${x}: ${d[0]}<br/>${y}: ${d[1]}${sizeField ? `<br/>${sizeField}: ${d[2]}` : ''}`;
          },
        },
        legend: categoryField ? {
          bottom: 0,
          textStyle: { color: textColor, fontSize: 12 },
          icon: 'circle',
          itemWidth: 8,
          itemHeight: 8,
        } : undefined,
        grid: {
          left: 16, right: 16, top: categoryField ? 40 : 16, bottom: categoryField ? 40 : 16,
          containLabel: true,
        },
        xAxis: {
          type: 'value',
          name: x,
          nameLocation: 'middle',
          nameGap: 30,
          nameTextStyle: { color: textColor, fontSize: 12 },
          axisLine: { lineStyle: { color: axisLineColor } },
          axisTick: { show: false },
          splitLine: { lineStyle: { color: splitLineColor } },
          axisLabel: { color: textColor, fontSize: 11 },
        },
        yAxis: {
          type: 'value',
          name: typeof y === 'string' ? y : undefined,
          nameLocation: 'middle',
          nameGap: 40,
          nameTextStyle: { color: textColor, fontSize: 12 },
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { lineStyle: { color: splitLineColor } },
          axisLabel: { color: textColor, fontSize: 11 },
        },
        series: scatterSeries,
      };
    }

    // ── Line / Bar / Area chart ───────────────────────────────
    const isLine = block.type === 'line_chart' || block.type === 'area_chart';
    const isArea = block.type === 'area_chart';
    const xValues = data.map((item: Record<string, any>) => String(item[x] ?? ''));

    // KEY FIX: y can be a string or an array of strings
    const yColumns: string[] = Array.isArray(y) ? y : (y ? [y] : []);
    const hasMultipleSeries = yColumns.length > 1 || !!series;

    let seriesData: any[];

    if (series) {
      // Group by series column
      const groups = new Map<string, Record<string, any>[]>();
      data.forEach((item: Record<string, any>) => {
        const key = String(item[series]);
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key)!.push(item);
      });

      const uniqueX = [...new Set(xValues)] as string[];
      const firstY = yColumns[0] || 'value';
      seriesData = Array.from(groups.entries()).map(([groupName, items], i) => {
        const valMap = new Map(items.map((it: Record<string, any>) => [String(it[x]), Number(it[firstY] ?? 0)]));
        const values = uniqueX.map((xv: string) => valMap.get(xv) ?? 0);
        const color = accentColors[i % accentColors.length];

        return {
          name: groupName,
          type: isLine ? 'line' : 'bar',
          data: values,
          smooth: isLine,
          symbol: isLine ? 'circle' : undefined,
          symbolSize: isLine ? 6 : undefined,
          itemStyle: { color, borderRadius: isLine ? undefined : [4, 4, 0, 0] },
          lineStyle: isLine ? { width: 2.5 } : undefined,
          areaStyle: isArea ? {
            color: {
              type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: color + '40' },
                { offset: 1, color: color + '05' },
              ],
            },
          } : undefined,
        };
      });
    } else {
      // Create one series per y column
      seriesData = yColumns.map((yCol: string, i: number) => {
        const color = accentColors[i % accentColors.length];
        const values = data.map((item: Record<string, any>) => Number(item[yCol] ?? 0));

        return {
          name: yCol,
          type: isLine ? 'line' : 'bar',
          data: values,
          smooth: isLine,
          symbol: isLine ? 'circle' : undefined,
          symbolSize: isLine ? 6 : undefined,
          itemStyle: { color, borderRadius: isLine ? undefined : [4, 4, 0, 0] },
          lineStyle: isLine ? { width: 2.5 } : undefined,
          areaStyle: isArea ? {
            color: {
              type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: color + '40' },
                { offset: 1, color: color + '05' },
              ],
            },
          } : undefined,
          barMaxWidth: 40,
        };
      });
    }

    const uniqueX = series ? [...new Set(xValues)] : xValues;

    return {
      tooltip: { ...tooltipStyle, trigger: 'axis' },
      legend: hasMultipleSeries ? {
        top: 0,
        textStyle: { color: textColor, fontSize: 12 },
        icon: 'circle',
        itemWidth: 8,
        itemHeight: 8,
      } : undefined,
      grid: {
        left: 16, right: 16, top: hasMultipleSeries ? 40 : 16, bottom: 16,
        containLabel: true,
      },
      xAxis: {
        type: 'category',
        data: uniqueX,
        axisLine: { lineStyle: { color: axisLineColor } },
        axisTick: { show: false },
        axisLabel: { color: textColor, fontSize: 11, rotate: uniqueX.length > 10 ? 30 : 0 },
      },
      yAxis: {
        type: 'value',
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { lineStyle: { color: splitLineColor } },
        axisLabel: {
          color: textColor,
          fontSize: 11,
          formatter: (val: number) => {
            if (Math.abs(val) >= 1_000_000) return (val / 1_000_000).toFixed(1) + 'M';
            if (Math.abs(val) >= 1_000) return (val / 1_000).toFixed(0) + 'K';
            return String(val);
          },
        },
      },
      series: seriesData,
    };
  }, [data, block.type, x, y, name, value, series, isDark]);

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
              height: height,
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
