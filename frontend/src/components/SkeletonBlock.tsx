import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Skeleton from '@mui/material/Skeleton';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';

// ─── Skeleton Block ───────────────────────────────────────────────────────────

interface SkeletonBlockProps {
  height?: number;
  variant?: 'chart' | 'table' | 'kpi';
}

export const SkeletonBlock: React.FC<SkeletonBlockProps> = ({ height = 360, variant = 'chart' }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';

  if (variant === 'kpi') {
    return (
      <Card
        elevation={0}
        sx={{
          borderRadius: 4,
          border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
          backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
          backdropFilter: 'blur(12px)',
          height: '100%',
        }}
      >
        <CardContent sx={{ pt: 3, px: 2.5 }}>
          <Skeleton variant="text" width="60%" height={16} sx={{ mb: 1.5 }} />
          <Skeleton variant="text" width="40%" height={40} sx={{ mb: 1 }} />
          <Skeleton variant="rounded" width={80} height={24} sx={{ borderRadius: 2 }} />
        </CardContent>
      </Card>
    );
  }

  if (variant === 'table') {
    return (
      <Card
        elevation={0}
        sx={{
          borderRadius: 4,
          border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
          backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
          backdropFilter: 'blur(12px)',
        }}
      >
        <CardContent sx={{ p: 3 }}>
          <Skeleton variant="text" width="30%" height={24} sx={{ mb: 2 }} />
          {Array.from({ length: 5 }).map((_, i) => (
            <Box key={i} sx={{ display: 'flex', gap: 2, mb: 1 }}>
              <Skeleton variant="text" width="25%" height={20} />
              <Skeleton variant="text" width="25%" height={20} />
              <Skeleton variant="text" width="25%" height={20} />
              <Skeleton variant="text" width="25%" height={20} />
            </Box>
          ))}
        </CardContent>
      </Card>
    );
  }

  // Chart variant (default)
  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
        backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
        backdropFilter: 'blur(12px)',
        height: '100%',
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Skeleton variant="text" width="35%" height={24} sx={{ mb: 2 }} />
        <Skeleton
          variant="rounded"
          width="100%"
          height={height}
          sx={{
            borderRadius: 3,
            animation: 'pulse 1.5s ease-in-out infinite',
          }}
        />
      </CardContent>
    </Card>
  );
};
