import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { useTheme } from '@mui/material/styles';
import { BlockRenderer } from '../registry';
import type { BlockSpec } from '../types';

interface SectionBlockProps {
  block: BlockSpec;
  index: number;
}

export const SectionBlock: React.FC<SectionBlockProps> = ({ block }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const { title, description, children } = block.props;
  const [expanded, setExpanded] = useState(true);

  return (
    <Box
      sx={{
        mt: 2,
        mb: 1,
        p: 3,
        borderRadius: 4,
        backgroundColor: isDark ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.01)',
        border: `1px solid ${isDark ? 'rgba(255,255,255,0.04)' : 'rgba(0,0,0,0.04)'}`,
        transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
        '&:hover': {
          borderColor: isDark ? 'rgba(99,102,241,0.1)' : 'rgba(99,102,241,0.08)',
        },
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1, mb: expanded ? 2 : 0 }}>
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Typography
            variant="h5"
            sx={{
              fontWeight: 700,
              fontSize: '1.25rem',
              mb: description ? 0.5 : 0,
              background: isDark
                ? 'linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 50%, #a5b4fc 100%)'
                : 'linear-gradient(135deg, #312e81 0%, #4338ca 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            {title}
          </Typography>
          {description && (
            <Typography variant="body2" color="text.secondary" sx={{ lineHeight: 1.6 }}>
              {description}
            </Typography>
          )}
        </Box>
        <IconButton
          onClick={() => setExpanded(!expanded)}
          size="small"
          sx={{
            color: 'text.secondary',
            mt: 0.25,
            transition: 'transform 0.3s ease',
            transform: expanded ? 'rotate(0deg)' : 'rotate(-90deg)',
            '&:hover': {
              color: 'primary.main',
              backgroundColor: isDark ? 'rgba(99,102,241,0.1)' : 'rgba(99,102,241,0.05)',
            },
          }}
        >
          {expanded ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
        </IconButton>
      </Box>

      {expanded && (
        <Divider
          sx={{
            mb: 2,
            borderColor: isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)',
          }}
        />
      )}

      <Collapse in={expanded} timeout={400} easing="cubic-bezier(0.4, 0, 0.2, 1)">
        {children && children.length > 0 && (
          <BlockRenderer blocks={children} />
        )}
      </Collapse>
    </Box>
  );
};
