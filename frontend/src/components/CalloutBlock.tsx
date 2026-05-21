import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme, alpha } from '@mui/material/styles';
import FormatQuoteIcon from '@mui/icons-material/FormatQuote';
import LightbulbOutlinedIcon from '@mui/icons-material/LightbulbOutlined';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';
import type { BlockComponentProps } from '../types';

// ─── Callout Block ────────────────────────────────────────────────────────────

type CalloutVariant = 'quote' | 'highlight' | 'note';

const variantConfig: Record<CalloutVariant, { color: string; Icon: React.ElementType }> = {
  quote: { color: '#8b5cf6', Icon: FormatQuoteIcon },
  highlight: { color: '#fbbf24', Icon: LightbulbOutlinedIcon },
  note: { color: '#38bdf8', Icon: InfoOutlinedIcon },
};

export const CalloutBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { content, author, icon, variant = 'note' } = block.props as {
    content: string;
    author?: string;
    icon?: string;
    variant?: CalloutVariant;
  };
  const isDark = theme.palette.mode === 'dark';
  const config = variantConfig[variant] || variantConfig.note;
  const accentColor = config.color;
  const AccentIcon = config.Icon;

  return (
    <Card
      elevation={0}
      sx={{
        borderRadius: 4,
        border: `1px solid ${alpha(accentColor, isDark ? 0.2 : 0.15)}`,
        backgroundColor: isDark
          ? alpha(accentColor, 0.06)
          : alpha(accentColor, 0.04),
        backdropFilter: 'blur(12px)',
        height: '100%',
        overflow: 'hidden',
        position: 'relative',
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

      <CardContent sx={{ p: 3, pl: 4, position: 'relative' }}>
        {/* Large decorative icon */}
        {variant === 'quote' && (
          <Box
            sx={{
              position: 'absolute',
              top: 12,
              right: 16,
              opacity: isDark ? 0.08 : 0.06,
            }}
          >
            <FormatQuoteIcon sx={{ fontSize: 80, color: accentColor }} />
          </Box>
        )}

        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1.5 }}>
          {/* Icon */}
          <Box
            sx={{
              mt: 0.25,
              flexShrink: 0,
              width: 32,
              height: 32,
              borderRadius: '50%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: alpha(accentColor, 0.12),
            }}
          >
            {icon ? (
              <Typography sx={{ fontSize: 16 }}>{icon}</Typography>
            ) : (
              <AccentIcon sx={{ fontSize: 18, color: accentColor }} />
            )}
          </Box>

          <Box sx={{ flex: 1, minWidth: 0 }}>
            {/* Content */}
            <Typography
              variant="body1"
              sx={{
                color: 'text.primary',
                fontSize: variant === 'quote' ? '1rem' : '0.9rem',
                fontStyle: variant === 'quote' ? 'italic' : 'normal',
                fontWeight: variant === 'highlight' ? 500 : 400,
                lineHeight: 1.7,
                wordBreak: 'break-word',
                position: 'relative',
                zIndex: 1,
              }}
            >
              {content}
            </Typography>

            {/* Author */}
            {author && (
              <Typography
                variant="body2"
                sx={{
                  color: accentColor,
                  fontWeight: 600,
                  mt: 1.5,
                  fontSize: '0.82rem',
                }}
              >
                — {author}
              </Typography>
            )}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};
