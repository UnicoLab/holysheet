import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useTheme, alpha } from '@mui/material/styles';
import { motion } from 'framer-motion';
import type { BlockComponentProps } from '../types';

// ─── Metric Block ─────────────────────────────────────────────────────────────

export const MetricBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { label, value, unit, icon } = block.props;
  const isDark = theme.palette.mode === 'dark';
  const accentColor = theme.palette.primary.main;

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        gap: 1.5,
        p: 2,
        borderRadius: 3,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(0,0,0,0.02)',
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'}`,
        backdropFilter: 'blur(8px)',
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          borderColor: alpha(accentColor, 0.2),
          backgroundColor: isDark ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.03)',
          transform: 'translateY(-1px)',
        },
        height: '100%',
        boxSizing: 'border-box',
      }}
    >
      {icon && (
        <Box
          sx={{
            width: 36,
            height: 36,
            borderRadius: 2,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: `linear-gradient(135deg, ${alpha(accentColor, 0.15)}, ${alpha(accentColor, 0.05)})`,
            fontSize: '1.1rem',
            flexShrink: 0,
          }}
        >
          {icon}
        </Box>
      )}
      <Box sx={{ flex: 1, minWidth: 0 }}>
        <Typography
          variant="caption"
          sx={{
            color: 'text.secondary',
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '0.06em',
            display: 'block',
            mb: 0.25,
            fontSize: '0.6rem',
            lineHeight: 1.3,
            wordBreak: 'break-word',
          }}
        >
          {label}
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 0.5, flexWrap: 'wrap' }}>
          <motion.div
            initial={{ opacity: 0, y: 4 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
          >
            <Typography
              sx={{
                fontSize: 'clamp(1rem, 3vw, 1.5rem)',
                fontWeight: 800,
                lineHeight: 1.1,
                letterSpacing: '-0.02em',
                color: 'text.primary',
                wordBreak: 'break-word',
              }}
            >
              {value}
            </Typography>
          </motion.div>
          {unit && (
            <Typography
              variant="body2"
              sx={{ color: 'text.secondary', fontWeight: 500, fontSize: '0.7rem' }}
            >
              {unit}
            </Typography>
          )}
        </Box>
      </Box>
    </Box>
  );
};
