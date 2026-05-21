import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import Select from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';
import type { SelectChangeEvent } from '@mui/material/Select';

// ─── Dropdown Block ───────────────────────────────────────────────────────────

export const DropdownBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { label, options = [], default_value, description } = block.props as {
    label: string;
    options: (string | { label: string; value: string })[];
    default_value?: string;
    description?: string;
  };
  const isDark = theme.palette.mode === 'dark';

  const normalizedOptions = (options as any[]).map((opt) =>
    typeof opt === 'string' ? { label: opt, value: opt } : opt,
  );

  const [value, setValue] = useState<string>(
    default_value ?? (normalizedOptions.length > 0 ? normalizedOptions[0].value : ''),
  );

  const handleChange = (event: SelectChangeEvent) => {
    setValue(event.target.value);
  };

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

        <FormControl fullWidth size="small">
          <InputLabel
            sx={{
              fontSize: '0.85rem',
              '&.Mui-focused': { color: '#6366f1' },
            }}
          >
            {label}
          </InputLabel>
          <Select
            value={value}
            label={label}
            onChange={handleChange}
            sx={{
              borderRadius: 2,
              '& .MuiOutlinedInput-notchedOutline': {
                borderColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.12)',
              },
              '&:hover .MuiOutlinedInput-notchedOutline': {
                borderColor: isDark ? 'rgba(99,102,241,0.3)' : 'rgba(99,102,241,0.3)',
              },
              '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                borderColor: '#6366f1',
              },
            }}
          >
            {normalizedOptions.map((opt) => (
              <MenuItem key={opt.value} value={opt.value}>
                {opt.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </CardContent>
    </Card>
  );
};
