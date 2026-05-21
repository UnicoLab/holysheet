import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Tooltip from '@mui/material/Tooltip';
import Divider from '@mui/material/Divider';
import { alpha, useTheme } from '@mui/material/styles';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';
import { motion } from 'framer-motion';
import type { BlockComponentProps, KPIProps, KPIStatus, KPITooltipDetail } from '../types';

// ─── Status Config ────────────────────────────────────────────────────────────

const statusConfig: Record<KPIStatus, { color: string; Icon: React.ElementType }> = {
  positive: { color: '#34D399', Icon: TrendingUpIcon },
  negative: { color: '#F87171', Icon: TrendingDownIcon },
  neutral: { color: '#94A3B8', Icon: TrendingFlatIcon },
};

// ─── Rich Tooltip Content ─────────────────────────────────────────────────────

interface TooltipCardProps {
  detail: KPITooltipDetail;
}

const TooltipCard: React.FC<TooltipCardProps> = ({ detail }) => {
  return (
    <Box sx={{ p: 0.5, minWidth: 180 }}>
      <Typography
        variant="caption"
        sx={{
          fontWeight: 700,
          textTransform: 'uppercase',
          letterSpacing: '0.06em',
          fontSize: '0.6rem',
          color: 'rgba(255,255,255,0.6)',
          mb: 1,
          display: 'block',
        }}
      >
        Breakdown
      </Typography>
      <Divider sx={{ mb: 1, borderColor: 'rgba(255,255,255,0.1)' }} />
      {detail.breakdown.map((item, idx) => (
        <Box
          key={idx}
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            py: 0.5,
            gap: 2,
          }}
        >
          <Typography variant="body2" sx={{ fontSize: '0.75rem', color: 'rgba(255,255,255,0.8)' }}>
            {item.label}
          </Typography>
          <Typography
            variant="body2"
            sx={{ fontSize: '0.75rem', fontWeight: 700, color: '#fff' }}
          >
            {item.value}
          </Typography>
        </Box>
      ))}
    </Box>
  );
};

// ─── KPI Block ────────────────────────────────────────────────────────────────

export const KPIBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const props = block.props as KPIProps;
  const status = props.status || 'neutral';
  const { color: statusColor, Icon: StatusIcon } = statusConfig[status];
  const accentColor = theme.palette.primary.main;
  const isDark = theme.palette.mode === 'dark';

  const hasTooltipDetail = props.tooltip_detail?.breakdown && props.tooltip_detail.breakdown.length > 0;

  const cardContent = (
    <Card
      sx={{
        position: 'relative',
        height: '100%',
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        cursor: hasTooltipDetail ? 'pointer' : 'default',
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

  // Wrap in rich tooltip if tooltip_detail is provided
  if (hasTooltipDetail) {
    return (
      <Tooltip
        title={<TooltipCard detail={props.tooltip_detail!} />}
        arrow
        placement="bottom"
        enterDelay={200}
        leaveDelay={100}
        componentsProps={{
          tooltip: {
            sx: {
              bgcolor: 'rgba(15, 15, 25, 0.95)',
              backdropFilter: 'blur(12px)',
              border: '1px solid rgba(255,255,255,0.1)',
              borderRadius: 3,
              p: 1.5,
              maxWidth: 320,
              boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
            },
          },
          arrow: {
            sx: {
              color: 'rgba(15, 15, 25, 0.95)',
            },
          },
        }}
      >
        <Box sx={{ height: '100%' }}>
          {cardContent}
        </Box>
      </Tooltip>
    );
  }

  return cardContent;
};
