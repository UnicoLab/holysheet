import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Skeleton from '@mui/material/Skeleton';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Embed Block ──────────────────────────────────────────────────────────────

export const EmbedBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { url, title, height = 400, aspect_ratio } = block.props as {
    url: string;
    title?: string;
    height?: number;
    aspect_ratio?: string;
  };
  const isDark = theme.palette.mode === 'dark';
  const [loading, setLoading] = useState(true);

  // Parse aspect ratio like "16:9" → paddingTop percentage
  const aspectPadding = aspect_ratio
    ? (() => {
        const parts = aspect_ratio.split(':').map(Number);
        return parts.length === 2 && parts[0] > 0
          ? `${(parts[1] / parts[0]) * 100}%`
          : undefined;
      })()
    : undefined;

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
          <Typography variant="h6" sx={{ mb: 2, fontWeight: 600, fontSize: '1rem' }}>
            {title}
          </Typography>
        )}

        <Box
          sx={{
            position: 'relative',
            borderRadius: 3,
            overflow: 'hidden',
            backgroundColor: isDark ? 'rgba(0,0,0,0.2)' : 'rgba(0,0,0,0.02)',
            ...(aspectPadding
              ? { width: '100%', paddingTop: aspectPadding }
              : { height }),
          }}
        >
          {loading && (
            <Skeleton
              variant="rectangular"
              sx={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                borderRadius: 3,
              }}
            />
          )}
          <iframe
            src={url}
            title={title || 'Embedded content'}
            onLoad={() => setLoading(false)}
            style={{
              position: aspectPadding ? 'absolute' : 'relative',
              top: 0,
              left: 0,
              width: '100%',
              height: aspectPadding ? '100%' : height,
              border: 'none',
              borderRadius: 12,
              display: loading ? 'none' : 'block',
            }}
            sandbox="allow-scripts allow-same-origin allow-popups"
            loading="lazy"
          />
        </Box>
      </CardContent>
    </Card>
  );
};
