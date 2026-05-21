import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Checkbox Group Block ─────────────────────────────────────────────────────

interface CheckboxOption {
  label: string;
  value: string;
}

export const CheckboxGroupBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { label, options = [], default_values = [], description } = block.props as {
    label: string;
    options: CheckboxOption[];
    default_values?: string[];
    description?: string;
  };
  const isDark = theme.palette.mode === 'dark';
  const [checked, setChecked] = useState<Set<string>>(new Set(default_values));

  const handleToggle = (value: string) => {
    setChecked((prev) => {
      const next = new Set(prev);
      if (next.has(value)) {
        next.delete(value);
      } else {
        next.add(value);
      }
      return next;
    });
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
        <Typography variant="h6" sx={{ mb: 0.5, fontWeight: 700, fontSize: '1rem' }}>
          {label}
        </Typography>

        {description && (
          <Typography
            variant="body2"
            sx={{ color: 'text.secondary', fontSize: '0.8rem', mb: 1.5, lineHeight: 1.5 }}
          >
            {description}
          </Typography>
        )}

        <FormGroup>
          {(options as CheckboxOption[]).map((opt) => (
            <FormControlLabel
              key={opt.value}
              control={
                <Checkbox
                  checked={checked.has(opt.value)}
                  onChange={() => handleToggle(opt.value)}
                  size="small"
                  sx={{
                    color: isDark ? 'rgba(255,255,255,0.3)' : 'rgba(0,0,0,0.3)',
                    '&.Mui-checked': { color: '#6366f1' },
                  }}
                />
              }
              label={
                <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                  {opt.label}
                </Typography>
              }
              sx={{
                mx: 0,
                py: 0.25,
                borderRadius: 1,
                '&:hover': {
                  backgroundColor: isDark ? 'rgba(255,255,255,0.02)' : 'rgba(0,0,0,0.01)',
                },
              }}
            />
          ))}
        </FormGroup>
      </CardContent>
    </Card>
  );
};
