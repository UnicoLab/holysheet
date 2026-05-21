import React, { useMemo } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme, alpha } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Scorecard Block ──────────────────────────────────────────────────────────

interface Thresholds {
  green?: string;
  yellow?: string;
  red?: string;
  [key: string]: string | undefined;
}

function evaluateThreshold(value: any, expr: string): boolean {
  const num = typeof value === 'number' ? value : parseFloat(String(value));
  if (isNaN(num)) return false;

  const match = expr.match(/^([><=!]+)\s*(-?\d+\.?\d*)$/);
  if (!match) return false;

  const [, op, threshStr] = match;
  const thresh = parseFloat(threshStr);

  switch (op) {
    case '>': return num > thresh;
    case '>=': return num >= thresh;
    case '<': return num < thresh;
    case '<=': return num <= thresh;
    case '==': return num === thresh;
    case '!=': return num !== thresh;
    default: return false;
  }
}

const colorMap: Record<string, { bg: string; text: string }> = {
  green: { bg: '#34d399', text: '#064e3b' },
  yellow: { bg: '#fbbf24', text: '#78350f' },
  red: { bg: '#f43f5e', text: '#881337' },
};

function getCellColor(
  value: any,
  thresholds?: Thresholds,
  isDark?: boolean,
): { bg?: string; text?: string } | null {
  if (!thresholds) return null;

  // Check in priority order: green, yellow, red, then any custom
  const ordered = ['green', 'yellow', 'red', ...Object.keys(thresholds).filter(
    (k) => !['green', 'yellow', 'red'].includes(k),
  )];

  for (const level of ordered) {
    const expr = thresholds[level];
    if (expr && evaluateThreshold(value, expr)) {
      const colors = colorMap[level];
      if (colors) {
        return {
          bg: isDark ? alpha(colors.bg, 0.25) : alpha(colors.bg, 0.2),
          text: isDark ? colors.bg : colors.text,
        };
      }
      return null;
    }
  }
  return null;
}

export const ScorecardBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const {
    title,
    data = [],
    columns = [],
    value_column,
    thresholds,
  } = block.props as {
    title?: string;
    data: Record<string, any>[];
    columns?: string[];
    value_column?: string;
    thresholds?: Thresholds;
  };
  const isDark = theme.palette.mode === 'dark';

  const displayColumns = useMemo(() => {
    if (columns && columns.length > 0) return columns;
    if (data && data.length > 0) return Object.keys(data[0]);
    return [];
  }, [columns, data]);

  if (!data || data.length === 0 || displayColumns.length === 0) {
    return (
      <Card
        elevation={0}
        sx={{
          borderRadius: 4,
          border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
          backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
          backdropFilter: 'blur(12px)',
          height: '100%',
        }}
      >
        <CardContent sx={{ p: 3 }}>
          {title && (
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, fontSize: '1rem' }}>
              {title}
            </Typography>
          )}
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: 120,
              color: 'text.secondary',
            }}
          >
            <Typography variant="body2">No scorecard data available</Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

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
        <Box sx={{ overflowX: 'auto' }}>
          <Box
            component="table"
            sx={{
              width: '100%',
              borderCollapse: 'separate',
              borderSpacing: 0,
              fontSize: '0.82rem',
            }}
          >
            <Box component="thead">
              <Box component="tr">
                {displayColumns.map((col) => (
                  <Box
                    component="th"
                    key={col}
                    sx={{
                      textAlign: 'left',
                      py: 1,
                      px: 1.5,
                      fontWeight: 700,
                      fontSize: '0.75rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                      color: 'text.secondary',
                      borderBottom: `2px solid ${isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)'}`,
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {col}
                  </Box>
                ))}
              </Box>
            </Box>
            <Box component="tbody">
              {data.map((row, rowIdx) => (
                <Box
                  component="tr"
                  key={rowIdx}
                  sx={{
                    '&:hover': {
                      backgroundColor: isDark ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.01)',
                    },
                  }}
                >
                  {displayColumns.map((col) => {
                    const cellValue = row[col];
                    const isValueCol = value_column ? col === value_column : false;
                    const cellColor =
                      isValueCol || !value_column
                        ? getCellColor(cellValue, thresholds, isDark)
                        : null;

                    return (
                      <Box
                        component="td"
                        key={col}
                        sx={{
                          py: 0.75,
                          px: 1.5,
                          borderBottom: `1px solid ${isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)'}`,
                          fontWeight: cellColor ? 700 : 400,
                          color: cellColor?.text || 'text.primary',
                          backgroundColor: cellColor?.bg || 'transparent',
                          borderRadius: cellColor ? 1 : 0,
                          whiteSpace: 'nowrap',
                        }}
                      >
                        {cellValue !== null && cellValue !== undefined ? String(cellValue) : '—'}
                      </Box>
                    );
                  })}
                </Box>
              ))}
            </Box>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};
