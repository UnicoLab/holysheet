import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Avatar from '@mui/material/Avatar';
import Chip from '@mui/material/Chip';
import { useTheme, alpha } from '@mui/material/styles';
import EmailOutlinedIcon from '@mui/icons-material/EmailOutlined';
import { motion } from 'framer-motion';
import type { BlockComponentProps } from '../types';

// ─── User Card Block ──────────────────────────────────────────────────────────

export const UserCardBlock: React.FC<BlockComponentProps> = ({ block }) => {
  const theme = useTheme();
  const { name, role, avatar_url, email, stats } = block.props as {
    name: string;
    role?: string;
    avatar_url?: string;
    email?: string;
    stats?: Record<string, string | number>;
  };
  const isDark = theme.palette.mode === 'dark';
  const accentColor = '#6366f1';

  // Generate initials for avatar fallback
  const initials = name
    ? name
        .split(' ')
        .map((n) => n[0])
        .join('')
        .slice(0, 2)
        .toUpperCase()
    : '?';

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: 'easeOut' }}
    >
      <Card
        elevation={0}
        sx={{
          borderRadius: 4,
          border: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.08)'}`,
          backgroundColor: isDark ? 'rgba(255,255,255,0.03)' : 'rgba(255,255,255,0.8)',
          backdropFilter: 'blur(12px)',
          height: '100%',
          overflow: 'hidden',
          position: 'relative',
          transition: 'all 0.25s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: isDark
              ? '0 8px 32px rgba(99,102,241,0.12)'
              : '0 8px 32px rgba(0,0,0,0.06)',
            borderColor: isDark
              ? 'rgba(99,102,241,0.2)'
              : 'rgba(99,102,241,0.15)',
          },
        }}
      >
        {/* Top gradient banner */}
        <Box
          sx={{
            height: 64,
            background: `linear-gradient(135deg, ${accentColor}, ${alpha(accentColor, 0.5)})`,
          }}
        />

        <CardContent sx={{ pt: 0, pb: '20px !important', px: 3, textAlign: 'center' }}>
          {/* Avatar */}
          <Avatar
            src={avatar_url}
            alt={name}
            sx={{
              width: 72,
              height: 72,
              mx: 'auto',
              mt: -4.5,
              mb: 1.5,
              border: `4px solid ${isDark ? '#1a1a2e' : '#ffffff'}`,
              boxShadow: `0 4px 14px ${alpha(accentColor, 0.25)}`,
              background: `linear-gradient(135deg, ${accentColor}, #8b5cf6)`,
              fontSize: '1.5rem',
              fontWeight: 700,
              color: '#fff',
            }}
          >
            {!avatar_url && initials}
          </Avatar>

          {/* Name */}
          <Typography
            variant="h6"
            sx={{ fontWeight: 700, fontSize: '1.05rem', lineHeight: 1.3 }}
          >
            {name}
          </Typography>

          {/* Role */}
          {role && (
            <Typography
              variant="body2"
              sx={{
                color: 'text.secondary',
                fontSize: '0.8rem',
                mt: 0.25,
                mb: 1,
              }}
            >
              {role}
            </Typography>
          )}

          {/* Email */}
          {email && (
            <Chip
              icon={<EmailOutlinedIcon sx={{ fontSize: 14 }} />}
              label={email}
              size="small"
              component="a"
              href={`mailto:${email}`}
              clickable
              sx={{
                mb: 1.5,
                fontSize: '0.72rem',
                height: 26,
                backgroundColor: alpha(accentColor, 0.08),
                color: accentColor,
                fontWeight: 500,
                '& .MuiChip-icon': { color: accentColor },
              }}
            />
          )}

          {/* Stats row */}
          {stats && Object.keys(stats).length > 0 && (
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'center',
                gap: 0,
                mt: 1.5,
                pt: 1.5,
                borderTop: `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'}`,
                flexWrap: 'wrap',
              }}
            >
              {Object.entries(stats).map(([key, val], i) => (
                <Box
                  key={key}
                  sx={{
                    px: 2,
                    borderLeft:
                      i > 0
                        ? `1px solid ${isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.06)'}`
                        : 'none',
                    textAlign: 'center',
                    minWidth: 60,
                  }}
                >
                  <Typography
                    sx={{
                      fontWeight: 800,
                      fontSize: '1rem',
                      color: accentColor,
                      lineHeight: 1.2,
                    }}
                  >
                    {val}
                  </Typography>
                  <Typography
                    variant="caption"
                    sx={{
                      color: 'text.secondary',
                      fontSize: '0.65rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.05em',
                    }}
                  >
                    {key}
                  </Typography>
                </Box>
              ))}
            </Box>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
};
