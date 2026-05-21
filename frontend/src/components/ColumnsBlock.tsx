import React from 'react';
import Box from '@mui/material/Box';
import useMediaQuery from '@mui/material/useMediaQuery';
import { useTheme } from '@mui/material/styles';
import { BlockRenderer } from '../registry';
import type { BlockComponentProps } from '../types';

// ─── Columns Block ────────────────────────────────────────────────────────────
//
// Uses CSS Grid with responsive breakpoints:
//   - Desktop (>1200px): use `widths` array or equal columns
//   - Tablet (768-1200px): 2 columns max (wrap overflow)
//   - Mobile (<768px): single column stack
//
// Each child is passed to BlockRenderer as a single block, which renders
// at full width within its column — no extra grid sizing applied.

export const ColumnsBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const isMobile = useMediaQuery('(max-width: 767px)');
  const isTablet = useMediaQuery('(min-width: 768px) and (max-width: 1199px)');
  const { children, widths, layout = 'equal' } = block.props;

  if (!children || children.length === 0) return null;

  const count = children.length;

  // ── Responsive grid template helper ──
  const getResponsiveTemplate = (desktopTemplate: string) => {
    if (isMobile) return '1fr';
    if (isTablet) return count <= 2 ? `repeat(${count}, 1fr)` : 'repeat(2, 1fr)';
    return desktopTemplate;
  };

  // Shared transition for smooth layout changes
  const transitionSx = {
    transition: 'grid-template-columns 0.3s ease, gap 0.3s ease',
  };

  // ── Bento grid ──
  if (layout === 'bento') {
    return (
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: getResponsiveTemplate(
            `repeat(${Math.min(count, 4)}, 1fr)`
          ),
          gap: 2.5,
          ...transitionSx,
          '& > *:first-of-type': !isMobile && !isTablet && count > 2 ? {
            gridColumn: 'span 2',
            gridRow: 'span 2',
          } : undefined,
        }}
      >
        {children.map((child: any, i: number) => (
          <Box
            key={child.id || `bento-${i}`}
            sx={{
              minWidth: 0,
              transition: 'all 0.3s ease',
            }}
          >
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
          gridTemplateColumns: getResponsiveTemplate(frTemplate),
          gap: 2.5,
          alignItems: 'stretch',
          ...transitionSx,
        }}
      >
        {children.map((child: any, i: number) => (
          <Box
            key={child.id || `col-${i}`}
            sx={{
              minWidth: 0,
              display: 'flex',
              flexDirection: 'column',
              '& > *': { flex: 1 },
              transition: 'all 0.3s ease',
            }}
          >
            <BlockRenderer blocks={[child]} />
          </Box>
        ))}
      </Box>
    );
  }

  // ── Equal columns (default) ──
  const equalDesktopTemplate = `repeat(${Math.min(count, 6)}, 1fr)`;

  return (
    <Box
      sx={{
        display: 'grid',
        gridTemplateColumns: getResponsiveTemplate(equalDesktopTemplate),
        gap: 2.5,
        alignItems: 'stretch',
        ...transitionSx,
      }}
    >
      {children.map((child: any, i: number) => (
        <Box
          key={child.id || `col-${i}`}
          sx={{
            minWidth: 0,
            display: 'flex',
            flexDirection: 'column',
            '& > *': { flex: 1 },
            transition: 'all 0.3s ease',
          }}
        >
          <BlockRenderer blocks={[child]} />
        </Box>
      ))}
    </Box>
  );
};
