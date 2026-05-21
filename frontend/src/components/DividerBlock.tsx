import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Divider Block ────────────────────────────────────────────────────────────

export const DividerBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { label, variant = 'solid' } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const borderStyle = variant === 'dashed' ? 'dashed' : variant === 'dotted' ? 'dotted' : 'solid';

  if (label) {
    return (
      <Box sx={{ py: 2 }}>
        <Divider
          sx={{
            '&::before, &::after': {
              borderTopStyle: borderStyle,
              borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
            },
          }}
        >
          <Typography
            variant="caption"
            sx={{
              color: 'text.secondary',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.1em',
              px: 2,
              fontSize: '0.7rem',
            }}
          >
            {label}
          </Typography>
        </Divider>
      </Box>
    );
  }

  return (
    <Box sx={{ py: 2 }}>
      <Divider
        sx={{
          borderStyle,
          borderColor: isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.08)',
        }}
      />
    </Box>
  );
};
