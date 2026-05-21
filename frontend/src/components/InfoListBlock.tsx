import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Info List Block ──────────────────────────────────────────────────────────

interface InfoItem {
  key: string;
  value: string | number;
  icon?: string;
}

export const InfoListBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, items = [] } = block.props as {
    title?: string;
    items: InfoItem[];
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

        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
          {(items as InfoItem[]).map((item, i) => (
            <Box
              key={i}
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                py: 1.25,
                px: 1,
                gap: 2,
                borderBottom:
                  i < items.length - 1
                    ? `1px solid ${isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)'}`
                    : 'none',
                transition: 'background-color 0.15s',
                borderRadius: 1,
                '&:hover': {
                  backgroundColor: isDark ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.01)',
                },
              }}
            >
              {/* Key side */}
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, minWidth: 0, flex: 1 }}>
                {item.icon && (
                  <Typography sx={{ fontSize: 16, flexShrink: 0 }}>{item.icon}</Typography>
                )}
                <Typography
                  variant="body2"
                  sx={{
                    color: 'text.secondary',
                    fontSize: '0.8rem',
                    fontWeight: 500,
                    wordBreak: 'break-word',
                  }}
                >
                  {item.key}
                </Typography>
              </Box>

              {/* Value side */}
              <Typography
                variant="body2"
                sx={{
                  fontWeight: 600,
                  fontSize: '0.82rem',
                  color: 'text.primary',
                  textAlign: 'right',
                  wordBreak: 'break-word',
                  flexShrink: 0,
                  maxWidth: '55%',
                }}
              >
                {item.value}
              </Typography>
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
};
