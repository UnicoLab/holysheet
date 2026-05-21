import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Skeleton from '@mui/material/Skeleton';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Image Block ──────────────────────────────────────────────────────────────

export const ImageBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { src, alt = '', caption, width, height } = block.props;
  const isDark = theme.palette.mode === 'dark';
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        overflow: 'hidden',
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box
          sx={{
            position: 'relative',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            borderRadius: 2,
            overflow: 'hidden',
            backgroundColor: isDark ? 'rgba(0,0,0,0.2)' : 'rgba(0,0,0,0.02)',
          }}
        >
          {loading && !error && (
            <Skeleton
              variant="rectangular"
              width="100%"
              height={height || 300}
              sx={{ borderRadius: 2, position: 'absolute', top: 0, left: 0 }}
            />
          )}
          {error ? (
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                height: height || 200,
                width: '100%',
                color: 'text.secondary',
              }}
            >
              <Typography variant="body2">Failed to load image</Typography>
            </Box>
          ) : (
            <img
              src={src}
              alt={alt}
              onLoad={() => setLoading(false)}
              onError={() => { setLoading(false); setError(true); }}
              style={{
                maxWidth: '100%',
                width: width || 'auto',
                height: height || 'auto',
                display: loading ? 'none' : 'block',
                borderRadius: 8,
                objectFit: 'contain',
              }}
            />
          )}
        </Box>
        {caption && (
          <Typography
            variant="body2"
            sx={{
              color: 'text.secondary',
              textAlign: 'center',
              mt: 2,
              fontStyle: 'italic',
              fontSize: '0.8rem',
              lineHeight: 1.5,
            }}
          >
            {caption}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};
