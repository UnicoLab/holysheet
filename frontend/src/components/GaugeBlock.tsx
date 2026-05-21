import React, { useMemo, useRef, useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Gauge Block ──────────────────────────────────────────────────────────────

export const GaugeBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, value, min = 0, max = 100, unit = '', thresholds, height: propHeight } = block.props;
  const isDark = theme.palette.mode === 'dark';

  // Responsive: measure container width and set height accordingly
  const containerRef = useRef<HTMLDivElement>(null);
  const [chartHeight, setChartHeight] = useState(propHeight || 240);

  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const w = entry.contentRect.width;
        // Height = proportional to width, capped
        setChartHeight(Math.max(160, Math.min(w * 0.85, propHeight || 300)));
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, [propHeight]);

  const option = useMemo(() => {
    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const normalizedValue = Math.max(min, Math.min(max, Number(value) || 0));

    let colorStops: [number, string][] = [
      [0.3, '#34d399'],
      [0.7, '#fbbf24'],
      [1, '#f43f5e'],
    ];

    if (thresholds && thresholds.length > 0) {
      const sorted = [...thresholds].sort((a: any, b: any) => a.value - b.value);
      colorStops = sorted.map((t: any) => [
        Math.min(1, Math.max(0, (t.value - min) / (max - min))),
        t.color,
      ] as [number, string]);
      if (colorStops[colorStops.length - 1][0] < 1) {
        colorStops.push([1, colorStops[colorStops.length - 1][1]]);
      }
    }

    const isSmall = chartHeight < 200;

    return {
      series: [{
        type: 'gauge',
        min,
        max,
        startAngle: 220,
        endAngle: -40,
        center: ['50%', '58%'],
        radius: '90%',
        progress: {
          show: true,
          width: isSmall ? 10 : 14,
          roundCap: true,
        },
        pointer: {
          length: '50%',
          width: isSmall ? 4 : 5,
          itemStyle: { color: isDark ? '#e0e7ff' : '#312e81' },
        },
        axisLine: {
          lineStyle: { width: isSmall ? 10 : 14, color: colorStops },
          roundCap: true,
        },
        axisTick: { show: false },
        splitLine: {
          show: !isSmall,
          distance: -18,
          length: 6,
          lineStyle: {
            color: isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.15)',
            width: 1.5,
          },
        },
        axisLabel: {
          show: !isSmall,
          distance: 16,
          color: textColor,
          fontSize: 9,
        },
        detail: {
          valueAnimation: true,
          formatter: (val: number) => {
            if (unit === '%') return val.toFixed(val % 1 === 0 ? 0 : 1) + '%';
            if (unit === 'ms') return val.toFixed(0) + 'ms';
            return val.toFixed(val % 1 === 0 ? 0 : 1) + (unit ? ' ' + unit : '');
          },
          color: textColor,
          fontSize: isSmall ? 16 : 20,
          fontWeight: 700,
          offsetCenter: [0, '78%'],
        },
        data: [{ value: normalizedValue }],
        animationDuration: 1500,
        animationEasing: 'cubicOut',
      }],
    };
  }, [value, min, max, unit, thresholds, isDark, chartHeight]);

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
      <CardContent sx={{ p: 2, pb: '12px !important' }}>
        {title && (
          <Typography
            variant="subtitle2"
            sx={{
              mb: 0.5,
              fontWeight: 600,
              fontSize: '0.8rem',
              textAlign: 'center',
              wordBreak: 'break-word',
              lineHeight: 1.3,
            }}
          >
            {title}
          </Typography>
        )}
        <Box ref={containerRef} sx={{ width: '100%' }}>
          <ReactECharts
            option={option}
            style={{ height: chartHeight, width: '100%' }}
            opts={{ renderer: 'svg' }}
            notMerge
          />
        </Box>
      </CardContent>
    </Card>
  );
};
