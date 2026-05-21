import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import { useTheme, alpha } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Data Profile Block ───────────────────────────────────────────────────────

interface ColumnProfile {
  name: string;
  dtype: string;
  count: number;
  null_count: number;
  null_pct: number;
  unique: number;
  mean?: number;
  std?: number;
  min?: number | string;
  max?: number | string;
  top_values?: Array<{ value: string; count: number }>;
}

function formatNum(v: number | string | undefined): string {
  if (v === undefined || v === null) return '—';
  if (typeof v === 'string') return v;
  if (Number.isInteger(v)) return v.toLocaleString();
  return v.toLocaleString(undefined, { maximumFractionDigits: 2 });
}

const dtypeColors: Record<string, string> = {
  int: '#6366f1',
  int64: '#6366f1',
  float: '#8b5cf6',
  float64: '#8b5cf6',
  object: '#38bdf8',
  string: '#38bdf8',
  str: '#38bdf8',
  bool: '#fbbf24',
  boolean: '#fbbf24',
  datetime: '#34d399',
  'datetime64[ns]': '#34d399',
  category: '#f97316',
};

function getDtypeColor(dtype: string): string {
  const lower = dtype.toLowerCase();
  return dtypeColors[lower] || '#94a3b8';
}

export const DataProfileBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, columns = [] } = block.props as {
    title?: string;
    columns: ColumnProfile[];
  };
  const isDark = theme.palette.mode === 'dark';

  if (!columns || columns.length === 0) {
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
            <Typography variant="body2">No profile data available</Typography>
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
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: {
              xs: '1fr',
              sm: 'repeat(2, 1fr)',
              md: `repeat(${Math.min(columns.length, 3)}, 1fr)`,
              lg: `repeat(${Math.min(columns.length, 4)}, 1fr)`,
            },
            gap: 2,
          }}
        >
          {columns.map((col, i) => {
            const dtypeColor = getDtypeColor(col.dtype);
            const nullPct = col.null_pct ?? (col.count > 0 ? (col.null_count / col.count) * 100 : 0);

            return (
              <Box
                key={col.name || i}
                sx={{
                  borderRadius: 3,
                  border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'}`,
                  backgroundColor: isDark ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.01)',
                  p: 2,
                  transition: 'all 0.2s',
                  '&:hover': {
                    borderColor: alpha(dtypeColor, 0.3),
                    backgroundColor: isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.02)',
                  },
                }}
              >
                {/* Column name & dtype */}
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1.5 }}>
                  <Typography
                    variant="subtitle2"
                    sx={{
                      fontWeight: 700,
                      fontSize: '0.82rem',
                      flex: 1,
                      minWidth: 0,
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {col.name}
                  </Typography>
                  <Chip
                    label={col.dtype}
                    size="small"
                    sx={{
                      height: 20,
                      fontSize: '0.65rem',
                      fontWeight: 600,
                      backgroundColor: alpha(dtypeColor, isDark ? 0.2 : 0.12),
                      color: dtypeColor,
                      borderRadius: 1.5,
                    }}
                  />
                </Box>

                {/* Stats grid */}
                <Box
                  sx={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(2, 1fr)',
                    gap: 0.75,
                    fontSize: '0.72rem',
                  }}
                >
                  <StatItem label="Count" value={formatNum(col.count)} isDark={isDark} />
                  <StatItem label="Unique" value={formatNum(col.unique)} isDark={isDark} />
                  <StatItem
                    label="Nulls"
                    value={`${col.null_count} (${nullPct.toFixed(1)}%)`}
                    isDark={isDark}
                    warn={nullPct > 10}
                  />
                  {col.mean !== undefined && (
                    <StatItem label="Mean" value={formatNum(col.mean)} isDark={isDark} />
                  )}
                  {col.std !== undefined && (
                    <StatItem label="Std" value={formatNum(col.std)} isDark={isDark} />
                  )}
                  {col.min !== undefined && (
                    <StatItem label="Min" value={formatNum(col.min)} isDark={isDark} />
                  )}
                  {col.max !== undefined && (
                    <StatItem label="Max" value={formatNum(col.max)} isDark={isDark} />
                  )}
                </Box>

                {/* Top values */}
                {col.top_values && col.top_values.length > 0 && (
                  <Box sx={{ mt: 1.5 }}>
                    <Typography
                      variant="caption"
                      sx={{
                        color: 'text.secondary',
                        fontSize: '0.65rem',
                        fontWeight: 600,
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em',
                      }}
                    >
                      Top Values
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                      {col.top_values.slice(0, 5).map((tv, ti) => (
                        <Chip
                          key={ti}
                          label={`${tv.value} (${tv.count})`}
                          size="small"
                          sx={{
                            height: 18,
                            fontSize: '0.62rem',
                            backgroundColor: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.04)',
                            borderRadius: 1,
                          }}
                        />
                      ))}
                    </Box>
                  </Box>
                )}
              </Box>
            );
          })}
        </Box>
      </CardContent>
    </Card>
  );
};

// ─── Stat Item Helper ─────────────────────────────────────────────────────────

interface StatItemProps {
  label: string;
  value: string;
  isDark: boolean;
  warn?: boolean;
}

const StatItem: React.FC<StatItemProps> = ({ label, value, isDark, warn }) => (
  <Box>
    <Typography
      variant="caption"
      sx={{
        color: 'text.secondary',
        fontSize: '0.62rem',
        fontWeight: 600,
        textTransform: 'uppercase',
        letterSpacing: '0.04em',
        lineHeight: 1.2,
        display: 'block',
      }}
    >
      {label}
    </Typography>
    <Typography
      variant="body2"
      sx={{
        fontWeight: 600,
        fontSize: '0.75rem',
        lineHeight: 1.3,
        color: warn ? '#f97316' : 'text.primary',
      }}
    >
      {value}
    </Typography>
  </Box>
);
