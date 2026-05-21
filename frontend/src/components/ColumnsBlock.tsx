import React from 'react';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import { BlockRenderer } from '../registry';
import type { BlockComponentProps } from '../types';

// ─── Columns Block ────────────────────────────────────────────────────────────
//
// Uses CSS Grid instead of MUI Grid to avoid double-nesting issues.
// Each child is passed to BlockRenderer as a single block, which renders
// at full width within its column — no extra grid sizing applied.

export const ColumnsBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { children, widths, layout = 'equal' } = block.props;

  if (!children || children.length === 0) return null;

  const count = children.length;

  // ── Bento grid ──
  if (layout === 'bento') {
    return (
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: {
            xs: '1fr',
            sm: 'repeat(2, 1fr)',
            md: `repeat(${Math.min(count, 4)}, 1fr)`,
          },
          gap: 2.5,
          '& > *:first-of-type': count > 2 ? {
            gridColumn: { md: 'span 2' },
            gridRow: { md: 'span 2' },
          } : undefined,
        }}
      >
        {children.map((child: any, i: number) => (
          <Box key={child.id || `bento-${i}`} sx={{ minWidth: 0 }}>
            <BlockRenderer blocks={[child]} />
          </Box>
        ))}
      </Box>
    );
  }

  // ── Custom widths → use fr units ──
  if (layout === 'custom' && widths && widths.length === count) {
    const frTemplate = widths.map((w: number) => `${w}fr`).join(' ');
    return (
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: {
            xs: '1fr',
            sm: count <= 2 ? frTemplate : '1fr',
            md: frTemplate,
          },
          gap: 2.5,
          alignItems: 'stretch',
        }}
      >
        {children.map((child: any, i: number) => (
          <Box key={child.id || `col-${i}`} sx={{ minWidth: 0, display: 'flex', flexDirection: 'column', '& > *': { flex: 1 } }}>
            <BlockRenderer blocks={[child]} />
          </Box>
        ))}
      </Box>
    );
  }

  // ── Equal columns (default) ──
  return (
    <Box
      sx={{
        display: 'grid',
        gridTemplateColumns: {
          xs: '1fr',
          sm: count <= 2 ? `repeat(${count}, 1fr)` : 'repeat(2, 1fr)',
          md: `repeat(${Math.min(count, 4)}, 1fr)`,
          lg: `repeat(${Math.min(count, 6)}, 1fr)`,
        },
        gap: 2.5,
        alignItems: 'stretch',
      }}
    >
      {children.map((child: any, i: number) => (
        <Box key={child.id || `col-${i}`} sx={{ minWidth: 0, display: 'flex', flexDirection: 'column', '& > *': { flex: 1 } }}>
          <BlockRenderer blocks={[child]} />
        </Box>
      ))}
    </Box>
  );
};
