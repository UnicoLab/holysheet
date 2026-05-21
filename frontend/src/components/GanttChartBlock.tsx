import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Gantt Chart Block ────────────────────────────────────────────────────────

interface GanttTask {
  name: string;
  start: string;
  end: string;
  progress?: number;
  color?: string;
  group?: string;
}

const accentColors = [
  '#6366f1', '#8b5cf6', '#38bdf8', '#2dd4bf',
  '#34d399', '#fbbf24', '#f97316', '#fb7185',
  '#a78bfa', '#c084fc', '#22d3ee', '#f43f5e',
];

export const GanttChartBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, tasks = [], height = 400 } = block.props as {
    title?: string;
    tasks: GanttTask[];
    height?: number;
  };
  const isDark = theme.palette.mode === 'dark';

  const option = useMemo(() => {
    if (!tasks || tasks.length === 0) return {};

    const textColor = isDark ? 'rgba(255,255,255,0.8)' : 'rgba(0,0,0,0.7)';
    const splitLineColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)';

    // Parse dates and compute time range
    const parsedTasks = tasks.map((t, i) => ({
      ...t,
      startTs: new Date(t.start).getTime(),
      endTs: new Date(t.end).getTime(),
      color: t.color || accentColors[i % accentColors.length],
    }));

    const allStarts = parsedTasks.map((t) => t.startTs).filter((v) => !isNaN(v));
    const allEnds = parsedTasks.map((t) => t.endTs).filter((v) => !isNaN(v));
    if (allStarts.length === 0 || allEnds.length === 0) return {};

    const minTime = Math.min(...allStarts);
    const maxTime = Math.max(...allEnds);

    // Reverse so first task appears at top
    const taskNames = parsedTasks.map((t) => t.name).reverse();
    const reversedTasks = [...parsedTasks].reverse();

    // Build bar data: each bar starts at (startTs - minTime) with width (endTs - startTs)
    const barData = reversedTasks.map((t, i) => ({
      value: [i, t.startTs, t.endTs, t.endTs - t.startTs],
      itemStyle: {
        color: t.color,
        borderRadius: [4, 4, 4, 4],
        opacity: 0.85,
      },
    }));

    // Build progress overlay data
    const progressData = reversedTasks
      .map((t, i) => {
        const progress = t.progress ?? 0;
        if (progress <= 0) return null;
        const duration = t.endTs - t.startTs;
        const progressEnd = t.startTs + duration * Math.min(progress / 100, 1);
        return {
          value: [i, t.startTs, progressEnd, progressEnd - t.startTs],
          itemStyle: {
            color: t.color,
            borderRadius: [4, 4, 4, 4],
            opacity: 1,
          },
        };
      })
      .filter(Boolean);

    return {
      tooltip: {
        backgroundColor: isDark ? 'rgba(15,15,25,0.95)' : 'rgba(255,255,255,0.98)',
        borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
        textStyle: { color: isDark ? '#fff' : '#1a1a2e', fontSize: 13 },
        borderRadius: 12,
        padding: [12, 16],
        formatter: (params: any) => {
          const d = params.data?.value || params.value;
          if (!d) return '';
          const idx = tasks.length - 1 - d[0];
          const t = tasks[idx];
          if (!t) return '';
          const start = new Date(d[1]).toLocaleDateString();
          const end = new Date(d[2]).toLocaleDateString();
          let html = `<strong>${t.name}</strong><br/>${start} → ${end}`;
          if (t.group) html += `<br/>Group: ${t.group}`;
          if (t.progress !== undefined) html += `<br/>Progress: ${t.progress}%`;
          return html;
        },
      },
      grid: {
        top: 16,
        right: 24,
        bottom: 40,
        left: 24,
        containLabel: true,
      },
      xAxis: {
        type: 'time',
        min: minTime,
        max: maxTime,
        axisLabel: {
          color: textColor,
          fontSize: 11,
        },
        axisLine: { lineStyle: { color: splitLineColor } },
        splitLine: { lineStyle: { color: splitLineColor } },
      },
      yAxis: {
        type: 'category',
        data: taskNames,
        inverse: false,
        axisLabel: {
          color: textColor,
          fontSize: 11,
          width: 120,
          overflow: 'truncate',
        },
        axisLine: { lineStyle: { color: splitLineColor } },
        axisTick: { show: false },
      },
      series: [
        {
          name: 'Duration',
          type: 'custom',
          renderItem: (params: any, api: any) => {
            const categoryIndex = api.value(0);
            const startTs = api.value(1);
            const endTs = api.value(2);
            const start = api.coord([startTs, categoryIndex]);
            const end = api.coord([endTs, categoryIndex]);
            const barHeight = api.size([0, 1])[1] * 0.6;
            const style = api.style();

            return {
              type: 'rect',
              shape: {
                x: start[0],
                y: start[1] - barHeight / 2,
                width: Math.max(end[0] - start[0], 2),
                height: barHeight,
                r: [4, 4, 4, 4],
              },
              style,
            };
          },
          data: barData,
          encode: { x: [1, 2], y: 0 },
          z: 1,
        },
        ...(progressData.length > 0
          ? [
              {
                name: 'Progress',
                type: 'custom',
                renderItem: (params: any, api: any) => {
                  const categoryIndex = api.value(0);
                  const startTs = api.value(1);
                  const endTs = api.value(2);
                  const start = api.coord([startTs, categoryIndex]);
                  const end = api.coord([endTs, categoryIndex]);
                  const barHeight = api.size([0, 1])[1] * 0.6;
                  const style = api.style();

                  return {
                    type: 'rect',
                    shape: {
                      x: start[0],
                      y: start[1] - barHeight / 2,
                      width: Math.max(end[0] - start[0], 2),
                      height: barHeight,
                      r: [4, 4, 4, 4],
                    },
                    style,
                  };
                },
                data: progressData,
                encode: { x: [1, 2], y: 0 },
                z: 2,
              },
            ]
          : []),
      ],
    };
  }, [tasks, isDark]);

  const hasData = tasks && tasks.length > 0;

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
            <Typography variant="body2">No tasks available</Typography>
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
