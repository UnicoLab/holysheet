import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import { useTheme, alpha } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Tag List Block ───────────────────────────────────────────────────────────

interface TagItem {
  label: string;
  color?: string;
  variant?: 'filled' | 'outlined';
}

const defaultColors = [
  '#6366f1', '#8b5cf6', '#38bdf8', '#34d399',
  '#fbbf24', '#f97316', '#fb7185', '#22d3ee',
];

export const TagListBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, tags = [] } = block.props as {
    title?: string;
    tags: TagItem[];
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

        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {(tags as TagItem[]).map((tag, i) => {
            const color = tag.color || defaultColors[i % defaultColors.length];
            const isOutlined = tag.variant === 'outlined';

            return (
              <Chip
                key={i}
                label={tag.label}
                size="small"
                variant={isOutlined ? 'outlined' : 'filled'}
                sx={{
                  fontWeight: 600,
                  fontSize: '0.75rem',
                  height: 28,
                  borderRadius: '8px',
                  ...(isOutlined
                    ? {
                        borderColor: alpha(color, 0.4),
                        color,
                        '&:hover': { backgroundColor: alpha(color, 0.08) },
                      }
                    : {
                        backgroundColor: alpha(color, 0.12),
                        color,
                        '&:hover': { backgroundColor: alpha(color, 0.2) },
                      }),
                }}
              />
            );
          })}
        </Box>
      </CardContent>
    </Card>
  );
};
