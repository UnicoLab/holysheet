import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import LinearProgress from '@mui/material/LinearProgress';
import { useTheme, alpha } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Progress Block ───────────────────────────────────────────────────────────

export const ProgressBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { label, value, max = 100, color, description } = block.props;
  const isDark = theme.palette.mode === 'dark';
  const normalizedValue = Math.min(100, Math.max(0, (value / max) * 100));
  const barColor = color || theme.palette.primary.main;

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-1px)',
          boxShadow: isDark ? '0 4px 20px rgba(99,102,241,0.08)' : '0 4px 20px rgba(0,0,0,0.04)',
          borderColor: isDark ? 'rgba(99,102,241,0.15)' : 'rgba(99,102,241,0.1)',
        },
      }}
    >
      <CardContent sx={{ p: 2.5, pb: '16px !important', flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
          <Typography
            variant="body2"
            sx={{
              fontWeight: 600,
              color: 'text.primary',
              fontSize: '0.8rem',
              flex: 1,
              minWidth: 0,
              mr: 1,
              wordBreak: 'break-word',
              lineHeight: 1.3,
            }}
          >
            {label}
          </Typography>
          <Typography
            variant="caption"
            sx={{
              fontWeight: 700,
              color: barColor,
              fontSize: '0.85rem',
              flexShrink: 0,
            }}
          >
            {Math.round(normalizedValue)}%
          </Typography>
        </Box>
        <Box
          sx={{
            position: 'relative',
            borderRadius: 2,
            overflow: 'hidden',
          }}
        >
          <LinearProgress
            variant="determinate"
            value={normalizedValue}
            sx={{
              height: 8,
              borderRadius: 2,
              backgroundColor: isDark
                ? 'rgba(255,255,255,0.06)'
                : 'rgba(0,0,0,0.06)',
              '& .MuiLinearProgress-bar': {
                borderRadius: 2,
                background: `linear-gradient(90deg, ${barColor}, ${alpha(barColor, 0.7)})`,
                transition: 'transform 0.8s cubic-bezier(0.4, 0, 0.2, 1)',
              },
            }}
          />
        </Box>
        {description && (
          <Typography
            variant="body2"
            sx={{
              color: 'text.secondary',
              mt: 1,
              lineHeight: 1.4,
              fontSize: '0.72rem',
              wordBreak: 'break-word',
            }}
          >
            {description}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};
