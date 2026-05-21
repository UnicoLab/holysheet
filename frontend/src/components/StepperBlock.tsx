import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import { useTheme, alpha } from '@mui/material/styles';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import RadioButtonCheckedIcon from '@mui/icons-material/RadioButtonChecked';
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked';
import type { BlockComponentProps } from '../types';

// ─── Stepper Block ────────────────────────────────────────────────────────────

type StepStatus = 'complete' | 'active' | 'pending';

interface StepItem {
  label: string;
  description?: string;
  status?: StepStatus;
}

const stepConfig: Record<StepStatus, { color: string; Icon: React.ElementType }> = {
  complete: { color: '#34d399', Icon: CheckCircleIcon },
  active: { color: '#6366f1', Icon: RadioButtonCheckedIcon },
  pending: { color: '#94a3b8', Icon: RadioButtonUncheckedIcon },
};

export const StepperBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { title, steps = [], current_step } = block.props as {
    title?: string;
    steps: StepItem[];
    current_step?: number;
  };
  const isDark = theme.palette.mode === 'dark';

  // Derive status from current_step if individual statuses are not set
  const resolvedSteps = (steps as StepItem[]).map((step, i) => {
    if (step.status) return step;
    if (current_step !== undefined) {
      return {
        ...step,
        status: (i < current_step ? 'complete' : i === current_step ? 'active' : 'pending') as StepStatus,
      };
    }
    return { ...step, status: 'pending' as StepStatus };
  });

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
          <Typography variant="h6" sx={{ mb: 3, fontWeight: 700, fontSize: '1rem' }}>
            {title}
          </Typography>
        )}

        <Box
          sx={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: 0,
            overflowX: 'auto',
            pb: 1,
            '&::-webkit-scrollbar': { height: 4 },
            '&::-webkit-scrollbar-thumb': {
              backgroundColor: isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)',
              borderRadius: 2,
            },
          }}
        >
          {resolvedSteps.map((step, i) => {
            const status = step.status || 'pending';
            const { color, Icon } = stepConfig[status];
            const isLast = i === resolvedSteps.length - 1;

            return (
              <Box
                key={i}
                sx={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  flex: 1,
                  minWidth: 100,
                }}
              >
                {/* Step content */}
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', flex: '0 0 auto', minWidth: 60 }}>
                  {/* Icon */}
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      width: 36,
                      height: 36,
                      borderRadius: '50%',
                      backgroundColor: alpha(color, 0.1),
                      mb: 1,
                    }}
                  >
                    <Icon sx={{ fontSize: 20, color }} />
                  </Box>

                  {/* Label */}
                  <Typography
                    variant="body2"
                    sx={{
                      fontWeight: status === 'active' ? 700 : 500,
                      fontSize: '0.78rem',
                      color: status === 'pending' ? 'text.secondary' : 'text.primary',
                      textAlign: 'center',
                      lineHeight: 1.3,
                      maxWidth: 100,
                      wordBreak: 'break-word',
                    }}
                  >
                    {step.label}
                  </Typography>

                  {/* Description */}
                  {step.description && (
                    <Typography
                      variant="caption"
                      sx={{
                        color: 'text.secondary',
                        fontSize: '0.68rem',
                        textAlign: 'center',
                        mt: 0.25,
                        maxWidth: 100,
                        wordBreak: 'break-word',
                      }}
                    >
                      {step.description}
                    </Typography>
                  )}
                </Box>

                {/* Connector line */}
                {!isLast && (
                  <Box
                    sx={{
                      flex: 1,
                      height: 2,
                      mt: '17px', // Align with center of icon
                      mx: 0.5,
                      minWidth: 20,
                      borderRadius: 1,
                      backgroundColor:
                        status === 'complete'
                          ? alpha(stepConfig.complete.color, 0.4)
                          : isDark
                          ? 'rgba(255,255,255,0.08)'
                          : 'rgba(0,0,0,0.08)',
                    }}
                  />
                )}
              </Box>
            );
          })}
        </Box>
      </CardContent>
    </Card>
  );
};
