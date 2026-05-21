import React, { useState } from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Radio from '@mui/material/Radio';
import { useTheme } from '@mui/material/styles';
import type { BlockComponentProps } from '../types';

// ─── Radio Group Block ────────────────────────────────────────────────────────

export const RadioGroupBlock: React.FC<BlockComponentProps> = ({ block }) => {
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

        <RadioGroup
          value={value}
          onChange={(e) => setValue(e.target.value)}
        >
          {normalizedOptions.map((opt) => (
            <FormControlLabel
              key={opt.value}
              value={opt.value}
              control={
                <Radio
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
        </RadioGroup>
      </CardContent>
    </Card>
  );
};
