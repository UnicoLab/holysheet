import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import { useTheme, alpha } from '@mui/material/styles';
import { BlockRenderer } from '../registry';
import type { BlockComponentProps, BlockSpec } from '../types';

// ─── Compare Block ────────────────────────────────────────────────────────────

export const CompareBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const {
    left_label = 'Left',
    right_label = 'Right',
    left_children = [],
    right_children = [],
    mode = 'side_by_side',
  } = block.props as {
    left_label?: string;
    right_label?: string;
    left_children: BlockSpec[];
    right_children: BlockSpec[];
    mode?: 'side_by_side' | 'overlay';
  };
  const isDark = theme.palette.mode === 'dark';

  const hasLeft = left_children && left_children.length > 0;
  const hasRight = right_children && right_children.length > 0;

  if (!hasLeft && !hasRight) {
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
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: 120,
              color: 'text.secondary',
            }}
          >
            <Typography variant="body2">No comparison data available</Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  const labelChipSx = {
    height: 24,
    fontSize: '0.72rem',
    fontWeight: 700,
    borderRadius: 1.5,
    mb: 1.5,
  };

  if (mode === 'overlay') {
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
          <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
            <Chip
              label={left_label}
              sx={{
                ...labelChipSx,
                backgroundColor: alpha('#6366f1', isDark ? 0.2 : 0.12),
                color: '#6366f1',
              }}
            />
            <Chip
              label={right_label}
              sx={{
                ...labelChipSx,
                backgroundColor: alpha('#f97316', isDark ? 0.2 : 0.12),
                color: '#f97316',
              }}
            />
          </Box>
          <Box sx={{ position: 'relative' }}>
            {hasLeft && (
              <Box sx={{ opacity: 0.7 }}>
                <BlockRenderer blocks={left_children} />
              </Box>
            )}
            {hasRight && (
              <Box sx={{ opacity: 0.7 }}>
                <BlockRenderer blocks={right_children} />
              </Box>
            )}
          </Box>
        </CardContent>
      </Card>
    );
  }

  // ── Side-by-side (default) ──
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
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: { xs: '1fr', md: '1fr 1fr' },
            gap: 3,
          }}
        >
          {/* Left column */}
          <Box>
            <Chip
              label={left_label}
              sx={{
                ...labelChipSx,
                backgroundColor: alpha('#6366f1', isDark ? 0.2 : 0.12),
                color: '#6366f1',
              }}
            />
            {hasLeft ? (
              <BlockRenderer blocks={left_children} />
            ) : (
              <Box sx={{ py: 4, textAlign: 'center', color: 'text.secondary' }}>
                <Typography variant="body2">No content</Typography>
              </Box>
            )}
          </Box>

          {/* Divider */}
          <Box
            sx={{
              display: { xs: 'none', md: 'block' },
              position: 'absolute',
              left: '50%',
              top: 0,
              bottom: 0,
              width: 1,
              backgroundColor: isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
            }}
          />

          {/* Right column */}
          <Box>
            <Chip
              label={right_label}
              sx={{
                ...labelChipSx,
                backgroundColor: alpha('#f97316', isDark ? 0.2 : 0.12),
                color: '#f97316',
              }}
            />
            {hasRight ? (
              <BlockRenderer blocks={right_children} />
            ) : (
              <Box sx={{ py: 4, textAlign: 'center', color: 'text.secondary' }}>
                <Typography variant="body2">No content</Typography>
              </Box>
            )}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};
