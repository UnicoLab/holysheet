import React, { useState, useCallback, useMemo } from 'react';
import ReactDOM from 'react-dom/client';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { themes } from './theme';
import App from './App';
import { ErrorBoundary } from './components/ErrorBoundary';
import type { ReportSpec, ThemeName } from './types';

// ─── Spec Loader ──────────────────────────────────────────────────────────────

async function loadSpec(): Promise<ReportSpec> {
  // 1. Try inline spec from Python generator
  if (window.__HOLYSHEET_SPEC__) {
    return window.__HOLYSHEET_SPEC__;
  }

  // 2. Try fetching report.json
  try {
    const res = await fetch('./report.json');
    if (res.ok) {
      return await res.json();
    }
  } catch {
    // fall through
  }

  // 3. Fallback demo spec
  return {
    schema_version: '1.0',
    title: 'HolySheet Dashboard',
    subtitle: 'No data loaded — place a report.json file or embed a spec.',
    theme: 'dark',
    created_at: new Date().toISOString(),
    blocks: [],
  };
}

// ─── Theme Toggle Wrapper ─────────────────────────────────────────────────────

const THEME_STORAGE_KEY = 'holysheet_theme_pref';

function getInitialTheme(specTheme: ThemeName): ThemeName {
  try {
    const stored = localStorage.getItem(THEME_STORAGE_KEY);
    if (stored && (stored === 'dark' || stored === 'light' || stored === 'executive')) {
      return stored as ThemeName;
    }
  } catch {
    // localStorage may not be available
  }
  return specTheme;
}

const AppWithTheme: React.FC<{ spec: ReportSpec }> = ({ spec }) => {
  const [themeName, setThemeName] = useState<ThemeName>(() => getInitialTheme(spec.theme));
  const theme = useMemo(() => themes[themeName] ?? themes.dark, [themeName]);

  const handleToggleTheme = useCallback(() => {
    setThemeName((prev) => {
      // Toggle between light and dark; executive stays in the dark/light cycle
      const next: ThemeName = prev === 'dark' || prev === 'executive' ? 'light' : 'dark';
      try {
        localStorage.setItem(THEME_STORAGE_KEY, next);
      } catch {
        // ignore
      }
      return next;
    });
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ErrorBoundary>
        <App spec={spec} currentTheme={themeName} onToggleTheme={handleToggleTheme} />
      </ErrorBoundary>
    </ThemeProvider>
  );
};

// ─── Bootstrap ────────────────────────────────────────────────────────────────

async function bootstrap() {
  const spec = await loadSpec();

  const root = ReactDOM.createRoot(document.getElementById('root')!);
  root.render(
    <React.StrictMode>
      <AppWithTheme spec={spec} />
    </React.StrictMode>,
  );
}

bootstrap();
