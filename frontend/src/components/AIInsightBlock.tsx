import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import { useTheme, alpha } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── AI Insight Block ─────────────────────────────────────────────────────────

const providerColors: Record<string, string> = {
  openai: '#10a37f',
  anthropic: '#d4a373',
  google: '#4285f4',
};

export const AIInsightBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const { title, text, provider = 'openai' } = block.props;

  const accentColor = providerColors[provider] || '#6366f1';

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${alpha(accentColor, 0.15)}`,
        background: isDark
          ? `linear-gradient(135deg, ${alpha(accentColor, 0.08)}, ${alpha(accentColor, 0.03)})`
          : `linear-gradient(135deg, ${alpha(accentColor, 0.06)}, ${alpha(accentColor, 0.02)})`,
        backdropFilter: 'blur(12px)',
        height: '100%',
        position: 'relative',
        overflow: 'hidden',
        borderLeft: `4px solid ${accentColor}`,
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: isDark
            ? `0 8px 32px ${alpha(accentColor, 0.15)}`
            : `0 8px 32px ${alpha(accentColor, 0.1)}`,
          borderColor: alpha(accentColor, 0.3),
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <AutoAwesomeIcon sx={{ color: accentColor, fontSize: 20 }} />
          <Typography
            variant="h6"
            sx={{
              fontWeight: 700,
              fontSize: '1rem',
              flex: 1,
              color: 'text.primary',
            }}
          >
            {title}
          </Typography>
          <Chip
            label={provider.toUpperCase()}
            size="small"
            sx={{
              backgroundColor: alpha(accentColor, 0.12),
              color: accentColor,
              fontWeight: 600,
              fontSize: '0.7rem',
              height: 24,
            }}
          />
        </Box>
        <Typography
          variant="body1"
          sx={{
            fontSize: '0.925rem',
            lineHeight: 1.7,
            color: 'text.secondary',
            fontStyle: text?.startsWith('[') ? 'italic' : 'normal',
            opacity: text?.startsWith('[') ? 0.7 : 1,
          }}
        >
          {text}
        </Typography>
      </CardContent>
    </Card>
  );
};
