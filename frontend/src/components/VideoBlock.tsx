import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Video Block ──────────────────────────────────────────────────────────────

export const VideoBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { src, title, poster, autoplay = false, controls = true } = block.props as {
    src: string;
    title?: string;
    poster?: string;
    autoplay?: boolean;
    controls?: boolean;
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
        overflow: 'hidden',
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
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, fontSize: '1rem' }}>
            {title}
          </Typography>
        )}

        <Box
          sx={{
            borderRadius: 3,
            overflow: 'hidden',
            backgroundColor: isDark ? 'rgba(0,0,0,0.3)' : 'rgba(0,0,0,0.03)',
            position: 'relative',
          }}
        >
          <video
            src={src}
            poster={poster}
            autoPlay={autoplay}
            controls={controls}
            muted={autoplay}
            playsInline
            style={{
              width: '100%',
              height: 'auto',
              display: 'block',
              borderRadius: 12,
            }}
          >
            Your browser does not support the video tag.
          </video>
        </Box>
      </CardContent>
    </Card>
  );
};
