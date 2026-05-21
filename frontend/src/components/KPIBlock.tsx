import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Tooltip from '@mui/material/Tooltip';
import { alpha, useTheme } from '@mui/material/styles';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';
import { motion } from 'framer-motion';
import type { BlockComponentProps, KPIProps, KPIStatus } from '../types';

// ─── Status Config ────────────────────────────────────────────────────────────

const statusConfig: Record<KPIStatus, { color: string; Icon: React.ElementType }> = {
  positive: { color: '#34D399', Icon: TrendingUpIcon },
  negative: { color: '#F87171', Icon: TrendingDownIcon },
  neutral: { color: '#94A3B8', Icon: TrendingFlatIcon },
};

// ─── KPI Block ────────────────────────────────────────────────────────────────

export const KPIBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const props = block.props as KPIProps;
  const status = props.status || 'neutral';
  const { color: statusColor, Icon: StatusIcon } = statusConfig[status];
  const accentColor = theme.palette.primary.main;
  const isDark = theme.palette.mode === 'dark';

  return (
    <Card
      sx={{
        position: 'relative',
        height: '100%',
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-3px)',
          boxShadow: isDark
            ? '0 12px 40px rgba(99,102,241,0.15)'
            : '0 12px 40px rgba(0,0,0,0.08)',
          borderColor: isDark
            ? 'rgba(99,102,241,0.3)'
            : 'rgba(99,102,241,0.2)',
        },
      }}
    >
      {/* Top accent line */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          height: 3,
          background: `linear-gradient(90deg, ${accentColor}, ${alpha(accentColor, 0.3)})`,
          borderRadius: '16px 16px 0 0',
        }}
      />

      <CardContent sx={{ pt: 3, pb: '16px !important', px: 2.5 }}>
        {/* Label */}
        <Typography
          variant="caption"
          sx={{
            color: 'text.secondary',
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '0.08em',
            fontSize: '0.65rem',
            lineHeight: 1.3,
            display: 'block',
            mb: 1,
            wordBreak: 'break-word',
          }}
        >
          {props.label}
        </Typography>

        {/* Value — NEVER truncate, auto-size font */}
        <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 0.5, mb: 1, flexWrap: 'wrap' }}>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, ease: 'easeOut' }}
          >
            <Typography
              sx={{
                fontSize: 'clamp(1.25rem, 4vw, 2rem)',
                fontWeight: 800,
                lineHeight: 1.1,
                letterSpacing: '-0.02em',
                color: 'text.primary',
                wordBreak: 'break-word',
              }}
            >
              {props.value}
            </Typography>
          </motion.div>

          {props.unit && (
            <Typography
              variant="body2"
              sx={{ color: 'text.secondary', fontWeight: 500, fontSize: '0.8rem' }}
            >
              {props.unit}
            </Typography>
          )}
        </Box>

        {/* Delta chip */}
        {props.delta && (
          <Box sx={{ mb: 0.5 }}>
            <Chip
              icon={<StatusIcon sx={{ fontSize: 14, color: `${statusColor} !important` }} />}
              label={props.delta}
              size="small"
              sx={{
                bgcolor: alpha(statusColor, 0.1),
                color: statusColor,
                fontWeight: 600,
                fontSize: '0.7rem',
                height: 24,
                '& .MuiChip-icon': { ml: 0.5 },
              }}
            />
          </Box>
        )}

        {/* Description */}
        {props.description && (
          <Tooltip title={props.description} arrow placement="bottom">
            <Typography
              variant="body2"
              sx={{
                color: 'text.secondary',
                lineHeight: 1.4,
                mt: 0.5,
                fontSize: '0.72rem',
                wordBreak: 'break-word',
              }}
            >
              {props.description}
            </Typography>
          </Tooltip>
        )}
      </CardContent>
    </Card>
  );
};
