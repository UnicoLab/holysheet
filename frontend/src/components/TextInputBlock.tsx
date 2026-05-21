import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Text Input Block ─────────────────────────────────────────────────────────

export const TextInputBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { label, placeholder, default_value = '', multiline = false, rows = 4, description } = block.props as {
    label: string;
    placeholder?: string;
    default_value?: string;
    multiline?: boolean;
    rows?: number;
    description?: string;
  };
  const isDark = theme.palette.mode === 'dark';
  const [value, setValue] = useState<string>(default_value);

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
        {description && (
          <Typography
            variant="body2"
            sx={{ color: 'text.secondary', fontSize: '0.8rem', mb: 2, lineHeight: 1.5 }}
          >
            {description}
          </Typography>
        )}

        <TextField
          fullWidth
          label={label}
          placeholder={placeholder}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          multiline={multiline}
          rows={multiline ? rows : undefined}
          size="small"
          variant="outlined"
          sx={{
            '& .MuiOutlinedInput-root': {
              borderRadius: 2,
              '& fieldset': {
                borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.12)',
              },
              '&:hover fieldset': {
                borderColor: isDark ? 'rgba(99,102,241,0.3)' : 'rgba(99,102,241,0.3)',
              },
              '&.Mui-focused fieldset': {
                borderColor: '#6366f1',
              },
            },
            '& .MuiInputLabel-root': {
              fontSize: '0.85rem',
              '&.Mui-focused': { color: '#6366f1' },
            },
          }}
        />
      </CardContent>
    </Card>
  );
};
