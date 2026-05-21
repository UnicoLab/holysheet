import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme, alpha } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Status List Block ────────────────────────────────────────────────────────

type StatusType = 'success' | 'warning' | 'error' | 'info' | 'pending';

interface StatusItem {
  label: string;
  status: StatusType;
  description?: string;
  value?: string | number;
}

const statusColors: Record<StatusType, string> = {
  success: '#34d399',
  warning: '#fbbf24',
  error: '#f43f5e',
  info: '#38bdf8',
  pending: '#94a3b8',
};

export const StatusListBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, items = [] } = block.props as {
    title?: string;
    items: StatusItem[];
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
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 700, fontSize: '1rem' }}>
            {title}
          </Typography>
        )}

        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0 }}>
          {(items as StatusItem[]).map((item, i) => {
            const color = statusColors[item.status] || statusColors.info;
            return (
              <Box
                key={i}
                sx={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 1.5,
                  py: 1.25,
                  px: 1,
                  borderRadius: 2,
                  borderBottom:
                    i < items.length - 1
                      ? `1px solid ${isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)'}`
                      : 'none',
                  transition: 'background-color 0.15s',
                  '&:hover': {
                    backgroundColor: isDark ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.01)',
                  },
                }}
              >
                {/* Status dot with glow */}
                <Box
                  sx={{
                    flexShrink: 0,
                    width: 10,
                    height: 10,
                    borderRadius: '50%',
                    backgroundColor: color,
                    boxShadow: `0 0 6px ${alpha(color, 0.4)}`,
                  }}
                />

                {/* Label + description */}
                <Box sx={{ flex: 1, minWidth: 0 }}>
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: 600,
                      fontSize: '0.82rem',
                      color: 'text.primary',
                      lineHeight: 1.3,
                    }}
                  >
                    {item.label}
                  </Typography>
                  {item.description && (
                    <Typography
                      variant="caption"
                      sx={{
                        color: 'text.secondary',
                        fontSize: '0.72rem',
                        lineHeight: 1.3,
                        display: 'block',
                        mt: 0.25,
                      }}
                    >
                      {item.description}
                    </Typography>
                  )}
                </Box>

                {/* Value */}
                {item.value !== undefined && (
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: 700,
                      fontSize: '0.82rem',
                      color,
                      flexShrink: 0,
                    }}
                  >
                    {item.value}
                  </Typography>
                )}
              </Box>
            );
          })}
        </Box>
      </CardContent>
    </Card>
  );
};
