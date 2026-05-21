import React from 'react';
import ReactDOM from 'react-dom/client';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { themes } from './theme';
import App from './App';
import { ErrorBoundary } from './components/ErrorBoundary';
import type { ReportSpec } from './types';

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

// ─── Bootstrap ────────────────────────────────────────────────────────────────

async function bootstrap() {
  const spec = await loadSpec();
  const theme = themes[spec.theme] ?? themes.dark;

  const root = ReactDOM.createRoot(document.getElementById('root')!);
  root.render(
    <React.StrictMode>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <ErrorBoundary>
          <App spec={spec} />
        </ErrorBoundary>
      </ThemeProvider>
    </React.StrictMode>,
  );
}

bootstrap();
