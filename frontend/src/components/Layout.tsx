import React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Tooltip from '@mui/material/Tooltip';
import PrintOutlinedIcon from '@mui/icons-material/PrintOutlined';
import { alpha, useTheme } from '@mui/material/styles';
import { motion } from 'framer-motion';
import type { ReportSpec } from '../types';

// ─── Print Styles ─────────────────────────────────────────────────────────────

const printStyles = {
  '@media print': {
    '& .no-print': { display: 'none !important' },
    '& *': {
      boxShadow: 'none !important',
      backdropFilter: 'none !important',
    },
    '& .MuiCard-root': {
      breakInside: 'avoid',
      pageBreakInside: 'avoid',
    },
  },
};

// ─── Layout Component ─────────────────────────────────────────────────────────

interface LayoutProps {
  spec: ReportSpec;
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ spec, children }) => {
  const theme = useTheme();
  const isDark = theme.palette.mode === 'dark';
  const accentColor = theme.palette.primary.main;

  const formattedDate = (() => {
    try {
      return new Date(spec.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return spec.created_at;
    }
  })();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: 'background.default',
        ...printStyles,
      }}
    >
      {/* ── Header ─────────────────────────────────────────────────────── */}
      <Box
        component="header"
        sx={{
          position: 'relative',
          overflow: 'hidden',
          px: { xs: 2, sm: 4, md: 6 },
          pt: { xs: 4, sm: 5, md: 6 },
          pb: { xs: 3, sm: 4, md: 5 },
        }}
      >
        {/* Subtle gradient background */}
        <Box
          sx={{
            position: 'absolute',
            inset: 0,
            background: isDark
              ? `radial-gradient(ellipse 80% 50% at 50% -20%, ${alpha(accentColor, 0.12)}, transparent)`
              : `radial-gradient(ellipse 80% 50% at 50% -20%, ${alpha(accentColor, 0.06)}, transparent)`,
            pointerEvents: 'none',
          }}
        />
        {/* Accent line */}
        <Box
          sx={{
            position: 'absolute',
            bottom: 0,
            left: 0,
            right: 0,
            height: 1,
            background: `linear-gradient(90deg, transparent, ${alpha(accentColor, 0.3)}, transparent)`,
          }}
        />

        <Box sx={{ position: 'relative', maxWidth: 1400, mx: 'auto', display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
          <Box sx={{ flex: 1, minWidth: 0 }}>
            {/* Brand badge */}
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <Box
                sx={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 0.8,
                  mb: 2,
                  px: 1.5,
                  py: 0.5,
                  borderRadius: 2,
                  bgcolor: alpha(accentColor, isDark ? 0.1 : 0.06),
                  border: `1px solid ${alpha(accentColor, 0.15)}`,
                }}
              >
                <Typography
                  variant="caption"
                  sx={{
                    fontWeight: 700,
                    color: accentColor,
                    letterSpacing: '0.12em',
                    textTransform: 'uppercase',
                    fontSize: '0.65rem',
                  }}
                >
                  ✦ HolySheet
                </Typography>
              </Box>
            </motion.div>

            {/* Title */}
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              <Typography
                variant="h1"
                sx={{
                  mb: spec.subtitle ? 1 : 0,
                  background: isDark
                    ? `linear-gradient(135deg, ${theme.palette.text.primary} 0%, ${alpha(theme.palette.text.primary, 0.7)} 100%)`
                    : 'none',
                  WebkitBackgroundClip: isDark ? 'text' : 'unset',
                  WebkitTextFillColor: isDark ? 'transparent' : 'unset',
                }}
              >
                {spec.title}
              </Typography>
            </motion.div>

            {/* Subtitle */}
            {spec.subtitle && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
              >
                <Typography
                  variant="body1"
                  sx={{
                    color: 'text.secondary',
                    maxWidth: 700,
                    mb: 1,
                  }}
                >
                  {spec.subtitle}
                </Typography>
              </motion.div>
            )}

            {/* Timestamp */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              <Typography
                variant="caption"
                sx={{ color: 'text.secondary', mt: 1, display: 'block' }}
              >
                Generated {formattedDate}
              </Typography>
            </motion.div>
          </Box>

          {/* Action buttons */}
          <Box className="no-print" sx={{ display: 'flex', gap: 1, mt: 1 }}>
            <Tooltip title="Print / Export PDF" arrow>
              <IconButton
                onClick={() => window.print()}
                sx={{
                  color: 'text.secondary',
                  border: `1px solid ${isDark ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'}`,
                  borderRadius: 2,
                  '&:hover': {
                    color: accentColor,
                    borderColor: alpha(accentColor, 0.3),
                    backgroundColor: alpha(accentColor, 0.05),
                  },
                }}
              >
                <PrintOutlinedIcon fontSize="small" />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>
      </Box>

      {/* ── Main Content ────────────────────────────────────────────── */}
      <Box component="main" sx={{ flex: 1 }}>
        {children}
      </Box>

      {/* ── Footer ─────────────────────────────────────────────────── */}
      <Box
        component="footer"
        className="no-print"
        sx={{
          py: 3,
          px: { xs: 2, md: 6 },
          textAlign: 'center',
          borderTop: `1px solid ${theme.palette.divider}`,
        }}
      >
        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
          Built with{' '}
          <Box component="span" sx={{ color: accentColor, fontWeight: 600 }}>
            HolySheet
          </Box>{' '}
          — Interactive Dashboard Engine
        </Typography>
      </Box>
    </Box>
  );
};
