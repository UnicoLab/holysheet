import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme, alpha } from '@mui/material/styles';
import { motion } from 'framer-motion';
import type { BlockComponentProps } from '../types';

// ─── Timeline Block ───────────────────────────────────────────────────────────

interface TimelineEvent {
  date: string;
  title: string;
  description?: string;
  icon?: string;
  color?: string;
}

export const TimelineBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, events = [] } = block.props as { title?: string; events: TimelineEvent[] };
  const isDark = theme.palette.mode === 'dark';
  const defaultColor = '#6366f1';

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
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 700, fontSize: '1rem' }}>
            {title}
          </Typography>
        )}

        <Box sx={{ position: 'relative', pl: 4 }}>
          {/* Vertical line */}
          <Box
            sx={{
              position: 'absolute',
              left: 7,
              top: 8,
              bottom: 8,
              width: 2,
              background: isDark
                ? 'linear-gradient(180deg, rgba(99,102,241,0.4), rgba(99,102,241,0.05))'
                : 'linear-gradient(180deg, rgba(99,102,241,0.3), rgba(99,102,241,0.05))',
              borderRadius: 1,
            }}
          />

          {(events as TimelineEvent[]).map((event, i) => {
            const color = event.color || defaultColor;
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.4, delay: i * 0.1, ease: 'easeOut' }}
              >
                <Box sx={{ position: 'relative', mb: i < events.length - 1 ? 3 : 0 }}>
                  {/* Dot */}
                  <Box
                    sx={{
                      position: 'absolute',
                      left: -29,
                      top: 4,
                      width: 16,
                      height: 16,
                      borderRadius: '50%',
                      backgroundColor: color,
                      border: `3px solid ${isDark ? '#1a1a2e' : '#ffffff'}`,
                      boxShadow: `0 0 0 3px ${alpha(color, 0.2)}`,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      zIndex: 1,
                    }}
                  >
                    {event.icon && (
                      <Typography sx={{ fontSize: 8, lineHeight: 1 }}>{event.icon}</Typography>
                    )}
                  </Box>

                  {/* Date */}
                  <Typography
                    variant="caption"
                    sx={{
                      color: color,
                      fontWeight: 600,
                      fontSize: '0.7rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                    }}
                  >
                    {event.date}
                  </Typography>

                  {/* Event title */}
                  <Typography
                    variant="body1"
                    sx={{
                      fontWeight: 600,
                      fontSize: '0.9rem',
                      color: 'text.primary',
                      mt: 0.25,
                      lineHeight: 1.4,
                    }}
                  >
                    {event.title}
                  </Typography>

                  {/* Description */}
                  {event.description && (
                    <Typography
                      variant="body2"
                      sx={{
                        color: 'text.secondary',
                        fontSize: '0.8rem',
                        mt: 0.5,
                        lineHeight: 1.5,
                        wordBreak: 'break-word',
                      }}
                    >
                      {event.description}
                    </Typography>
                  )}
                </Box>
              </motion.div>
            );
          })}
        </Box>
      </CardContent>
    </Card>
  );
};
