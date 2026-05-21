import { createTheme, type Theme, alpha } from '@mui/material/styles';
import type { ThemeName } from './types';

// ─── Color Palettes ───────────────────────────────────────────────────────────

const palettes = {
  dark: {
    bg: '#0a0a0f',
    paper: '#12121a',
    cardBg: 'rgba(20, 20, 35, 0.85)',
    cardBorder: 'rgba(255, 255, 255, 0.06)',
    primary: '#6C63FF',
    secondary: '#00D9FF',
    textPrimary: '#EAEAF0',
    textSecondary: 'rgba(234, 234, 240, 0.55)',
    divider: 'rgba(255, 255, 255, 0.06)',
    positive: '#34D399',
    negative: '#F87171',
    neutral: '#94A3B8',
    chartColors: ['#6C63FF', '#00D9FF', '#34D399', '#FBBF24', '#F87171', '#A78BFA', '#FB923C', '#38BDF8'],
  },
  light: {
    bg: '#F5F7FA',
    paper: '#FFFFFF',
    cardBg: '#FFFFFF',
    cardBorder: 'rgba(0, 0, 0, 0.06)',
    primary: '#4F46E5',
    secondary: '#0EA5E9',
    textPrimary: '#1E293B',
    textSecondary: 'rgba(30, 41, 59, 0.6)',
    divider: 'rgba(0, 0, 0, 0.08)',
    positive: '#10B981',
    negative: '#EF4444',
    neutral: '#64748B',
    chartColors: ['#4F46E5', '#0EA5E9', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#F97316', '#06B6D4'],
  },
  executive: {
    bg: '#09090C',
    paper: '#111114',
    cardBg: 'rgba(18, 18, 24, 0.9)',
    cardBorder: 'rgba(212, 175, 55, 0.12)',
    primary: '#D4AF37',
    secondary: '#C0A062',
    textPrimary: '#F5F0E8',
    textSecondary: 'rgba(245, 240, 232, 0.5)',
    divider: 'rgba(212, 175, 55, 0.1)',
    positive: '#34D399',
    negative: '#F87171',
    neutral: '#94A3B8',
    chartColors: ['#D4AF37', '#C0A062', '#34D399', '#F5F0E8', '#F87171', '#A78BFA', '#E8C547', '#8B7536'],
  },
} as const;

// ─── Shared component overrides ───────────────────────────────────────────────

function makeComponentOverrides(palette: (typeof palettes)[keyof typeof palettes]) {
  return {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: palette.bg,
          minHeight: '100vh',
        },
        '::-webkit-scrollbar': { width: 6 },
        '::-webkit-scrollbar-track': { background: 'transparent' },
        '::-webkit-scrollbar-thumb': { background: alpha(palette.textPrimary, 0.15), borderRadius: 3 },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: palette.cardBg,
          borderRadius: 16,
          border: `1px solid ${palette.cardBorder}`,
          backdropFilter: 'blur(20px)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: palette.cardBg,
          borderRadius: 16,
          border: `1px solid ${palette.cardBorder}`,
          backdropFilter: 'blur(20px)',
          boxShadow: `0 4px 24px ${alpha(palette.bg, 0.4)}`,
          transition: 'box-shadow 0.3s ease, border-color 0.3s ease',
          '&:hover': {
            borderColor: alpha(palette.primary, 0.2),
            boxShadow: `0 8px 40px ${alpha(palette.primary, 0.08)}`,
          },
        },
      },
    },
    MuiCardContent: {
      styleOverrides: {
        root: {
          padding: '24px',
          '&:last-child': { paddingBottom: '24px' },
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: {
          borderBottomColor: palette.divider,
        },
        head: {
          fontWeight: 600,
          fontSize: '0.75rem',
          textTransform: 'uppercase' as const,
          letterSpacing: '0.08em',
          color: palette.textSecondary,
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:nth-of-type(even)': {
            backgroundColor: alpha(palette.primary, 0.02),
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 10,
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 600,
        },
      },
    },
  };
}

// ─── Theme Builder ────────────────────────────────────────────────────────────

function buildTheme(name: ThemeName): Theme {
  const palette = palettes[name];
  const isDark = name === 'dark' || name === 'executive';

  return createTheme({
    palette: {
      mode: isDark ? 'dark' : 'light',
      primary: { main: palette.primary },
      secondary: { main: palette.secondary },
      background: {
        default: palette.bg,
        paper: palette.paper,
      },
      text: {
        primary: palette.textPrimary,
        secondary: palette.textSecondary,
      },
      divider: palette.divider,
      success: { main: palette.positive },
      error: { main: palette.negative },
    },
    typography: {
      fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
      h1: { fontWeight: 800, fontSize: '2rem', letterSpacing: '-0.02em', lineHeight: 1.2 },
      h2: { fontWeight: 700, fontSize: '1.5rem', letterSpacing: '-0.01em', lineHeight: 1.3 },
      h3: { fontWeight: 600, fontSize: '1.15rem', letterSpacing: '-0.01em', lineHeight: 1.4 },
      h4: { fontWeight: 600, fontSize: '1rem', lineHeight: 1.4 },
      h5: { fontWeight: 500, fontSize: '0.875rem', lineHeight: 1.5 },
      h6: { fontWeight: 500, fontSize: '0.8rem', lineHeight: 1.5 },
      body1: { fontSize: '0.9rem', lineHeight: 1.6 },
      body2: { fontSize: '0.8rem', lineHeight: 1.6 },
      caption: { fontSize: '0.7rem', letterSpacing: '0.04em' },
    },
    shape: { borderRadius: 12 },
    components: makeComponentOverrides(palette) as any,
  });
}

// ─── Exported themes map ──────────────────────────────────────────────────────

export const themes: Record<ThemeName, Theme> = {
  dark: buildTheme('dark'),
  light: buildTheme('light'),
  executive: buildTheme('executive'),
};

// ─── Chart color accessor ─────────────────────────────────────────────────────

export function getChartColors(themeName: ThemeName): string[] {
  return [...palettes[themeName].chartColors];
}

export function getPalette(themeName: ThemeName) {
  return palettes[themeName];
}
