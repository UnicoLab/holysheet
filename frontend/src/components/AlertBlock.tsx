import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';
import Alert from '@mui/material/Alert';
import AlertTitle from '@mui/material/AlertTitle';
import { useTheme, alpha } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Alert Block ──────────────────────────────────────────────────────────────

const severityColors: Record<string, string> = {
  info: '#38bdf8',
  warning: '#fbbf24',
  error: '#f43f5e',
  success: '#34d399',
};

export const AlertBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { severity = 'info', title, message } = block.props;
  const isDark = theme.palette.mode === 'dark';

  const accentColor = severityColors[severity] || severityColors.info;

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${alpha(accentColor, 0.2)}`,
        backgroundColor: isDark
          ? alpha(accentColor, 0.06)
          : alpha(accentColor, 0.04),
        backdropFilter: 'blur(12px)',
        overflow: 'hidden',
        position: 'relative',
      }}
    >
      {/* Left accent bar */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          bottom: 0,
          width: 4,
          backgroundColor: accentColor,
          borderRadius: '16px 0 0 16px',
        }}
      />
      <CardContent sx={{ p: 0 }}>
        <Alert
          severity={severity as any}
          sx={{
            backgroundColor: 'transparent',
            border: 'none',
            '& .MuiAlert-icon': {
              color: accentColor,
            },
            '& .MuiAlert-message': {
              color: 'text.primary',
              fontSize: '0.875rem',
              lineHeight: 1.6,
            },
            py: 2,
            px: 2.5,
            pl: 3,
          }}
        >
          {title && (
            <AlertTitle
              sx={{
                fontWeight: 700,
                fontSize: '0.95rem',
                mb: 0.5,
              }}
            >
              {title}
            </AlertTitle>
          )}
          {message}
        </Alert>
      </CardContent>
    </Card>
  );
};
