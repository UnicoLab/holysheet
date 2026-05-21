import React, { useState, useCallback } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import IconButton from '@mui/material/IconButton';
import { useTheme } from '@mui/material/styles';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import type { BlockComponentProps } from '../types';

// ─── JSON Viewer Block ────────────────────────────────────────────────────────

interface JsonNodeProps {
  data: any;
  depth: number;
  collapsedDepth: number;
  isDark: boolean;
  keyName?: string;
  isLast?: boolean;
}

const colors = {
  key: (isDark: boolean) => (isDark ? '#c084fc' : '#7c3aed'),
  string: (isDark: boolean) => (isDark ? '#34d399' : '#059669'),
  number: (isDark: boolean) => (isDark ? '#38bdf8' : '#0284c7'),
  boolean: (isDark: boolean) => (isDark ? '#fbbf24' : '#d97706'),
  null: (isDark: boolean) => (isDark ? '#94a3b8' : '#64748b'),
  bracket: (isDark: boolean) => (isDark ? 'rgba(255,255,255,0.5)' : 'rgba(0,0,0,0.45)'),
};

const JsonNode: React.FC<JsonNodeProps> = ({ data, depth, collapsedDepth, isDark, keyName, isLast = true }) => {
  const [collapsed, setCollapsed] = useState(depth >= collapsedDepth);

  const toggle = useCallback(() => setCollapsed((c) => !c), []);

  const renderValue = (val: any): React.ReactNode => {
    if (val === null || val === undefined) {
      return <span style={{ color: colors.null(isDark), fontStyle: 'italic' }}>null</span>;
    }
    if (typeof val === 'string') {
      return <span style={{ color: colors.string(isDark) }}>"{val}"</span>;
    }
    if (typeof val === 'number') {
      return <span style={{ color: colors.number(isDark) }}>{val}</span>;
    }
    if (typeof val === 'boolean') {
      return <span style={{ color: colors.boolean(isDark) }}>{String(val)}</span>;
    }
    return null;
  };

  const keyLabel = keyName !== undefined ? (
    <>
      <span style={{ color: colors.key(isDark) }}>"{keyName}"</span>
      <span style={{ color: colors.bracket(isDark) }}>: </span>
    </>
  ) : null;

  // Primitive
  if (data === null || data === undefined || typeof data !== 'object') {
    return (
      <Box sx={{ pl: depth * 2, fontFamily: '"JetBrains Mono", "Fira Code", monospace', fontSize: '0.8rem', lineHeight: 1.8 }}>
        {keyLabel}{renderValue(data)}{!isLast && <span style={{ color: colors.bracket(isDark) }}>,</span>}
      </Box>
    );
  }

  const isArray = Array.isArray(data);
  const entries = isArray ? data.map((v: any, i: number) => [i, v]) : Object.entries(data);
  const openBracket = isArray ? '[' : '{';
  const closeBracket = isArray ? ']' : '}';

  if (entries.length === 0) {
    return (
      <Box sx={{ pl: depth * 2, fontFamily: '"JetBrains Mono", "Fira Code", monospace', fontSize: '0.8rem', lineHeight: 1.8 }}>
        {keyLabel}
        <span style={{ color: colors.bracket(isDark) }}>{openBracket}{closeBracket}</span>
        {!isLast && <span style={{ color: colors.bracket(isDark) }}>,</span>}
      </Box>
    );
  }

  return (
    <Box>
      <Box
        sx={{
          pl: depth * 2,
          fontFamily: '"JetBrains Mono", "Fira Code", monospace',
          fontSize: '0.8rem',
          lineHeight: 1.8,
          display: 'flex',
          alignItems: 'center',
          cursor: 'pointer',
          '&:hover': { backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(0,0,0,0.02)' },
          borderRadius: 1,
          mx: -0.5,
          px: 0.5,
        }}
        onClick={toggle}
      >
        <IconButton size="small" sx={{ p: 0, mr: 0.5, width: 18, height: 18 }}>
          {collapsed
            ? <KeyboardArrowRightIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
            : <KeyboardArrowDownIcon sx={{ fontSize: 14, color: 'text.secondary' }} />
          }
        </IconButton>
        {keyLabel}
        <span style={{ color: colors.bracket(isDark) }}>{openBracket}</span>
        {collapsed && (
          <>
            <span style={{ color: colors.bracket(isDark), fontSize: '0.75rem', margin: '0 4px' }}>
              {entries.length} {isArray ? 'items' : 'keys'}
            </span>
            <span style={{ color: colors.bracket(isDark) }}>{closeBracket}</span>
            {!isLast && <span style={{ color: colors.bracket(isDark) }}>,</span>}
          </>
        )}
      </Box>
      {!collapsed && (
        <>
          {entries.map((entry: any, i: number) => {
            const [key, val] = entry;
            return (
            <JsonNode
              key={String(key)}
              data={val}
              depth={depth + 1}
              collapsedDepth={collapsedDepth}
              isDark={isDark}
              keyName={isArray ? undefined : String(key)}
              isLast={i === entries.length - 1}
            />
            );
          })}
          <Box sx={{ pl: depth * 2, fontFamily: '"JetBrains Mono", "Fira Code", monospace', fontSize: '0.8rem', lineHeight: 1.8 }}>
            <span style={{ color: colors.bracket(isDark) }}>{closeBracket}</span>
            {!isLast && <span style={{ color: colors.bracket(isDark) }}>,</span>}
          </Box>
        </>
      )}
    </Box>
  );
};

export const JsonViewerBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { data, title, collapsed_depth = 2 } = block.props as {
    data: any;
    title?: string;
    collapsed_depth?: number;
  };
  const isDark = theme.palette.mode === 'dark';

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
            backgroundColor: isDark ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.02)',
            borderRadius: 2,
            p: 2,
            overflow: 'auto',
            maxHeight: 500,
            '&::-webkit-scrollbar': { width: 6, height: 6 },
            '&::-webkit-scrollbar-thumb': {
              backgroundColor: isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.15)',
              borderRadius: 3,
            },
          }}
        >
          <JsonNode data={data} depth={0} collapsedDepth={collapsed_depth} isDark={isDark} />
        </Box>
      </CardContent>
    </Card>
  );
};
